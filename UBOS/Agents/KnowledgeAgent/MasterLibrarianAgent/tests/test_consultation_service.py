"""Tests for the ConsultationService."""

from master_librarian.models import ConsultationRequest
from master_librarian.services import ConsultationService
from master_librarian.llm import GeminiResponse, GeminiUnavailableError


class StubGeminiClient:
    def __init__(self, response = None):
        self._response = response
        self.calls = 0

    def available(self) -> bool:
        return self._response is not None

    def generate_consultation(self, prompt: str) -> GeminiResponse:
        self.calls += 1
        if not self._response:
            raise GeminiUnavailableError("stub unavailable")
        return self._response


def test_consultation_service_with_stubbed_gemini(knowledge_base):
    concepts, graph = knowledge_base
    stub_response = GeminiResponse(
        analysis="Gemini sees strong alignment with Blueprint Thinking.",
        recommended_concepts=["idea-01-blueprint-thinking"],
        strategic_guidance="Focus on foundational architecture first.",
        risks="Overlooking practice execution.",
        next_steps=["Map current routines", "Design supporting structures"],
    )
    service = ConsultationService(concepts, graph, StubGeminiClient(stub_response))

    request = ConsultationRequest(
        task_id="test-001",
        summary="We need to build a system for consistent daily planning.",
        objectives=["Increase predictability", "Reduce willpower reliance"],
        context=["Currently ad-hoc planning", "UBOS methodology"],
    )

    result = service.consult(request)

    assert result.task_id == "test-001"
    assert result.recommendations
    assert any(r.concept_id == "idea-01-blueprint-thinking" for r in result.recommendations)
    assert result.ubos_alignment_notes
    assert result.confidence > 0.4


def test_consultation_service_without_gemini(knowledge_base):
    concepts, graph = knowledge_base
    service = ConsultationService(concepts, graph, StubGeminiClient(None))

    request = ConsultationRequest(
        task_id="test-002",
        summary="Create a system for weekly reflection",
        context=["Need alignment with identity"],
        objectives=["Build consistency"],
    )

    result = service.consult(request)

    assert result.task_id == "test-002"
    assert result.recommendations
    assert "Gemini insights unavailable" in " ".join(result.warnings)
