from __future__ import annotations

import json
import logging
import os
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Optional

from trinity.config import APIKeys
from trinity.data_commons_oracle import DataCommonsOracle
from trinity.wolfram_alpha_oracle import WolframAlphaOracle
from trinity.tool_audit_logger import audit_tool_call
from trinity.oracle_cache import OracleCache
from trinity.dual_speed_brain import DualSpeedCognition

TOOLS_PATH = Path("/srv/janus/02_FORGE/tools")
if TOOLS_PATH.exists():  # pragma: no cover - environment dependent
    sys.path.insert(0, str(TOOLS_PATH))

try:  # pragma: no cover - optional dependency
    from groq_integration import GroqClient  # type: ignore

    GROQ_SUPPORTED = True
except Exception:  # pragma: no cover
    GroqClient = None  # type: ignore
    GROQ_SUPPORTED = False

try:  # pragma: no cover - optional dependency
    from trinity.perplexity_oracle import PerplexityOracle  # type: ignore

    PERPLEXITY_SUPPORTED = True
except Exception:  # pragma: no cover
    PerplexityOracle = None  # type: ignore
    PERPLEXITY_SUPPORTED = False


LOGGER = logging.getLogger("trinity.oracle_bridge")


class OracleError(Exception):
    """Oracle integration failure."""

    def __init__(self, message: str, attempts: list[str]) -> None:
        self.message = message
        self.attempts = attempts
        super().__init__(self.user_message())

    def user_message(self) -> str:
        msg = f"Oracle failure: {self.message}\n"
        msg += "Attempted:\n"
        for attempt in self.attempts:
            msg += f"  - {attempt}\n"
        msg += "\nCheck API keys in /etc/janus/trinity.env"
        msg += "\nRun: python3 trinity/oracle_health_check.py"
        return msg


class OracleBridge:
    """Interface to Groq and allied oracle tools."""

    DEFAULT_CACHE_DIR = Path("/tmp/janus_oracle_cache")
    ERROR_LOG_PATH = Path("/srv/janus/logs/oracle_errors.jsonl")

    def __init__(
        self,
        api_keys: APIKeys,
        *,
        cache: OracleCache | None = None,
        error_log_path: Path | None = None,
        perplexity_client: Optional["PerplexityOracle"] = None,
        data_commons: Optional[DataCommonsOracle] = None,
        wolfram_client: Optional[WolframAlphaOracle] = None,
    ) -> None:
        self.brain = DualSpeedCognition(local_model_path=os.getenv("LLAMA_MODEL_PATH"))

        self.perplexity_client: Optional[PerplexityOracle] = None
        self.perplexity_client = perplexity_client or self._init_perplexity_client(api_keys)

        self.data_commons: Optional[DataCommonsOracle] = None
        self.data_commons = data_commons or self._init_data_commons(api_keys)

        self.wolfram_alpha_client: Optional[WolframAlphaOracle] = None
        self.wolfram_alpha_client = wolfram_client or self._init_wolfram(api_keys)

        self.cache = cache or OracleCache(self.DEFAULT_CACHE_DIR)
        self.error_log_path = Path(error_log_path or self.ERROR_LOG_PATH)
        self.error_log_path.parent.mkdir(parents=True, exist_ok=True)

    # ------------------------------------------------------------------ client initializers
    def _init_perplexity_client(self, api_keys: APIKeys) -> Optional["PerplexityOracle"]:
        if not (PERPLEXITY_SUPPORTED and api_keys.perplexity):
            return None
        try:
            client = PerplexityOracle(api_key=api_keys.perplexity)
            if not client.is_available():
                return None
            return client
        except Exception as exc:  # pragma: no cover
            LOGGER.warning("Perplexity oracle initialization failed: %s", exc)
            return None

    def _init_data_commons(self, api_keys: APIKeys) -> Optional[DataCommonsOracle]:
        try:
            return DataCommonsOracle(api_keys.data_commons)
        except Exception as exc:  # pragma: no cover - defensive
            LOGGER.warning("Data Commons oracle initialization failed: %s", exc)
            return None

    def _init_wolfram(self, api_keys: APIKeys) -> Optional[WolframAlphaOracle]:
        try:
            return WolframAlphaOracle(api_keys.wolfram)
        except Exception as exc:  # pragma: no cover - defensive
            LOGGER.warning("Wolfram Alpha oracle initialization failed: %s", exc)
            return None

    @audit_tool_call("oracle.fast_think")
    def fast_think(self, prompt: str) -> str:
        return self.brain.think(prompt)

    @audit_tool_call("oracle.wolfram")
    def wolfram(self, query: str, fallback: bool = True) -> str:
        cached = self._cache_get("wolfram", query)
        if cached:
            return cached

        attempts: list[str] = []
        if self.wolfram_alpha_client:
            try:
                response = self.wolfram_alpha_client.query(query)
                if not self._is_failure_message(response):
                    self._cache_set("wolfram", query, response)
                    return response
                attempts.append(f"Wolfram Alpha: {response.strip() or 'no response'}")
            except Exception as exc:  # pragma: no cover - network variability
                attempts.append(f"Wolfram Alpha exception: {exc}")
        else:
            attempts.append("Wolfram Alpha: client unavailable")

        if fallback:
            try:
                result = self._groq_wolfram(query)
                formatted = f"[Fallback: Groq compound]\n{result}"
                self._cache_set("wolfram", query, formatted)
                return formatted
            except Exception as exc:
                attempts.append(f"Groq Wolfram: {exc}")

        self._raise_oracle_error("wolfram", query, "All math oracles failed", attempts)
        return ""  # Unreachable, appease type checker

    @audit_tool_call("oracle.research")
    def research(self, query: str, fallback: bool = True, mode: str = "balanced") -> str:
        """
        Research with automatic fallback chain.

        Args:
            query: Research query.
            fallback: Enable automatic fallback to backup oracles.
            mode: "quick" (Groq only) | "balanced" (Perplexity → Groq) | "comprehensive" (all sources).

        Returns:
            Research results or raises OracleError if all fail.
        """
        normalized = (mode or "balanced").strip().lower()
        if normalized not in {"quick", "balanced", "comprehensive"}:
            LOGGER.warning("Unknown research mode '%s'; defaulting to balanced.", mode)
            normalized = "balanced"

        errors: list[str] = []

        if normalized in {"balanced", "comprehensive"}:
            cached = self._cache_get("perplexity", query)
            if cached:
                return cached
            try:
                primary = self._perplexity_query(query, normalized)
                if normalized == "comprehensive":
                    try:
                        augment = self._groq_web_search(query)
                        combined = self._combine_research(primary, augment)
                        self._cache_set("perplexity", query, combined)
                        return combined
                    except Exception as exc:  # pragma: no cover - network variability
                        errors.append(f"Groq augment: {exc}")
                self._cache_set("perplexity", query, primary)
                return primary
            except Exception as exc:
                errors.append(f"Perplexity: {exc}")
                if not fallback:
                    self._raise_oracle_error(
                        "perplexity",
                        query,
                        "Perplexity failed and fallback disabled",
                        errors,
                    )

        cached_groq = self._cache_get("groq_web", query)
        if cached_groq:
            return cached_groq

        try:
            groq_response = self._groq_web_search(query)
            result = groq_response
            if errors:
                result = f"[Fallback: Groq web]\n{groq_response}"
            self._cache_set("groq_web", query, result)
            return result
        except Exception as exc:
            errors.append(f"Groq web: {exc}")
            self._raise_oracle_error("perplexity", query, "All research oracles failed", errors)
        return ""

    @audit_tool_call("oracle.quick_research")
    def quick_research(self, query: str) -> str:
        return self.research(query, fallback=True, mode="quick")

    @audit_tool_call("oracle.deep_research")
    def deep_research(self, query: str) -> str:
        return self.research(query, fallback=True, mode="comprehensive")

    @audit_tool_call("oracle.reason")
    def reason(self, query: str) -> str:
        if not self.perplexity_client:
            return "Perplexity oracle unavailable (missing API key or integration)."
        return self.perplexity_client.reason(query)

    @audit_tool_call("oracle.query_demographics")
    def query_demographics(self, dcid: str) -> str:
        if not self.data_commons:
            return "Data Commons oracle unavailable (missing configuration)."
        return self.data_commons.query_demographics(dcid)

    @audit_tool_call("oracle.query_economics")
    def query_economics(self, dcid: str, fallback: bool = True) -> str:
        cached = self._cache_get("datacommons", dcid)
        if cached:
            return cached

        attempts: list[str] = []
        if self.data_commons:
            try:
                response = self.data_commons.query_economics(dcid)
                if not self._is_failure_message(response):
                    self._cache_set("datacommons", dcid, response)
                    return response
                attempts.append(f"Data Commons: {response.strip() or 'no response'}")
            except Exception as exc:  # pragma: no cover - network variability
                attempts.append(f"Data Commons exception: {exc}")
        else:
            attempts.append("Data Commons: client unavailable")

        if fallback:
            try:
                search = self._groq_web_search(f"{dcid} GDP per capita latest data trend")
                synthesis = self._groq_extract_economics(dcid, search)
                self._cache_set("datacommons", dcid, synthesis)
                return synthesis
            except Exception as exc:
                attempts.append(f"Groq fallback: {exc}")

        self._raise_oracle_error("datacommons", dcid, "All economics oracles failed", attempts)
        return ""

    @audit_tool_call("oracle.resolve_place")
    def resolve_place(self, name: str) -> str:
        if not self.data_commons:
            return "Data Commons oracle unavailable (missing configuration)."
        return self.data_commons.resolve_place(name)

    @audit_tool_call("oracle.groq_web")
    def groq_web_search(self, query: str) -> str:
        return self._groq_web_search(query)

    # ------------------------------------------------------------------ helpers
    def _perplexity_query(self, query: str, mode: str) -> str:
        if not self.perplexity_client:
            raise RuntimeError("Perplexity client unavailable.")
        mode_map = {
            "balanced": "auto",
            "comprehensive": "deep",
            "quick": "quick",
        }
        selected = mode_map.get(mode, "auto")
        if selected == "deep":
            response = self.perplexity_client.deep_research(query)
        elif selected == "quick":
            response = self.perplexity_client.quick_research(query)
        else:
            response = self.perplexity_client.research(query, mode=selected)
        if self._is_failure_message(response):
            raise RuntimeError(response)
        return response

    def _combine_research(self, primary: str, secondary: str) -> str:
        segments = [
            primary.rstrip(),
            "",
            "---",
            "Groq Web Search Summary:",
            secondary.strip(),
        ]
        return "\n".join(segment for segment in segments if segment is not None)

    def _groq_wolfram(self, query: str) -> str:
        if not self.client or not self.client.is_available():
            raise RuntimeError("Groq client unavailable for Wolfram fallback.")
        result = self.client.wolfram(query)
        if self._is_failure_message(result):
            raise RuntimeError(result)
        return result

    def _groq_web_search(self, query: str) -> str:
        if not self.client or not self.client.is_available():
            raise RuntimeError("Groq client unavailable for web search.")
        response = self.client.web_search(query, max_results=5)  # type: ignore[arg-type]
        if isinstance(response, dict) and response.get("error"):
            raise RuntimeError(str(response["error"]))

        summary_lines = [f"Groq Web Search for '{query}':"]
        if isinstance(response, dict):
            results = response.get("results") or response.get("data") or []
            if isinstance(results, list) and results:
                for item in results[:5]:
                    if not isinstance(item, dict):
                        continue
                    title = str(item.get("title") or item.get("name") or "Untitled result")
                    url = str(item.get("url") or item.get("link") or "").strip()
                    snippet = str(item.get("snippet") or item.get("summary") or "")
                    line = f"- {title}"
                    if url:
                        line += f" ({url})"
                    if snippet:
                        line += f": {snippet}"
                    summary_lines.append(line)
            else:
                summary_lines.append(json.dumps(response, ensure_ascii=False))
        else:
            summary_lines.append(str(response))
        return "\n".join(summary_lines)

    def _groq_extract_economics(self, dcid: str, search_results: str) -> str:
        if not self.client or not self.client.is_available():
            raise RuntimeError("Groq client unavailable for economics fallback.")
        prompt = (
            f"You are the UBOS constitutional economics oracle. "
            f"Using the search results below, extract the latest GDP per capita (PPP) or other key economic indicators "
            f"for the Data Commons place '{dcid}'. Respond with concise bullet points including the value, "
            f"the reference year, and cite the source URL.\n\n{search_results}"
        )
        response = self.client.fast_think(prompt)
        if self._is_failure_message(response):
            raise RuntimeError(response)
        return f"Groq economic synthesis for {dcid}:\n{response.strip()}"

    def _cache_get(self, oracle: str, query: str) -> str | None:
        return self.cache.get(oracle, query) if self.cache else None

    def _cache_set(self, oracle: str, query: str, result: str) -> None:
        if self.cache:
            self.cache.set(oracle, query, result)

    @staticmethod
    def _is_failure_message(text: str | None) -> bool:
        if not text:
            return True
        normalized = text.strip().lower()
        failure_tokens = (
            "unavailable",
            "missing api key",
            "error",
            "failed",
            "cannot",
        )
        return any(token in normalized for token in failure_tokens)

    def _log_error(self, oracle: str, query: str, message: str, attempts: list[str]) -> None:
        payload = {
            "timestamp": datetime.now(UTC).isoformat(),
            "oracle": oracle,
            "query": query,
            "message": message,
            "attempts": attempts,
        }
        try:
            with self.error_log_path.open("a", encoding="utf-8") as handle:
                handle.write(json.dumps(payload, ensure_ascii=False) + "\n")
        except OSError:  # pragma: no cover - logging best effort
            LOGGER.exception("Failed to write oracle error log")

    def _raise_oracle_error(self, oracle: str, query: str, message: str, attempts: list[str]) -> None:
        self._log_error(oracle, query, message, attempts)
        raise OracleError(message, attempts)

    @audit_tool_call("oracle.query_oracle")
    def query_oracle(self, target: str, query: str) -> str:
        normalized = (target or "").lower()
        if normalized in {"perplexity", "research"}:
            return self.research(query)
        if normalized in {"quick_research", "quick"}:
            return self.quick_research(query)
        if normalized in {"deep_research", "deep"}:
            return self.deep_research(query)
        if normalized in {"reason", "reasoning"}:
            return self.reason(query)
        if normalized in {"wolfram", "math"}:
            return self.wolfram(query)
        if normalized in {"groq", "fast"}:
            return self.fast_think(query)
        if normalized in {"demographics", "population"}:
            return self.query_demographics(query)
        if normalized in {"economics", "gdp"}:
            return self.query_economics(query)
        if normalized in {"resolve", "place"}:
            return self.resolve_place(query)
        return f"Unknown oracle target '{target}'."
