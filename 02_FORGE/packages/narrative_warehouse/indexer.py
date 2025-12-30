"""Index construction for the Narrative Warehouse."""
from __future__ import annotations

import json
import logging
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Sequence

import numpy as np

from .encoder import EncoderConfig, BaseEncoder, select_encoder
from .storage import save_index_bundle
from .utils import chunk_text

LOGGER = logging.getLogger(__name__)

INDEX_VERSION = 1

DEFAULT_SCOPE = [
    "00_CONSTITUTION",
    "01_STRATEGY",
    "02_FORGE/docs",
    "docs",
]


@dataclass(slots=True)
class IndexEntry:
    """Represents a chunk of narrative knowledge."""

    entry_id: int
    source_file: str
    content: str

    def to_dict(self) -> dict[str, object]:
        return {
            "entry_id": self.entry_id,
            "source_file": self.source_file,
            "content": self.content,
        }


def _iter_documents(paths: Sequence[Path], extensions: Sequence[str]) -> Iterable[Path]:
    for root in paths:
        if not root.exists():
            LOGGER.debug("Skipping missing path %s", root)
            continue
        for candidate in sorted(root.rglob("*")):
            if candidate.is_file() and candidate.suffix.lower() in extensions:
                yield candidate


def _gather_entries(files: Iterable[Path], base_dir: Path, max_words: int) -> list[IndexEntry]:
    entries: list[IndexEntry] = []
    entry_id = 0
    for file_path in files:
        try:
            raw = file_path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            raw = file_path.read_text(encoding="utf-8", errors="ignore")
        rel_path = str(file_path.relative_to(base_dir))
        for chunk in chunk_text(raw, max_words=max_words):
            if not chunk.strip():
                continue
            entries.append(IndexEntry(entry_id=entry_id, source_file=rel_path, content=chunk.strip()))
            entry_id += 1
    return entries


def build_index(
    workspace_root: Path,
    output_dir: Path,
    include_paths: Sequence[str | Path] | None = None,
    preferred_model: str | None = "sentence-transformers/all-MiniLM-L6-v2",
    extensions: Sequence[str] = (".md", ".txt"),
    max_words: int = 220,
) -> dict[str, object]:
    """Build the narrative index."""
    scope = include_paths or DEFAULT_SCOPE
    resolved_scope = [workspace_root / Path(path) for path in scope]
    resolved_scope = [path for path in resolved_scope if path.exists()]
    if not resolved_scope:
        raise ValueError("No valid paths found for narrative index scope")

    encoder: BaseEncoder = select_encoder(preferred_model)

    files = list(_iter_documents(resolved_scope, extensions))
    entries = _gather_entries(files, workspace_root, max_words=max_words)
    if not entries:
        raise ValueError("No narrative content discovered for indexing")

    contents = [entry.content for entry in entries]
    embeddings = encoder.encode(contents)

    metadata = {
        "version": INDEX_VERSION,
        "created_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "entry_count": len(entries),
        "encoder": encoder.config.to_dict(),
        "scope": [str(path.relative_to(workspace_root)) for path in resolved_scope],
        "extensions": list(extensions),
        "max_words": max_words,
    }

    save_index_bundle(
        output_dir=output_dir,
        embeddings=embeddings,
        entries=[entry.to_dict() for entry in entries],
        metadata=metadata,
    )

    return metadata
