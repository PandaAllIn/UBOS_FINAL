"""Wrapper utilities for interacting with Google Gemini."""

from __future__ import annotations

import json
import os
from dataclasses import dataclass
from typing import Any, Dict, Optional

from tenacity import retry, stop_after_attempt, wait_exponential

try:  # pragma: no cover - optional dependency
    from google import genai
except Exception:  # pragma: no cover
    genai = None


@dataclass
class GeminiResponse:
    """Normalised response structure returned by the Gemini client."""

    analysis: str
    recommended_concepts: list[str]
    strategic_guidance: str
    risks: str
    next_steps: list[str]


class GeminiUnavailableError(RuntimeError):
    """Raised when Gemini cannot be used (missing dependency or API key)."""


class GeminiClient:
    """Thin wrapper around the official Gemini SDK with graceful fallbacks."""

    def __init__(
        self,
        api_key: Optional[str] = None,
        *,
        model: str = "gemini-1.5-pro-latest",
        temperature: float = 0.2,
    ) -> None:
        self._api_key = api_key or os.getenv("GEMINI_API_KEY")
        self._model = model
        self._temperature = temperature
        self._client = None

        if genai and self._api_key:
            try:  # pragma: no cover - SDK initialisation path
                self._client = genai.Client(api_key=self._api_key)
            except Exception:  # pragma: no cover
                self._client = None

    # ------------------------------------------------------------------
    def available(self) -> bool:
        return self._client is not None

    # ------------------------------------------------------------------
    @retry(reraise=True, wait=wait_exponential(multiplier=2, max=8), stop=stop_after_attempt(3))
    def _generate(self, prompt: str) -> str:
        if not self.available():
            raise GeminiUnavailableError("Gemini client not configured")
        response = self._client.models.generate_content(
            model=self._model,
            contents=prompt,
        )
        return response.text  # type: ignore[attr-defined]

    # ------------------------------------------------------------------
    def generate_consultation(self, prompt: str) -> GeminiResponse:
        try:
            raw_text = self._generate(prompt)
            payload: Dict[str, Any] = json.loads(raw_text)
        except GeminiUnavailableError:
            raise
        except Exception:
            # Fallback: provide structured empty response with prompt echo
            payload = {
                "analysis": raw_text if 'raw_text' in locals() else "",
                "recommended_concepts": [],
                "strategic_guidance": "Consult Gemini manually; automated call failed.",
                "risks": "Gemini response could not be parsed.",
                "next_steps": [],
            }

        return GeminiResponse(
            analysis=str(payload.get("analysis", "")),
            recommended_concepts=list(payload.get("recommended_concepts", [])),
            strategic_guidance=str(payload.get("strategic_guidance", "")),
            risks=str(payload.get("risks", "")),
            next_steps=list(payload.get("next_steps", [])),
        )


__all__ = ["GeminiClient", "GeminiResponse", "GeminiUnavailableError"]
