"""
UBOS Blueprint: Agent Communication Protocol (v0.1)

Philosophy: Smallest Working Version + Systems Over Willpower
Strategic Purpose: Provide a strict, validated envelope for inter‑agent messages so
delegation and tracing are predictable, auditable, and easy to extend.
System Design: Dataclasses for message and ack/nack envelopes, UUID/ISO validation,
and helpers to create and verify messages consistently.
Feedback Loops: Validation failures surface immediately; correlation IDs enable
end‑to‑end tracing; versioned protocol supports safe evolution.
Environmental Support: Designed for in‑process bus today; swappable to HTTP/MCP/queue
transports later without changing message semantics.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, Optional
import uuid


PROTOCOL_VERSION = "0.1"


class ProtocolError(ValueError):
    """Raised when a message fails protocol validation."""


def _now_iso_utc() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _require_uuid(name: str, value: str) -> str:
    try:
        uuid.UUID(str(value))
        return str(value)
    except Exception as exc:  # pragma: no cover - defensive path
        raise ProtocolError(f"{name} must be a valid UUID") from exc


def _require_str(name: str, value: Any) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ProtocolError(f"{name} must be a non-empty string")
    return value.strip()


def _require_dict(name: str, value: Any) -> Dict[str, Any]:
    if not isinstance(value, dict):
        raise ProtocolError(f"{name} must be an object")
    return value


def _require_iso_utc(name: str, value: Any) -> str:
    s = _require_str(name, value)
    try:
        datetime.strptime(s, "%Y-%m-%dT%H:%M:%SZ")
        return s
    except Exception as exc:  # pragma: no cover - defensive path
        raise ProtocolError(f"{name} must be ISO-8601 UTC 'YYYY-MM-DDTHH:MM:SSZ'") from exc


@dataclass
class TaskMessage:
    """
    UBOS Principle: Consistency enables repeatability (Blueprint Thinking)
    Strategic Value: A single canonical envelope for all inter‑agent tasks.
    System Role: Inputs to the communication bus; persisted in transcripts.

    Fields mirror the initial v0.1 protocol, and are intentionally minimal.
    """

    protocol_version: str
    message_id: str
    correlation_id: str
    timestamp_utc: str
    source_agent_id: str
    destination_agent_id: str
    task: str
    payload: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def new(
        cls,
        *,
        source_agent_id: str,
        destination_agent_id: str,
        task: str,
        payload: Optional[Dict[str, Any]] = None,
        metadata: Optional[Dict[str, Any]] = None,
        correlation_id: Optional[str] = None,
    ) -> "TaskMessage":
        return cls(
            protocol_version=PROTOCOL_VERSION,
            message_id=str(uuid.uuid4()),
            correlation_id=correlation_id or str(uuid.uuid4()),
            timestamp_utc=_now_iso_utc(),
            source_agent_id=_require_str("source_agent_id", source_agent_id),
            destination_agent_id=_require_str("destination_agent_id", destination_agent_id),
            task=_require_str("task", task),
            payload=dict(payload or {}),
            metadata=dict(metadata or {}),
        )

    def validate(self) -> "TaskMessage":
        if self.protocol_version != PROTOCOL_VERSION:
            raise ProtocolError("protocol_version mismatch")
        _require_uuid("message_id", self.message_id)
        _require_uuid("correlation_id", self.correlation_id)
        _require_iso_utc("timestamp_utc", self.timestamp_utc)
        _require_str("source_agent_id", self.source_agent_id)
        _require_str("destination_agent_id", self.destination_agent_id)
        _require_str("task", self.task)
        _require_dict("payload", self.payload)
        _require_dict("metadata", self.metadata)
        return self


@dataclass
class Ack:
    """
    UBOS Principle: Strategic Pause (explicit acknowledgment)
    Strategic Value: Immediate feedback that the bus accepted responsibility.
    System Role: Synchronous response to dispatch; not task completion.
    """

    message_id: str
    correlation_id: str
    status: str = "ACK"
    reason: Optional[str] = None

    @classmethod
    def for_message(cls, msg: TaskMessage, reason: Optional[str] = None) -> "Ack":
        return cls(message_id=msg.message_id, correlation_id=msg.correlation_id, reason=reason)


@dataclass
class Nack:
    """
    UBOS Principle: Systems Over Willpower (fail fast with clarity)
    Strategic Value: Reject invalid or unroutable messages early and explicitly.
    System Role: Synchronous response to dispatch when validation/route fails.
    """

    message_id: str
    correlation_id: str
    status: str = "NACK"
    reason: str = ""

    @classmethod
    def for_message(cls, msg: TaskMessage, reason: str) -> "Nack":
        return cls(message_id=msg.message_id, correlation_id=msg.correlation_id, reason=_require_str("reason", reason))


def validate_message(payload: Dict[str, Any]) -> TaskMessage:
    """Construct and validate a TaskMessage from a dict payload."""
    msg = TaskMessage(
        protocol_version=str(payload.get("protocol_version", "")),
        message_id=str(payload.get("message_id", "")),
        correlation_id=str(payload.get("correlation_id", "")),
        timestamp_utc=str(payload.get("timestamp_utc", "")),
        source_agent_id=str(payload.get("source_agent_id", "")),
        destination_agent_id=str(payload.get("destination_agent_id", "")),
        task=str(payload.get("task", "")),
        payload=dict(payload.get("payload", {}) or {}),
        metadata=dict(payload.get("metadata", {}) or {}),
    )
    return msg.validate()


__all__ = [
    "PROTOCOL_VERSION",
    "ProtocolError",
    "TaskMessage",
    "Ack",
    "Nack",
    "validate_message",
]

