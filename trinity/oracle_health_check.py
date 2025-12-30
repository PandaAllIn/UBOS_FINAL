"""CLI utility for monitoring oracle availability and performance."""
from __future__ import annotations

import argparse
import json
import time
from dataclasses import dataclass, asdict
from datetime import UTC, datetime
from pathlib import Path
from typing import Dict

from trinity.config import APIKeys, load_configuration
import sys
from pathlib import Path

# Add the Forge packages to the path
FORGE_PATH = Path("/srv/janus/02_FORGE/packages")
if str(FORGE_PATH) not in sys.path:
    sys.path.append(str(FORGE_PATH))

from agent.llm_client import OracleBridge


@dataclass(slots=True)
class OracleHealth:
    """Oracle health status."""

    name: str
    status: bool  # True = healthy, False = down
    latency_ms: float
    last_check: str
    error: str | None = None


class OracleHealthChecker:
    """Monitors oracle endpoint health."""

    def __init__(
        self,
        *,
        api_keys: APIKeys | None = None,
        bridge: OracleBridge | None = None,
        log_path: Path | str | None = None,
    ) -> None:
        if api_keys is None:
            _, api_keys = load_configuration()
        self.api_keys = api_keys
        self.bridge = bridge or OracleBridge(api_keys)
        self.log_path = Path(log_path or "/srv/janus/logs/oracle_health.jsonl")
        self.log_path.parent.mkdir(parents=True, exist_ok=True)

    # ------------------------------------------------------------------ public API
    def check_all(self) -> dict[str, OracleHealth]:
        """Run health checks on all oracles."""
        results = {
            "perplexity": self._check_perplexity(),
            "wolfram": self._check_wolfram(),
            "datacommons": self._check_datacommons(),
            "groq_web": self._check_groq_web(),
        }
        self._write_log(results)
        return results

    # ------------------------------------------------------------------ internal checks
    def _check_perplexity(self) -> OracleHealth:
        return self._invoke(
            name="perplexity",
            func=lambda: self.bridge.research("UBOS oracle health ping", fallback=False, mode="quick"),
            failure_markers=("unavailable", "error"),
        )

    def _check_wolfram(self) -> OracleHealth:
        return self._invoke(
            name="wolfram",
            func=lambda: self.bridge.wolfram("2+2", fallback=False),
            failure_markers=("unavailable", "error"),
        )

    def _check_datacommons(self) -> OracleHealth:
        return self._invoke(
            name="datacommons",
            func=lambda: self.bridge.query_economics("country/USA", fallback=False),
            failure_markers=("unavailable", "unable", "error"),
        )

    def _check_groq_web(self) -> OracleHealth:
        return self._invoke(
            name="groq_web",
            func=lambda: self.bridge.groq_web_search("UBOS oracle health ping"),
            failure_markers=("error", "unavailable"),
        )

    # ------------------------------------------------------------------ helpers
    def _invoke(self, name: str, func, failure_markers: tuple[str, ...]) -> OracleHealth:
        start = time.perf_counter()
        message: str | None = None
        success = False
        try:
            result = func()
            message = (result or "").strip()
            normalized = message.lower()
            success = bool(message) and not any(marker in normalized for marker in failure_markers)
        except OracleError as exc:
            message = exc.user_message()
        except Exception as exc:  # pragma: no cover - defensive
            message = str(exc)
        latency_ms = (time.perf_counter() - start) * 1000
        return OracleHealth(
            name=name,
            status=success,
            latency_ms=latency_ms,
            last_check=datetime.now(UTC).isoformat(),
            error=None if success else message,
        )

    def _write_log(self, results: Dict[str, OracleHealth]) -> None:
        payload = {
            "timestamp": datetime.now(UTC).isoformat(),
            "results": {name: asdict(health) for name, health in results.items()},
        }
        try:
            with self.log_path.open("a", encoding="utf-8") as handle:
                handle.write(json.dumps(payload, ensure_ascii=False) + "\n")
        except OSError:  # pragma: no cover - disk errors
            pass


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Check oracle health status.")
    parser.add_argument("--json", action="store_true", help="Emit JSON payload.")
    return parser.parse_args()


def _format_terminal(results: Dict[str, OracleHealth]) -> str:
    lines = []
    for name, health in results.items():
        status = "✅" if health.status else "⚠️"
        latency = f"{health.latency_ms:.1f}ms"
        lines.append(f"{status} {name:12s} {latency}")
        if health.error:
            lines.append(f"   ↳ {health.error}")
    return "\n".join(lines)


def main() -> None:
    args = _parse_args()
    checker = OracleHealthChecker()
    results = checker.check_all()
    if args.json:
        print(json.dumps({name: asdict(health) for name, health in results.items()}, indent=2))
    else:
        print(_format_terminal(results))


if __name__ == "__main__":
    main()
