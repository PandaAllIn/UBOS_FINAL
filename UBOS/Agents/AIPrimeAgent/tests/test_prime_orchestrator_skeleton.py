"""Tests for AI Prime Orchestrator skeleton."""

from pathlib import Path
import sys

import pytest

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from ai_prime_agent.blueprint.schema import StrategicBlueprint
from ai_prime_agent.orchestrator import AIPrimeAgent
from ai_prime_agent.registry import AgentCapability, AgentRecord, AgentRegistry, AgentStatus


@pytest.fixture()
def sample_blueprint() -> StrategicBlueprint:
    from ai_prime_agent.blueprint.schema import validate_blueprint_dict

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


def test_prime_orchestrator_initialises_with_components(sample_blueprint):
    registry = AgentRegistry()
    prime = AIPrimeAgent(blueprint=sample_blueprint, registry=registry)
    comps = prime.components
    assert comps.blueprint.mission_statement.startswith("Coordinate")
    assert comps.registry is registry
    assert comps.bus is not None


def test_prime_registers_handler_and_reports_agents(sample_blueprint):
    registry = AgentRegistry()
    agent = registry.register(
        AgentRecord.create(
            agent_id="A-ml-001",
            agent_type="MasterLibrarian",
            capabilities=[
                AgentCapability(
                    name="consult.align",
                    version="1.0",
                    description="Alignment consultation",
                    input_schema={"type": "object"},
                    output_schema={"type": "object"},
                )
            ],
            status=AgentStatus.IDLE,
        )
    )
    prime = AIPrimeAgent(blueprint=sample_blueprint, registry=registry)

    def dummy_handler(msg):  # pragma: no cover - trivial path
        return {"ok": True}

    prime.register_adapter(agent_id=agent.agent_id, task="consult.align", handler=dummy_handler)
    info = prime.run_workflow(name="noop")
    assert info["status"] == "READY"
    assert agent.agent_id in info["registered_agents"]

