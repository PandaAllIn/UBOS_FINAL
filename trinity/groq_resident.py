"""Groq resident hot vessel with model registry and Trinity integration.

This resident mirrors OpenAI resident patterns:
- Model registry with strengths and selection
- Comms Hub integration (pack/unpack)
- Oracle access via OracleBridge
- Tooling via ToolExecutor

The resident supports manual model overrides and simple task classification
to select a default model when not specified.
"""
from __future__ import annotations

import time
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence

from comms_hub_client import CommsHubClient
from config import APIKeys, TrinityPaths, load_configuration
from master_librarian_adapter import MasterLibrarianAdapter
from oracle_bridge import OracleBridge
from tool_executor import ToolExecutor
from trinity_event_stream import TrinityEventStream

try:  # Optional to allow tests without the SDK
    from groq import Groq
except Exception:  # pragma: no cover
    Groq = None


class AITask(Enum):
    SPEED = "speed"
    FAST_INFERENCE = "fast_inference"
    GENERAL_CHAT = "general_chat"


@dataclass
class GroqModel:
    model_id: str
    name: str
    strengths: Sequence[str]
    context_tokens: int
    modalities: Sequence[str] = field(default_factory=lambda: ("text",))


# Curated registry with commonly used Groq models.
GROQ_MODEL_REGISTRY: Dict[str, GroqModel] = {
    "llama-3.3-70b-versatile": GroqModel(
        model_id="llama-3.3-70b-versatile",
        name="LLaMA-3.3 70B Versatile",
        strengths=("speed", "reasoning", "general_chat"),
        context_tokens=16384,
    ),
    "llama-3.1-8b-instant": GroqModel(
        model_id="llama-3.1-8b-instant",
        name="LLaMA-3.1 8B Instant",
        strengths=("fast_inference", "chat"),
        context_tokens=16384,
    ),
    "mixtral-8x7b-32768": GroqModel(
        model_id="mixtral-8x7b-32768",
        name="Mixtral 8x7B",
        strengths=("speed", "long_context"),
        context_tokens=32768,
    ),
}


@dataclass(slots=True)
class GroqResidentConfig:
    api_key: Optional[str] = None
    default_model: str = "llama-3.3-70b-versatile"
    temperature: float = 0.2
    top_p: float = 0.9
    max_output_tokens: int = 8192
    memory_db: Path = Path("/srv/janus/trinity_memory/groq_resident.db")


class GroqResident:
    """Groq hot vessel with model registry and Trinity integrations."""

    def __init__(
        self,
        config: Optional[GroqResidentConfig] = None,
        *,
        groq_client: Optional[Any] = None,
    ) -> None:
        paths, keys = load_configuration()
        self.paths: TrinityPaths = paths
        self.keys: APIKeys = keys
        self.config = config or GroqResidentConfig(api_key=keys.groq)

        api_key = self.config.api_key or self.keys.groq
        if not api_key:
            raise RuntimeError("GROQ_API_KEY is not configured. Export it or update /etc/janus/trinity.env.")

        if groq_client is not None:
            self.client = groq_client
        else:
            if Groq is None:  # pragma: no cover
                raise RuntimeError("groq SDK not installed. pip install groq")
            self.client = Groq(api_key=api_key)

        self.events = TrinityEventStream()
        self.comms = CommsHubClient("groq_resident", event_stream=self.events)
        self.librarian = MasterLibrarianAdapter(self.paths)
        self.oracle_bridge = OracleBridge(self.keys)
        self.tools = ToolExecutor()
        self.model_registry = GROQ_MODEL_REGISTRY

    # ------------------------------------------------------------------ utilities
    def list_models(self) -> List[GroqModel]:
        return list(self.model_registry.values())

    def best_model_for(self, task: AITask) -> str:
        mapping = {
            AITask.SPEED: "llama-3.3-70b-versatile",
            AITask.FAST_INFERENCE: "llama-3.1-8b-instant",
            AITask.GENERAL_CHAT: "llama-3.3-70b-versatile",
        }
        return mapping.get(task, self.config.default_model)

    # ------------------------------------------------------------------ chat API
    def generate_response(
        self,
        conversation_id: str,
        user_message: str,
        *,
        model: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        metadata: Optional[dict[str, Any]] = None,
        system_prompt: Optional[str] = None,
    ) -> str:
        """Generate a conversational response using selected Groq model."""
        selected_model_id = model or self.config.default_model

        text = ""
        last_error = None
        try:
            messages = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            messages.append({"role": "user", "content": user_message})

            response = self.client.chat.completions.create(
                model=selected_model_id,
                messages=messages,
                temperature=temperature if temperature is not None else self.config.temperature,
                max_tokens=max_tokens if max_tokens is not None else self.config.max_output_tokens,
            )
            text = (response.choices[0].message.content or "").strip()
        except Exception as exc:  # capture and try next model
            last_error = exc

        if not text:
            if last_error is not None:
                return f"Groq resident encountered an error generating a response: {last_error}"
            text = "I processed your message but have no immediate response."

        self.events.log_event(
            source="groq_resident",
            event_type="conversation.reply",
            data={"conversation_id": conversation_id, "model": selected_model_id, "preview": text[:100]},
        )
        return text

    # ------------------------------------------------------------------ routing
    def classify(self, text: str) -> AITask:
        t = text.lower()
        if any(w in t for w in ("fast", "quick", "instant")):
            return AITask.FAST_INFERENCE
        if any(w in t for w in ("speed", "performance", "benchmark")):
            return AITask.SPEED
        return AITask.GENERAL_CHAT

    def route_and_respond(self, conversation_id: str, user_message: str) -> dict[str, Any]:
        task = self.classify(user_message)
        model = self.best_model_for(task)
        system_prompt = (
            "You are the Groq resident, the high-speed specialist of the UBOS Trinity, "
            "running inside the Balaur vessel. Respond as quickly and concisely as possible, "
            "prioritizing speed and immediate, useful answers."
        )
        answer = self.generate_response(
            conversation_id, user_message, model=model, system_prompt=system_prompt
        )
        return {"task": task.value, "model": model, "answer": answer}