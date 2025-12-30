from __future__ import annotations

import io
import logging
import os
import sys
from contextlib import redirect_stdout
from pathlib import Path
from typing import Any, Dict, Optional


LOGGER = logging.getLogger("trinity.perplexity_oracle")

RESEARCH_AGENT_DIR = Path("/srv/janus/02_FORGE/src/UBOS/Agents/ResearchAgent")
if RESEARCH_AGENT_DIR.exists() and str(RESEARCH_AGENT_DIR) not in sys.path:
    sys.path.insert(0, str(RESEARCH_AGENT_DIR))

try:  # pragma: no cover - import guard for optional dependency
    from ubos_research_agent import ResearchConfig, SonarModel, UBOSResearchAgent  # type: ignore

    RESEARCH_AGENT_AVAILABLE = True
except Exception as exc:  # pragma: no cover - handled gracefully later
    LOGGER.warning("Unable to import UBOS Research Agent: %s", exc)
    ResearchConfig = None  # type: ignore[attr-defined]
    SonarModel = None  # type: ignore[attr-defined]
    UBOSResearchAgent = None  # type: ignore[attr-defined]
    RESEARCH_AGENT_AVAILABLE = False


class PerplexityOracle:
    """Adapter that exposes UBOS Research Agent through the Oracle Bridge interface."""

    def __init__(
        self,
        api_key: Optional[str] = None,
        *,
        agent: Optional[UBOSResearchAgent] = None,
        base_url: str = "https://api.perplexity.ai",
    ) -> None:
        if agent is None:
            if not RESEARCH_AGENT_AVAILABLE:
                raise RuntimeError(
                    "Perplexity oracle unavailable; UBOS Research Agent dependency is missing."
                )
            resolved_key = api_key or os.getenv("PERPLEXITY_API_KEY")
            if not resolved_key:
                raise ValueError(
                    "PERPLEXITY_API_KEY is not configured. "
                    "Add it to /etc/janus/trinity.env or pass it explicitly."
                )
            if ResearchConfig is None or UBOSResearchAgent is None:  # pragma: no cover - defensive
                raise RuntimeError("Research agent components unavailable.")
            config = ResearchConfig(api_key=resolved_key, base_url=base_url)
            agent = UBOSResearchAgent(config)
        self.api_key = api_key or os.getenv("PERPLEXITY_API_KEY", "")
        self._agent = agent
        self._mode_to_model = self._build_mode_map()

    # --------------------------------------------------------------------- public
    def is_available(self) -> bool:
        """Return True when the oracle can execute research requests."""
        return self._agent is not None

    def research(self, query: str, mode: str = "auto", depth: str = "medium") -> str:
        """General-purpose research with optional Sonar model override."""
        return self._execute(query=query, model=self._model_for_mode(mode), depth=depth)

    def quick_research(self, query: str) -> str:
        """High-volume fact gathering using the base Sonar model."""
        return self._execute(query=query, model=self._mode_to_model["quick"], depth="quick")

    def deep_research(self, query: str) -> str:
        """Exhaustive research pass using sonar-deep-research."""
        return self._execute(query=query, model=self._mode_to_model["deep"], depth="deep")

    def reason(self, query: str) -> str:
        """Reasoning-focused investigation using sonar-reasoning-pro."""
        return self._execute(query=query, model=self._mode_to_model["reason"], depth="medium")

    # ------------------------------------------------------------------ internals
    def _execute(self, query: str, model: Optional[str], depth: str) -> str:
        result = self._run(query=query, model=model, depth=depth)
        if isinstance(result, dict) and result.get("error"):
            return self._format_error(result)
        if isinstance(result, dict):
            return self._format_success(result)
        return str(result)

    def _run(self, query: str, model: Optional[str], depth: str) -> Dict[str, Any] | str:
        if not self._agent:
            return "Perplexity oracle unavailable (missing API key or integration)."
        buffer = io.StringIO()
        try:
            with redirect_stdout(buffer):
                return self._agent.research(
                    query=query,
                    model=model,
                    depth=depth,
                    format_output="json",
                )
        except Exception as exc:  # pragma: no cover - network/runtime faults
            LOGGER.error("Perplexity oracle request failed: %s", exc)
            return {"error": True, "error_type": type(exc).__name__, "error_message": str(exc)}
        finally:
            captured = buffer.getvalue().strip()
            if captured:
                LOGGER.debug("Research agent output:\n%s", captured)

    def _build_mode_map(self) -> dict[str, Optional[str]]:
        """Create a normalized model lookup for each oracle method."""
        sonar_defaults = {
            "auto": None,
            "quick": "sonar",
            "pro": "sonar-pro",
            "research": "sonar-pro",
            "reasoning": "sonar-reasoning",
            "reason": "sonar-reasoning-pro",
            "reasoning-pro": "sonar-reasoning-pro",
            "deep": "sonar-deep-research",
            "deep-research": "sonar-deep-research",
        }
        if SonarModel:
            sonar_defaults.update(
                {
                    "quick": SonarModel.SONAR.value,
                    "pro": SonarModel.SONAR_PRO.value,
                    "research": SonarModel.SONAR_PRO.value,
                    "reasoning": SonarModel.SONAR_REASONING.value,
                    "reason": SonarModel.SONAR_REASONING_PRO.value,
                    "reasoning-pro": SonarModel.SONAR_REASONING_PRO.value,
                    "deep": SonarModel.SONAR_DEEP_RESEARCH.value,
                    "deep-research": SonarModel.SONAR_DEEP_RESEARCH.value,
                }
            )
        return sonar_defaults

    def _model_for_mode(self, mode: str) -> Optional[str]:
        normalized = (mode or "auto").strip().lower()
        if normalized not in self._mode_to_model:
            LOGGER.warning("Unknown Perplexity mode '%s'; defaulting to auto.", mode)
            return None
        return self._mode_to_model[normalized]

    def _format_success(self, payload: Dict[str, Any]) -> str:
        """Render structured research data as a readable text response."""
        content = payload.get("content") or ""
        model = payload.get("model_used") or "unknown-model"
        research_id = payload.get("research_id")
        citations = payload.get("citations") or []
        usage = payload.get("usage") or {}

        sections: list[str] = [f"Perplexity ({model})"]
        if research_id:
            sections.append(f"Research ID: {research_id}")
        sections.append("")
        sections.append(content.strip() or "[No content returned]")

        if citations:
            sections.append("")
            sections.append("Sources:")
            for idx, citation in enumerate(citations, start=1):
                sections.append(f"{idx}. {citation}")

        if usage:
            sections.append("")
            sections.append("Usage:")
            for key, value in usage.items():
                sections.append(f"- {key}: {value}")

        return "\n".join(sections).strip()

    def _format_error(self, payload: Dict[str, Any]) -> str:
        message = payload.get("error_message") or "Unknown Perplexity error."
        error_type = payload.get("error_type") or "Error"
        suggestions = payload.get("suggestions") or []

        sections = [f"{error_type}: {message}"]
        if suggestions:
            sections.append("")
            sections.append("Suggested actions:")
            for suggestion in suggestions:
                sections.append(f"- {suggestion}")
        return "\n".join(sections).strip()

    # JSON-returning helpers for integrations
    def research_json(self, query: str, mode: str = "auto", depth: str = "medium") -> Dict[str, Any] | str:
        return self._run(query=query, model=self._model_for_mode(mode), depth=depth)

    def quick_research_json(self, query: str) -> Dict[str, Any] | str:
        return self._run(query=query, model=self._mode_to_model["quick"], depth="quick")

    def deep_research_json(self, query: str) -> Dict[str, Any] | str:
        return self._run(query=query, model=self._mode_to_model["deep"], depth="deep")

    def reason_json(self, query: str) -> Dict[str, Any] | str:
        return self._run(query=query, model=self._mode_to_model["reason"], depth="medium")

