"""Query interface for the Narrative Warehouse index."""
from __future__ import annotations

import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Sequence

import numpy as np

from .encoder import EncoderConfig, encoder_from_config
from .storage import load_index_bundle, METADATA_FILENAME

LOGGER = logging.getLogger(__name__)


@dataclass(slots=True)
class NarrativeResult:
    """Result payload for narrative queries."""

    source_file: str
    content: str
    score: float


def _normalise_scope(scope: Sequence[str] | None) -> list[str]:
    if not scope:
        return []
    normalised: list[str] = []
    for item in scope:
        if not item:
            continue
        candidate = item.strip().replace("\\", "/")
        if candidate.startswith("./"):
            candidate = candidate[2:]
        normalised.append(candidate)
    return normalised


class NarrativeQueryEngine:
    """Loads the persisted index and answers semantic queries."""

    def __init__(self, index_dir: Path) -> None:
        self._index_dir = index_dir
        self._embeddings, self._entries, metadata = load_index_bundle(index_dir)
        encoder_meta = metadata.get("encoder")
        if not isinstance(encoder_meta, dict):
            raise RuntimeError(f"Invalid encoder metadata in {METADATA_FILENAME}")
        self._encoder = encoder_from_config(EncoderConfig.from_dict(encoder_meta))
        self._metadata = metadata

    @property
    def metadata(self) -> dict[str, object]:
        return dict(self._metadata)

    def query(self, query: str, scope: Sequence[str] | None = None, top_k: int = 5) -> list[NarrativeResult]:
        if not query.strip():
            raise ValueError("Query text must not be empty")

        query_vector = self._encoder.encode([query])[0]
        scores = (self._embeddings * query_vector).sum(axis=1)

        mask = np.ones(len(self._entries), dtype=bool)
        scope_filters = _normalise_scope(scope)
        if scope_filters:
            mask = np.array(
                [
                    any(entry["source_file"].startswith(prefix) for prefix in scope_filters)
                    for entry in self._entries
                ],
                dtype=bool,
            )
            if not mask.any():
                LOGGER.info("Scope %s matched no documents", scope_filters)
                return []

        ranked_indices = np.argsort(scores)[::-1]
        results: list[NarrativeResult] = []
        for idx in ranked_indices:
            if not mask[idx]:
                continue
            entry = self._entries[idx]
            results.append(
                NarrativeResult(
                    source_file=str(entry["source_file"]),
                    content=str(entry["content"]),
                    score=float(scores[idx]),
                )
            )
            if len(results) >= top_k:
                break
        return results
