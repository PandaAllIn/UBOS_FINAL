from __future__ import annotations

import json
from pathlib import Path

from config import TrinityPaths
from mission_queue_manager import MissionQueueManager, isoformat_now
from pucklib import TalkingDrumTransmitter
from resident_mission_executor import ResidentMissionExecutor


def _mission_template(template: str, resident: str) -> dict[str, object]:
    return {
        "mission_id": f"{template}-001",
        "objective": "Test mission execution",
        "assigned_to": resident,
        "priority": 3,
        "required_tools": [],
        "deliverable": {
            "type": "comms_hub_message",
            "recipient": "captain",
            "message_type": "test_completion",
        },
        "created_at": isoformat_now(),
        "source_template": template,
    }


def test_resident_executor_processes_mission(tmp_path: Path) -> None:
    comms_root = tmp_path / "comms"
    mission_root = comms_root / "missions"
    log_path = tmp_path / "executor.jsonl"

    manager = MissionQueueManager(
        dispatcher_agent="codex",
        comms_root=comms_root,
        mission_root=mission_root,
        log_path=tmp_path / "queue_manager.jsonl",
    )

    mission = _mission_template("test_template", "groq")
    queued_path = manager.queue_mission(mission)
    mission_id = mission["mission_id"]

    assert manager.assign_specific_mission(mission_id) is not None
    assignment_files = list((comms_root / "groq" / "inbox").glob("*.json"))
    assert assignment_files, "Mission assignment puck not delivered"

    summary_store: list[dict[str, object]] = []

    def handler(_mission: dict[str, object], _ctx):
        summary_store.append({"status": "ok"})
        return {"status": "ok"}

    executor = ResidentMissionExecutor(
        resident="groq",
        handlers={"test_template": handler},
        manager=manager,
        poll_interval=0.1,
        heartbeat_interval=2.0,
        log_path=log_path,
        paths=TrinityPaths(comms_hub=comms_root),
        transmitter=TalkingDrumTransmitter("groq", comms_root=comms_root),
    )

    processed = executor.process_once()
    assert processed == 1

    completed_file = manager.missions.completed / f"{mission_id}.json"
    assert completed_file.exists()
    completed_payload = json.loads(completed_file.read_text(encoding="utf-8"))
    assert completed_payload["status"] == "completed"

    deliverable_files = list((comms_root / "captain" / "inbox").glob("*.json"))
    assert deliverable_files, "Deliverable not transmitted to recipient inbox"

    log_entries = [json.loads(line) for line in log_path.read_text(encoding="utf-8").splitlines() if line.strip()]
    assert any(entry.get("event") == "mission_completed" for entry in log_entries)
    assert summary_store and summary_store[0]["status"] == "ok"
