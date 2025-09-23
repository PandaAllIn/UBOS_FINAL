"""
UBOS Blueprint: Master Librarian Adapter (MVP)

Philosophy: Systems Over Willpower + Strategic Starting Points
Strategic Purpose: Provide a clean, minimal adapter that registers the
Master Librarian capability and a handler for `librarian.consult` without
coupling Prime to Librarian internals.
System Design: Registry entry + bus handler; the handler is written so it can
be replaced by a REST/MCP client later with no orchestration changes.
Feedback Loops: Handler returns structured recommendations and alignment notes
that the Prime workflow can reflect on.
"""

from __future__ import annotations

from typing import Callable, Dict, List, Optional

from ai_prime_agent.bus import TaskMessage
from ai_prime_agent.bus.inproc_bus import Handler
from ai_prime_agent.registry import AgentCapability, AgentRecord, AgentRegistry, AgentStatus


CAPABILITY_NAME = "librarian.consult"


def default_consult_handler(msg: TaskMessage) -> dict:
    """
    UBOS Principle: Provide the smallest working version.
    Strategic Value: Deterministic, test-friendly shape mirroring consultation output.

    Args:
        msg: Validated TaskMessage with payload keys: summary, objectives?, context?
    Returns:
        dict with recommendations and alignment_notes.
    """

    payload = msg.payload or {}
    summary = str(payload.get("summary", ""))
    objectives: List[str] = list(payload.get("objectives", []) or [])
    context: List[str] = list(payload.get("context", []) or [])

    recs = [
        {
            "title": "Blueprint Thinking",
            "rationale": "Core principle underpinning the request.",
            "confidence": 0.75,
        },
        {
            "title": "Systems over Willpower",
            "rationale": "Automate instead of relying on intention.",
            "confidence": 0.7,
        },
    ]
    notes = [
        "Consulted Principle 'Blueprint Thinking' for alignment.",
        "Consulted Practice 'Systems over Willpower' for operationalization.",
    ]

    return {
        "summary": summary,
        "objectives": objectives,
        "context": context,
        "recommendations": recs,
        "alignment_notes": notes,
        "confidence": 0.8,
    }


def register_with_prime(
    *,
    agent_id: str,
    registry: AgentRegistry,
    register_handler: Callable[[str, str, Handler], None],
    handler: Optional[Handler] = None,
) -> AgentRecord:
    """
    UBOS Principle: Strategic Starting Points
    Register the Master Librarian adapter with the Prime system.

    Args:
        agent_id: Externalized id so agents remain independent
        registry: AgentRegistry instance
        register_handler: bus hook to bind (agent_id, task) to handler
        handler: optional override to integrate real REST/MCP client later
    Returns:
        AgentRecord that was registered
    """

    record = AgentRecord.create(
        agent_id=agent_id,
        agent_type="MasterLibrarian",
        capabilities=[
            AgentCapability(
                name=CAPABILITY_NAME,
                version="1.0",
                description="Alignment consultation",
                input_schema={"type": "object"},
                output_schema={"type": "object"},
            )
        ],
        status=AgentStatus.IDLE,
    )
    registry.register(record)

    register_handler(agent_id=agent_id, task=CAPABILITY_NAME, handler=handler or default_consult_handler)
    return record


__all__ = ["register_with_prime", "CAPABILITY_NAME", "default_consult_handler"]
