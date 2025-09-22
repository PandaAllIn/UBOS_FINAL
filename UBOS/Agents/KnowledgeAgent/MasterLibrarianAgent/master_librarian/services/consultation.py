"""Consultation orchestration for the Master Librarian Agent."""

from __future__ import annotations

import logging
from typing import Dict, List

from master_librarian.graph import UBOSKnowledgeGraph
from master_librarian.llm import GeminiClient, GeminiResponse, GeminiUnavailableError
from master_librarian.models import (
    Concept,
    ConceptType,
    ConsultationRequest,
    ConsultationResult,
    Recommendation,
)
from master_librarian.services.pattern_engine import PatternEngine

LOGGER = logging.getLogger(__name__)


class ConsultationService:
    """High-level orchestration for Master Librarian consultations."""

    def __init__(
        self,
        concepts: Dict[str, Concept],
        graph: UBOSKnowledgeGraph,
        gemini_client: GeminiClient,
    ) -> None:
        self._concepts = concepts
        self._graph = graph
        self._gemini = gemini_client
        self._patterns = PatternEngine(concepts, graph)

    # ------------------------------------------------------------------
    def refresh(self, concepts: Dict[str, Concept], graph: UBOSKnowledgeGraph) -> None:
        self._concepts = concepts
        self._graph = graph
        self._patterns = PatternEngine(concepts, graph)

    # ------------------------------------------------------------------
    def consult(self, request: ConsultationRequest) -> ConsultationResult:
        relevant_ids = self._patterns.find_relevant_concepts(request.summary, context=request.context)
        supporting_ids = self._patterns.supporting_concepts(relevant_ids)
        concept_ids = list(dict.fromkeys([*relevant_ids, *supporting_ids]))

        recommendations = [self._build_recommendation(concept_id) for concept_id in concept_ids[:3]]
        alignment_notes = self._build_alignment_notes(concept_ids)

        gemini_payload: GeminiResponse | None = None
        prompt = self._compose_prompt(request, concept_ids)
        if self._gemini.available():
            try:
                gemini_payload = self._gemini.generate_consultation(prompt)
            except GeminiUnavailableError:
                LOGGER.warning("Gemini unavailable; returning heuristic guidance only")
            except Exception as exc:  # pragma: no cover - defensive logging
                LOGGER.warning("Gemini call failed: %s", exc)

        if gemini_payload:
            recommendations = self._merge_gemini_recommendations(recommendations, gemini_payload)
            alignment_notes.append(gemini_payload.analysis)

        result = ConsultationResult(
            task_id=request.task_id,
            recommendations=recommendations,
            key_concepts=concept_ids[:6],
            confidence=self._compute_confidence(recommendations),
            ubos_alignment_notes=alignment_notes or ["Referred to UBOS principle corpus for validation."],
            follow_up_actions=["Review recommended concepts", "Align routines with UBOS principles"],
            warnings=[] if gemini_payload else ["Gemini insights unavailable - using heuristic guidance"],
        )
        return result

    # ------------------------------------------------------------------
    def _build_recommendation(self, concept_id: str) -> Recommendation:
        concept = self._concepts.get(concept_id)
        if not concept:
            return Recommendation(
                concept_id=concept_id,
                title="Unknown Concept",
                description="Concept not found in knowledge base.",
                rationale="No supporting data available.",
            )

        rationale = "This concept ranks highly for the current query based on topic overlap and centrality."
        if concept.concept_type == ConceptType.PRINCIPLE:
            rationale = "Core principle underpinning the request."
        elif concept.concept_type == ConceptType.PRACTICE:
            rationale = "Actionable practice to operationalise the principle."

        return Recommendation(
            concept_id=concept.id,
            title=concept.title,
            description=concept.description,
            rationale=rationale,
            actions=concept.actions[:3],
            confidence=0.6,
        )

    def _build_alignment_notes(self, concept_ids: List[str]) -> List[str]:
        notes: List[str] = []
        for cid in concept_ids[:3]:
            concept = self._concepts.get(cid)
            if not concept:
                continue
            notes.append(f"Consulted {concept.concept_type.value.title()} '{concept.title}' for alignment.")
        conflicts = self._patterns.conflicting_concepts(concept_ids)
        if conflicts:
            notes.append(f"Identified potential conflicts with: {', '.join(conflicts)}")
        return notes

    def _compose_prompt(self, request: ConsultationRequest, concept_ids: List[str]) -> str:
        lines = [
            "You are the UBOS Master Librarian. Provide structured JSON with keys: analysis, recommended_concepts, strategic_guidance, risks, next_steps.",
            "Align guidance with UBOS philosophy (Blueprint Thinking, Systems over Willpower, Strategic Pause, Abundance Mindset).",
            "Task summary:",
            request.summary,
            "Objectives:",
            " ; ".join(request.objectives) or "(none provided)",
            "Context:",
            " ; ".join(request.context) or "(none provided)",
            "Candidate concepts:",
        ]
        for cid in concept_ids[:6]:
            concept = self._concepts.get(cid)
            if concept:
                lines.append(f"- {concept.title} ({concept.concept_type.value}) :: {concept.description[:120]}")
        return "\n".join(lines)

    def _merge_gemini_recommendations(
        self,
        current: List[Recommendation],
        payload: GeminiResponse,
    ) -> List[Recommendation]:
        recommendations = current.copy()
        for concept_id in payload.recommended_concepts:
            concept = self._concepts.get(concept_id)
            if not concept:
                continue
            recommendations.append(
                Recommendation(
                    concept_id=concept.id,
                    title=concept.title,
                    description=concept.description,
                    rationale=payload.strategic_guidance or "Gemini identified this concept as strategically valuable.",
                    actions=concept.actions[:2],
                    confidence=0.75,
                )
            )
        return recommendations[:5]

    @staticmethod
    def _compute_confidence(recommendations: List[Recommendation]) -> float:
        if not recommendations:
            return 0.2
        return min(0.95, 0.4 + 0.1 * len(recommendations))


__all__ = ["ConsultationService"]
