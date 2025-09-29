"""Wrapper utilities for interacting with Google Gemini."""

from __future__ import annotations

import json
import os
from dataclasses import dataclass
from typing import Any, Dict, Optional

from tenacity import retry, stop_after_attempt, wait_exponential

# Use the modern Google GenerativeAI SDK
try:
    import google.generativeai as genai  # type: ignore
    _GENAI_AVAILABLE = True
except Exception:  # pragma: no cover
    genai = None
    _GENAI_AVAILABLE = False


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
        model: str = "models/gemini-2.5-pro",
        temperature: float = 0.2,
    ) -> None:
        self._api_key = api_key or os.getenv("GEMINI_API_KEY")
        self._model = os.getenv("GEMINI_MODEL", model)
        self._temperature = temperature
        self._model_client = None

        # Initialize the modern Google GenerativeAI SDK
        if _GENAI_AVAILABLE and self._api_key:
            try:  # pragma: no cover - SDK initialisation path
                genai.configure(api_key=self._api_key)
                self._model_client = genai.GenerativeModel(
                    model_name=self._model,
                    generation_config=genai.types.GenerationConfig(
                        temperature=self._temperature,
                        max_output_tokens=4096,
                    )
                )
            except Exception:  # pragma: no cover
                self._model_client = None

    # ------------------------------------------------------------------
    def available(self) -> bool:
        return bool(self._model_client)

    # ------------------------------------------------------------------
    @retry(reraise=True, wait=wait_exponential(multiplier=2, max=8), stop=stop_after_attempt(3))
    def _generate(self, prompt: str) -> str:
        if not self.available():
            raise GeminiUnavailableError("Gemini client not configured")

        # Use modern Google GenerativeAI SDK
        if self._model_client is not None:
            response = self._model_client.generate_content(prompt)
            return response.text

        # If we reach here, initialization failed at runtime
        raise GeminiUnavailableError("Gemini SDK initialisation failed")

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
            analysis=payload.get("analysis", ""),
            recommended_concepts=payload.get("recommended_concepts", []),
            strategic_guidance=payload.get("strategic_guidance", ""),
            risks=payload.get("risks", ""),
            next_steps=payload.get("next_steps", [])
        )

    def constitutional_consultation(self, question: str, context: Dict[str, Any]) -> GeminiResponse:
        """Constitutional consultation method for compatibility"""
        prompt = f"""
        Constitutional AI Consultation:
        Question: {question}
        Context: {context}

        Analyze this from UBOS constitutional principles:
        - Blueprint Thinking: Plan before execution
        - Strategic Pause: Analyze complexity before proceeding
        - Systems Over Willpower: Create systematic approaches
        - Constitutional AI: Embed UBOS alignment throughout

        Return JSON with analysis, recommended_concepts, strategic_guidance, risks, next_steps.
        """

        return self.generate_consultation(prompt)



__all__ = ["GeminiClient", "GeminiResponse", "GeminiUnavailableError"]
