"""Agent Registry module tests."""

from datetime import datetime, timedelta, timezone
from pathlib import Path
import sys

import pytest

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from ai_prime_agent.registry import (
    AgentCapability,
    AgentRecord,
    AgentRegistry,
    AgentStatus,
    RegistryError,
)


@pytest.fixture()
def registry() -> AgentRegistry:
    return AgentRegistry()


@pytest.fixture()
def sample_capabilities():
    return [
        AgentCapability(
            name="concept_lookup",
            version="1.0.0",
            description="Query knowledge base",
            input_schema={"type": "object"},
            output_schema={"type": "object"},
        ),
        AgentCapability(
            name="alignment_consult",
            version="1.0.0",
            description="Consult Master Librarian",
            input_schema={"type": "object"},
            output_schema={"type": "object"},
        ),
    ]


def test_register_and_get_agent(registry, sample_capabilities):
    record = registry.register(
        AgentRecord.create(
            agent_id="A-ml-001",
            agent_type="MasterLibrarian",
            capabilities=sample_capabilities,
            status=AgentStatus.IDLE,
            metadata={"version": "2.0"},
        )
    )
    fetched = registry.get(record.agent_id)
    assert fetched.agent_type == "MasterLibrarian"
    assert fetched.metadata["version"] == "2.0"


def test_register_duplicate_fails(registry, sample_capabilities):
    record = AgentRecord.create(
        agent_id="A-dup-001",
        agent_type="ResearchAgent",
        capabilities=sample_capabilities,
    )
    registry.register(record)
    with pytest.raises(RegistryError):
        registry.register(record)


def test_capability_query_filters_status(registry):
    cap = AgentCapability(
        name="execute_web_search",
        version="1.0",
        description="Perform web research",
        input_schema={"type": "object"},
        output_schema={"type": "object"},
    )
    agent = AgentRecord.create(
        agent_id="A-re-001",
        agent_type="ResearchAgent",
        capabilities=[cap],
        status=AgentStatus.IDLE,
    )
    registry.register(agent)
    results = registry.query_by_capability("execute_web_search", include_statuses=[AgentStatus.IDLE])
    assert results and results[0].agent_id == "A-re-001"
    assert not registry.query_by_capability("execute_web_search", include_statuses=[AgentStatus.BUSY])


def test_record_heartbeat_updates_status_and_metrics(registry, sample_capabilities):
    agent = registry.register(
        AgentRecord.create(
            agent_id="A-ml-002",
            agent_type="MasterLibrarian",
            capabilities=sample_capabilities,
            status=AgentStatus.IDLE,
        )
    )
    registry.record_heartbeat(
        agent.agent_id,
        status=AgentStatus.BUSY,
        load_percentage=80,
        response_time_ms=120,
        error_count=3,
    )
    updated = registry.get(agent.agent_id)
    assert updated.status == AgentStatus.BUSY
    assert updated.telemetry.current_load_percentage == 80.0
    assert updated.telemetry.avg_response_time_ms == 120
    assert updated.telemetry.error_count == 3


def test_prune_marks_stale_agents(registry, sample_capabilities, monkeypatch):
    agent = registry.register(
        AgentRecord.create(
            agent_id="A-tm-001",
            agent_type="TelemetryAgent",
            capabilities=sample_capabilities,
            status=AgentStatus.ACTIVE,
        )
    )

    # Force telemetry to appear old
    stale_time = (datetime.now(timezone.utc) - timedelta(seconds=3600)).strftime("%Y-%m-%dT%H:%M:%SZ")
    agent.telemetry.last_heartbeat_utc = stale_time

    stale = registry.prune_stale(timeout_seconds=300)
    assert stale and stale[0].agent_id == agent.agent_id
    assert registry.get(agent.agent_id).status == AgentStatus.ERROR


def test_deregister_removes_agent(registry, sample_capabilities):
    agent = registry.register(
        AgentRecord.create(
            agent_id="A-rm-001",
            agent_type="RemovableAgent",
            capabilities=sample_capabilities,
        )
    )
    registry.deregister(agent.agent_id)
    with pytest.raises(RegistryError):
        registry.get(agent.agent_id)
