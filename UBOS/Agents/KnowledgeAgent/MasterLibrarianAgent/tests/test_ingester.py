"""Tests for the UBOSKnowledgeIngester."""

from pathlib import Path

from master_librarian.ingestion import UBOSKnowledgeIngester
from master_librarian.models import RelationshipType


def _ubos_books_root() -> Path:
    current = Path(__file__).resolve()
    for parent in current.parents:
        candidate = parent / "SystemFundamentals" / "Books"
        if candidate.exists():
            return candidate
    raise RuntimeError("Unable to locate UBOS books directory")


def test_load_concepts_and_relationships():
    books_root = _ubos_books_root()

    ingester = UBOSKnowledgeIngester(books_root)
    concepts = ingester.load_concepts()

    assert len(concepts) > 100, "Expected to load a substantial number of concepts"
    assert "idea-01-blueprint-thinking" in concepts
    assert "practice-01-architecture-audit" in concepts

    relationships = ingester.load_relationships(concepts)
    assert relationships, "Relationships list should not be empty"

    rel_map = {
        (rel.source_id, rel.target_id, rel.relationship_type)
        for rel in relationships
    }
    assert (
        "idea-01-blueprint-thinking",
        "practice-01-architecture-audit",
        RelationshipType.SYNERGIZES_WITH,
    ) in rel_map
