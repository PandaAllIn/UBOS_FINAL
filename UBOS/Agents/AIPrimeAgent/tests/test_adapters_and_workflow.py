"""Integration-style tests for adapters and the Research & Synthesize workflow."""

from pathlib import Path
import sys

import pytest

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from ai_prime_agent.blueprint.schema import validate_blueprint_dict
from ai_prime_agent.orchestrator import AIPrimeAgent
from ai_prime_agent.adapters import knowledge as knowledge_adapter
from ai_prime_agent.adapters import research as research_adapter


@pytest.fixture()
def blueprint():
    data = {
        "blueprint_metadata": {
            "schema_version": "1.0",
            "document_version": "1.0.0",
            "last_updated_utc": "2025-09-22T10:00:00Z",
            "review_cadence_days": 30,
            "ubos_alignment": ["Blueprint Thinking"],
        },
        "missionStatement": "Coordinate agents to multiply capacity.",
        "corePrinciples": [
            {"principleId": "UBOS-P-01", "statement": "Operate from a Strategic Blueprint"}
        ],
        "activeGoals": [],
        "agentRegistry": [],
        "guardrails": {},
    }
    return validate_blueprint_dict(data)


def test_register_adapters_and_run_workflow(blueprint):
    prime = AIPrimeAgent(blueprint=blueprint)
    comps = prime.components

    # Register adapters (keeping agents independent with explicit IDs)
    r = research_adapter.register_with_prime(
        agent_id="A-re-001",
        registry=comps.registry,
        register_handler=prime.register_adapter,
    )
    l = knowledge_adapter.register_with_prime(
        agent_id="A-ml-001",
        registry=comps.registry,
        register_handler=prime.register_adapter,
    )

    # Execute pilot workflow
    from ai_prime_agent.orchestrator.workflows import research_synthesize

    result = research_synthesize.run(prime, query="UBOS agent orchestration", depth="medium")

    assert "correlation_id" in result
    assert result["research"]["query"].startswith("UBOS agent orchestration")
    assert result["consultation"]["recommendations"]
    assert result["final_confidence"] >= 0.5
    # Pause and Validation now present
    assert "pause" in result and "validation" in result
    assert result["validation"]["status"] in {"VALID", "INVALID", "ESCALATE"}
