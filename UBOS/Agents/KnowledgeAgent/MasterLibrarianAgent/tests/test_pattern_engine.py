"""Tests for the PatternEngine."""

from master_librarian.services import PatternEngine


def test_pattern_engine_find_relevant(knowledge_base):
    concepts, graph = knowledge_base
    engine = PatternEngine(concepts, graph)

    results = engine.find_relevant_concepts("architecture system design")
    assert results, "Expected concepts to be returned"
    assert "idea-01-blueprint-thinking" in results[:5]

    conflicts = engine.conflicting_concepts(results[:3])
    assert isinstance(conflicts, list)
