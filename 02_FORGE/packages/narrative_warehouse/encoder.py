"""Embedding backends for the Narrative Warehouse."""
from __future__ import annotations

import hashlib
import logging
from dataclasses import dataclass
from typing import Iterable, Sequence

import numpy as np

LOGGER = logging.getLogger(__name__)


def _tokenize(text: str) -> list[str]:
    """Crude but robust tokenizer that is locale-agnostic."""
    tokens: list[str] = []
    current: list[str] = []
    for ch in text.lower():
        if ch.isalnum():
            current.append(ch)
        else:
            if current:
                tokens.append("".join(current))
                current.clear()
    if current:
        tokens.append("".join(current))
    return tokens


def _stable_hash(token: str) -> int:
    digest = hashlib.blake2s(token.encode("utf-8"), digest_size=4).digest()
    return int.from_bytes(digest, "big")


@dataclass(frozen=True)
class EncoderConfig:
    """Persistable configuration for recreating an encoder instance."""

    kind: str
    model_name: str | None = None
    dimension: int | None = None

    def to_dict(self) -> dict[str, str | int | None]:
        return {
            "kind": self.kind,
            "model_name": self.model_name,
            "dimension": self.dimension,
        }

    @classmethod
    def from_dict(cls, data: dict[str, object]) -> "EncoderConfig":
        return cls(
            kind=str(data["kind"]),
            model_name=data.get("model_name") if data.get("model_name") is not None else None,
            dimension=int(data["dimension"]) if data.get("dimension") is not None else None,
        )


class BaseEncoder:
    """Interface for text embedding backends."""

    name: str
    config: EncoderConfig

    def encode(self, texts: Sequence[str]) -> np.ndarray:  # pragma: no cover - interface
        raise NotImplementedError


class HashingEncoder(BaseEncoder):
    """Deterministic hashing encoder used when transformer models are unavailable."""

    def __init__(self, dimension: int = 768) -> None:
        self._dimension = dimension
        self.name = f"hashing-{dimension}"
        self.config = EncoderConfig(kind="hashing", model_name=None, dimension=dimension)

    def _vector_for_tokens(self, tokens: Iterable[str]) -> np.ndarray:
        vec = np.zeros(self._dimension, dtype=np.float32)
        for token in tokens:
            idx = _stable_hash(token) % self._dimension
            vec[idx] += 1.0
        norm = np.linalg.norm(vec)
        if norm:
            vec /= norm
        return vec

    def encode(self, texts: Sequence[str]) -> np.ndarray:
        vectors = np.zeros((len(texts), self._dimension), dtype=np.float32)
        for i, text in enumerate(texts):
            tokens = _tokenize(text)
            vectors[i] = self._vector_for_tokens(tokens)
        return vectors


class SentenceTransformerEncoder(BaseEncoder):
    """Wrapper around sentence-transformers with graceful fallback."""

    def __init__(self, model_name: str = "sentence-transformers/all-MiniLM-L6-v2") -> None:
        from sentence_transformers import SentenceTransformer  # type: ignore[import]

        self._model_name = model_name
        self._backend = SentenceTransformer(model_name)
        self.name = f"sentence-transformer:{model_name}"
        self.config = EncoderConfig(kind="sentence_transformer", model_name=model_name)

    def encode(self, texts: Sequence[str]) -> np.ndarray:
        embeddings = self._backend.encode(
            list(texts),
            show_progress_bar=False,
            convert_to_numpy=True,
            normalize_embeddings=True,
        )
        if isinstance(embeddings, list):
            return np.asarray(embeddings, dtype=np.float32)
        return embeddings.astype(np.float32)


def select_encoder(preferred_model: str | None = "sentence-transformers/all-MiniLM-L6-v2") -> BaseEncoder:
    """Return the best available encoder."""
    if preferred_model:
        try:
            encoder = SentenceTransformerEncoder(preferred_model)
            LOGGER.info("Using sentence-transformer model '%s'", preferred_model)
            return encoder
        except Exception as exc:  # pragma: no cover - environment-dependent
            LOGGER.warning("Falling back to hashing encoder: %s", exc)
    return HashingEncoder()


def encoder_from_config(config: EncoderConfig) -> BaseEncoder:
    """Recreate an encoder instance given its persisted configuration."""
    if config.kind == "sentence_transformer":
        try:
            return SentenceTransformerEncoder(config.model_name or "sentence-transformers/all-MiniLM-L6-v2")
        except Exception as exc:  # pragma: no cover - environment-dependent
            LOGGER.error("Failed to load sentence-transformer '%s': %s. Falling back to hashing encoder.", config.model_name, exc)
            return HashingEncoder()
    if config.kind == "hashing":
        return HashingEncoder(dimension=config.dimension or 768)
    raise ValueError(f"Unsupported encoder kind '{config.kind}'")
