"""
UBOS Blueprint: Strategic Pause Module (MVP)

Philosophy: Strategic Pause + Systems Produce Current Results
Strategic Purpose: Insert lightweight reflection checkpoints before delegation
and after synthesis to prevent willpower-driven improvisation.
System Design: Deterministic checks with clear decisions: proceed | adjust |
escalate. Designed to be extended with telemetry and LLM-backed assessment.
Feedback Loops: Returns structured reasons and suggested next actions.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Dict, Any

from ai_prime_agent.blueprint.schema import StrategicBlueprint


@dataclass
class PauseDecision:
    status: str  # "proceed" | "adjust" | "escalate"
    reasons: List[str] = field(default_factory=list)
    actions: List[str] = field(default_factory=list)


class StrategicPause:
    """
    UBOS Principle: Pause before response. Check alignment and risk cheaply.
    """

    def __init__(self, blueprint: StrategicBlueprint) -> None:
        self._bp = blueprint

    # --------------------------------------------------------------
    def pre_delegation(self, *, query: str, objectives: List[str] | None = None) -> PauseDecision:
        """Quick checks before sending work to agents."""
        reasons: List[str] = []
        actions: List[str] = []
        status = "proceed"

        if not query or len(query.strip()) < 3:
            status = "adjust"
            reasons.append("Query too short or empty")
            actions.append("Clarify the objective and provide more context")

        if not self._bp.core_principles:
            status = "escalate"
            reasons.append("No core principles defined in blueprint")
            actions.append("Populate blueprint corePrinciples before orchestration")

        return PauseDecision(status=status, reasons=reasons, actions=actions)

    # --------------------------------------------------------------
    def post_synthesis(self, *, result: Dict[str, Any]) -> PauseDecision:
        """Checks after a workflow completes but before committing outputs."""
        status = "proceed"
        reasons: List[str] = []
        actions: List[str] = []

        final_conf = float(result.get("final_confidence", 0.0))
        recs = result.get("consultation", {}).get("recommendations", [])

        if not recs:
            status = "escalate"
            reasons.append("No recommendations produced by consultation")
            actions.append("Retry consultation or broaden candidate concepts")

        if final_conf < 0.5:
            status = "escalate"
            reasons.append("Low overall confidence in result (<0.5)")
            actions.append("Trigger deeper research or human review")

        if 0.5 <= final_conf < 0.65:
            if status != "escalate":
                status = "adjust"
            reasons.append("Moderate confidence; consider minor adjustments")
            actions.append("Tighten objectives and re-run consult")

        return PauseDecision(status=status, reasons=reasons, actions=actions)


__all__ = ["StrategicPause", "PauseDecision"]

