"""Tests for the Strategic Blueprint schema utilities."""

from pathlib import Path
import sys

import pytest

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from ai_prime_agent.blueprint.schema import (
    BlueprintValidationError,
    StrategicBlueprint,
    validate_blueprint_dict,
)


@pytest.fixture()
def sample_blueprint_dict() -> dict:
    return {
        "blueprint_metadata": {
            "schema_version": "1.0",
            "document_version": "1.0.0",
            "last_updated_utc": "2025-09-22T10:00:00Z",
            "review_cadence_days": 30,
            "ubos_alignment": ["Blueprint Thinking", "Strategic Pause"],
        },
        "missionStatement": "Build systems that multiply contribution without constant supervision.",
        "corePrinciples": [
            {
                "principleId": "UBOS-P-01",
                "statement": "Never orchestrate without a valid Strategic Blueprint loaded.",
                "rationale": "Prevents willpower-driven improvisation.",
            }
        ],
        "activeGoals": [
            {
                "goalId": "G-0001",
                "objective": "Document research-to-librarian workflow.",
                "keyResults": [
                    "Process documented within 48 hours",
                    "Validation service certifies alignment",
                ],
                "status": "active",
                "assignedAgentIds": ["A-0002"],
                "processDocumentationURI": "ubos://docs/workflows/G-0001.md",
            }
        ],
        "agentRegistry": [
            {
                "agentId": "A-0001",
                "name": "Master Librarian",
                "capabilities": ["concept_lookup", "alignment_consult"],
                "status": "active",
            },
            {
                "agentId": "A-0002",
                "name": "Research Agent",
                "capabilities": ["external_research", "insight_synthesis"],
                "status": "active",
            },
        ],
        "guardrails": {
            "operational": {
                "maxResourceAllocation": 25,
                "apiCallLimits": {"per_hour": 50},
            },
            "ethical": {
                "principleConflictPolicy": "pause_and_escalate",
                "humanInTheLoopTriggers": ["High risk user impact"],
            },
            "adaptive": {
                "reviewCadenceDays": 30,
                "performanceDegradationThreshold": 5,
            },
        },
    }


def test_validate_blueprint_success(sample_blueprint_dict):
    blueprint = validate_blueprint_dict(sample_blueprint_dict)
    assert isinstance(blueprint, StrategicBlueprint)
    assert blueprint.metadata.schema_version == "1.0"
    assert blueprint.core_principles[0].principle_id == "UBOS-P-01"
    assert blueprint.active_goals[0].goal_id == "G-0001"


def test_validate_blueprint_missing_mission_statement(sample_blueprint_dict):
    sample_blueprint_dict.pop("missionStatement")
    with pytest.raises(BlueprintValidationError):
        validate_blueprint_dict(sample_blueprint_dict)


def test_goal_id_pattern_enforced(sample_blueprint_dict):
    sample_blueprint_dict["activeGoals"][0]["goalId"] = "INVALID"
    with pytest.raises(BlueprintValidationError):
        validate_blueprint_dict(sample_blueprint_dict)


def test_agent_pattern_enforced(sample_blueprint_dict):
    sample_blueprint_dict["agentRegistry"][0]["agentId"] = "AGENT-1"
    with pytest.raises(BlueprintValidationError):
        validate_blueprint_dict(sample_blueprint_dict)


def test_guardrails_defaults(sample_blueprint_dict):
    sample_blueprint_dict["guardrails"].pop("operational")
    blueprint = validate_blueprint_dict(sample_blueprint_dict)
    assert blueprint.guardrails.operational == {}
