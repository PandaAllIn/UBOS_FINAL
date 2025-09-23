"""Tests for the Blueprint Validation service."""

from pathlib import Path
import sys

import pytest

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from ai_prime_agent.blueprint.schema import validate_blueprint_dict
from ai_prime_agent.validation import BlueprintValidator


@pytest.fixture()
def blueprint():
    return validate_blueprint_dict(
        {
            "blueprint_metadata": {
                "schema_version": "1.0",
                "document_version": "1.0.0",
                "last_updated_utc": "2025-09-22T10:00:00Z",
                "review_cadence_days": 30,
                "ubos_alignment": ["Blueprint Thinking"],
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


def test_validation_passes_minimum_requirements(blueprint):
    validator = BlueprintValidator(blueprint)
    workflow_result = {
        "final_confidence": 0.7,
        "research": {"query": "ubos"},
        "consultation": {"recommendations": [{"title": "Blueprint Thinking"}]},
    }
    report = validator.validate_workflow_result(workflow_result)
    assert report.status == "VALID"
    assert not report.issues
    assert any("Alignment" in n for n in report.alignment_notes)


def test_validation_flags_missing_recommendations(blueprint):
    validator = BlueprintValidator(blueprint)
    bad_result = {"final_confidence": 0.6, "research": {"query": "x"}, "consultation": {"recommendations": []}}
    report = validator.validate_workflow_result(bad_result)
    assert report.status in {"INVALID", "ESCALATE"}
    assert any("recommendations" in i for i in report.issues)

