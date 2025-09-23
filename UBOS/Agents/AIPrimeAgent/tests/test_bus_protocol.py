"""Tests for the Agent Communication Protocol (v0.1)."""

from pathlib import Path
import sys
import uuid

import pytest

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from ai_prime_agent.bus import (
    PROTOCOL_VERSION,
    ProtocolError,
    TaskMessage,
    Ack,
    Nack,
    validate_message,
)


def test_new_message_and_validate_roundtrip():
    msg = TaskMessage.new(
        source_agent_id="A-prime",
        destination_agent_id="A-ml-001",
        task="consult.align",
        payload={"summary": "How to structure a bus?"},
        metadata={"priority": "high"},
    )
    assert msg.protocol_version == PROTOCOL_VERSION
    assert uuid.UUID(msg.message_id)
    assert uuid.UUID(msg.correlation_id)
    validated = msg.validate()
    assert validated is msg


def test_validate_message_from_dict_success():
    msg = TaskMessage.new(
        source_agent_id="A-prime",
        destination_agent_id="A-re-001",
        task="research.topics",
    )
    payload = {
        "protocol_version": msg.protocol_version,
        "message_id": msg.message_id,
        "correlation_id": msg.correlation_id,
        "timestamp_utc": msg.timestamp_utc,
        "source_agent_id": msg.source_agent_id,
        "destination_agent_id": msg.destination_agent_id,
        "task": msg.task,
        "payload": {},
        "metadata": {"trace": True},
    }
    out = validate_message(payload)
    assert out.message_id == msg.message_id


def test_validate_message_rejects_bad_uuid():
    payload = {
        "protocol_version": PROTOCOL_VERSION,
        "message_id": "not-a-uuid",
        "correlation_id": str(uuid.uuid4()),
        "timestamp_utc": "2025-09-22T10:00:00Z",
        "source_agent_id": "A-prime",
        "destination_agent_id": "A-unknown",
        "task": "noop",
        "payload": {},
        "metadata": {},
    }
    with pytest.raises(ProtocolError):
        validate_message(payload)


def test_ack_and_nack_helpers():
    msg = TaskMessage.new(
        source_agent_id="A-prime",
        destination_agent_id="A-ml-001",
        task="consult.align",
    )
    ack = Ack.for_message(msg)
    assert ack.status == "ACK" and ack.message_id == msg.message_id

    nack = Nack.for_message(msg, reason="Unknown destination")
    assert nack.status == "NACK" and "Unknown" in nack.reason

