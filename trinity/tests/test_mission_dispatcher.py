from __future__ import annotations

import json
from pathlib import Path

from mission_dispatcher_daemon import DispatcherConfig, MissionDispatcher
from mission_queue_manager import MissionQueueManager, isoformat_now


def _mission(template: str, assigned_to: str, priority: int) -> dict[str, object]:
    return {
        "mission_id": f"{template}-{priority}",
        "objective": "Test assignment flow",
        "assigned_to": assigned_to,
        "priority": priority,
        "required_tools": [],
        "deliverable": {
            "type": "comms_hub_message",
            "recipient": "captain",
            "message_type": "test_report",
        },
        "created_at": isoformat_now(),
    }


def test_dispatcher_assigns_high_priority_first(tmp_path: Path) -> None:
    comms_root = tmp_path / "comms"
    mission_root = comms_root / "missions"
    log_path = tmp_path / "dispatcher.jsonl"

    manager = MissionQueueManager(
        dispatcher_agent="codex",
        comms_root=comms_root,
        mission_root=mission_root,
        log_path=tmp_path / "queue_manager.jsonl",
    )

    manager.queue_mission(_mission("low", "groq", 1))
    manager.queue_mission(_mission("high", "groq", 5))

    dispatcher = MissionDispatcher(
        DispatcherConfig(poll_interval=0.1, heartbeat_interval=5.0),
        manager=manager,
        log_path=log_path,
    )

    assigned = dispatcher.process_queue()
    assert assigned == 2

    active_files = sorted(manager.missions.active.glob("*.json"))
    assert len(active_files) == 2
    with active_files[0].open("r", encoding="utf-8") as handle:
        mission_data = json.load(handle)
    assert mission_data["assigned_to"] == "groq"

    log_entries = [json.loads(line) for line in log_path.read_text(encoding="utf-8").splitlines() if line.strip()]
    assignment_events = [entry for entry in log_entries if entry.get("event") == "mission_assigned"]
    assert len(assignment_events) == 2
