"""Pattern recognition helpers for the UBOS Master Librarian."""

from __future__ import annotations

import math
import re
from collections import Counter
from typing import Dict, Iterable, List, Sequence

from master_librarian.graph import UBOSKnowledgeGraph
from master_librarian.models import Concept, ConceptType, RelationshipType

_TOKEN_RE = re.compile(r"[a-z0-9']+")


class PatternEngine:
    """Surface meaningful concept patterns from the knowledge graph."""

    def __init__(self, concepts: Dict[str, Concept], graph: UBOSKnowledgeGraph) -> None:
        self._concepts = concepts
        self._graph = graph
        self._centrality = graph.centrality()

    # ------------------------------------------------------------------
    def find_relevant_concepts(
        self,
        query: str,
        *,
        context: Sequence[str] = (),
        limit: int = 10,
    ) -> List[str]:
        """Return concept IDs ranked by fuzzy relevance to the task query."""

        tokens = _tokenise(" ".join([query, *context]))
        if not tokens:
            return []

        scores: Dict[str, float] = {}
        for concept in self._concepts.values():
            concept_tokens = _tokenise(" ".join([
                concept.title,
                concept.description,
                " ".join(concept.topics),
                concept.one_liner or "",
            ]))
            overlap = len(tokens & concept_tokens)
            if overlap:
                centrality_bonus = self._centrality.get(concept.id, 0.0)
                type_bonus = 0.1 if concept.concept_type in {ConceptType.PRINCIPLE, ConceptType.FRAMEWORK} else 0.0
                scores[concept.id] = overlap + centrality_bonus + type_bonus

        ranked = sorted(scores.items(), key=lambda item: item[1], reverse=True)
        return [concept_id for concept_id, _ in ranked[:limit]]

    # ------------------------------------------------------------------
    def supporting_concepts(self, concept_ids: Iterable[str], limit: int = 5) -> List[str]:
        suggestions: Counter[str] = Counter()
        for concept_id in concept_ids:
            try:
                neighbors = self._graph.neighbors(concept_id)
            except Exception:
                continue
            for neighbor in neighbors:
                relation_type = self._graph.graph.edges[concept_id, neighbor].get("relationship_type")
                if relation_type == RelationshipType.CONFLICTS_WITH.value:
                    continue
                suggestions[neighbor] += 1
        return [cid for cid, _ in suggestions.most_common(limit)]

    # ------------------------------------------------------------------
    def conflicting_concepts(self, concept_ids: Iterable[str]) -> List[str]:
        conflicts: set[str] = set()
        for concept_id in concept_ids:
            for successor in self._graph.graph.successors(concept_id):
                edge = self._graph.graph.edges[concept_id, successor]
                if edge.get("relationship_type") == RelationshipType.CONFLICTS_WITH.value:
                    conflicts.add(successor)
        return sorted(conflicts)


def _tokenise(text: str) -> set[str]:
    return {match.group(0) for match in _TOKEN_RE.finditer(text.lower()) if len(match.group(0)) > 2}


__all__ = ["PatternEngine"]
