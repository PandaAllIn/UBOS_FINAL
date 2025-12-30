#!/usr/bin/env python3
"""Mission Orchestrator for Janus autonomous sequencing.

Monitors mission completion criteria and transitions through a predefined
sequence without human intervention. Designed to run as a daemon on The Balaur.
"""
from __future__ import annotations

import json
import os
import shutil
import sys
import time
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

try:
    import yaml  # type: ignore
except ImportError:  # pragma: no cover - dependency should exist
    print("PyYAML is required (install python3-yaml)", file=sys.stderr)
    sys.exit(1)

TRINITY_ROOT = Path("/srv/janus/trinity")
if TRINITY_ROOT.exists() and str(TRINITY_ROOT) not in sys.path:
    sys.path.insert(0, str(TRINITY_ROOT))

from config import APIKeys, TrinityPaths, load_configuration
from janus_orchestrator import DelegationPlan
from orchestrator_executor import execute_plan

REPO_ROOT = Path("/srv/janus")

CONFIG_CANDIDATES = [
    REPO_ROOT / "trinity/config/mission_sequence.yaml",
    REPO_ROOT / "02_FORGE/scripts/deploy/janus/config/mission_sequence.yaml",
]
for candidate in CONFIG_CANDIDATES:
    if candidate.exists():
        CONFIG_PATH = candidate
        break
else:  # pragma: no cover - fallback when no candidates exist
    CONFIG_PATH = CONFIG_CANDIDATES[-1]

STATE_PATH = REPO_ROOT / "03_OPERATIONS/vessels/balaur/state/mission_orchestrator_state.json"
LOG_PATH = REPO_ROOT / "03_OPERATIONS/vessels/balaur/logs/mission_transitions.log"
MISSION_LOG_JSONL = REPO_ROOT / "03_OPERATIONS/vessels/balaur/logs/mission_log.jsonl"
PROPOSALS_PATH = REPO_ROOT / "03_OPERATIONS/vessels/balaur/logs/proposals.jsonl"
MISSION_OBJECTIVES_JSON = REPO_ROOT / "03_OPERATIONS/vessels/balaur/state/mission_objectives.json"
ACTIVE_MISSION_LINK = REPO_ROOT / "03_OPERATIONS/vessels/balaur/runtime/controls/current_mission.yaml"
STATE_DIR = STATE_PATH.parent
CURRENT_MISSION_JSON = STATE_DIR / "current_mission.json"
NEXT_MISSION_JSON = STATE_DIR / "next_mission.json"
MISSION_TRANSITION_SIGNAL = STATE_DIR / "mission_transition_signal"
MISSION_ACK_JSON = STATE_DIR / "mission_ack.json"
MISSION_HISTORY_JSONL = STATE_DIR / "mission_history.jsonl"
ROADMAP_PATH = REPO_ROOT / "01_STRATEGY/ROADMAP.md"
DEFAULT_CHECK_INTERVAL = 300  # seconds
DEFAULT_STAGNATION_MINUTES = 30
ISO_FORMAT = "%Y-%m-%dT%H:%M:%S.%f%z"


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def parse_iso(ts: str | None) -> Optional[datetime]:
    if not ts:
        return None
    try:
        return datetime.fromisoformat(ts.replace("Z", "+00:00"))
    except ValueError:
        return None


def ensure_parent(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


def append_log(message: str) -> None:
    ensure_parent(LOG_PATH)
    timestamp = utc_now().isoformat()
    with LOG_PATH.open("a", encoding="utf-8") as handle:
        handle.write(f"[{timestamp}] {message}\n")

    entry = {
        "timestamp": timestamp,
        "event": "mission_orchestrator",
        "message": message,
    }
    ensure_parent(MISSION_LOG_JSONL)
    with MISSION_LOG_JSONL.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(entry) + "\n")


def append_history(event: str, mission_id: str, payload: Optional[Dict[str, Any]] = None) -> None:
    """Append a structured transition record to mission_history.jsonl."""
    ensure_parent(MISSION_HISTORY_JSONL)
    record = {
        "timestamp": utc_now().isoformat(),
        "event": event,
        "mission_id": mission_id,
        "payload": payload or {},
    }
    with MISSION_HISTORY_JSONL.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(record) + "\n")


def load_yaml(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def read_state() -> Dict[str, Any]:
    if STATE_PATH.exists():
        try:
            with STATE_PATH.open("r", encoding="utf-8") as handle:
                return json.load(handle)
        except json.JSONDecodeError:
            append_log("State file corrupt, resetting")
    return {
        "current_mission": None,
        "missions": {},
    }


def write_state(state: Dict[str, Any]) -> None:
    ensure_parent(STATE_PATH)
    tmp = STATE_PATH.with_suffix(".tmp")
    with tmp.open("w", encoding="utf-8") as handle:
        json.dump(state, handle, indent=2, sort_keys=True)
    tmp.replace(STATE_PATH)


def write_active_mission_summary(entry: MissionEntry) -> None:
    """Publish the active mission summary for the agent harness."""
    try:
        mission_data = load_yaml(entry.file) or {}
    except FileNotFoundError:
        append_log(f"Mission summary skipped; file missing: {entry.file}")
        return
    except Exception as exc:
        append_log(f"Failed to load mission for summary: {exc}")
        return

    ensure_parent(MISSION_OBJECTIVES_JSON)
    summary = {
        "current": {
            "mission_id": entry.mission_id,
            "mission_name": mission_data.get("mission_name"),
            "objective": mission_data.get("objective"),
            "status": mission_data.get("status"),
            "deliverable": mission_data.get("deliverable"),
            "tasks": mission_data.get("tasks"),
        },
        "updated_at": utc_now().isoformat(),
    }
    try:
        with MISSION_OBJECTIVES_JSON.open("w", encoding="utf-8") as handle:
            json.dump(summary, handle, indent=2)
    except Exception as exc:
        append_log(f"Failed to write mission summary: {exc}")

    ensure_parent(ACTIVE_MISSION_LINK)
    try:
        if ACTIVE_MISSION_LINK.exists() or ACTIVE_MISSION_LINK.is_symlink():
            ACTIVE_MISSION_LINK.unlink()
        ACTIVE_MISSION_LINK.symlink_to(entry.file)
    except Exception as exc:
        append_log(f"Failed to update active mission link: {exc}")


def clear_active_mission_summary() -> None:
    """Remove mission summary artifacts when sequence completes."""
    try:
        if MISSION_OBJECTIVES_JSON.exists():
            MISSION_OBJECTIVES_JSON.unlink()
    except Exception as exc:
        append_log(f"Failed clearing mission summary: {exc}")
    try:
        if ACTIVE_MISSION_LINK.exists() or ACTIVE_MISSION_LINK.is_symlink():
            ACTIVE_MISSION_LINK.unlink()
    except Exception as exc:
        append_log(f"Failed clearing mission link: {exc}")


@dataclass
class MissionEntry:
    mission_id: str
    file: Path
    deliverable_path: Optional[Path]
    max_duration: Optional[timedelta]
    min_duration: Optional[timedelta]
    min_proposals: int


def load_config(config_path: Path = CONFIG_PATH) -> tuple[list[MissionEntry], int, int]:
    if not config_path.exists():
        raise FileNotFoundError(f"Config file missing: {config_path}")
    raw = load_yaml(config_path) or {}
    sequence_raw = raw.get("sequence") or []
    check_interval = int(raw.get("check_interval_seconds", DEFAULT_CHECK_INTERVAL))
    stagnation_minutes = int(raw.get("stagnation_minutes", DEFAULT_STAGNATION_MINUTES))

    sequence: list[MissionEntry] = []
    for item in sequence_raw:
        mission_id = item["mission_id"]
        file = REPO_ROOT / item["file"]
        deliverable = Path(item["deliverable_path"]) if item.get("deliverable_path") else None
        max_dur = timedelta(hours=float(item["max_duration_hours"])) if item.get("max_duration_hours") else None
        min_dur = timedelta(hours=float(item["min_duration_hours"])) if item.get("min_duration_hours") else None
        min_proposals = int(item.get("min_proposals", 0))
        sequence.append(MissionEntry(mission_id, file, deliverable, max_dur, min_dur, min_proposals))

    if not sequence:
        raise ValueError("Mission sequence empty")
    return sequence, check_interval, stagnation_minutes


def get_mission_status(path: Path) -> Optional[str]:
    if not path.exists():
        return None
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            stripped = line.strip()
            if stripped.startswith("status:"):
                # remove comments
                value = stripped.split("#", 1)[0]
                value = value.split(":", 1)[1].strip()
                return value.strip('"\' ')
    return None


def replace_field(path: Path, field: str, value: str) -> None:
    if not path.exists():
        raise FileNotFoundError(path)
    lines = path.read_text(encoding="utf-8").splitlines()
    field_prefix = f"{field}:"
    updated = False
    for idx, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith(field_prefix):
            indent = line[: len(line) - len(line.lstrip())]
            comment = ''
            if '#' in line:
                comment = '  ' + line.split('#', 1)[1].strip()
            lines[idx] = f"{indent}{field}: \"{value}\"{('  #' if comment and not comment.startswith('  #') else '') + comment if comment else ''}".rstrip()
            updated = True
            break
    if not updated:
        indent = ''
        insert_idx = len(lines)
        for idx, line in enumerate(lines):
            if line.strip().startswith('status:'):
                indent = line[: len(line) - len(line.lstrip())]
                insert_idx = idx + 1
        lines.insert(insert_idx, f"{indent}{field}: \"{value}\"")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def archive_proposals(mission_id: str) -> Optional[Path]:
    if not PROPOSALS_PATH.exists():
        return None
    timestamp = utc_now().strftime("%Y%m%d-%H%M%S")
    dest = (REPO_ROOT / "intel_cache") / f"proposals_{mission_id}_{timestamp}.jsonl"
    ensure_parent(dest)
    shutil.copy2(PROPOSALS_PATH, dest)
    return dest


def get_proposals_info() -> tuple[int, Optional[datetime]]:
    if not PROPOSALS_PATH.exists():
        return 0, None
    count = 0
    last_ts: Optional[datetime] = None
    with PROPOSALS_PATH.open("r", encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if not line:
                continue
            count += 1
            try:
                data = json.loads(line)
                ts = parse_iso(data.get("timestamp"))
                if ts:
                    last_ts = ts
            except json.JSONDecodeError:
                continue
    return count, last_ts


class MissionOrchestrator:
    def __init__(self, *, paths: TrinityPaths | None = None, keys: APIKeys | None = None, config_path: Path | None = None) -> None:
        loaded_paths, loaded_keys = load_configuration()
        self.paths = paths or loaded_paths
        self.keys = keys or loaded_keys
        self.config_path = config_path or CONFIG_PATH
        self.roadmap_path = ROADMAP_PATH
        self.sequence, self.check_interval, self.stagnation_minutes = load_config(self.config_path)
        self.state = read_state()

    def run(self) -> None:
        append_log("Mission orchestrator starting")
        while True:
            try:
                self.reload_config_if_needed()
                self.tick()
            except Exception as exc:  # pragma: no cover - daemon resilience
                append_log(f"Error: {exc}")
            time.sleep(self.check_interval)

    def reload_config_if_needed(self) -> None:
        # Reload each loop to pick up manual changes
        self.sequence, self.check_interval, self.stagnation_minutes = load_config(self.config_path)

    def tick(self) -> None:
        active_entry = self.find_active_mission()
        if active_entry is None:
            self.ensure_initial_activation()
            return
        self.ensure_state_for_mission(active_entry)
        if self.is_mission_complete(active_entry):
            next_entry = self.get_next_mission(active_entry)
            self.transition(active_entry, next_entry)

    def find_active_mission(self) -> Optional[MissionEntry]:
        for entry in self.sequence:
            status = get_mission_status(entry.file)
            if status == "active":
                return entry
        return None

    def ensure_initial_activation(self) -> None:
        for entry in self.sequence:
            status = get_mission_status(entry.file)
            if status != "completed":
                append_log(f"No active mission detected; activating {entry.mission_id}")
                self.activate_mission(entry)
                return
        append_log("All missions completed; orchestrator idle")

    def ensure_state_for_mission(self, entry: MissionEntry) -> None:
        missions_state = self.state.setdefault("missions", {})
        mission_state = missions_state.get(entry.mission_id)
        if mission_state is None:
            proposals_count, _ = get_proposals_info()
            mission_state = {
                "activated_at": utc_now().isoformat(),
                "proposal_count_start": proposals_count,
            }
            missions_state[entry.mission_id] = mission_state
            self.state["current_mission"] = entry.mission_id
            write_state(self.state)

    def is_mission_complete(self, entry: MissionEntry) -> bool:
        missions_state = self.state.get("missions", {})
        mission_state = missions_state.get(entry.mission_id, {})
        activated_at = parse_iso(mission_state.get("activated_at")) or utc_now()
        now = utc_now()

        # Strategy 1: deliverable exists
        deliverable_ready = False
        if entry.deliverable_path and entry.deliverable_path.exists():
            if entry.min_duration:
                if now - activated_at >= entry.min_duration:
                    deliverable_ready = True
            else:
                deliverable_ready = True
        if deliverable_ready:
            append_log(f"Deliverable detected for {entry.mission_id}: {entry.deliverable_path}")
            return True

        # Strategy 2: max duration exceeded
        if entry.max_duration and now - activated_at >= entry.max_duration:
            append_log(f"Max duration exceeded for {entry.mission_id}")
            return True

        # Strategy 3: proposal stagnation
        total_proposals, last_ts = get_proposals_info()
        proposal_start = mission_state.get("proposal_count_start", 0)
        if total_proposals - proposal_start >= entry.min_proposals and last_ts:
            if now - last_ts >= timedelta(minutes=self.stagnation_minutes):
                append_log(
                    f"Proposal stagnation detected for {entry.mission_id}: no activity since {last_ts.isoformat()}"
                )
                return True
        return False

    def get_next_mission(self, current: MissionEntry) -> Optional[MissionEntry]:
        try:
            idx = self.sequence.index(current)
        except ValueError:
            return None
        return self.sequence[idx + 1] if idx + 1 < len(self.sequence) else None

    def transition(self, current: MissionEntry, next_entry: Optional[MissionEntry]) -> None:
        append_log(f"Transitioning {current.mission_id} -> {next_entry.mission_id if next_entry else 'NONE'}")
        now_iso = utc_now().isoformat()
        replace_field(current.file, "status", "completed")
        replace_field(current.file, "completed_timestamp", now_iso)
        append_history("mission_completed", current.mission_id, {"completed_timestamp": now_iso})

        archive_path = archive_proposals(current.mission_id)
        if archive_path:
            append_log(f"Archived proposals to {archive_path}")

        if next_entry:
            replace_field(next_entry.file, "status", "active")
            replace_field(next_entry.file, "activated_timestamp", now_iso)
            self.update_state_for_new_mission(next_entry)
            payload = self._build_mission_payload(next_entry, now_iso)
            self.stage_mission_transition(payload)
            if not self.wait_for_acknowledgment(next_entry.mission_id):
                append_log(f"Mission {next_entry.mission_id} transition awaiting manual intervention")
        else:
            append_log("No next mission; sequence complete")
            self.state["current_mission"] = None
            write_state(self.state)
            clear_active_mission_summary()

    def update_state_for_new_mission(self, next_entry: MissionEntry) -> None:
        total_proposals, _ = get_proposals_info()
        missions_state = self.state.setdefault("missions", {})
        missions_state[next_entry.mission_id] = {
            "activated_at": utc_now().isoformat(),
            "proposal_count_start": total_proposals,
        }
        self.state["current_mission"] = next_entry.mission_id
        write_state(self.state)
        write_active_mission_summary(next_entry)

    def activate_mission(self, entry: MissionEntry) -> None:
        now_iso = utc_now().isoformat()
        replace_field(entry.file, "status", "active")
        replace_field(entry.file, "activated_timestamp", now_iso)
        self.update_state_for_new_mission(entry)
        payload = self._build_mission_payload(entry, now_iso)
        self.stage_mission_transition(payload)
        if not self.wait_for_acknowledgment(entry.mission_id):
            append_log(f"Initial activation for {entry.mission_id} not acknowledged within timeout")
        append_log(f"Activated mission {entry.mission_id}")

    def _build_mission_payload(self, entry: MissionEntry, activated_timestamp: str) -> Dict[str, Any]:
        mission_data: Dict[str, Any]
        try:
            mission_data = load_yaml(entry.file) or {}
        except Exception as exc:
            append_log(f"Failed to load mission data for payload: {exc}")
            mission_data = {}
        payload: Dict[str, Any] = {
            "mission_id": entry.mission_id,
            "mission_file": str(entry.file),
            "activated_timestamp": activated_timestamp,
            "status": "active",
            "mission": mission_data,
        }
        return payload

    def stage_mission_transition(self, new_mission: Dict[str, Any]) -> None:
        """Stage mission data and raise the semaphore for the agent."""
        ensure_parent(NEXT_MISSION_JSON)
        ensure_parent(MISSION_TRANSITION_SIGNAL)
        if MISSION_ACK_JSON.exists():
            try:
                MISSION_ACK_JSON.unlink()
            except OSError:
                append_log("Unable to remove stale mission acknowledgment file")
        with NEXT_MISSION_JSON.open("w", encoding="utf-8") as handle:
            json.dump(new_mission, handle, indent=2)
        try:
            os.chmod(NEXT_MISSION_JSON, 0o644)
        except OSError:
            pass
        MISSION_TRANSITION_SIGNAL.touch()
        append_log(f"Mission staged: {new_mission.get('mission_id', 'unknown')}")
        append_history("mission_staged", new_mission.get("mission_id", "unknown"), new_mission)

    def wait_for_acknowledgment(self, mission_id: str, timeout: int = 120) -> bool:
        """Wait for the agent to acknowledge a staged mission."""
        start = time.time()
        while time.time() - start < timeout:
            if MISSION_ACK_JSON.exists():
                try:
                    ack = json.loads(MISSION_ACK_JSON.read_text(encoding="utf-8"))
                except json.JSONDecodeError:
                    append_log("Invalid JSON in mission_ack.json; waiting for valid acknowledgment")
                else:
                    if ack.get("mission_id") == mission_id:
                        append_log(f"Mission {mission_id} acknowledged by agent")
                        append_history("mission_acknowledged", mission_id, ack)
                        try:
                            MISSION_ACK_JSON.unlink()
                        except OSError:
                            append_log("Failed to remove mission_ack.json after acknowledgment")
                        return True
                time.sleep(5)
                continue
            time.sleep(5)
        append_log(f"Agent failed to acknowledge mission {mission_id} within {timeout}s")
        append_history("mission_ack_timeout", mission_id, {"timeout_seconds": timeout})
        return False

    # ------------------------------------------------------------------ integrations
    def read_roadmap_missions(self) -> List[Dict[str, str]]:
        """Parse the strategic roadmap into simple mission descriptors."""
        missions: List[Dict[str, str]] = []
        if not self.roadmap_path.exists():
            return missions

        current_phase: Optional[str] = None
        try:
            with self.roadmap_path.open("r", encoding="utf-8") as handle:
                for raw_line in handle:
                    line = raw_line.rstrip()
                    stripped = line.strip()
                    if stripped.startswith("## "):
                        current_phase = stripped[3:].strip()
                        continue
                    if stripped.startswith("*"):
                        description = stripped.lstrip("* ")
                        missions.append(
                            {
                                "phase": current_phase or "Unspecified",
                                "description": description.strip(),
                            }
                        )
        except Exception as exc:  # pragma: no cover - defensive
            append_log(f"Failed to parse roadmap missions: {exc}")
        return missions

    def delegate_to_resident(self, task: str, resident: str) -> str:
        """Send a mission task to a Trinity resident via the executor."""
        plan = DelegationPlan(mode="override", target=resident.lower(), query=task, model=None)
        return execute_plan(plan, self.paths, self.keys)


def main() -> None:
    orchestrator = MissionOrchestrator()
    orchestrator.run()


if __name__ == "__main__":
    main()
