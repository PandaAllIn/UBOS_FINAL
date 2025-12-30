"""Dual-speed cognition engine combining Groq API with local llama.cpp."""
from __future__ import annotations

import datetime as dt
import logging
import os
import subprocess
import textwrap
from pathlib import Path
from typing import Any

from dotenv import load_dotenv

from .groq_client import GroqClient, GroqUnavailableError

LOGGER = logging.getLogger("dual_speed_brain")
LOGGER.setLevel(logging.INFO)


class DualSpeedCognition:
    """Coordinate Groq fast thinking with deep local llama.cpp deliberation."""

    def __init__(self, groq_client: GroqClient, local_model_path: str) -> None:
        load_dotenv()
        self.groq = groq_client
        self.local_model_path = Path(local_model_path)
        self.llama_cli = self._resolve_llama_cli()
        self.api_calls_today = 0
        self.daily_limit = int(os.getenv("GROQ_DAILY_LIMIT", "500"))
        self.hourly_limit = int(os.getenv("GROQ_HOURLY_LIMIT", "100"))
        self._hourly_calls: list[dt.datetime] = []
        self._today = dt.date.today()
        self.receipt_dir = Path("/srv/janus/03_OPERATIONS/receipts")
        self.receipt_dir.mkdir(exist_ok=True)

    # ------------------------------------------------------------------ public API
    def think(self, prompt: str, mode: str = "adaptive") -> str:
        """Primary thinking interface."""
        mode = mode.lower()
        if mode == "scout":
            return self.scout(prompt)
        if mode == "deliberate":
            return self.deliberate(prompt)
        return self.adaptive(prompt)

    def scout(self, prompt: str) -> str:
        """Fast reconnaissance via Groq if allowed, otherwise fallback to local."""
        if self.check_for_receipt(prompt):
            return "This task has already been completed. A receipt exists."
        if self.should_use_groq():
            try:
                result = self.groq.fast_think(prompt)
                self._record_api_call()
                return result
            except GroqUnavailableError as exc:
                LOGGER.warning("Groq unavailable for scout: %s", exc)
        return self._local_response(prompt, temperature=0.8, tokens=256)

    def deliberate(self, prompt: str) -> str:
        """Deep thinking via local llama.cpp."""
        response = self._local_response(prompt, temperature=0.4, tokens=768)
        self.create_receipt(prompt)
        return response

    def adaptive(self, prompt: str) -> str:
        """Scout with Groq then deliberate locally with contextual synthesis."""
        scout_context = ""
        if self.should_use_groq():
            try:
                scout_context = self.scout(prompt)
            except GroqUnavailableError:
                scout_context = ""
        combined = textwrap.dedent(
            f"""
            Prompt:
            {prompt}

            Fast reconnaissance:
            {scout_context or '[Groq scout unavailable – rely on local deliberation only]'}

            Provide a constitutional analysis that integrates actionable next steps.
            """
        ).strip()
        response = self.deliberate(combined)
        if scout_context:
            synthesis = textwrap.dedent(
                f"""
                ### Fast scout
                {scout_context}

                ### Deep deliberation
                {response}
                """
            ).strip()
            return synthesis
        return response

    def should_use_groq(self) -> bool:
        """Determine if Groq can be used under rate limits and availability."""
        self._roll_counters()
        if not self.groq.is_available():
            return False
        if self.api_calls_today >= self.daily_limit:
            LOGGER.warning("Groq daily limit reached (%s/%s).", self.api_calls_today, self.daily_limit)
            return False
        if len(self._hourly_calls) >= self.hourly_limit:
            LOGGER.warning("Groq hourly limit reached (%s/%s).", len(self._hourly_calls), self.hourly_limit)
            return False
        return True

    def create_receipt(self, text: str) -> None:
        """Create a receipt file for a given text."""
        receipt_path = self.receipt_dir / f"{hash(text)}.receipt"
        receipt_path.touch()

    def check_for_receipt(self, text: str) -> bool:
        """Check if a receipt file exists for a given text."""
        receipt_path = self.receipt_dir / f"{hash(text)}.receipt"
        return receipt_path.exists()

    # ------------------------------------------------------------------ internals
    def _resolve_llama_cli(self) -> Path:
        candidates = [
            Path(os.getenv("LLAMA_CLI_PATH", "")),
            Path("/srv/janus/bin/run_llama_cli.sh"),
            Path("/opt/llama.cpp/build/bin/llama-cli"),
            Path("/srv/janus/bin/llama-cli"),
            Path("/opt/llama.cpp/build-vk/bin/llama-cli"),
        ]
        for candidate in candidates:
            if candidate and candidate.exists():
                return candidate
        raise FileNotFoundError("Unable to locate llama-cli binary for local deliberation.")

    def _local_response(self, prompt: str, *, temperature: float, tokens: int) -> str:
        args = [
            str(self.llama_cli),
            "-m",
            str(self.local_model_path),
            "-p",
            prompt,
            "-n",
            str(tokens),
            "--temp",
            str(temperature),
            "--threads",
            os.getenv("LLAMA_THREADS", "8"),
            "--simple-io",
            "--no-display-prompt",
        ]
        LOGGER.info("Invoking local llama-cli with %s tokens", tokens)
        proc = subprocess.run(
            args,
            capture_output=True,
            text=True,
            timeout=180,
            check=False,
            cwd=self.llama_cli.parent,
        )
        if proc.returncode != 0:
            LOGGER.error("Local LLM error (%s): %s", proc.returncode, proc.stderr.strip())
            return f"[Local LLM error: {proc.stderr.strip() or proc.stdout.strip()}]"
        return proc.stdout.strip()

    def _record_api_call(self) -> None:
        self._roll_counters()
        timestamp = dt.datetime.now(dt.timezone.utc)
        self._hourly_calls.append(timestamp)
        self.api_calls_today += 1

    def _roll_counters(self) -> None:
        now = dt.datetime.now(dt.timezone.utc)
        if now.date() != self._today:
            self._today = now.date()
            self.api_calls_today = 0
            self._hourly_calls.clear()
        cutoff = now - dt.timedelta(hours=1)
        self._hourly_calls = [ts for ts in self._hourly_calls if ts >= cutoff]


__all__ = ["DualSpeedCognition"]
