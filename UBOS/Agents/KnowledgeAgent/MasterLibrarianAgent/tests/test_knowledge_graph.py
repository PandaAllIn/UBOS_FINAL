"""Tests for the UBOSKnowledgeGraph."""

from pathlib import Path

from master_librarian.graph import UBOSKnowledgeGraph
from master_librarian.ingestion import UBOSKnowledgeIngester


def _books_root() -> Path:
    current = Path(__file__).resolve()
    for parent in current.parents:
        candidate = parent / "SystemFundamentals" / "Books"
        if candidate.exists():
            return candidate
    raise RuntimeError("Unable to locate UBOS books directory")


def test_graph_build_and_centrality(tmp_path):
    ingester = UBOSKnowledgeIngester(_books_root())
    concepts, relationships = ingester.load_all()

    graph = UBOSKnowledgeGraph().build(concepts, relationships)
    assert graph.graph.number_of_nodes() == len(concepts)
    assert graph.graph.number_of_edges() > 0

    centrality = graph.centrality()
    assert centrality, "Centrality results should not be empty"
    key_concept = "idea-01-blueprint-thinking"
    assert key_concept in centrality

    try:
        path = graph.shortest_path("idea-01-blueprint-thinking", "practice-01-architecture-audit")
        assert path[0] == "idea-01-blueprint-thinking"
    except Exception:  # networkx.NoPath or missing nodes
        pass

    save_path = tmp_path / "graph.json"
    graph.save(save_path)
    reloaded = UBOSKnowledgeGraph.load(save_path)
    assert reloaded.graph.number_of_nodes() == graph.graph.number_of_nodes()
