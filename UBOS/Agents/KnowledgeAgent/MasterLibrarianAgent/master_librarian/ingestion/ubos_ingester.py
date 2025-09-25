"""Ingestion utilities for building the UBOS knowledge base."""

from __future__ import annotations

import logging
import os
from collections import defaultdict
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Tuple

from master_librarian.models import Concept, ConceptType, Relationship, RelationshipType

from .yaml_parser import parse_concept_yaml

LOGGER = logging.getLogger(__name__)


class UBOSKnowledgeIngester:
    """Load concepts and relationships from the UBOS book collection."""

    def __init__(
        self,
        books_root: Optional[Path | str] = None,
        *,
        overrides_path: Optional[Path | str] = None,
    ) -> None:
        self.books_root = Path(books_root or self._default_books_root()).expanduser().resolve()
        self.overrides_path = Path(overrides_path).expanduser().resolve() if overrides_path else None

        if not self.books_root.exists():
            raise FileNotFoundError(f"Books root does not exist: {self.books_root}")

    def load_all(self) -> Tuple[Dict[str, Concept], List[Relationship]]:
        concepts = self.load_concepts()
        relationships = self.load_relationships(concepts)
        return concepts, relationships

    # ------------------------------------------------------------------
    # Concept loading
    # ------------------------------------------------------------------
    def load_concepts(self) -> Dict[str, Concept]:
        concept_map: Dict[str, Concept] = {}
        for root, concept_type in self._concept_roots():
            for yaml_path in root.glob("*.yaml"):
                chapter = root.parent.name
                book = self._book_from_path(yaml_path)
                try:
                    concept = parse_concept_yaml(
                        yaml_path,
                        concept_type_hint=concept_type,
                        chapter=chapter,
                        book=book,
                    )
                except Exception as exc:  # pragma: no cover - logged for operator review
                    LOGGER.warning("Failed to parse %s: %s", yaml_path, exc)
                    continue

                existing = concept_map.get(concept.id)
                if existing:
                    existing.merge(concept)
                else:
                    concept_map[concept.id] = concept
        return concept_map

    # ------------------------------------------------------------------
    # Relationship loading
    # ------------------------------------------------------------------
    def load_relationships(self, concepts: Dict[str, Concept]) -> List[Relationship]:
        relationships: List[Relationship] = []
        seen: set[Tuple[str, str, RelationshipType]] = set()

        for concept in concepts.values():
            # related_ids heuristic
            for target_id in concept.related_ids:
                if target_id not in concepts:
                    continue
                key = (concept.id, target_id, RelationshipType.SYNERGIZES_WITH)
                if key in seen:
                    continue
                relationships.append(
                    Relationship(
                        source_id=concept.id,
                        target_id=target_id,
                        relationship_type=RelationshipType.SYNERGIZES_WITH,
                        confidence=0.7,
                        description="Declared related_ids linkage",
                    )
                )
                seen.add(key)

            # practice to principle heuristics via actions referencing IDs
            if concept.concept_type == ConceptType.PRACTICE:
                for token in _extract_ids_from_text(concept.actions):
                    if token in concepts:
                        key = (concept.id, token, RelationshipType.ENABLES)
                        if key in seen:
                            continue
                        relationships.append(
                            Relationship(
                                source_id=concept.id,
                                target_id=token,
                                relationship_type=RelationshipType.ENABLES,
                                confidence=0.5,
                                description="Practice references concept identifier in steps/actions",
                            )
                        )
                        seen.add(key)

        # Apply manual overrides if provided
        if self.overrides_path and self.overrides_path.exists():
            try:
                overrides = _load_manual_overrides(self.overrides_path)
            except Exception as exc:  # pragma: no cover
                LOGGER.warning("Failed to load manual overrides %s: %s", self.overrides_path, exc)
            else:
                for override in overrides:
                    if override.source_id not in concepts or override.target_id not in concepts:
                        continue
                    key = (override.source_id, override.target_id, override.relationship_type)
                    if key in seen:
                        continue
                    relationships.append(override)
                    seen.add(key)
        return relationships

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------
    def _concept_roots(self) -> Iterable[Tuple[Path, ConceptType]]:
        patterns = {
            "ideas": ConceptType.PRINCIPLE,
            "practices": ConceptType.PRACTICE,
            "quotes": ConceptType.QUOTE,
        }
        for book_dir in sorted(self.books_root.glob("Book*")):
            for ai_dir in book_dir.glob("ai-structured/*/chapters/*"):
                for name, concept_type in patterns.items():
                    root = ai_dir / name
                    if root.exists() and root.is_dir():
                        yield root, concept_type

    @staticmethod
    def _book_from_path(path: Path) -> Optional[str]:
        for part in path.parts:
            if part.startswith("Book"):
                return part
        return None

    @staticmethod
    def _default_books_root() -> Path:
        env_path = os.getenv("UBOS_BOOKS_PATH")
        if env_path:
            return Path(env_path)

        current = Path(__file__).resolve()
        for parent in current.parents:
            candidate = parent / "SystemFundamentals" / "Books"
            if candidate.exists():
                return candidate
        raise FileNotFoundError("Unable to locate SystemFundamentals/Books in parent directories")


# ----------------------------------------------------------------------
# Manual override loading
# ----------------------------------------------------------------------

def _load_manual_overrides(path: Path) -> List[Relationship]:
    import json

    with path.open("r", encoding="utf-8") as fh:
        data = json.load(fh)

    overrides: List[Relationship] = []
    if not isinstance(data, list):
        return overrides

    for entry in data:
        try:
            overrides.append(
                Relationship(
                    source_id=entry["source_id"],
                    target_id=entry["target_id"],
                    relationship_type=RelationshipType.from_raw(entry.get("relationship_type")),
                    confidence=float(entry.get("confidence", 0.9)),
                    description=str(entry.get("description", "Manual override")),
                    evidence_refs=entry.get("evidence_refs", []) or [],
                    metadata=entry.get("metadata", {}) or {},
                )
            )
        except KeyError:
            continue
    return overrides


def _extract_ids_from_text(chunks: List[str]) -> List[str]:
    candidates: set[str] = set()
    for chunk in chunks:
        for token in chunk.split():
            token = token.strip().lower()
            if token.startswith("idea-") or token.startswith("practice-") or token.startswith("concept-"):
                candidates.add(token)
    return sorted(candidates)


# Alias for backward compatibility
UbosIngester = UBOSKnowledgeIngester

__all__ = ["UBOSKnowledgeIngester", "UbosIngester"]
