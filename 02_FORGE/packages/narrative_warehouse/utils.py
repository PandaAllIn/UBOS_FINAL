"""Utility helpers for the narrative warehouse."""
from __future__ import annotations

from typing import Iterable


def chunk_text(text: str, max_words: int = 220) -> Iterable[str]:
    """Split text into roughly even word-limited chunks."""
    paragraphs = [paragraph.strip() for paragraph in text.split("\n\n") if paragraph.strip()]
    for paragraph in paragraphs:
        words = paragraph.split()
        if len(words) <= max_words:
            yield paragraph
            continue

        start = 0
        while start < len(words):
            end = min(start + max_words, len(words))
            yield " ".join(words[start:end])
            start = end
