"""Storage helpers for narrative warehouse indexes."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Iterable

import numpy as np

METADATA_FILENAME = "metadata.json"
ENTRIES_FILENAME = "entries.jsonl"
EMBEDDINGS_FILENAME = "embeddings.npy"


def save_index_bundle(
    output_dir: Path,
    embeddings: np.ndarray,
    entries: Iterable[dict[str, Any]],
    metadata: dict[str, Any],
) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    np.save(output_dir / EMBEDDINGS_FILENAME, embeddings)

    with (output_dir / ENTRIES_FILENAME).open("w", encoding="utf-8") as handle:
        for entry in entries:
            handle.write(json.dumps(entry, ensure_ascii=False))
            handle.write("\n")

    with (output_dir / METADATA_FILENAME).open("w", encoding="utf-8") as handle:
        json.dump(metadata, handle, indent=2)


def load_index_bundle(index_dir: Path) -> tuple[np.ndarray, list[dict[str, Any]], dict[str, Any]]:
    embeddings = np.load(index_dir / EMBEDDINGS_FILENAME)
    entries: list[dict[str, Any]] = []
    with (index_dir / ENTRIES_FILENAME).open("r", encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                entries.append(json.loads(line))

    with (index_dir / METADATA_FILENAME).open("r", encoding="utf-8") as handle:
        metadata = json.load(handle)

    return embeddings, entries, metadata
