"""Tests for the in‑process bus MVP."""

from pathlib import Path
import sys

import pytest

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from ai_prime_agent.bus import TaskMessage
from ai_prime_agent.bus.inproc_bus import InProcBus
from ai_prime_agent.registry import AgentCapability, AgentRecord, AgentRegistry, AgentStatus


@pytest.fixture()
def registry() -> AgentRegistry:
    return AgentRegistry()


def test_dispatch_ack_and_handler_execution(registry):
    # Register destination agent
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

    # Bus with simple handler
    bus = InProcBus(registry)

    def handler(msg: TaskMessage) -> dict:
        return {"ok": True, "echo": msg.payload}

    bus.register_handler(destination_agent_id=agent.agent_id, task="consult.align", handler=handler)

    # Send message
    msg = TaskMessage.new(
        source_agent_id="A-prime",
        destination_agent_id=agent.agent_id,
        task="consult.align",
        payload={"summary": "Align protocol"},
    )
    ack = bus.dispatch(msg)
    assert getattr(ack, "status", "") == "ACK"

    # Transcript and stored result
    entries = bus.transcript()
    assert entries and entries[-1].result == {"ok": True, "echo": {"summary": "Align protocol"}}
    stored = bus.last_result_for(msg.message_id)
    assert stored and stored["ok"] is True


def test_dispatch_nack_unknown_destination(registry):
    bus = InProcBus(registry)
    msg = TaskMessage.new(
        source_agent_id="A-prime",
        destination_agent_id="A-missing",
        task="noop",
    )
    nack = bus.dispatch(msg)
    assert getattr(nack, "status", "") == "NACK"
    assert "Unknown destination" in getattr(nack, "reason", "")


def test_dispatch_nack_no_handler(registry):
    # Register agent but no handler for the task
    registry.register(
        AgentRecord.create(
            agent_id="A-ml-002",
            agent_type="MasterLibrarian",
            capabilities=[],
            status=AgentStatus.IDLE,
        )
    )
    bus = InProcBus(registry)
    msg = TaskMessage.new(
        source_agent_id="A-prime",
        destination_agent_id="A-ml-002",
        task="unknown.task",
    )
    nack = bus.dispatch(msg)
    assert getattr(nack, "status", "") == "NACK"
    assert "No handler" in getattr(nack, "reason", "")

