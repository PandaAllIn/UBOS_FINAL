"""Relationship data model for UBOS concept graph."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional


class RelationshipType(str, Enum):
    """Supported semantic edges in the UBOS knowledge graph."""

    BUILDS_ON = "builds_on"
    ENABLES = "enables"
    CONFLICTS_WITH = "conflicts_with"
    REQUIRES = "requires"
    SYNERGIZES_WITH = "synergizes_with"
    SUPPORTS = "supports"

    @classmethod
    def from_raw(
        cls,
        value: Optional[str],
        *,
        fallback: Optional["RelationshipType"] = None,
    ) -> "RelationshipType":
        if not value:
            return fallback or cls.SYNERGIZES_WITH
        normalised = str(value).strip().lower()
        for member in cls:
            if normalised == member.value:
                return member
        alias_map = {
            "support": cls.SUPPORTS,
            "related": cls.SYNERGIZES_WITH,
            "conflict": cls.CONFLICTS_WITH,
        }
        return alias_map.get(normalised, fallback or cls.SYNERGIZES_WITH)


@dataclass
class Relationship:
    """Directed relationship between two concepts."""

    source_id: str
    target_id: str
    relationship_type: RelationshipType
    confidence: float = 0.5
    description: str = ""
    evidence_refs: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def as_dict(self) -> Dict[str, Any]:
        return {
            "source_id": self.source_id,
            "target_id": self.target_id,
            "relationship_type": self.relationship_type.value,
            "confidence": self.confidence,
            "description": self.description,
            "evidence_refs": self.evidence_refs,
            "metadata": self.metadata,
        }


__all__ = ["Relationship", "RelationshipType"]
