"""
UBOS Blueprint: In‑Process Communication Bus (MVP)

Philosophy: The Smallest Working Version with clear structure.
Strategic Purpose: Provide a minimal, validated dispatch path that returns
immediate ACK/NACK and records transcripts for traceability.
System Design: Registry‑aware router with (agent_id, task) handlers, strict
message validation, and simple in‑memory transcripts.
Feedback Loops: Transcripts and handler errors surface quickly; ready to swap
transport without changing protocol.
Environmental Support: Depends only on the AgentRegistry and Protocol.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Dict, List, Optional, Tuple

from ai_prime_agent.bus import Ack, Nack, ProtocolError, TaskMessage, validate_message
from ai_prime_agent.registry import AgentRegistry, AgentStatus, RegistryError


Handler = Callable[[TaskMessage], dict]


@dataclass
class TranscriptEntry:
    direction: str  # "ingress" | "egress"
    message: TaskMessage
    result: Optional[dict] = None
    error: Optional[str] = None


class InProcBus:
    """Minimal in‑process bus with synchronous handler execution and ACK/NACK."""

    def __init__(self, registry: AgentRegistry) -> None:
        self._registry = registry
        self._handlers: Dict[Tuple[str, str], Handler] = {}
        self._transcript: List[TranscriptEntry] = []
        self._results: Dict[str, dict] = {}
        self._observers: List[Callable[[TranscriptEntry], None]] = []

    # --------------------------------------------------------------
    def register_handler(self, destination_agent_id: str, task: str, handler: Handler) -> None:
        key = (destination_agent_id, task)
        self._handlers[key] = handler

    # --------------------------------------------------------------
    def add_observer(self, observer: Callable[[TranscriptEntry], None]) -> None:
        """Register a callback to observe transcript entries as they are added."""
        self._observers.append(observer)

    # --------------------------------------------------------------
    def dispatch(self, payload: TaskMessage | dict) -> Ack | Nack:
        try:
            msg = payload if isinstance(payload, TaskMessage) else validate_message(payload)
        except ProtocolError as exc:
            # Cannot create a TaskMessage reliably; synthesize a minimal NACK
            correlation = getattr(payload, "get", lambda *_: None)("correlation_id") if isinstance(payload, dict) else None
            dummy = TaskMessage.new(
                source_agent_id="unknown",
                destination_agent_id="unknown",
                task="unknown",
                correlation_id=correlation,
            )
            return Nack.for_message(dummy, reason=str(exc))

        ingress = TranscriptEntry(direction="ingress", message=msg)
        self._transcript.append(ingress)
        for obs in self._observers:
            try:
                obs(ingress)
            except Exception:
                pass

        # Check destination exists and is routable
        try:
            agent = self._registry.get(msg.destination_agent_id)
        except RegistryError:
            egress = TranscriptEntry(direction="egress", message=msg, error="Unknown destination")
            self._transcript.append(egress)
            for obs in self._observers:
                try:
                    obs(egress)
                except Exception:
                    pass
            return Nack.for_message(msg, reason="Unknown destination agent")

        if agent.status in {AgentStatus.INACTIVE, AgentStatus.ERROR}:
            egress = TranscriptEntry(direction="egress", message=msg, error=f"Agent not available: {agent.status}")
            self._transcript.append(egress)
            for obs in self._observers:
                try:
                    obs(egress)
                except Exception:
                    pass
            return Nack.for_message(msg, reason=f"Destination not available: {agent.status}")

        handler = self._handlers.get((msg.destination_agent_id, msg.task))
        if not handler:
            egress = TranscriptEntry(direction="egress", message=msg, error="No handler for task")
            self._transcript.append(egress)
            for obs in self._observers:
                try:
                    obs(egress)
                except Exception:
                    pass
            return Nack.for_message(msg, reason="No handler for destination/task")

        # Execute synchronously for MVP; still return ACK to signal acceptance
        try:
            result = handler(msg)
            self._results[msg.message_id] = result
            egress = TranscriptEntry(direction="egress", message=msg, result=result)
            self._transcript.append(egress)
            for obs in self._observers:
                try:
                    obs(egress)
                except Exception:
                    pass
            return Ack.for_message(msg)
        except Exception as exc:  # pragma: no cover - handler failures are defensive
            egress = TranscriptEntry(direction="egress", message=msg, error=str(exc))
            self._transcript.append(egress)
            for obs in self._observers:
                try:
                    obs(egress)
                except Exception:
                    pass
            return Nack.for_message(msg, reason=f"Handler error: {exc}")

    # --------------------------------------------------------------
    def transcript(self) -> List[TranscriptEntry]:
        return list(self._transcript)

    # --------------------------------------------------------------
    def last_result_for(self, message_id: str) -> Optional[dict]:
        return self._results.get(message_id)


__all__ = ["InProcBus", "TranscriptEntry", "Handler"]
