"""Command-line utility to run Master Librarian consultations."""

from __future__ import annotations

import argparse
import os
from pathlib import Path
from textwrap import indent

from dotenv import load_dotenv

import sys
import pathlib

# Use relative imports for standalone script execution
from .graph import UBOSKnowledgeGraph
from .ingestion import UBOSKnowledgeIngester
from .llm import GeminiClient
from .models import ConsultationRequest
from .services import ConsultationService
from .visualization import generate_mermaid
from master_librarian.models import ConsultationRequest
from master_librarian.services import ConsultationService
from master_librarian.visualization import generate_mermaid
from master_librarian.models import ConsultationRequest
from master_librarian.services import ConsultationService
from master_librarian.visualization import generate_mermaid


def _load_dotenv() -> None:
    current = Path(__file__).resolve()
    for parent in current.parents:
        env_path = parent / ".env"
        if env_path.exists():
            load_dotenv(env_path)
            return


def build_service() -> tuple[ConsultationService, dict, UBOSKnowledgeGraph]:
    ingester = UBOSKnowledgeIngester()
    concepts, relationships = ingester.load_all()
    graph = UBOSKnowledgeGraph().build(concepts, relationships)
    gemini = GeminiClient()
    service = ConsultationService(concepts, graph, gemini)
    return service, concepts, graph


def format_recommendation(rec) -> str:
    lines = [f"- {rec.title} (confidence {rec.confidence:.2f})"]
    if rec.rationale:
        lines.append(indent(rec.rationale, "  "))
    if rec.actions:
        lines.append(indent("Actions: " + "; ".join(rec.actions), "  "))
    return "\n".join(lines)


def main() -> None:  # pragma: no cover - CLI entry point
    parser = argparse.ArgumentParser(description="Consult the UBOS Master Librarian")
    parser.add_argument("summary", help="Task summary or question for the librarian")
    parser.add_argument(
        "--objective",
        action="append",
        dest="objectives",
        default=[],
        help="Add an objective (can be supplied multiple times)",
    )
    parser.add_argument(
        "--context",
        action="append",
        dest="context",
        default=[],
        help="Provide contextual notes (can be supplied multiple times)",
    )
    parser.add_argument(
        "--constraint",
        action="append",
        dest="constraints",
        default=[],
        help="Specify constraints or limitations",
    )
    parser.add_argument(
        "--mermaid",
        action="store_true",
        help="Output a Mermaid diagram for the recommended concepts",
    )

    args = parser.parse_args()

    _load_dotenv()

    service, concepts, graph = build_service()
    request = ConsultationRequest(
        task_id="cli-run",
        summary=args.summary,
        context=args.context,
        objectives=args.objectives,
        constraints=args.constraints,
        metadata={"invocation": "cli"},
    )

    result = service.consult(request)

    print("\n=== UBOS Master Librarian Consultation ===\n")
    print("Summary:", request.summary)
    if request.objectives:
        print("Objectives:", "; ".join(request.objectives))
    if request.context:
        print("Context:", "; ".join(request.context))
    print()

    print("Recommendations:")
    for rec in result.recommendations:
        print(format_recommendation(rec))
    print()

    print("UBOS Alignment Notes:")
    for note in result.ubos_alignment_notes:
        print("-", note)
    if result.warnings:
        print("\nWarnings:")
        for warning in result.warnings:
            print("-", warning)

    if args.mermaid:
        mermaid = generate_mermaid(concepts, graph, result.key_concepts[:6])
        print("\nMermaid Diagram:\n")
        print(mermaid)


if __name__ == "__main__":  # pragma: no cover
    main()
