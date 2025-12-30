from __future__ import annotations

import argparse
import json
import signal
import subprocess
import sys
import tempfile
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, Dict, Iterable, Mapping, MutableMapping, Optional

from config import APIKeys, TrinityPaths, load_configuration
from master_librarian_adapter import MasterLibrarianAdapter
from mission_queue_manager import MissionQueueManager, isoformat_now
from oracle_bridge import OracleBridge
from pucklib import TalkingDrumTransmitter
from tool_audit_logger import audit_tool_call


MissionHandler = Callable[[dict[str, Any], "MissionRuntimeContext"], Mapping[str, Any]]


@dataclass(slots=True)
class MissionRuntimeContext:
    resident: str
    paths: TrinityPaths
    librarian: MasterLibrarianAdapter
    oracle: OracleBridge


@audit_tool_call("mission.execute_grant_hunter")
def execute_grant_hunter(mission: dict[str, Any], ctx: MissionRuntimeContext) -> Mapping[str, Any]:
    skill_script = ctx.paths.base_dir / "skills" / "eu-grant-hunter" / "scripts" / "scan_eu_databases.py"
    if skill_script.exists():
        subprocess.run(
            [sys.executable, str(skill_script), "--auto"],
            check=False,
            capture_output=True,
            text=True,
        )

    pipeline_state_path = Path("/srv/janus/01_STRATEGY/grant_pipeline/pipeline_state.json")
    try:
        state_raw = ctx.librarian.read_file(pipeline_state_path)
        payload = json.loads(state_raw)
    except FileNotFoundError:
        payload = {}
    except json.JSONDecodeError:
        payload = {}

    opportunities = payload.get("opportunities", [])
    total = len(opportunities)
    high_fit = sum(1 for item in opportunities if (item.get("fit_score") or 0) >= 4.0)
    top_titles = [item.get("title") for item in opportunities if (item.get("fit_score") or 0) >= 4.0][:3]

    return {
        "total_opportunities": total,
        "high_fit_count": high_fit,
        "top_titles": top_titles,
        "pipeline_source": str(pipeline_state_path),
    }


@audit_tool_call("mission.execute_malaga_briefing")
def execute_malaga_briefing(mission: dict[str, Any], ctx: MissionRuntimeContext) -> Mapping[str, Any]:
    script = ctx.paths.base_dir / "skills" / "malaga-embassy-operator" / "scripts" / "generate_daily_briefing.py"
    summary: dict[str, Any] = {}
    if script.exists():
        proc = subprocess.run(
            [sys.executable, str(script), "--json", "--no-comms"],
            capture_output=True,
            text=True,
            check=False,
        )
        try:
            summary = json.loads(proc.stdout) if proc.returncode == 0 else {}
        except json.JSONDecodeError:
            summary = {}

    dashboard = Path("/srv/janus/01_STRATEGY/malaga_embassy/dashboard/revenue_dashboard.html")
    return {
        "health_score": summary.get("health_score"),
        "runway_days": summary.get("runway_days"),
        "revenue_month": summary.get("revenue_month"),
        "actions": summary.get("actions", []),
        "dashboard_path": str(dashboard),
    }


@audit_tool_call("mission.execute_monetization_analysis")
def execute_monetization_analysis(mission: dict[str, Any], ctx: MissionRuntimeContext) -> Mapping[str, Any]:
    script = ctx.paths.base_dir / "skills" / "monetization-strategist" / "scripts" / "calculate_revenue_projections.py"
    temp_output = None
    if script.exists():
        with tempfile.NamedTemporaryFile(mode="w+", suffix=".json", delete=False) as handle:
            temp_output = Path(handle.name)
        subprocess.run(
            [
                sys.executable,
                str(script),
                "--scenario",
                "base",
                "--months",
                "12",
                "--runs",
                "2000",
                "--output",
                str(temp_output),
            ],
            capture_output=True,
            text=True,
            check=False,
        )
    projections: Mapping[str, Any] = {}
    if temp_output and temp_output.exists():
        try:
            projections = json.loads(temp_output.read_text(encoding="utf-8"))
        finally:
            temp_output.unlink(missing_ok=True)

    quantiles = projections.get("quantiles", [])
    final_month = quantiles[-1] if quantiles else {}

    return {
        "months": projections.get("months"),
        "mrr_p50_month12": final_month.get("mrr_p50"),
        "arr_p50_month12": final_month.get("arr_p50"),
        "runs": projections.get("runs"),
    }


@audit_tool_call("mission.execute_innovation_scout")
def execute_innovation_scout(mission: dict[str, Any], ctx: MissionRuntimeContext) -> Mapping[str, Any]:
    log_search = ctx.librarian.search_content("ERROR|WARNING", "/srv/janus/logs")
    highlights = []
    for path, lines in list(log_search.items())[:3]:
        snippet = "; ".join(lines[:2])
        highlights.append({"path": path, "snippet": snippet})

    research_summary = ""
    if highlights:
        query = f"Suggest mitigations for: {highlights[0]['snippet']}"
        research_summary = ctx.oracle.research(query, mode="quick")

    return {
        "issues_detected": highlights,
        "research_recommendation": research_summary,
    }


DEFAULT_HANDLERS: Dict[str, MissionHandler] = {
    "grant_hunter_daily": execute_grant_hunter,
    "malaga_briefing_daily": execute_malaga_briefing,
    "monetization_analysis_daily": execute_monetization_analysis,
    "innovation_scout_daily": execute_innovation_scout,
}


class ResidentMissionExecutor:
    """Processes mission assignments for a specific resident."""

    def __init__(
        self,
        resident: str,
        *,
        handlers: Mapping[str, MissionHandler] | None = None,
        manager: MissionQueueManager | None = None,
        poll_interval: float = 60.0,
        heartbeat_interval: float = 300.0,
        log_path: Path | None = None,
        librarian: MasterLibrarianAdapter | None = None,
        oracle: OracleBridge | None = None,
        transmitter: TalkingDrumTransmitter | None = None,
        paths: TrinityPaths | None = None,
        keys: APIKeys | None = None,
    ) -> None:
        self.resident = resident
        self.poll_interval = poll_interval
        self.heartbeat_interval = heartbeat_interval

        default_paths, default_keys = load_configuration()
        self.paths = paths or default_paths
        self.keys = keys or default_keys
        self.handlers: Mapping[str, MissionHandler] = handlers or DEFAULT_HANDLERS
        self.manager = manager or MissionQueueManager()
        self.librarian = librarian or MasterLibrarianAdapter()
        self.oracle = oracle or OracleBridge(self.keys)
        self.transmitter = transmitter or TalkingDrumTransmitter(resident, comms_root=self.paths.comms_hub)

        default_log = self.paths.log_dir / f"executor_{resident}.jsonl"
        self.log_path = log_path or default_log
        self.log_path.parent.mkdir(parents=True, exist_ok=True)

        self.inbox = self.paths.comms_hub / resident / "inbox"
        self.inbox.mkdir(parents=True, exist_ok=True)
        self.archive_dir = self.inbox.parent / "archive"
        self.archive_dir.mkdir(parents=True, exist_ok=True)
        self._stop_requested = False
        signal.signal(signal.SIGTERM, self._request_stop)
        signal.signal(signal.SIGINT, self._request_stop)

    def _request_stop(self, _signum: int, _frame: Any) -> None:
        self._stop_requested = True

    def log_event(self, event: str, payload: Dict[str, Any]) -> None:
        record = {
            "timestamp": isoformat_now(),
            "resident": self.resident,
            "event": event,
            **payload,
        }
        with self.log_path.open("a", encoding="utf-8") as handle:
            json.dump(record, handle)
            handle.write("\n")

    def _list_inbox_messages(self) -> Iterable[Path]:
        if not self.inbox.exists():
            return []
        return sorted(self.inbox.glob("*.json"))

    def _load_message(self, path: Path) -> Optional[dict[str, Any]]:
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            self.log_event("invalid_message", {"path": str(path)})
            return None
        return payload

    def _archive(self, path: Path) -> None:
        target = self.archive_dir / path.name
        counter = 1
        while target.exists():
            target = self.archive_dir / f"{path.stem}-{counter}{path.suffix}"
            counter += 1
        path.rename(target)

    def _resolve_handler(self, mission: dict[str, Any]) -> MissionHandler:
        source_template = mission.get("source_template")
        mission_id = mission.get("mission_id", "")
        if source_template and source_template in self.handlers:
            return self.handlers[source_template]
        if mission_id and mission_id in self.handlers:
            return self.handlers[mission_id]
        raise KeyError(f"No mission handler registered for template '{source_template or mission_id}'")

    def process_once(self) -> int:
        processed = 0
        for message_path in list(self._list_inbox_messages()):
            message = self._load_message(message_path)
            if not message:
                self._archive(message_path)
                continue

            if message.get("message_type") != "mission_assignment":
                self.log_event(
                    "skipped_message",
                    {"path": str(message_path), "message_type": message.get("message_type")},
                )
                self._archive(message_path)
                continue

            mission = message.get("payload", {}).get("mission")
            if not mission:
                self.log_event("missing_mission_payload", {"path": str(message_path)})
                self._archive(message_path)
                continue

            mission_id = mission.get("mission_id") or "unknown"
            try:
                handler = self._resolve_handler(mission)
                ctx = MissionRuntimeContext(
                    resident=self.resident,
                    paths=self.paths,
                    librarian=self.librarian,
                    oracle=self.oracle,
                )
                summary = dict(handler(mission, ctx))
                self._send_deliverable(mission, summary)
                self.manager.complete_mission(mission_id)
                self.log_event("mission_completed", {"mission_id": mission_id})
                processed += 1
            except Exception as exc:
                self.manager.fail_mission(mission_id, str(exc))
                self.log_event("mission_failed", {"mission_id": mission_id, "error": str(exc)})
            finally:
                self._archive(message_path)
        return processed

    def _send_deliverable(self, mission: MutableMapping[str, Any], summary: Mapping[str, Any]) -> None:
        deliverable = mission.get("deliverable", {})
        if not isinstance(deliverable, Mapping):
            return
        recipient = deliverable.get("recipient")
        if not recipient:
            return

        message_payload = {
            "type": deliverable.get("message_type", "mission_report"),
            "mission_id": mission.get("mission_id"),
            "source_template": mission.get("source_template"),
            "summary": summary,
        }
        try:
            written = self.transmitter.transmit(
                message_payload,
                recipient=str(recipient),
                rhythm="standard",
                tone="mission_update",
            )
            mission.setdefault("deliveries", []).append([str(path) for path in written])
        except Exception as exc:  # pragma: no cover - filesystem guard
            self.log_event("deliverable_error", {"mission_id": mission.get("mission_id"), "error": str(exc)})

    def run_forever(self) -> None:
        self.log_event("executor_started", {"poll_interval": self.poll_interval})
        next_heartbeat = time.monotonic() + self.heartbeat_interval
        while not self._stop_requested:
            try:
                self.process_once()
            except Exception as exc:  # pragma: no cover - defensive
                self.log_event("executor_exception", {"error": str(exc)})

            now = time.monotonic()
            if now >= next_heartbeat:
                queued_active = len(list(self.manager.missions.active.glob("*.json")))
                self.log_event("heartbeat", {"active_missions": queued_active})
                next_heartbeat = now + self.heartbeat_interval

            end_time = time.monotonic() + self.poll_interval
            while time.monotonic() < end_time:
                if self._stop_requested:
                    break
                time.sleep(min(1.0, end_time - time.monotonic()))
        self.log_event("executor_stopped", {})


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Resident mission executor daemon.")
    parser.add_argument("--resident", required=True, help="Resident identifier (e.g., groq, claude).")
    parser.add_argument("--poll-interval", type=float, default=60.0, help="Polling cadence in seconds.")
    parser.add_argument("--heartbeat-interval", type=float, default=300.0, help="Heartbeat cadence in seconds.")
    parser.add_argument("--once", action="store_true", help="Process inbox once and exit.")
    return parser


def main(argv: Iterable[str] | None = None) -> int:
    args = build_parser().parse_args(list(argv) if argv is not None else None)
    executor = ResidentMissionExecutor(
        resident=args.resident,
        poll_interval=args.poll_interval,
        heartbeat_interval=args.heartbeat_interval,
    )
    if args.once:
        executor.process_once()
        executor.log_event("heartbeat", {"active_missions": 0})
        return 0
    executor.run_forever()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
