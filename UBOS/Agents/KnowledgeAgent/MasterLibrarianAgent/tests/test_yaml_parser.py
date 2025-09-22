"""Tests for YAML parsing utilities."""

from pathlib import Path

from master_librarian.ingestion import parse_concept_yaml
from master_librarian.models import ConceptType


def _ubos_root() -> Path:
    current = Path(__file__).resolve()
    for parent in current.parents:
        if (parent / "SystemFundamentals" / "Books").exists():
            return parent
    raise RuntimeError("Unable to locate UBOS root")


def test_parse_concept_yaml_idea():
    base_dir = _ubos_root()
    idea_path = (
        base_dir
        / "SystemFundamentals"
        / "Books"
        / "Book01-BuildTheSystem"
        / "ai-structured"
        / "build-the-system"
        / "chapters"
        / "01-architecture"
        / "ideas"
        / "idea-01-blueprint-thinking.yaml"
    )

    concept = parse_concept_yaml(
        idea_path,
        concept_type_hint=ConceptType.PRINCIPLE,
        chapter="01-architecture",
        book="Book01-BuildTheSystem",
    )

    assert concept.id == "idea-01-blueprint-thinking"
    assert concept.concept_type == ConceptType.PRINCIPLE
    assert "architecture" in concept.topics
    assert concept.related_ids == ["practice-01-architecture-audit"]
    assert concept.book == "Book01-BuildTheSystem"
