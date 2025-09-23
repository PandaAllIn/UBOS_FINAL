"""Flask application exposing the Master Librarian services.

Adds optional bearer token authentication for write endpoints when
`LIBRARIAN_API_TOKEN` (or `ML_API_TOKEN`) is set in the environment.
"""

from __future__ import annotations

import logging
from typing import Dict, Optional

import os
from flask import Flask, jsonify, request

from master_librarian.graph import UBOSKnowledgeGraph
from master_librarian.ingestion import UBOSKnowledgeIngester
from master_librarian.llm import GeminiClient
from master_librarian.models import (
    Concept,
    ConsultationRequest,
)
from master_librarian.services import ConsultationService
from master_librarian.visualization import generate_mermaid

LOGGER = logging.getLogger(__name__)


def create_app(
    *,
    concepts: Optional[Dict[str, Concept]] = None,
    graph: Optional[UBOSKnowledgeGraph] = None,
    consultation_service: Optional[ConsultationService] = None,
    gemini_client: Optional[GeminiClient] = None,
) -> Flask:
    if concepts is None or graph is None:
        ingester = UBOSKnowledgeIngester()
        loaded_concepts, relationships = ingester.load_all()
        kb_graph = UBOSKnowledgeGraph().build(loaded_concepts, relationships)
        concepts = loaded_concepts
        graph = kb_graph

    if consultation_service is None:
        gemini_client = gemini_client or GeminiClient()
        consultation_service = ConsultationService(concepts, graph, gemini_client)

    app = Flask(__name__)
    # Optional bearer auth token
    app.config["AUTH_TOKEN"] = os.getenv("LIBRARIAN_API_TOKEN") or os.getenv("ML_API_TOKEN")

    app.config["knowledge_concepts"] = concepts
    app.config["knowledge_graph"] = graph
    app.config["consultation_service"] = consultation_service

    # ------------------------------------------------------------------
    @app.get("/concepts")
    def list_concepts():
        topic = request.args.get("topic")
        ctype = request.args.get("type")
        search = request.args.get("search") or request.args.get("q")

        results = []
        for concept in concepts.values():
            if topic and topic not in concept.topics:
                continue
            if ctype and concept.concept_type.value != ctype:
                continue
            if search and search.lower() not in (concept.title + concept.description).lower():
                continue
            results.append(concept.as_dict())
        return jsonify(results)

    # ------------------------------------------------------------------
    @app.get("/concepts/<concept_id>")
    def get_concept(concept_id: str):
        concept = concepts.get(concept_id)
        if not concept:
            return jsonify({"error": "Concept not found"}), 404
        return jsonify(concept.as_dict())

    # ------------------------------------------------------------------
    @app.post("/consult")
    def consult():
        # Optional bearer token enforcement
        token = app.config.get("AUTH_TOKEN")
        if token:
            auth_header = request.headers.get("Authorization", "")
            expected = f"Bearer {token}"
            if auth_header != expected:
                return jsonify({"error": "Unauthorized"}), 401
        payload = request.get_json(force=True) or {}
        req = ConsultationRequest(
            task_id=str(payload.get("task_id", "anonymous")),
            summary=str(payload.get("summary", "")),
            context=payload.get("context", []) or [],
            objectives=payload.get("objectives", []) or [],
            constraints=payload.get("constraints", []) or [],
            preferred_topics=payload.get("preferred_topics", []) or [],
            metadata=payload.get("metadata", {}) or {},
            needs_context=bool(payload.get("needs_context", False)),
        )
        result = consultation_service.consult(req)
        return jsonify({
            "task_id": result.task_id,
            "recommendations": [
                {
                    "concept_id": rec.concept_id,
                    "title": rec.title,
                    "description": rec.description,
                    "rationale": rec.rationale,
                    "actions": rec.actions,
                    "confidence": rec.confidence,
                }
                for rec in result.recommendations
            ],
            "key_concepts": result.key_concepts,
            "confidence": result.confidence,
            "ubos_alignment_notes": result.ubos_alignment_notes,
            "warnings": result.warnings,
            "follow_up_actions": result.follow_up_actions,
            "mermaid_diagram": result.mermaid_diagram,
        })

    # ------------------------------------------------------------------
    @app.get("/graph/path")
    def graph_path():
        source = request.args.get("source_id")
        target = request.args.get("target_id")
        if not source or not target:
            return jsonify({"error": "source_id and target_id are required"}), 400
        try:
            path = graph.shortest_path(source, target)
        except Exception as exc:  # pragma: no cover - variations on networkx errors
            return jsonify({"error": str(exc)}), 404
        return jsonify({"path": path})

    @app.get("/graph/neighbors/<concept_id>")
    def graph_neighbors(concept_id: str):
        neighbors = []
        for successor in graph.graph.successors(concept_id):
            edge_data = graph.graph.edges[concept_id, successor]
            neighbors.append({
                "concept_id": successor,
                "relationship_type": edge_data.get("relationship_type"),
                "confidence": edge_data.get("confidence"),
            })
        return jsonify(neighbors)

    @app.post("/graph/diagram")
    def graph_diagram():
        payload = request.get_json(force=True) or {}
        concept_ids = payload.get("concept_ids", []) or []
        mermaid = generate_mermaid(concepts, graph, concept_ids)
        return jsonify({"mermaid": mermaid})

    return app


__all__ = ["create_app"]
