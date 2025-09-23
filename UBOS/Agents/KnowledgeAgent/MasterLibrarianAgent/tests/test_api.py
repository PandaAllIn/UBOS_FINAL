"""API endpoint tests for the Master Librarian."""

import json

from master_librarian import create_app
from master_librarian.llm import GeminiResponse
from master_librarian.models import ConsultationRequest
from master_librarian.services import ConsultationService


class StubGeminiClient:
    def __init__(self, response = None):
        self._response = response

    def available(self) -> bool:
        return self._response is not None

    def generate_consultation(self, prompt: str) -> GeminiResponse:
        if not self._response:
            raise RuntimeError("Gemini not available in stub")
        return self._response


def build_app(concepts, graph):
    consultation_service = ConsultationService(
        concepts,
        graph,
        StubGeminiClient(
            GeminiResponse(
                analysis="Stub analysis",
                recommended_concepts=[],
                strategic_guidance="",
                risks="",
                next_steps=[],
            )
        ),
    )
    return create_app(
        concepts=concepts,
        graph=graph,
        consultation_service=consultation_service,
    )


def test_get_concept_endpoint(knowledge_base):
    concepts, graph = knowledge_base
    app = build_app(concepts, graph)
    client = app.test_client()

    response = client.get("/concepts/idea-01-blueprint-thinking")
    assert response.status_code == 200
    payload = response.get_json()
    assert payload["id"] == "idea-01-blueprint-thinking"


def test_list_concepts_filtering(knowledge_base):
    concepts, graph = knowledge_base
    app = build_app(concepts, graph)
    client = app.test_client()

    response = client.get("/concepts?topic=architecture")
    assert response.status_code == 200
    payload = response.get_json()
    assert any(item["id"] == "idea-01-blueprint-thinking" for item in payload)


def test_consult_endpoint(knowledge_base):
    concepts, graph = knowledge_base
    app = build_app(concepts, graph)
    client = app.test_client()

    payload = {
        "task_id": "api-001",
        "summary": "Need a system for morning routines",
        "objectives": ["Consistency"],
    }
    response = client.post("/consult", data=json.dumps(payload), content_type="application/json")
    assert response.status_code == 200
    data = response.get_json()
    assert data["task_id"] == "api-001"
    assert data["recommendations"]


def test_graph_diagram_endpoint(knowledge_base):
    concepts, graph = knowledge_base
    app = build_app(concepts, graph)
    client = app.test_client()

    payload = {"concept_ids": ["idea-01-blueprint-thinking", "practice-01-architecture-audit"]}
    response = client.post("/graph/diagram", data=json.dumps(payload), content_type="application/json")
    assert response.status_code == 200
    data = response.get_json()
    assert data["mermaid"].startswith("graph TD")
