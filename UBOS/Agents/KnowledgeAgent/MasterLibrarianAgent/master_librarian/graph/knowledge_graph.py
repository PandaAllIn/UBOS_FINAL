"""Knowledge graph utilities for the Master Librarian Agent."""

from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Dict, Iterable, List, Optional

import networkx as nx

from master_librarian.models import Concept, ConceptType, Relationship, RelationshipType

LOGGER = logging.getLogger(__name__)


class UBOSKnowledgeGraph:
    """Wrapper around :class:`networkx.DiGraph` providing UBOS helpers."""

    def __init__(self) -> None:
        self._graph: nx.DiGraph = nx.DiGraph()
        self._centrality_cache: Optional[Dict[str, float]] = None

    # ------------------------------------------------------------------
    def build(self, concepts: Dict[str, Concept], relationships: Iterable[Relationship]) -> "UBOSKnowledgeGraph":
        for concept in concepts.values():
            self.add_concept(concept)
        for relationship in relationships:
            self.add_relationship(relationship)
        return self

    def add_concept(self, concept: Concept) -> None:
        self._graph.add_node(concept.id, concept=concept, **concept.as_dict())
        self._centrality_cache = None

    def add_relationship(self, relationship: Relationship) -> None:
        if not self._graph.has_node(relationship.source_id) or not self._graph.has_node(relationship.target_id):
            LOGGER.debug("Skipping relationship %s -> %s", relationship.source_id, relationship.target_id)
            return
        self._graph.add_edge(
            relationship.source_id,
            relationship.target_id,
            relationship=relationship,
            relationship_type=relationship.relationship_type.value,
            confidence=relationship.confidence,
            description=relationship.description,
            evidence_refs=relationship.evidence_refs,
        )
        self._centrality_cache = None

    # ------------------------------------------------------------------
    def get_concept(self, concept_id: str) -> Optional[Concept]:
        node_data = self._graph.nodes.get(concept_id)
        return node_data.get("concept") if node_data else None

    def neighbors(self, concept_id: str) -> List[str]:
        return list(self._graph.successors(concept_id))

    def shortest_path(self, source_id: str, target_id: str) -> List[str]:
        return nx.shortest_path(self._graph, source=source_id, target=target_id)

    def centrality(self) -> Dict[str, float]:
        if self._centrality_cache is None:
            if not self._graph.number_of_nodes():
                self._centrality_cache = {}
            else:
                centrality = nx.in_degree_centrality(self._graph)
                self._centrality_cache = {node: float(value) for node, value in centrality.items()}
        return self._centrality_cache

    # ------------------------------------------------------------------
    def save(self, path: Path | str) -> None:
        serialised = {
            "nodes": [
                {
                    "id": node,
                    "concept": data.get("concept").as_dict() if data.get("concept") else None,
                    "data": {k: v for k, v in data.items() if k not in {"concept"}},
                }
                for node, data in self._graph.nodes(data=True)
            ],
            "edges": [
                {
                    "source": source,
                    "target": target,
                    "data": {
                        **{k: v for k, v in data.items() if k not in {"relationship"}},
                        "relationship": data.get("relationship").as_dict()
                        if data.get("relationship")
                        else None,
                    },
                }
                for source, target, data in self._graph.edges(data=True)
            ],
        }
        with Path(path).open("w", encoding="utf-8") as fh:
            json.dump(serialised, fh, indent=2)

    @classmethod
    def load(cls, path: Path | str) -> "UBOSKnowledgeGraph":
        graph = cls()
        with Path(path).open("r", encoding="utf-8") as fh:
            payload = json.load(fh)

        for node in payload.get("nodes", []):
            concept_payload = node.get("concept")
            concept_obj: Optional[Concept] = None
            if concept_payload:
                concept_obj = Concept(
                    id=concept_payload["id"],
                    title=concept_payload["title"],
                    description=concept_payload["description"],
                    concept_type=ConceptType.from_raw(concept_payload.get("concept_type")),
                    topics=concept_payload.get("topics", []),
                    source_refs=concept_payload.get("source_refs", []),
                    actions=concept_payload.get("actions", []),
                    related_ids=concept_payload.get("related_ids", []),
                    one_liner=concept_payload.get("one_liner"),
                    metadata=concept_payload.get("metadata", {}),
                    chapter=concept_payload.get("chapter"),
                    book=concept_payload.get("book"),
                )
            graph._graph.add_node(node["id"], concept=concept_obj, **node.get("data", {}))

        for edge in payload.get("edges", []):
            edge_data = edge.get("data", {})
            rel_payload = edge_data.get("relationship")
            if rel_payload:
                edge_data["relationship"] = Relationship(
                    source_id=edge["source"],
                    target_id=edge["target"],
                    relationship_type=RelationshipType.from_raw(rel_payload.get("relationship_type")),
                    confidence=rel_payload.get("confidence", 0.5),
                    description=rel_payload.get("description", ""),
                    evidence_refs=rel_payload.get("evidence_refs", []),
                    metadata=rel_payload.get("metadata", {}),
                )
            graph._graph.add_edge(edge["source"], edge["target"], **edge_data)
        graph._centrality_cache = None
        return graph

    # ------------------------------------------------------------------
    @property
    def graph(self) -> nx.DiGraph:
        return self._graph


__all__ = ["UBOSKnowledgeGraph"]
