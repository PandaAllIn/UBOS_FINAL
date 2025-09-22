"""Consultation-oriented data models."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class ConsultationRequest:
    """Payload provided by the AI Prime Agent when seeking guidance."""

    task_id: str
    summary: str
    context: List[str] = field(default_factory=list)
    objectives: List[str] = field(default_factory=list)
    constraints: List[str] = field(default_factory=list)
    preferred_topics: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    needs_context: bool = False


@dataclass
class Recommendation:
    """A single actionable recommendation returned to the orchestrator."""

    concept_id: str
    title: str
    description: str
    rationale: str
    actions: List[str] = field(default_factory=list)
    confidence: float = 0.5


@dataclass
class ConsultationResult:
    """Structured response returned by the Master Librarian Agent."""

    task_id: str
    recommendations: List[Recommendation]
    key_concepts: List[str]
    confidence: float
    ubos_alignment_notes: List[str]
    mermaid_diagram: Optional[str] = None
    follow_up_actions: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
