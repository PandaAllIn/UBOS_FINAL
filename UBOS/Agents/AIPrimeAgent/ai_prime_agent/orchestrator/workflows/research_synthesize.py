"""
UBOS Blueprint: Research & Synthesize Workflow (Pilot)

Philosophy: Strategic Starting Points + Systems Over Willpower
Strategic Purpose: Execute a smallest-working-cycle that delegates research to
the Research Agent and then consults the Master Librarian to align outputs.
System Design: Capability-driven agent selection via registry, standardized
messages via the bus, and structured outputs for synthesis.
Feedback Loops: Correlation IDs enable tracing; outputs include basic
confidence measures and alignment notes for pause/validation later.
"""

from __future__ import annotations

import uuid
from typing import Dict, Iterable, List, Optional

from ai_prime_agent.bus import TaskMessage
from ai_prime_agent.orchestrator import AIPrimeAgent
from ai_prime_agent.registry import AgentStatus
from ai_prime_agent.pause import StrategicPause, PauseDecision
from ai_prime_agent.validation import BlueprintValidator, ValidationReport


def _select_agent_by_capability(prime: AIPrimeAgent, capability: str) -> Optional[str]:
    reg = prime.components.registry
    candidates = reg.query_by_capability(capability, include_statuses=[AgentStatus.IDLE, AgentStatus.ACTIVE])
    return candidates[0].agent_id if candidates else None


def _pause_to_dict(p: PauseDecision) -> Dict[str, object]:
    return {"status": p.status, "reasons": list(p.reasons), "actions": list(p.actions)}


def _validation_to_dict(v: ValidationReport) -> Dict[str, object]:
    return {"status": v.status, "issues": list(v.issues), "alignment_notes": list(v.alignment_notes)}


def run(prime: AIPrimeAgent, *, query: str, depth: str = "medium") -> Dict[str, object]:
    """
    UBOS Principle: Blueprint Thinking (clear path, clear output)
    Strategic Value: Demonstrates end‑to‑end delegation through the Prime system.

    Args:
        prime: AIPrimeAgent instance with registry and bus
        query: user research query
        depth: research depth (quick|medium|deep)
    Returns:
        dict containing research output, consultation output, and tracing info
    """

    bus = prime.components.bus
    registry = prime.components.registry

    correlation_id = str(uuid.uuid4())

    # Strategic Pause: pre-delegation check
    pauser = StrategicPause(prime.components.blueprint)
    pre_decision = pauser.pre_delegation(query=query, objectives=None)
    if pre_decision.status == "escalate":
        return {
            "error": "pre_pause_escalate",
            "pause": {"pre": _pause_to_dict(pre_decision)},
            "blueprint_mission": prime.components.blueprint.mission_statement,
        }

    # Step 1: Dispatch research
    research_agent_id = _select_agent_by_capability(prime, "research.query")
    if not research_agent_id:
        raise RuntimeError("No research agent available with capability 'research.query'")

    research_msg = TaskMessage.new(
        source_agent_id="A-prime",
        destination_agent_id=research_agent_id,
        task="research.query",
        payload={"query": query, "depth": depth},
        correlation_id=correlation_id,
    )
    ack = bus.dispatch(research_msg)
    if getattr(ack, "status", "NACK") != "ACK":
        return {"error": "research_nack", "reason": getattr(ack, "reason", "unknown"), "correlation_id": correlation_id}
    research_result = bus.last_result_for(research_msg.message_id) or {}

    # Step 2: Prepare and dispatch consultation to Librarian
    summary = str(research_result.get("content", "")).strip() or f"Research summary for: {query}"
    summary = summary[:400]
    objectives = ["Align with UBOS principles", "Identify next high-leverage actions"]
    context = [f"citations={len(research_result.get('citations', []))}"]

    librarian_agent_id = _select_agent_by_capability(prime, "librarian.consult")
    if not librarian_agent_id:
        raise RuntimeError("No librarian agent available with capability 'librarian.consult'")

    consult_msg = TaskMessage.new(
        source_agent_id="A-prime",
        destination_agent_id=librarian_agent_id,
        task="librarian.consult",
        payload={"summary": summary, "objectives": objectives, "context": context},
        correlation_id=correlation_id,
    )
    ack2 = bus.dispatch(consult_msg)
    if getattr(ack2, "status", "NACK") != "ACK":
        return {"error": "consult_nack", "reason": getattr(ack2, "reason", "unknown"), "correlation_id": correlation_id}
    consult_result = bus.last_result_for(consult_msg.message_id) or {}

    # Step 3: Synthesize outputs
    recommendations = consult_result.get("recommendations", [])
    alignment_notes = consult_result.get("alignment_notes", [])
    confidence = min(0.95, 0.5 + 0.1 * len(recommendations)) if recommendations else 0.4

    result: Dict[str, object] = {
        "correlation_id": correlation_id,
        "messages": [research_msg.message_id, consult_msg.message_id],
        "research": research_result,
        "consultation": {
            "recommendations": recommendations,
            "alignment_notes": alignment_notes,
            "confidence": consult_result.get("confidence", 0.0),
        },
        "final_confidence": confidence,
        "blueprint_mission": prime.components.blueprint.mission_statement,
    }

    # Strategic Pause: post-synthesis and validation
    post_decision = pauser.post_synthesis(result=result)
    validator = BlueprintValidator(prime.components.blueprint)
    report = validator.validate_workflow_result(result)
    result["pause"] = {"pre": _pause_to_dict(pre_decision), "post": _pause_to_dict(post_decision)}
    result["validation"] = _validation_to_dict(report)
    return result


__all__ = ["run"]
