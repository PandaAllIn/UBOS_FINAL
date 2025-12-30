from __future__ import annotations

import json
import uuid
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

from config import TrinityPaths, load_configuration
from pucklib import TalkingDrumTransmitter

ISO_FORMAT = "%Y-%m-%dT%H:%M:%S.%fZ"


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def isoformat_now() -> str:
    return utc_now().strftime(ISO_FORMAT)


@dataclass(frozen=True)
class MissionPaths:
    root: Path
    queued: Path
    active: Path
    completed: Path
    failed: Path
    log_file: Path


class MissionQueueManager:
    """Filesystem-backed mission queue for COMMS_HUB operations."""

    def __init__(
        self,
        *,
        dispatcher_agent: str = "codex",
        comms_root: Path | None = None,
        mission_root: Path | None = None,
        log_path: Path | None = None,
    ) -> None:
        paths, _ = load_configuration()
        self.paths: TrinityPaths = paths
        self.comms_root = Path(comms_root) if comms_root else paths.comms_hub
        self.missions = self._ensure_paths(mission_root)
        self.dispatcher_agent = dispatcher_agent
        self.transmitter = TalkingDrumTransmitter(dispatcher_agent, comms_root=self.comms_root)
        self.log_path = Path(log_path) if log_path else paths.log_dir / "mission_queue_manager.jsonl"

    def load_mission(self, mission_file: Path | str) -> Dict[str, Any]:
        path = Path(mission_file)
        with path.open("r", encoding="utf-8") as handle:
            return json.load(handle)

    def queue_mission(self, mission: Dict[str, Any]) -> Path:
        mission_record = dict(mission)
        mission_record.setdefault("mission_id", self._generate_mission_id(mission_record))
        mission_record["status"] = "queued"
        mission_record.setdefault("created_at", isoformat_now())
        mission_record.setdefault("queued_at", mission_record["created_at"])

        destination = self.missions.queued / f"{mission_record['mission_id']}.json"
        self._write_json_atomic(destination, mission_record)
        self._append_log("queued", mission_record["mission_id"], {"mission": mission_record})
        return destination

    def assign_mission(self, resident_name: str) -> Dict[str, Any] | None:
        candidate = self._next_mission_for_resident(resident_name)
        if candidate is None:
            return None

        mission_path, mission_record = candidate
        return self._activate_mission(mission_path, mission_record, resident_name)

    def assign_specific_mission(self, mission_id: str) -> Dict[str, Any] | None:
        source = self._mission_file("queued", mission_id)
        if source is None:
            return None
        mission_record = self.load_mission(source)
        resident_name = mission_record.get("assigned_to")
        if not resident_name:
            raise ValueError(f"Mission {mission_id} missing 'assigned_to'")
        return self._activate_mission(source, mission_record, resident_name)

    def complete_mission(self, mission_id: str) -> Optional[Path]:
        source = self._mission_file("active", mission_id)
        if source is None:
            return None
        mission_record = self.load_mission(source)
        mission_record["status"] = "completed"
        mission_record["completed_at"] = isoformat_now()
        destination = self.missions.completed / source.name
        self._write_json_atomic(destination, mission_record)
        source.unlink(missing_ok=True)
        self._append_log("completed", mission_id, {})
        return destination

    def fail_mission(self, mission_id: str, error_message: str) -> Optional[Path]:
        source = self._mission_file("active", mission_id)
        if source is None:
            return None
        mission_record = self.load_mission(source)
        mission_record["status"] = "failed"
        mission_record["failed_at"] = isoformat_now()
        mission_record["error_message"] = error_message
        destination = self.missions.failed / source.name
        self._write_json_atomic(destination, mission_record)
        source.unlink(missing_ok=True)
        self._append_log("failed", mission_id, {"error": error_message})
        return destination

    def fail_queued_mission(self, mission_id: str, error_message: str) -> Optional[Path]:
        source = self._mission_file("queued", mission_id)
        if source is None:
            return None
        mission_record = self.load_mission(source)
        mission_record["status"] = "failed"
        mission_record["failed_at"] = isoformat_now()
        mission_record["error_message"] = error_message
        destination = self.missions.failed / source.name
        self._write_json_atomic(destination, mission_record)
        source.unlink(missing_ok=True)
        self._append_log("failed", mission_id, {"error": error_message, "stage": "assignment"})
        return destination

    def list_missions(self, status: str | None = None) -> List[Dict[str, Any]]:
        statuses = [status] if status else ["queued", "active", "completed", "failed"]
        records: List[Dict[str, Any]] = []
        for entry_status in statuses:
            directory = getattr(self.missions, entry_status, None)
            if directory is None or not directory.exists():
                continue
            for path in sorted(directory.glob("*.json")):
                try:
                    mission = self.load_mission(path)
                    mission.setdefault("status", entry_status)
                    records.append(mission)
                except json.JSONDecodeError:
                    continue
        return records

    def _ensure_paths(self, mission_root: Path | None) -> MissionPaths:
        root = Path(mission_root) if mission_root else self.comms_root / "missions"
        queued = root / "queued"
        active = root / "active"
        completed = root / "completed"
        failed = root / "failed"
        log_file = root / "mission_queue.log"
        for directory in (root, queued, active, completed, failed):
            directory.mkdir(parents=True, exist_ok=True)
        return MissionPaths(root=root, queued=queued, active=active, completed=completed, failed=failed, log_file=log_file)

    def _next_mission_for_resident(self, resident_name: str) -> tuple[Path, Dict[str, Any]] | None:
        for path in sorted(self.missions.queued.glob("*.json")):
            mission = self.load_mission(path)
            assigned_to = mission.get("assigned_to")
            if assigned_to and assigned_to.lower() != resident_name.lower():
                continue
            return path, mission
        return None

    def _mission_file(self, status: str, mission_id: str) -> Optional[Path]:
        directory = getattr(self.missions, status, None)
        if directory is None:
            return None
        candidate = directory / f"{mission_id}.json"
        if candidate.exists():
            return candidate
        for path in directory.glob("*.json"):
            if path.stem == mission_id:
                return path
        return None

    def _write_json_atomic(self, destination: Path, payload: Dict[str, Any]) -> None:
        destination.parent.mkdir(parents=True, exist_ok=True)
        tmp_path = destination.with_suffix(".tmp")
        with tmp_path.open("w", encoding="utf-8") as handle:
            json.dump(payload, handle, indent=2, sort_keys=True)
        tmp_path.replace(destination)

    def _build_assignment_puck(self, mission: Dict[str, Any], resident_name: str) -> Dict[str, Any]:
        timestamp = isoformat_now()
        return {
            "message_id": f"mission-{mission['mission_id']}-{uuid.uuid4().hex[:8]}",
            "timestamp": timestamp,
            "from_vessel": self.dispatcher_agent,
            "to_vessel": resident_name,
            "message_type": "mission_assignment",
            "priority": str(mission.get("priority", "")),
            "payload": {
                "mission": mission,
                "instructions": "Mission assigned via queue manager.",
            },
        }

    def _append_log(self, event: str, mission_id: str, extra: Dict[str, Any]) -> None:
        record = {
            "timestamp": isoformat_now(),
            "event": event,
            "mission_id": mission_id,
            **extra,
        }
        try:
            with self.log_path.open("a", encoding="utf-8") as handle:
                json.dump(record, handle)
                handle.write("\n")
        except OSError:
            self._write_json_atomic(self.missions.log_file, {"last_error": record})

    def _generate_mission_id(self, mission: Dict[str, Any]) -> str:
        assigned_to = mission.get("assigned_to", "mission")
        prefix = str(assigned_to).upper().replace(" ", "-")
        timestamp = utc_now().strftime("%Y%m%d-%H%M%S")
        return f"{prefix}-{timestamp}-{uuid.uuid4().hex[:6]}"

    def _activate_mission(
        self,
        mission_path: Path,
        mission_record: Dict[str, Any],
        resident_name: str,
    ) -> Dict[str, Any]:
        mission_record["status"] = "active"
        mission_record["assigned_at"] = isoformat_now()

        destination = self.missions.active / mission_path.name
        self._write_json_atomic(destination, mission_record)
        mission_path.unlink(missing_ok=True)

        puck = self._build_assignment_puck(mission_record, resident_name)
        try:
            written_files = self.transmitter.transmit(puck, recipient=resident_name)
            mission_record["assignment_delivery"] = [str(path) for path in written_files]
            assignment_error: str | None = None
        except Exception as exc:  # pragma: no cover - filesystem or permission error path
            mission_record["assignment_delivery"] = []
            mission_record["assignment_error"] = str(exc)
            assignment_error = str(exc)
        else:
            assignment_error = None

        self._write_json_atomic(destination, mission_record)
        self._append_log(
            "assigned",
            mission_record["mission_id"],
            {
                "resident": resident_name,
                "delivery_files": mission_record["assignment_delivery"],
                "error": assignment_error,
            },
        )
        return mission_record


__all__ = ["MissionQueueManager"]
