"""Filesystem-backed cache for oracle responses."""
from __future__ import annotations

import hashlib
import json
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any


class OracleCache:
    """Cache oracle responses to reduce API usage and provide resilience."""

    _TTL_HOURS = {"perplexity": 12, "wolfram": 6, "datacommons": 24}

    def __init__(self, cache_dir: Path | str) -> None:
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    # ------------------------------------------------------------------ public API
    def get(self, oracle: str, query: str) -> str | None:
        """Retrieve cached response when within TTL window."""
        cache_file = self._cache_path(oracle, query)
        if not cache_file.exists():
            return None

        try:
            cached = json.loads(cache_file.read_text(encoding="utf-8"))
        except (ValueError, OSError):
            return None

        timestamp = cached.get("timestamp")
        if not isinstance(timestamp, str):
            return None

        try:
            cached_time = datetime.fromisoformat(timestamp)
        except ValueError:
            return None

        ttl_hours = self._ttl_for(oracle)
        now = datetime.now(UTC)
        # Normalize naive timestamps written by older versions.
        if cached_time.tzinfo is None:
            cached_time = cached_time.replace(tzinfo=UTC)
        if now - cached_time > timedelta(hours=ttl_hours):
            return None

        result = cached.get("result")
        return result if isinstance(result, str) else None

    def set(self, oracle: str, query: str, result: str) -> None:
        """Persist oracle response for future reuse."""
        cache_file = self._cache_path(oracle, query)
        payload: dict[str, Any] = {
            "oracle": oracle,
            "query": query,
            "result": result,
            "timestamp": datetime.now(UTC).isoformat(),
            "ttl_hours": self._ttl_for(oracle),
        }
        tmp_path = cache_file.with_suffix(".tmp")
        try:
            tmp_path.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
            tmp_path.replace(cache_file)
        finally:
            if tmp_path.exists():
                try:
                    tmp_path.unlink()
                except OSError:
                    pass

    # ------------------------------------------------------------------ helpers
    def _ttl_for(self, oracle: str) -> int:
        return self._TTL_HOURS.get(oracle, 6)

    def _cache_path(self, oracle: str, query: str) -> Path:
        key = self._hash_key(oracle, query)
        return self.cache_dir / f"{key}.json"

    @staticmethod
    def _hash_key(oracle: str, query: str) -> str:
        digest = hashlib.sha256()
        digest.update(oracle.encode("utf-8"))
        digest.update(b"\x00")
        digest.update(query.encode("utf-8"))
        return digest.hexdigest()
