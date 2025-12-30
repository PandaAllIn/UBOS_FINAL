"""Production-grade Groq API client for Balaur dual-speed cognition."""
from __future__ import annotations

import json
import logging
import os
import re
import shutil
import subprocess
import time
from pathlib import Path
from typing import Any, Callable, Iterable

from dotenv import load_dotenv

try:
    from groq import Groq
except ImportError:  # pragma: no cover
    Groq = None  # type: ignore

try:
    from groq.types import ChatCompletion
except ImportError:  # pragma: no cover
    ChatCompletion = dict[str, Any]  # type: ignore


LOGGER = logging.getLogger("groq_client")
LOGGER.setLevel(logging.INFO)


class GroqUnavailableError(RuntimeError):
    """Raised when Groq API cannot be reached."""


class GroqClient:
    """Lightweight Groq wrapper that powers six oracle tools."""

    def __init__(self, api_key: str | None = None, timeout: float = 5.0, max_retries: int = 3) -> None:
        self._load_environment()
        self.api_key = api_key or os.getenv("GROQ_API_KEY")
        self.timeout = float(os.getenv("GROQ_TIMEOUT_SECONDS", timeout))
        self.max_retries = int(os.getenv("GROQ_MAX_RETRIES", max_retries))
        self.fast_model = os.getenv("GROQ_FAST_MODEL", "llama-3.3-70b-versatile")
        self.compound_model = os.getenv("GROQ_COMPOUND_MODEL", "groq/compound")
        self.enable_logs = os.getenv("GROQ_LOG_QUERIES", "true").lower() == "true"
        self.enable_perf = os.getenv("GROQ_LOG_PERFORMANCE", "true").lower() == "true"
        self.client = self._create_client()

    # ------------------------------------------------------------------ public API
    def is_available(self) -> bool:
        """Return True if Groq API is configured and reachable."""
        return self.client is not None

    def fast_think(self, prompt: str, model: str | None = None) -> str:
        """Rapid reconnaissance with Groq's fast model."""
        if not self.is_available():
            return self._error("fast_think", "Groq client unavailable (missing API key).")
        try:
            return self._chat_completion(
                tool="fast_think",
                model=model or self.fast_model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,
            )
        except GroqUnavailableError as exc:
            return self._error("fast_think", str(exc))

    def web_search(self, query: str, max_results: int = 5) -> dict[str, Any]:
        """Perform live web search with citations."""
        if not self.is_available():
            return self._error_dict("web_search", "Groq client unavailable (missing API key).")
        extra: dict[str, Any] = {}
        if max_results:
            extra["max_tokens"] = max(600, max_results * 400)
        try:
            return self._chat_completion_json(
                tool="web_search",
                model=self.compound_model,
                messages=[{"role": "user", "content": query}],
                enable_feature="web_search",
                extra=extra,
            )
        except GroqUnavailableError as exc:
            return self._error_dict("web_search", str(exc))

    def wolfram(self, math_query: str) -> str:
        """Query Wolfram Alpha via Groq compound model."""
        app_id = os.getenv("WOLFRAM_APP_ID")
        if not app_id:
            return self._error("wolfram", "WOLFRAM_APP_ID missing; cannot execute query.")
        if not self.is_available():
            return self._error("wolfram", "Groq client unavailable (missing API key).")
        try:
            return self._chat_completion(
                tool="wolfram",
                model=self.compound_model,
                messages=[{"role": "user", "content": math_query}],
                compound_custom={
                    "tools": {
                        "enabled_tools": ["wolfram_alpha"],
                        "wolfram_settings": {"authorization": app_id},
                    }
                },
            )
        except GroqUnavailableError as exc:
            return self._error("wolfram", str(exc))

    def reason(self, problem: str, effort: str = "medium") -> dict[str, Any]:
        """Deep reasoning with parsed structured output."""
        effort_normalized = effort.lower()
        if effort_normalized not in {"low", "medium", "high"}:
            return self._error_dict("reason", f"Invalid effort level '{effort}'. Use low|medium|high.")
        if not self.is_available():
            return self._error_dict("reason", "Groq client unavailable (missing API key).")
        effort_guidance = {
            "low": "Return exactly two concise reasoning steps.",
            "medium": "Return three to five reasoning steps with clear justification.",
            "high": "Return up to eight detailed reasoning steps with explicit assumptions.",
        }
        system_instruction = (
            "You are the constitutional reasoning co-processor for the UBOS republic. "
            "Analyse the user's problem and respond strictly in JSON with two keys: "
            "'answer' (string summarising the recommendation) and 'reasoning' (array of step-by-step strings). "
            "Do not include any additional keys or commentary outside the JSON object."
        )
        messages = [
            {"role": "system", "content": f"{system_instruction} {effort_guidance[effort_normalized]}"},
            {"role": "user", "content": problem},
        ]
        try:
            response = self._chat_completion_json(
                tool="reason",
                model=self.compound_model,
                messages=messages,
                extra={"temperature": 0.2},
            )
        except GroqUnavailableError as exc:
            return self._error_dict("reason", str(exc))
        if isinstance(response, dict):
            answer = response.get("answer") or response.get("final_answer")
            if isinstance(response.get("reasoning"), str):
                response["reasoning"] = [response["reasoning"]]
            if not answer:
                response["answer"] = self._extract_text(response)
            return response
        return {"answer": self._extract_text(response), "reasoning": response}

    def code_exec(self, code: str, language: str = "python") -> dict[str, Any]:
        """Execute code in Groq's sandboxed compound environment."""
        if not self.is_available():
            return self._error_dict("code_exec", "Groq client unavailable (missing API key).")
        payload = json.dumps({"language": language, "code": code}, ensure_ascii=False)
        system_prompt = (
            "You execute code in a secure sandbox. Run the provided snippet and respond strictly as JSON "
            "with the keys 'stdout', 'stderr', 'exit_code', and 'summary'. "
            "Populate stdout/stderr with strings (use empty string if nothing was emitted). "
            "Set exit_code to an integer and keep the summary concise. Do not emit markdown or additional text."
        )
        try:
            return self._chat_completion_json(
                tool="code_exec",
                model=self.compound_model,
                messages=[
                    {
                        "role": "system",
                        "content": system_prompt,
                    },
                    {"role": "user", "content": payload},
                ],
                extra={"temperature": 0},
                compound_custom={"tools": {"enabled_tools": ["code_interpreter"]}},
            )
        except GroqUnavailableError as exc:
            return self._error_dict("code_exec", str(exc))

    def local_scout(self, pattern: str, path: str = ".") -> dict[str, Any]:
        """Combine ripgrep search with Groq synthesis for fast repository reconnaissance."""
        matches = self._search_locally(pattern, path)
        summary = "No matches found."
        if matches and self.should_summarise():
            match_preview = "\n".join(
                f"{item['file']}:{item['line']} - {item['text']}" for item in matches[:20]
            )
            summary = self.fast_think(
                f"Synthesize the following search results.\nPattern: {pattern}\nMatches:\n{match_preview}"
            )
        return {"pattern": pattern, "matches": matches, "summary": summary}

    # ------------------------------------------------------------------ internals
    def _create_client(self) -> Groq | None:
        if not self.api_key:
            LOGGER.warning("Groq API key not configured; client disabled.")
            return None
        if Groq is None:
            LOGGER.error("groq package unavailable; install groq>=0.4.0 to enable API access.")
            return None
        return Groq(api_key=self.api_key)

    def _load_environment(self) -> None:
        candidates: list[Path] = []
        env_file = os.getenv("GROQ_ENV_FILE")
        if env_file:
            candidates.append(Path(env_file))
        candidates.append(Path("/srv/janus/config/.env"))
        candidates.append(Path.cwd() / ".env")
        candidates.append(Path.home() / ".env")
        for path in candidates:
            try:
                if path.is_file():
                    load_dotenv(path, override=False)
            except OSError:
                continue
        load_dotenv(override=False)

    def should_summarise(self) -> bool:
        return self.is_available()

    def _chat_completion(
        self,
        tool: str,
        *,
        model: str,
        messages: list[dict[str, Any]],
        temperature: float | None = None,
        extra: dict[str, Any] | None = None,
        enable_feature: str | None = None,
        compound_custom: dict[str, Any] | None = None,
    ) -> str:
        merged_extra = dict(extra or {})
        if temperature is not None:
            merged_extra.setdefault("temperature", temperature)
        response = self._invoke(tool, model, messages, merged_extra, enable_feature, compound_custom)
        return self._extract_text(response)

    def _chat_completion_json(
        self,
        tool: str,
        *,
        model: str,
        messages: list[dict[str, Any]],
        temperature: float | None = None,
        extra: dict[str, Any] | None = None,
        enable_feature: str | None = None,
        compound_custom: dict[str, Any] | None = None,
    ) -> dict[str, Any] | list[Any] | str:
        merged_extra = dict(extra or {})
        if temperature is not None:
            merged_extra.setdefault("temperature", temperature)
        response = self._invoke(tool, model, messages, merged_extra, enable_feature, compound_custom)
        payload = self._to_dict(response)
        if isinstance(payload, dict):
            parsed = payload.get("choices", [{}])[0]
            if isinstance(parsed, dict):
                if parsed.get("message") and parsed["message"].get("parsed"):
                    return parsed["message"]["parsed"]
                if parsed.get("message") and parsed["message"].get("content"):
                    content = parsed["message"]["content"]
                    if isinstance(content, list):
                        texts = [item.get("text", "") for item in content if isinstance(item, dict)]
                        try:
                            return json.loads("\n".join(texts))
                        except json.JSONDecodeError:
                            return "\n".join(texts)
                    if isinstance(content, str):
                        try:
                            return json.loads(content)
                        except json.JSONDecodeError:
                            return content
        return payload

    def _invoke(
        self,
        tool: str,
        model: str,
        messages: list[dict[str, Any]],
        extra: dict[str, Any] | None,
        enable_feature: str | None,
        compound_custom: dict[str, Any] | None,
    ) -> ChatCompletion | dict[str, Any]:
        if self.client is None:
            raise GroqUnavailableError("Groq client unavailable (missing API key).")

        payload: dict[str, Any] = {"model": model}
        if enable_feature:
            feature_flag = f"GROQ_ENABLE_{enable_feature.upper()}"
            if os.getenv(feature_flag, "true").lower() != "true":
                return {"error": f"{enable_feature} feature disabled via {feature_flag}."}
        if compound_custom:
            payload["compound_custom"] = compound_custom
        if extra:
            payload.update(extra)

        self._audit(tool, {"model": model, "messages": messages})

        attempt = 0
        delay = 1.0
        last_error: Exception | None = None
        while attempt < self.max_retries:
            attempt += 1
            start = time.perf_counter()
            try:
                response = self.client.chat.completions.create(
                    messages=messages,
                    timeout=self.timeout,
                    **payload,
                )
                duration = time.perf_counter() - start
                self._record_performance(tool, response, duration)
                return response
            except Exception as exc:  # pragma: no cover - network edge cases
                last_error = exc
                if self._is_retryable(exc) and attempt < self.max_retries:
                    LOGGER.warning(
                        "Groq %s call failed attempt %s/%s: %s (retrying in %.1fs)",
                        tool,
                        attempt,
                        self.max_retries,
                        exc,
                        delay,
                    )
                    time.sleep(delay)
                    delay *= 2
                    continue
                LOGGER.error("Groq %s call failed: %s", tool, exc)
                break
        raise GroqUnavailableError(f"Groq {tool} call failed after {self.max_retries} attempts: {last_error}")

    def _record_performance(self, tool: str, response: ChatCompletion | dict[str, Any], duration: float) -> None:
        if not self.enable_perf:
            return
        payload = self._to_dict(response)
        usage = payload.get("usage") if isinstance(payload, dict) else None
        if isinstance(usage, dict):
            tokens = usage.get("total_tokens")
            if isinstance(tokens, (int, float)) and duration > 0:
                tps = tokens / duration
                LOGGER.info(
                    "Groq %s usage: %.2f tokens in %.2fs (%.2f tok/s)",
                    tool,
                    tokens,
                    duration,
                    tps,
                )

    def _audit(self, tool: str, payload: dict[str, Any]) -> None:
        if not self.enable_logs:
            return
        redacted = json.dumps(self._redact(payload), ensure_ascii=False)[:2000]
        LOGGER.info("Groq audit %s: %s", tool, redacted)

    @staticmethod
    def _redact(payload: dict[str, Any]) -> dict[str, Any]:
        clean = json.loads(json.dumps(payload))
        messages = clean.get("messages")
        if isinstance(messages, list):
            for message in messages:
                if isinstance(message, dict) and "content" in message:
                    content = message["content"]
                    if isinstance(content, str) and len(content) > 512:
                        message["content"] = content[:512] + "...[truncated]"
        return clean

    @staticmethod
    def _to_dict(response: ChatCompletion | dict[str, Any]) -> dict[str, Any]:
        if isinstance(response, dict):
            return response
        for method in ("model_dump", "to_dict", "dict"):
            func = getattr(response, method, None)
            if callable(func):
                try:
                    return func()
                except TypeError:
                    continue
        return json.loads(json.dumps(response))

    @staticmethod
    def _extract_text(response: Any) -> str:
        payload = GroqClient._to_dict(response)
        choices = payload.get("choices")
        if isinstance(choices, list) and choices:
            choice = choices[0]
            if isinstance(choice, dict):
                message = choice.get("message", {})
                if isinstance(message, dict):
                    content = message.get("content")
                    if isinstance(content, list):
                        texts = [item.get("text") for item in content if isinstance(item, dict)]
                        return "\n".join(t for t in texts if isinstance(t, str))
                    if isinstance(content, str):
                        return content
                if isinstance(choice.get("content"), list):
                    texts = [item.get("text") for item in choice["content"] if isinstance(item, dict)]
                    return "\n".join(t for t in texts if isinstance(t, str))
                if isinstance(choice.get("content"), str):
                    return choice["content"]
        return json.dumps(payload, ensure_ascii=False)

    @staticmethod
    def _is_retryable(exc: Exception) -> bool:
        text = str(exc).lower()
        if any(keyword in text for keyword in ["timeout", "temporary", "connection", "rate limit", "429"]):
            return True
        return getattr(exc, "status_code", None) in {408, 429, 500, 502, 503, 504}

    def _error(self, tool: str, message: str) -> str:
        LOGGER.error("Groq %s error: %s", tool, message)
        return message

    def _error_dict(self, tool: str, message: str) -> dict[str, Any]:
        LOGGER.error("Groq %s error: %s", tool, message)
        return {"error": message}

    def _search_locally(self, pattern: str, path: str) -> list[dict[str, Any]]:
        root = (Path(path) if Path(path).is_absolute() else Path.cwd() / path).resolve()
        try:
            root.relative_to(Path.cwd().resolve())
        except ValueError:
            # Outside repo; allow but caution.
            pass
        if shutil.which("rg"):
            return self._run_ripgrep(pattern, root)
        return self._scan_pythonically(pattern, root)

    def _run_ripgrep(self, pattern: str, root: Path) -> list[dict[str, Any]]:
        try:
            proc = subprocess.run(
                ["rg", "--json", pattern, "."],
                cwd=root,
                capture_output=True,
                text=True,
                timeout=10,
                check=False,
            )
        except subprocess.TimeoutExpired as exc:
            return [{"error": f"ripgrep timeout: {exc}"}]
        except FileNotFoundError:
            return self._scan_pythonically(pattern, root)

        matches: list[dict[str, Any]] = []
        for line in proc.stdout.splitlines():
            try:
                payload = json.loads(line)
            except json.JSONDecodeError:
                continue
            if payload.get("type") != "match":
                continue
            data = payload.get("data", {})
            rel_path = data.get("path", {}).get("text")
            lines = data.get("lines", {}).get("text", "")
            line_no = data.get("line_number")
            if rel_path and isinstance(line_no, int):
                matches.append(
                    {
                        "file": str((root / rel_path).resolve()),
                        "line": line_no,
                        "text": lines.strip(),
                    }
                )
        return matches

    def _scan_pythonically(self, pattern: str, root: Path) -> list[dict[str, Any]]:
        try:
            regex = re.compile(pattern)
        except re.error as exc:
            return [{"error": f"Invalid pattern: {exc}"}]
        matches: list[dict[str, Any]] = []
        for file_path in root.rglob("*"):
            if file_path.is_dir():
                continue
            try:
                text = file_path.read_text(encoding="utf-8", errors="ignore")
            except OSError:
                continue
            for idx, line in enumerate(text.splitlines(), start=1):
                if regex.search(line):
                    matches.append(
                        {
                            "file": str(file_path.resolve()),
                            "line": idx,
                            "text": line.strip(),
                        }
                    )
        return matches[:50]


__all__ = ["GroqClient", "GroqUnavailableError"]
