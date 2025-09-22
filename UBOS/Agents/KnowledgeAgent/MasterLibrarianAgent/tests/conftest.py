"""Shared fixtures for Master Librarian tests."""

from pathlib import Path

import pytest

from master_librarian.graph import UBOSKnowledgeGraph
from master_librarian.ingestion import UBOSKnowledgeIngester


def _books_root() -> Path:
    current = Path(__file__).resolve()
    for parent in current.parents:
        candidate = parent / "SystemFundamentals" / "Books"
        if candidate.exists():
            return candidate
    raise RuntimeError("Unable to locate UBOS books directory")


@pytest.fixture(scope="session")
def knowledge_base():
    ingester = UBOSKnowledgeIngester(_books_root())
    concepts, relationships = ingester.load_all()
    graph = UBOSKnowledgeGraph().build(concepts, relationships)
    return concepts, graph
