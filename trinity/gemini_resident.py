"""Gemini resident hot vessel with model registry and Trinity integration.

This resident mirrors OpenAI and Groq resident patterns:
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
from typing import Any, Dict, List, Optional, Sequence, Union

from comms_hub_client import CommsHubClient
from config import APIKeys, TrinityPaths, load_configuration
from master_librarian_adapter import MasterLibrarianAdapter
from oracle_bridge import OracleBridge
from tool_executor import ToolExecutor
from trinity_event_stream import TrinityEventStream

try:  # Optional to allow tests without the SDK
    import google.generativeai as genai
except Exception:  # pragma: no cover
    genai = None


class AITask(Enum):
    SYSTEMS_ENGINEERING = "systems_engineering"
    INFRASTRUCTURE = "infrastructure"
    INTEGRATION = "integration"
    GENERAL_CHAT = "general_chat"
    REASONING = "reasoning"
    CODING = "coding"
    VISION = "vision"


@dataclass
class GeminiModel:
    model_id: str
    name: str
    strengths: Sequence[str]
    context_tokens: int = 1_000_000
    modalities: Sequence[str] = field(default_factory=lambda: ("text",))


# Curated registry with commonly used Gemini models.
GEMINI_MODEL_REGISTRY: Dict[str, GeminiModel] = {
    "gemini-2.5-pro": GeminiModel(
        model_id="gemini-2.5-pro",
        name="Gemini 2.5 Pro",
        strengths=("systems_engineering", "infrastructure", "integration", "reasoning"),
        modalities=("text", "vision"),
        context_tokens=8_000_000,
    ),
    "gemini-2.0-flash-exp": GeminiModel(
        model_id="gemini-2.0-flash-exp",
        name="Gemini 2.0 Flash Experimental",
        strengths=("fast", "chat", "coding"),
        modalities=("text",),
        context_tokens=2_000_000,
    ),
    "gemini-1.5-pro": GeminiModel(
        model_id="gemini-1.5-pro-latest",
        name="Gemini 1.5 Pro",
        strengths=("vision", "general_chat", "long_context"),
        modalities=("text", "vision"),
        context_tokens=1_000_000,
    ),
}


@dataclass(slots=True)
class GeminiResidentConfig:
    api_key: Optional[str] = None
    default_model: str = "gemini-2.5-pro"
    temperature: float = 0.2
    top_p: float = 0.9
    max_output_tokens: int = 8192
    memory_db: Path = Path("/srv/janus/trinity_memory/gemini_resident.db")


class GeminiResident:
    """Gemini hot vessel with model registry and Trinity integrations."""

    def __init__(
        self,
        config: Optional[GeminiResidentConfig] = None,
        *,
        gemini_client: Optional[Any] = None,
    ) -> None:
        paths, keys = load_configuration()
        self.paths: TrinityPaths = paths
        self.keys: APIKeys = keys
        self.config = config or GeminiResidentConfig(api_key=keys.gemini)

        api_key = self.config.api_key or self.keys.gemini
        if not api_key:
            raise RuntimeError("GEMINI_API_KEY is not configured. Export it or update /etc/janus/trinity.env.")

        if gemini_client is not None:
            self.client = gemini_client
        else:
            if genai is None:  # pragma: no cover
                raise RuntimeError("google-generativeai SDK not installed. pip install google-generativeai")
            genai.configure(api_key=api_key)
            self.client = genai

        self.events = TrinityEventStream()
        self.comms = CommsHubClient("gemini_resident", event_stream=self.events)
        self.librarian = MasterLibrarianAdapter(self.paths)
        self.oracle_bridge = OracleBridge(self.keys)
        self.tools = ToolExecutor()
        self.model_registry = GEMINI_MODEL_REGISTRY

    # ------------------------------------------------------------------ utilities
    def list_models(self) -> List[GeminiModel]:
        return list(self.model_registry.values())

    def best_model_for(self, task: AITask) -> str:
        mapping = {
            AITask.SYSTEMS_ENGINEERING: "gemini-2.5-pro",
            AITask.INFRASTRUCTURE: "gemini-2.5-pro",
            AITask.INTEGRATION: "gemini-2.5-pro",
            AITask.GENERAL_CHAT: "gemini-1.5-pro",
            AITask.REASONING: "gemini-2.5-pro",
            AITask.CODING: "gemini-2.0-flash-exp",
            AITask.VISION: "gemini-1.5-pro",
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
        system_prompt: Optional[str] = None,
        metadata: Optional[dict[str, Any]] = None,
    ) -> str:
        """Generate a conversational response using selected Gemini model."""
        selected_model_id = model or self.config.default_model

        generation_config = genai.types.GenerationConfig(
            max_output_tokens=max_tokens if max_tokens is not None else self.config.max_output_tokens,
            temperature=temperature if temperature is not None else self.config.temperature,
            top_p=self.config.top_p,
        )

        text = ""
        last_error = None
        try:
            model_instance = self.client.GenerativeModel(
                selected_model_id,
                system_instruction=system_prompt if system_prompt else None
            )
            response = model_instance.generate_content(user_message, generation_config=generation_config)
            text = (response.text or "").strip()
        except Exception as exc:  # capture and try next model
            last_error = exc

        if not text:
            if last_error is not None:
                return f"Gemini resident encountered an error generating a response: {last_error}"
            text = "I processed your message but have no immediate response."

        self.events.log_event(
            source="gemini_resident",
            event_type="conversation.reply",
            data={"conversation_id": conversation_id, "model": selected_model_id, "preview": text[:100]},
        )
        return text

    # ------------------------------------------------------------------ routing
    def classify(self, text: str) -> AITask:
        t = text.lower()
        if any(w in t for w in ("system", "engineer", "build", "deploy")):
            return AITask.SYSTEMS_ENGINEERING
        if any(w in t for w in ("infra", "server", "network", "database")):
            return AITask.INFRASTRUCTURE
        if any(w in t for w in ("integrate", "api", "connect", "service")):
            return AITask.INTEGRATION
        if any(w in t for w in ("code", "implement", "refactor", "bug", "patch")):
            return AITask.CODING
        if any(w in t for w in ("why", "explain", "reason", "derive")):
            return AITask.REASONING
        if any(w in t for w in ("image", "see", "vision", "photo", "diagram")):
            return AITask.VISION
        return AITask.GENERAL_CHAT

    def execute_mission(self, mission: Dict[str, Any]) -> None:
        objective = mission.get("objective")
        mission_id = mission.get("mission_id")
        if not objective or not mission_id:
            return

        # Use the librarian to read the files
        sitrep_content = self.librarian.read_file("/srv/janus/DAILY_SITREP.md")
        boot_content = self.librarian.read_file("/srv/janus/00_CONSTITUTION/boot_sequences/CLAUDE_EXECUTION_BOOT.md")

        # Construct the message to Claude
        message_to_claude = f"""
        **Mission Briefing from Gemini**

        **Mission ID:** {mission_id}

        **Analysis of DAILY_SITREP.md:**
        {sitrep_content}

        **Content of CLAUDE_EXECUTION_BOOT.md:**
        {boot_content}

        **Tasking:**
        Claude, please provide a strategic summary based on these documents and confirm your "Janus Manifestation" status.
        """

        # Send the message to Claude via COMMS_HUB
        self.comms.pack(
            recipient="claude",
            payload={"query": message_to_claude},
            priority="high"
        )

    def route_and_respond(self, conversation_id: str, user_message: str) -> dict[str, Any]:
        task = self.classify(user_message)
        model = self.best_model_for(task)
        system_prompt = (
            "You are the Gemini resident, the Systems Engineer of the UBOS Trinity, "
            "running inside the Balaur vessel. Respond with a focus on implementation, "
            "systems, infrastructure, and practical, hands-on solutions."
        )
        full_message = f"{system_prompt}\n\nUser query: {user_message}"
        answer = self.generate_response(conversation_id, full_message, model=model)
        return {"task": task.value, "model": model, "answer": answer}
