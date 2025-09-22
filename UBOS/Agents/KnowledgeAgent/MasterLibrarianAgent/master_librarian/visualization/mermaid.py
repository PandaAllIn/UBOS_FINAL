"""Utilities for generating Mermaid diagrams from the UBOS knowledge graph."""

from __future__ import annotations

from typing import Dict, Iterable

from master_librarian.models import Concept
from master_librarian.graph import UBOSKnowledgeGraph


def generate_mermaid(concepts: Dict[str, Concept], graph: UBOSKnowledgeGraph, concept_ids: Iterable[str]) -> str:
    nodes = []
    edges = []
    focus_set = {cid for cid in concept_ids if cid in concepts}

    for cid in focus_set:
        concept = concepts[cid]
        label = concept.title.replace("\"", "\'")
        nodes.append(f'    {cid}["{label}"]')

    nx_graph = graph.graph
    for source, target, data in nx_graph.edges(data=True):
        if source in focus_set and target in focus_set:
            relation = data.get("relationship_type", "related")
            edges.append(f"    {source} -->|{relation}| {target}")

    if not nodes:
        return "graph TD\n    Empty[\"No concepts provided\"]"

    lines = ["graph TD", *nodes, *edges]
    return "\n".join(lines)


__all__ = ["generate_mermaid"]
