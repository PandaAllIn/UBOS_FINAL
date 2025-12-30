from __future__ import annotations

import json
from pathlib import Path

from trinity.mission_queue_manager import MissionQueueManager, isoformat_now


def _sample_mission() -> dict[str, object]:
    return {
        "objective": "Verify mission queue end-to-end flow.",
        "assigned_to": "groq",
        "priority": 1,
        "required_tools": ["test.tool"],
        "deliverable": {
            "type": "comms_hub_message",
            "recipient": "captain",
            "message_type": "test_report",
        },
        "created_at": isoformat_now(),
        "deadline": None,
    }


def test_mission_queue_end_to_end(tmp_path: Path) -> None:
    comms_root = tmp_path / "comms"
    mission_root = comms_root / "missions"
    log_path = tmp_path / "mission_log.jsonl"
    manager = MissionQueueManager(
        dispatcher_agent="codex",
        comms_root=comms_root,
        mission_root=mission_root,
        log_path=log_path,
    )

    queued_path = manager.queue_mission(_sample_mission())
    assert queued_path.exists()
    queued_data = json.loads(queued_path.read_text(encoding="utf-8"))
    mission_id = queued_data["mission_id"]

    assigned = manager.assign_mission("groq")
    assert assigned is not None
    assert assigned["mission_id"] == mission_id
    active_file = mission_root / "active" / f"{mission_id}.json"
    assert active_file.exists()

    inbox_files = sorted((comms_root / "groq" / "inbox").glob("*.json"))
    assert inbox_files, "Mission assignment puck not delivered to inbox"

    completed_path = manager.complete_mission(mission_id)
    assert completed_path is not None
    assert completed_path.exists()
    assert not active_file.exists()

    completed_data = json.loads(completed_path.read_text(encoding="utf-8"))
    assert completed_data["status"] == "completed"
    assert "completed_at" in completed_data

    listed = manager.list_missions("completed")
    assert any(m.get("mission_id") == mission_id for m in listed)


def test_assign_specific_and_fail_queued(tmp_path: Path) -> None:
    comms_root = tmp_path / "comms"
    mission_root = comms_root / "missions"
    log_path = tmp_path / "mission_log.jsonl"
    manager = MissionQueueManager(
        dispatcher_agent="codex",
        comms_root=comms_root,
        mission_root=mission_root,
        log_path=log_path,
    )

    mission = _sample_mission()
    queued_path = manager.queue_mission(mission)
    mission_id = queued_path.stem

    assigned = manager.assign_specific_mission(mission_id)
    assert assigned is not None
    assert assigned["mission_id"] == mission_id
    assert (mission_root / "active" / f"{mission_id}.json").exists()

    mission2 = _sample_mission()
    mission2["mission_id"] = "MISSION-TWO"
    manager.queue_mission(mission2)
    failed_path = manager.fail_queued_mission("MISSION-TWO", "invalid setup")
    assert failed_path is not None
    assert failed_path.exists()
    failed_data = json.loads(failed_path.read_text(encoding="utf-8"))
    assert failed_data["status"] == "failed"
    assert failed_data["error_message"] == "invalid setup"
