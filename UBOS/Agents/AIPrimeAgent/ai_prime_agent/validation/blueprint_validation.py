"""
UBOS Blueprint: Blueprint Validation Service (MVP)

Philosophy: Structure Over Control + Blueprint Thinking
Strategic Purpose: Confirm that proposed outputs meet minimum structural and
alignment requirements before acceptance.
System Design: Deterministic rule checks with clear status and issues; ready to
add Gemini 2.5 Pro backed checks later.
Feedback Loops: Returns structured issues and alignment notes for continuous improvement.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List

from ai_prime_agent.blueprint.schema import StrategicBlueprint


@dataclass
class ValidationReport:
    status: str  # "VALID" | "INVALID" | "ESCALATE"
    issues: List[str] = field(default_factory=list)
    alignment_notes: List[str] = field(default_factory=list)


class BlueprintValidator:
    """Rule-based validator for workflow results against the blueprint."""

    def __init__(self, blueprint: StrategicBlueprint) -> None:
        self._bp = blueprint

    def validate_workflow_result(self, result: Dict[str, Any]) -> ValidationReport:
        issues: List[str] = []
        notes: List[str] = []

        # Structural checks
        if not isinstance(result.get("research"), dict):
            issues.append("Missing or invalid research block")
        consult = result.get("consultation") or {}
        if not consult.get("recommendations"):
            issues.append("No consultation recommendations present")

        # Confidence check
        final_conf = float(result.get("final_confidence", 0.0))
        if final_conf < 0.5:
            issues.append("Final confidence below threshold (0.5)")

        # Blueprint alignment (very light-touch for MVP)
        if self._bp.core_principles:
            first = self._bp.core_principles[0].statement.lower()
            if "blueprint" in first:
                notes.append("Alignment: Blueprint principles present")

        status = "VALID" if not issues else ("ESCALATE" if any("below" in i for i in issues) else "INVALID")
        return ValidationReport(status=status, issues=issues, alignment_notes=notes)


__all__ = ["BlueprintValidator", "ValidationReport"]

