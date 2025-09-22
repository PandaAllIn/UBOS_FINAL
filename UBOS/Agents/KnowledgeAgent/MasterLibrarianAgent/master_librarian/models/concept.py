"""Concept data model definitions for the Master Librarian Agent."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional


class ConceptType(str, Enum):
    """Supported UBOS concept categories."""

    PRINCIPLE = "principle"
    PRACTICE = "practice"
    FRAMEWORK = "framework"
    QUOTE = "quote"
    CHECKLIST = "checklist"
    RITUAL = "ritual"
    METAPHOR = "metaphor"
    QUESTION = "question"
    SUMMARY = "summary"
    UNKNOWN = "unknown"

    @classmethod
    def from_raw(
        cls,
        value: Optional[str],
        *,
        fallback: Optional["ConceptType"] = None,
    ) -> "ConceptType":
        """Convert raw kind strings into a :class:`ConceptType`."""

        effective_fallback = fallback or cls.UNKNOWN
        if not value:
            return effective_fallback

        normalised = str(value).strip().lower()
        for member in cls:
            if normalised == member.value:
                return member

        # Common aliases
        alias_map = {
            "principle": cls.PRINCIPLE,
            "idea": cls.PRINCIPLE,
            "practice": cls.PRACTICE,
            "exercise": cls.PRACTICE,
            "quote": cls.QUOTE,
            "framework": cls.FRAMEWORK,
            "checklist": cls.CHECKLIST,
            "ritual": cls.RITUAL,
            "metaphor": cls.METAPHOR,
            "question": cls.QUESTION,
        }
        return alias_map.get(normalised, effective_fallback)


@dataclass
class Concept:
    """Represents a single UBOS concept and its contextual metadata."""

    id: str
    title: str
    description: str
    concept_type: ConceptType
    topics: List[str] = field(default_factory=list)
    source_refs: List[str] = field(default_factory=list)
    actions: List[str] = field(default_factory=list)
    related_ids: List[str] = field(default_factory=list)
    one_liner: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    chapter: Optional[str] = None
    book: Optional[str] = None

    def as_dict(self) -> Dict[str, Any]:
        """Serialise the concept into a JSON-friendly dictionary."""

        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "concept_type": self.concept_type.value,
            "topics": sorted(set(self.topics)),
            "source_refs": self.source_refs,
            "actions": self.actions,
            "related_ids": sorted(set(self.related_ids)),
            "one_liner": self.one_liner,
            "metadata": self.metadata,
            "chapter": self.chapter,
            "book": self.book,
        }

    def merge(self, other: "Concept") -> None:
        """Merge another concept record into this one (used when duplicates occur)."""

        if self.id != other.id:
            raise ValueError("Cannot merge concepts with different IDs")

        if len(other.description) > len(self.description):
            self.description = other.description
        if other.one_liner:
            self.one_liner = other.one_liner
        if other.chapter:
            self.chapter = other.chapter
        if other.book:
            self.book = other.book

        self.topics = sorted({*self.topics, *other.topics})
        self.source_refs = list(dict.fromkeys(self.source_refs + other.source_refs))
        self.actions = list(dict.fromkeys(self.actions + other.actions))
        self.related_ids = sorted({*self.related_ids, *other.related_ids})
        self.metadata.update(other.metadata)

    @classmethod
    def from_yaml(
        cls,
        payload: Dict[str, Any],
        *,
        concept_type: ConceptType,
        source_path: str,
        chapter: Optional[str] = None,
        book: Optional[str] = None,
    ) -> "Concept":
        """Create a :class:`Concept` instance from a parsed YAML payload."""

        raw_id = payload.get("id")
        if not raw_id:
            raise ValueError(f"Concept YAML missing 'id' field: {source_path}")

        raw_title = payload.get("title")
        if not raw_title:
            raw_title = payload.get("text") or payload.get("quote")
        if not raw_title:
            raise ValueError(f"Concept YAML missing 'title' field: {source_path}")

        description = str(payload.get("description", "")).strip()
        if not description:
            description = str(payload.get("text", "")).strip()
        one_liner = payload.get("one_liner")

        topics = _ensure_list(payload.get("topics"))
        source_refs = _ensure_list(payload.get("source_refs"))
        related_ids = _ensure_list(payload.get("related_ids"))

        actions = _ensure_list(payload.get("actions"))
        if not actions:
            actions = _ensure_list(payload.get("steps"))

        metadata_value = payload.get("metadata")
        metadata: Dict[str, Any]
        if isinstance(metadata_value, dict):
            metadata = metadata_value.copy()
        else:
            metadata = {}

        kind_override = ConceptType.from_raw(payload.get("kind"), fallback=concept_type)

        return cls(
            id=str(raw_id).strip(),
            title=str(raw_title).strip(),
            description=description,
            concept_type=kind_override,
            topics=topics,
            source_refs=source_refs or [source_path],
            actions=actions,
            related_ids=related_ids,
            one_liner=str(one_liner).strip() if one_liner else None,
            metadata=metadata,
            chapter=chapter,
            book=book,
        )


def _ensure_list(value: Any) -> List[str]:
    """Normalise YAML values into a list of strings."""

    if value is None:
        return []
    if isinstance(value, (list, tuple, set)):
        return [str(item).strip() for item in value if item is not None and str(item).strip()]
    stripped = str(value).strip()
    return [stripped] if stripped else []


__all__ = ["Concept", "ConceptType"]
