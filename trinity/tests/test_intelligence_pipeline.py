from __future__ import annotations

import json
from datetime import datetime, timedelta, timezone
from pathlib import Path

from trinity.intelligence_action_generator import IntelligenceActionGenerator
from trinity.intelligence_collector import IntelligenceCollector
from trinity.intelligence_tools import IntelligenceDatabase, _INTEL_DB, intel_lookup
from trinity.mission_queue_manager import MissionQueueManager


def _write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def _build_grant_mission(tmp_path: Path) -> tuple[Path, Path]:
    mission_dir = tmp_path / "missions" / "completed"
    archive_dir = tmp_path / "COMMS_HUB" / "claude" / "archive"
    deadline = (datetime.now(timezone.utc) + timedelta(days=20)).isoformat()
    mission_payload = {
        "mission_id": "GROQ-TEST-GRANT-001",
        "source_template": "grant_hunter_daily",
        "priority": 4,
        "completed_at": datetime.now(timezone.utc).isoformat(),
        "deliverable": {
            "type": "comms_hub_message",
            "recipient": "claude",
            "message_type": "grant_opportunity",
        },
        "objective": "Identify high-fit EU funding opportunities with upcoming deadlines.",
    }
    deliverable_payload = {
        "opportunities": [
            {
                "title": "Sovereign Data Center Upgrade",
                "program": "Horizon Europe",
                "deadline": deadline,
                "budget": 7500000,
                "fit_score": 4.8,
                "status": "new",
            }
        ]
    }
    mission_path = mission_dir / f"{mission_payload['mission_id']}.json"
    archive_path = archive_dir / f"groq-msg-{mission_payload['mission_id']}.json"
    _write_json(mission_path, mission_payload)
    _write_json(archive_path, deliverable_payload)
    return mission_path, archive_path


def _build_revenue_mission(tmp_path: Path) -> tuple[Path, Path]:
    mission_dir = tmp_path / "missions" / "completed"
    archive_dir = tmp_path / "COMMS_HUB" / "claude" / "archive"
    mission_payload = {
        "mission_id": "GROQ-TEST-REMOTE-001",
        "source_template": "eu_remote_opportunity_scout_daily",
        "priority": 3,
        "completed_at": datetime.now(timezone.utc).isoformat(),
        "deliverable": {
            "type": "comms_hub_message",
            "recipient": "claude",
            "message_type": "remote_revenue_signals",
        },
        "objective": "Locate remote EU AI consulting engagements.",
    }
    deliverable_payload = {
        "signals": [
            {
                "title": "Fractional AI Lead",
                "company": "Nordic AI Labs",
                "channel": "RemoteEU",
                "value_estimate": 6000,
                "probability": 0.6,
                "stage": "lead",
                "duration": "3 months",
                "tags": ["remote", "ai_consulting"],
            }
        ],
        "summary": {"total_signals": 1},
    }
    mission_path = mission_dir / f"{mission_payload['mission_id']}.json"
    archive_path = archive_dir / f"groq-msg-{mission_payload['mission_id']}.json"
    _write_json(mission_path, mission_payload)
    _write_json(archive_path, deliverable_payload)
    return mission_path, archive_path


def test_full_intelligence_pipeline(tmp_path: Path, monkeypatch) -> None:
    db_path = tmp_path / "intelligence.db"
    cache_dir = tmp_path / "intel_cache"
    mission_path, archive_path = _build_grant_mission(tmp_path)

    test_db = IntelligenceDatabase(db_path=db_path)
    monkeypatch.setattr("trinity.intelligence_tools._INTEL_DB", test_db, raising=False)

    collector = IntelligenceCollector(
        missions_dir=mission_path.parent,
        archive_root=archive_path.parents[2],
        cache_dir=cache_dir,
        log_path=tmp_path / "collector.log",
        db_path=db_path,
    )

    nodes = collector.collect_once(force_rescan=True)
    assert nodes, "collector should extract at least one intelligence node"

    with test_db._connection() as connection:
        rows = list(connection.execute("SELECT title, fit_score, status FROM grants"))
    assert rows, "grant intelligence should be stored in database"
    title, fit_score, status = rows[0]
    assert "Sovereign Data Center" in title
    assert abs(fit_score - 4.8) < 0.01
    assert status == "new"

    results = intel_lookup("grants", {"fit_score": ">=4.5", "deadline": "<=30"}, limit=5)
    assert results and results[0]["title"].startswith("Sovereign")

    # Revenue mission ingestion
    revenue_mission, revenue_archive = _build_revenue_mission(tmp_path)
    collector.collect_once()
    with test_db._connection() as connection:
        revenue_rows = list(connection.execute("SELECT channel, value_estimate FROM revenue_signals"))
    assert revenue_rows and revenue_rows[0][0] == "RemoteEU"

    queue_root = tmp_path / "queue"
    queue_manager = MissionQueueManager(
        dispatcher_agent="codex",
        comms_root=queue_root,
        mission_root=queue_root / "missions",
        log_path=tmp_path / "queue.log",
    )
    generator = IntelligenceActionGenerator(
        db_path=db_path,
        queue_manager=queue_manager,
        state_file=tmp_path / "actions_state.json",
        log_path=tmp_path / "actions.log",
    )

    generated = generator.run(dry_run=False)
    assert generated, "action generator should spawn a mission for high-fit grant"
    queued_files = list((queue_root / "missions" / "queued").glob("*.json"))
    assert queued_files, "queued mission file should exist"

    # Ensure no duplicate mission spawns on second run
    second_pass = generator.run(dry_run=False)
    assert not second_pass, "processed intelligence should not spawn duplicate missions"
