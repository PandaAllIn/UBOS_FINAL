"""Tests for transcript logging via bus observer and JSONL logger."""

from pathlib import Path
import json
import sys

import pytest

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from ai_prime_agent.bus import TaskMessage
from ai_prime_agent.bus.inproc_bus import InProcBus
from ai_prime_agent.registry import AgentCapability, AgentRecord, AgentRegistry, AgentStatus
from ai_prime_agent.telemetry.transcript import TranscriptLogger


def test_transcript_jsonl(tmp_path: Path):
    reg = AgentRegistry()
    agent = reg.register(
        AgentRecord.create(
            agent_id="A-ml-009",
            agent_type="MasterLibrarian",
            capabilities=[
                AgentCapability(
                    name="librarian.consult",
                    version="1.0",
                    description="Alignment consultation",
                    input_schema={"type": "object"},
                    output_schema={"type": "object"},
                )
            ],
            status=AgentStatus.IDLE,
        )
    )

    bus = InProcBus(reg)
    log_path = tmp_path / "transcript.jsonl"
    logger = TranscriptLogger(log_path)
    bus.add_observer(logger.append)

    def handler(msg: TaskMessage) -> dict:
        return {"ok": True}

    bus.register_handler(destination_agent_id=agent.agent_id, task="librarian.consult", handler=handler)

    msg = TaskMessage.new(
        source_agent_id="A-prime",
        destination_agent_id=agent.agent_id,
        task="librarian.consult",
        payload={"summary": "Test"},
    )
    ack = bus.dispatch(msg)
    assert getattr(ack, "status", "") == "ACK"

    lines = log_path.read_text(encoding="utf-8").strip().splitlines()
    assert len(lines) >= 2
    last = json.loads(lines[-1])
    assert last["direction"] == "egress"
    assert last["message"]["message_id"] == msg.message_id

