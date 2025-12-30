from __future__ import annotations
import os

import argparse
import json
import signal
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple

from datetime import datetime
from config import load_configuration
from mission_queue_manager import MissionQueueManager
from reasoning_fork import ReasoningFork, Task, Resident
from mechanical_bouncer import MechanicalBouncer

def _parse_priority(value: Any) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return 0.0


def _parse_timestamp(value: Any) -> float:
    if isinstance(value, (int, float)):
        return float(value)
    if isinstance(value, str):
        try:
            normalized = value.replace("Z", "+00:00")
            return datetime.fromisoformat(normalized).timestamp()
        except (ValueError, TypeError):
            return 0.0
    return 0.0


@dataclass(slots=True)
class DispatcherConfig:
    poll_interval: float = 30.0
    heartbeat_interval: float = 300.0
    dispatcher_name: str = "mission_dispatcher"


class MissionDispatcher:
    """Continuously assigns queued missions to residents based on priority."""

    def __init__(
        self,
        config: DispatcherConfig | None = None,
        *,
        manager: MissionQueueManager | None = None,
        log_path: Path | None = None,
    ) -> None:
        self.config = config or DispatcherConfig()
        paths, _ = load_configuration()
        self.manager = manager or MissionQueueManager()
        self.log_path = log_path or (paths.log_dir / "dispatcher.jsonl")
        self.log_path.parent.mkdir(parents=True, exist_ok=True)
        self.fork = ReasoningFork()
        self.bouncer = MechanicalBouncer()
        self._stop_requested = False
        signal.signal(signal.SIGTERM, self._request_stop)
        signal.signal(signal.SIGINT, self._request_stop)

    def _request_stop(self, _signum: int, _frame: Any) -> None:
        self._stop_requested = True

    def log_event(self, event: str, payload: Dict[str, Any]) -> None:
        record = {
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "event": event,
            **payload,
        }
        with self.log_path.open("a", encoding="utf-8") as handle:
            json.dump(record, handle)
            handle.write("\n")

    def _queued_missions(self) -> List[Tuple[float, float, Path, Dict[str, Any]]]:
        missions: List[Tuple[float, float, Path, Dict[str, Any]]] = []
        queue_dir = self.manager.missions.queued
        
        try:
            found_files_raw = os.listdir(queue_dir)
        except OSError:
            return []

        found_files = [queue_dir / f for f in found_files_raw if f.endswith(".json")]
        for path in sorted(found_files):
            try:
                with path.open("r", encoding="utf-8") as handle:
                    mission = json.load(handle)
            except json.JSONDecodeError:
                self.manager.fail_queued_mission(path.stem, "Invalid JSON payload")
                self.log_event(
                    "assignment_error",
                    {"mission_id": path.stem, "error": "Invalid JSON payload"},
                )
                continue
            priority = _parse_priority(mission.get("priority"))
            created_at = (
                _parse_timestamp(mission.get("created_at"))
                or _parse_timestamp(mission.get("queued_at"))
                or path.stat().st_mtime
            )
            missions.append((-priority, created_at, path, mission))
        missions.sort()
        return missions

    def process_queue(self) -> int:
        assignments = 0
        queued = self._queued_missions()
        for _, _, path, mission in queued:
            mission_id = mission.get("mission_id") or path.stem
            
            # 1. Reasoning Fork: Determine Resident
            # If assigned_to is already set (forced), respect it, unless it's 'auto'
            assigned_to = mission.get("assigned_to")
            
            if not assigned_to or assigned_to == "auto" or assigned_to == "janus":
                task = Task(
                    type=mission.get("type", "analysis"),
                    priority=str(mission.get("priority", "normal")).lower(),
                    complexity=mission.get("complexity", "medium"),
                    cost_budget=float(mission.get("cost_budget", 1.0)),
                    requires_reasoning=mission.get("requires_reasoning", False),
                    source=mission.get("source", "internal")
                )
                decision = self.fork.route(task)
                assigned_to = decision.value
                
                # Update mission with decision
                mission["assigned_to"] = assigned_to
                mission["routing_decision"] = self.fork.explain_routing(task)
                
                # Save update back to queue file before assigning
                with path.open("w", encoding="utf-8") as f:
                    json.dump(mission, f, indent=2)

            # 2. Mechanical Bouncer: Check Availability
            if not self.bouncer.check_admission(assigned_to):
                # Rate limited, try failover
                backup = self.bouncer.get_backup(assigned_to)
                self.log_event("rate_limited", {"mission_id": mission_id, "resident": assigned_to, "failover": backup})
                assigned_to = backup
                # Update again
                mission["assigned_to"] = assigned_to
                with path.open("w", encoding="utf-8") as f:
                    json.dump(mission, f, indent=2)
                
                # If backup also full? (Simple check for now: allow backup)
            
            if not assigned_to:
                 self.manager.fail_queued_mission(mission_id, "Mission missing assigned_to")
                 continue

            try:
                # Note: assign_specific_mission sends the message to the resident's inbox
                result = self.manager.assign_specific_mission(mission_id)
                if result is None:
                    continue
                assignments += 1
                self.log_event(
                    "mission_assigned",
                    {
                        "mission_id": mission_id,
                        "resident": assigned_to,
                        "priority": mission.get("priority"),
                        "routing": mission.get("routing_decision", {}).get("reason")
                    },
                )
            except Exception as exc:
                self.manager.fail_queued_mission(mission_id, str(exc))
                self.log_event(
                    "assignment_error",
                    {"mission_id": mission_id, "error": str(exc)},
                )
        return assignments

    def run_forever(self) -> None:
        next_heartbeat = time.monotonic() + self.config.heartbeat_interval
        self.log_event("dispatcher_started", {"poll_interval": self.config.poll_interval})

        while not self._stop_requested:
            try:
                self.process_queue()
            except Exception as exc:  # pragma: no cover - defensive guard
                self.log_event("dispatcher_exception", {"error": str(exc)})

            now = time.monotonic()
            if now >= next_heartbeat:
                queued_count = len(list(self.manager.missions.queued.glob("*.json")))
                active_count = len(list(self.manager.missions.active.glob("*.json")))
                self.log_event(
                    "heartbeat",
                    {"queued": queued_count, "active": active_count},
                )
                next_heartbeat = now + self.config.heartbeat_interval

            sleep_seconds = max(self.config.poll_interval, 0.1)
            # Wait with responsiveness to stop requests.
            end_time = time.monotonic() + sleep_seconds
            while time.monotonic() < end_time:
                if self._stop_requested:
                    break
                time.sleep(min(0.5, end_time - time.monotonic()))

        self.log_event("dispatcher_stopped", {})


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Janus mission dispatcher daemon.")
    parser.add_argument("--poll-interval", type=float, default=30.0, help="Polling cadence in seconds.")
    parser.add_argument("--heartbeat-interval", type=float, default=300.0, help="Heartbeat cadence in seconds.")
    parser.add_argument("--once", action="store_true", help="Process queue once and exit (testing mode).")
    return parser


def main(argv: Iterable[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(list(argv) if argv is not None else None)

    try:
        dispatcher = MissionDispatcher(
            DispatcherConfig(
                poll_interval=args.poll_interval,
                heartbeat_interval=args.heartbeat_interval,
            )
        )
    except Exception as exc:
        print(f"ERROR: Dispatcher initialization failed: {exc}", file=sys.stderr)
        return 1

    if args.once:
        try:
            dispatcher.process_queue()
            dispatcher.log_event("heartbeat", {"queued": 0, "active": 0})
            return 0
        except Exception as exc:
            print(f"ERROR: Dispatcher --once execution failed: {exc}", file=sys.stderr)
            dispatcher.log_event("dispatcher_exception_once", {"error": str(exc)})
            return 1

    try:
        dispatcher.run_forever()
    except Exception as exc:
        print(f"ERROR: Dispatcher run_forever failed: {exc}", file=sys.stderr)
        dispatcher.log_event("dispatcher_exception_run_forever", {"error": str(exc)})
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
