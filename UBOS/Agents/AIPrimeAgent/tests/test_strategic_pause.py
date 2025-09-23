"""Tests for Strategic Pause module."""

from pathlib import Path
import sys

import pytest

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from ai_prime_agent.blueprint.schema import validate_blueprint_dict
from ai_prime_agent.pause import StrategicPause


@pytest.fixture()
def blueprint():
    return validate_blueprint_dict(
        {
            "blueprint_metadata": {
                "schema_version": "1.0",
                "document_version": "1.0.0",
                "last_updated_utc": "2025-09-22T10:00:00Z",
                "review_cadence_days": 30,
                "ubos_alignment": ["Strategic Pause"],
            },
            "missionStatement": "Multiply capacity via orchestration.",
            "corePrinciples": [
                {"principleId": "UBOS-P-01", "statement": "Blueprint Thinking"}
            ],
            "activeGoals": [],
            "agentRegistry": [],
            "guardrails": {},
        }
    )


def test_post_synthesis_proceed(blueprint):
    pause = StrategicPause(blueprint)
    result = {
        "final_confidence": 0.7,
        "consultation": {"recommendations": [{"title": "X"}]},
    }
    decision = pause.post_synthesis(result=result)
    assert decision.status == "proceed"


def test_post_synthesis_escalate_low_confidence(blueprint):
    pause = StrategicPause(blueprint)
    result = {"final_confidence": 0.4, "consultation": {"recommendations": [{"t": 1}]}}
    decision = pause.post_synthesis(result=result)
    assert decision.status == "escalate"
    assert any("Low" in r for r in decision.reasons)

