"""
UBOS Blueprint: Research Agent Adapter (MVP)

Philosophy: Blueprint Thinking + Smallest Working Version
Strategic Purpose: Offer a clean, independent interface for dispatching research
tasks (`research.query`) without embedding CLI or HTTP specifics here.
System Design: Registry entry + bus handler; handler can later call external
services (Perplexity, archives) but defaults to a deterministic stub for tests.
Feedback Loops: Returns analysis and citations for downstream synthesis.
"""

from __future__ import annotations

from typing import Callable, Dict, Optional

from ai_prime_agent.bus import TaskMessage
from ai_prime_agent.bus.inproc_bus import Handler
from ai_prime_agent.registry import AgentCapability, AgentRecord, AgentRegistry, AgentStatus


CAPABILITY_NAME = "research.query"


def default_research_handler(msg: TaskMessage) -> dict:
    """
    UBOS Principle: Systems Produce Current Results
    Strategic Value: Produce a stable shape representative of research output.

    Args:
        msg: TaskMessage with payload keys: query (str), depth (str?)
    Returns:
        dict with content, citations, and a simple query analysis
    """

    payload = msg.payload or {}
    query = str(payload.get("query", ""))
    depth = str(payload.get("depth", "medium"))

    content = f"Synthesis for query: {query} (depth={depth}). Key themes: systems, orchestration, alignment."
    citations = [
        "https://example.com/ubos/blueprint",
        "https://example.com/ubos/systems-over-willpower",
    ]
    analysis = {
        "score": 3,
        "recommended_model": "sonar-pro",
    }

    return {
        "query": query,
        "depth": depth,
        "content": content,
        "citations": citations,
        "analysis": analysis,
        "confidence": 0.7,
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
    Register the Research Agent adapter with the Prime system.

    Args:
        agent_id: Externalized id so agents remain independent
        registry: AgentRegistry instance
        register_handler: bus hook to bind (agent_id, task) to handler
        handler: optional override for real CLI/HTTP integration later
    Returns:
        AgentRecord that was registered
    """

    record = AgentRecord.create(
        agent_id=agent_id,
        agent_type="ResearchAgent",
        capabilities=[
            AgentCapability(
                name=CAPABILITY_NAME,
                version="1.0",
                description="External research and synthesis",
                input_schema={"type": "object"},
                output_schema={"type": "object"},
            )
        ],
        status=AgentStatus.IDLE,
    )
    registry.register(record)

    register_handler(agent_id=agent_id, task=CAPABILITY_NAME, handler=handler or default_research_handler)
    return record


__all__ = ["register_with_prime", "CAPABILITY_NAME", "default_research_handler"]
