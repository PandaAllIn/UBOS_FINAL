"""Claude resident (Anthropic) for strategy, coordination, and oversight.

Design goals
- Mirror the ResidentOpenAI interface shape where practical.
- Defensive initialization: do not raise on missing SDK or API key.
- Provide simple chat generation, task classification, and routing helpers.

Notes
- Default model per spec: "claude-sonnet-4.5".
- Methods return friendly error strings when unavailable.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence

from comms_hub_client import CommsHubClient
from config import APIKeys, TrinityPaths, load_configuration
from master_librarian_adapter import MasterLibrarianAdapter
from oracle_bridge import OracleBridge
from trinity_event_stream import TrinityEventStream

try:  # Optional SDK import; keep defensive
    import anthropic  # type: ignore
except Exception:  # pragma: no cover
    anthropic = None  # type: ignore


class AITask(Enum):
    STRATEGIC = "strategic"
    GENERAL_CHAT = "general_chat"
    REASONING = "reasoning"
    CODING = "coding"
    FUNCTION_CALLING = "function_calling"
    STRUCTURED = "structured_output"
    VISION = "vision"


@dataclass
class ClaudeModel:
    model_id: str
    name: str
    strengths: Sequence[str]
    context_tokens: int = 200_000
    modalities: Sequence[str] = field(default_factory=lambda: ("text",))


CLAUDE_MODEL_REGISTRY: Dict[str, ClaudeModel] = {
    "claude-sonnet-4.5": ClaudeModel(
        model_id="claude-sonnet-4.5",
        name="Claude Sonnet 4.5",
        strengths=("strategy", "coordination", "oversight", "reasoning"),
        modalities=("text",),
        context_tokens=200_000,
    ),
    "claude-haiku-4-5-20251001": ClaudeModel(
        model_id="claude-haiku-4-5-20251001",
        name="Claude Haiku 4.5",
        strengths=("strategy", "fast_response"),
        modalities=("text",),
        context_tokens=200_000,
    ),
    "claude-3-haiku-20240307": ClaudeModel(
        model_id="claude-3-haiku-20240307",
        name="Claude 3 Haiku",
        strengths=("strategy", "fast_response"),
        modalities=("text",),
        context_tokens=200_000,
    ),
    "claude-3.5-sonnet": ClaudeModel(
        model_id="claude-3.5-sonnet",
        name="Claude 3.5 Sonnet",
        strengths=("strategy", "planning"),
        modalities=("text",),
        context_tokens=200_000,
    ),
}


@dataclass(slots=True)
class ClaudeResidentConfig:
    api_key: Optional[str] = None
    default_model: str = "claude-haiku-4-5-20251001"
    temperature: float = 0.2
    max_output_tokens: int = 1024
    memory_db: Path = Path("/srv/janus/trinity_memory/claude_resident.db")


class ResidentClaude:
    """Anthropic Claude resident with Trinity integrations (defensive)."""

    def __init__(
        self,
        config: Optional[ClaudeResidentConfig] = None,
        *,
        anthropic_client: Optional[Any] = None,
    ) -> None:
        paths, keys = load_configuration()
        self.paths: TrinityPaths = paths
        self.keys: APIKeys = keys
        self.config = config or ClaudeResidentConfig(api_key=keys.claude)

        self.events = TrinityEventStream()
        self.comms = CommsHubClient("claude_resident", event_stream=self.events)
        self.librarian = MasterLibrarianAdapter(self.paths)
        self.oracle_bridge = OracleBridge(self.keys)
        self.model_registry = CLAUDE_MODEL_REGISTRY

        self.client = None
        api_key = self.config.api_key or self.keys.claude
        if anthropic_client is not None:
            self.client = anthropic_client
        elif anthropic is not None and api_key:
            try:
                self.client = anthropic.Anthropic(api_key=api_key)
            except Exception:
                self.client = None

    def list_models(self) -> List[ClaudeModel]:
        return list(self.model_registry.values())

    def best_model_for(self, task: AITask) -> str:
        return self.config.default_model if self.config.default_model in self.model_registry else "claude-sonnet-4.5"

    def is_available(self) -> bool:
        return self.client is not None

    def generate_response(
        self,
        conversation_id: str,
        user_message: str,
        *,
        model: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        system_prompt: Optional[str] = None,
        metadata: Optional[dict[str, Any]] = None,
    ) -> str:
        if self.client is None:
            return "Claude resident unavailable (missing Anthropic SDK or CLAUDE_API_KEY)."

        selected = model or self.best_model_for(AITask.STRATEGIC)
        alias_map = {
            "claude": "claude-haiku-4-5-20251001",
            "claude-haiku-4-5": "claude-haiku-4-5-20251001",
        }
        selected = alias_map.get(selected, selected)
        try:
            resp = self.client.messages.create(
                model=selected,
                max_tokens=max_tokens or self.config.max_output_tokens,
                temperature=temperature if temperature is not None else self.config.temperature,
                system=[{"type": "text", "text": system_prompt}] if system_prompt else [],
                messages=[{"role": "user", "content": user_message}],
            )
            text = "".join(
                [block.text for block in resp.content if getattr(block, "type", "") == "text"]
            ).strip()
            if not text:
                text = "[Claude returned no content]"

            self.events.log_event(
                source="claude_resident",
                event_type="conversation.reply",
                data={"conversation_id": conversation_id, "model": selected, "preview": text[:100]},
            )
            return text
        except Exception as exc:
            return f"Claude resident error: {exc}"

    def classify(self, text: str) -> AITask:
        t = (text or "").lower()
        if any(w in t for w in ("plan", "strategy", "roadmap", "policy", "principle", "constitution")):
            return AITask.STRATEGIC
        if any(w in t for w in ("why", "explain", "prove", "derive", "deep research", "multi-step")):
            return AITask.REASONING
        if any(w in t for w in ("code", "implement", "refactor", "bug", "patch", "pr ")):
            return AITask.CODING
        if any(w in t for w in ("function", "tool", "schema", "json")):
            return AITask.STRUCTURED
        if any(w in t for w in ("image", "see", "vision", "photo", "diagram")):
            return AITask.VISION
        return AITask.GENERAL_CHAT

    def route_and_respond(self, conversation_id: str, user_message: str) -> dict[str, Any]:
        task = self.classify(user_message)
        model = self.best_model_for(task)
        system_prompt = (
            "You are the Claude resident, the Master Strategist of the UBOS Trinity, "
            "running inside the Balaur vessel. Respond with constitutional awareness, "
            "strategic insight, and a focus on the Republic's roadmap."
        )
        answer = self.generate_response(
            conversation_id, user_message, model=model, system_prompt=system_prompt
        )
        return {"task": task.value, "model": model, "answer": answer}

    def healthcheck(self) -> dict[str, Any]:
        ok = self.is_available()
        return {
            "resident": "claude",
            "available": ok,
            "default_model": self.config.default_model,
        }