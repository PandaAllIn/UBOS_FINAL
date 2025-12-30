"""OpenAI resident hot vessel with model registry and Trinity integration.

This resident mirrors Groq resident patterns:
- Model registry with strengths and selection
- Comms Hub integration (pack/unpack)
- Oracle access via OracleBridge
- Tooling via ToolExecutor

The resident supports manual model overrides and simple task classification
to select a default model when not specified.
"""
from __future__ import annotations

import base64
import mimetypes
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
    from openai import OpenAI  # type: ignore
except Exception:  # pragma: no cover
    OpenAI = None  # type: ignore


class AITask(Enum):
    STRATEGIC = "strategic"
    GENERAL_CHAT = "general_chat"
    REASONING = "reasoning"
    CODING = "coding"
    FUNCTION_CALLING = "function_calling"
    STRUCTURED = "structured_output"
    VISION = "vision"
    EMBEDDINGS = "embeddings"
    IMAGE_GENERATION = "image_generation"
    TRANSCRIPTION = "transcription"
    TTS = "tts"


@dataclass
class OpenAIModel:
    model_id: str
    name: str
    strengths: Sequence[str]
    context_tokens: int = 128_000
    modalities: Sequence[str] = field(default_factory=lambda: ("text",))


# Curated registry with commonly used OpenAI models.
OPENAI_MODEL_REGISTRY: Dict[str, OpenAIModel] = {
    # Chat + Vision
    "gpt-4o": OpenAIModel(
        model_id="gpt-4o",
        name="GPT-4o",
        strengths=("vision", "tool_use", "chat", "function_calling"),
        modalities=("text", "vision"),
        context_tokens=128_000,
    ),
    "gpt-4o-mini": OpenAIModel(
        model_id="gpt-4o-mini",
        name="GPT-4o Mini",
        strengths=("chat", "low_cost", "function_calling"),
        modalities=("text", "vision"),
        context_tokens=128_000,
    ),
    # GPT-5 family (curated per strategy)
    "gpt-5": OpenAIModel(
        model_id="gpt-5",
        name="GPT-5",
        strengths=("complex_tasks", "planning", "tool_use"),
        modalities=("text", "vision"),
        context_tokens=200_000,
    ),
    "gpt-5-mini": OpenAIModel(
        model_id="gpt-5-mini",
        name="GPT-5 Mini",
        strengths=("fast", "cheap", "chat"),
        modalities=("text", "vision"),
        context_tokens=128_000,
    ),
    "gpt-5-nano": OpenAIModel(
        model_id="gpt-5-nano",
        name="GPT-5 Nano",
        strengths=("ultra_fast", "high_volume"),
        modalities=("text",),
        context_tokens=64_000,
    ),
    # Reasoning / Deep Research
    "o1": OpenAIModel(
        model_id="o1",
        name="O1",
        strengths=("deep_reasoning", "planning"),
        modalities=("text",),
        context_tokens=200_000,
    ),
    "o1-mini": OpenAIModel(
        model_id="o1-mini",
        name="O1 Mini",
        strengths=("reasoning", "lower_cost", "faster"),
        modalities=("text",),
        context_tokens=200_000,
    ),
    "o3-mini": OpenAIModel(
        model_id="o3-mini",
        name="O3 Mini",
        strengths=("reasoning", "fast"),
        modalities=("text",),
        context_tokens=200_000,
    ),
    "o4-mini-deep-research": OpenAIModel(
        model_id="o4-mini-deep-research",
        name="O4 Mini Deep Research",
        strengths=("deep_research", "reasoning", "multi_step"),
        modalities=("text",),
        context_tokens=200_000,
    ),
    # Images
    "gpt-image-1": OpenAIModel(
        model_id="gpt-image-1",
        name="GPT Image 1",
        strengths=("image_generation", "diagram"),
        modalities=("image",),
        context_tokens=0,
    ),
    # Audio
    "whisper-1": OpenAIModel(
        model_id="whisper-1",
        name="Whisper v1",
        strengths=("transcription",),
        modalities=("audio",),
        context_tokens=0,
    ),
    "tts-1": OpenAIModel(
        model_id="tts-1",
        name="Text-to-Speech 1",
        strengths=("tts",),
        modalities=("audio",),
        context_tokens=0,
    ),
    "tts-1-hd": OpenAIModel(
        model_id="tts-1-hd",
        name="Text-to-Speech 1 HD",
        strengths=("tts", "high_quality"),
        modalities=("audio",),
        context_tokens=0,
    ),
}


@dataclass(slots=True)
class OpenAIResidentConfig:
    api_key: Optional[str] = None
    default_model: str = "gpt-5-mini"
    temperature: float = 0.2
    top_p: float = 0.9
    max_output_tokens: int = 1024
    memory_db: Path = Path("/srv/janus/trinity_memory/openai_resident.db")


class ResidentOpenAI:
    """OpenAI hot vessel with model registry and Trinity integrations."""

    def __init__(
        self,
        config: Optional[OpenAIResidentConfig] = None,
        *,
        openai_client: Optional[Any] = None,
    ) -> None:
        paths, keys = load_configuration()
        self.paths: TrinityPaths = paths
        self.keys: APIKeys = keys
        self.config = config or OpenAIResidentConfig(api_key=keys.openai)

        api_key = self.config.api_key or self.keys.openai
        if not api_key:
            raise RuntimeError("OPENAI_API_KEY is not configured. Export it or update /etc/janus/trinity.env.")

        if openai_client is not None:
            self.client = openai_client
        else:
            if OpenAI is None:  # pragma: no cover
                raise RuntimeError("openai SDK not installed. pip install openai>=1.0")
            self.client = OpenAI(api_key=api_key)

        self.events = TrinityEventStream()
        self.comms = CommsHubClient("openai_resident", event_stream=self.events)
        self.librarian = MasterLibrarianAdapter(self.paths)
        self.oracle_bridge = OracleBridge(self.keys)
        self.tools = ToolExecutor()
        self.model_registry = OPENAI_MODEL_REGISTRY

    # ------------------------------------------------------------------ utilities
    def list_models(self) -> List[OpenAIModel]:
        return list(self.model_registry.values())

    def best_model_for(self, task: AITask) -> str:
        mapping = {
            # Priority 1 strategy
            AITask.STRATEGIC: "gpt-5",
            AITask.GENERAL_CHAT: "gpt-5-mini",
            AITask.REASONING: "o4-mini-deep-research",
            AITask.CODING: "gpt-5-codex",
            # Complementary capabilities
            AITask.FUNCTION_CALLING: "gpt-5",
            AITask.STRUCTURED: "gpt-5",
            AITask.VISION: "gpt-5",
            AITask.EMBEDDINGS: "text-embedding-3-large",
            AITask.IMAGE_GENERATION: "gpt-image-1",
            AITask.TRANSCRIPTION: "whisper-1",
            AITask.TTS: "tts-1-hd",
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
        """Generate a conversational response using selected OpenAI model."""
        selected = model or self.config.default_model
        candidates = [selected]
        if selected not in ("gpt-4o", "gpt-4o-mini"):
            candidates += ["gpt-4o", "gpt-4o-mini"]

        text = ""
        last_error = None
        for m in candidates:
            try:
                messages = []
                if system_prompt:
                    messages.append({"role": "system", "content": system_prompt})
                messages.append({"role": "user", "content": user_message})
                response = self.client.chat.completions.create(
                    model=m,
                    messages=messages,
                    temperature=temperature if temperature is not None else self.config.temperature,
                    max_tokens=max_tokens if max_tokens is not None else self.config.max_output_tokens,
                )
                try:
                    text = (response.choices[0].message.content or "").strip()
                except Exception:
                    text = ""
                if text:
                    selected = m
                    break
            except Exception as exc:  # capture and try next model
                last_error = exc
                continue

        if not text:
            if last_error is not None:
                return f"OpenAI resident encountered an error generating a response: {last_error}"
            text = "I processed your message but have no immediate response."

        self.events.log_event(
            source="openai_resident",
            event_type="conversation.reply",
            data={"conversation_id": conversation_id, "model": selected, "preview": text[:100]},
        )
        return text

    # ---------------------------------------------------------------- embeddings
    def create_embeddings(self, text: Union[str, List[str]], model: Optional[str] = None) -> str:
        selected = model or "text-embedding-3-large"
        inputs = [text] if isinstance(text, str) else text
        try:
            resp = self.client.embeddings.create(model=selected, input=inputs)
            dims = len(resp.data[0].embedding) if getattr(resp, "data", None) else 0
            return f"Embeddings created: model={selected}, items={len(inputs)}, dimensions={dims}"
        except Exception as exc:  # pragma: no cover - network/runtime faults
            return f"OpenAI embeddings error: {exc}"

    def embed_texts(self, texts: List[str], model: Optional[str] = None) -> List[List[float]]:
        selected = model or "text-embedding-3-large"
        try:
            resp = self.client.embeddings.create(model=selected, input=texts)
            return [item.embedding for item in getattr(resp, "data", [])]
        except Exception:
            return []

    # ------------------------------------------------------------------ images
    def generate_image(self, prompt: str, *, size: str = "1024x1024") -> str:
        out_dir = self.paths.memory_dir / "openai_images"
        out_dir.mkdir(parents=True, exist_ok=True)
        now = int(time.time())
        out_path = out_dir / f"img_{now}.png"
        try:
            result = self.client.images.generate(model="gpt-image-1", prompt=prompt, size=size)
            b64 = result.data[0].b64_json  # type: ignore[attr-defined]
            with out_path.open("wb") as fh:
                fh.write(base64.b64decode(b64))
            ts = datetime.fromtimestamp(now, tz=timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
            return f"Image generated: {out_path} | model=gpt-image-1 | ts={ts}"
        except Exception as exc:  # pragma: no cover
            return f"OpenAI image error: {exc}"

    # ----------------------------------------------------------------------- TTS
    def text_to_speech(
        self,
        text: str,
        *,
        voice: str = "alloy",
        model: str = "tts-1",
        format: str = "mp3",
    ) -> str:
        out_dir = self.paths.memory_dir / "openai_audio"
        out_dir.mkdir(parents=True, exist_ok=True)
        now = int(time.time())
        out_path = out_dir / f"tts_{now}.{format}"
        try:
            audio = self.client.audio.speech.create(model=model, voice=voice, input=text)
            content = getattr(audio, "content", None)
            if content is None and hasattr(audio, "read"):
                content = audio.read()
            if not content:
                raise RuntimeError("TTS response missing audio content")
            with out_path.open("wb") as fh:
                fh.write(content)
            ts = datetime.fromtimestamp(now, tz=timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
            return f"Audio generated: {out_path} | model={model} | voice={voice} | ts={ts}"
        except Exception as exc:  # pragma: no cover
            return f"OpenAI TTS error: {exc}"

    def transcribe_audio(self, file_path: Path, model: str = "whisper-1") -> str:
        try:
            with file_path.open("rb") as fh:
                result = self.client.audio.transcriptions.create(model=model, file=fh)
            text = getattr(result, "text", "") or ""
            return text.strip() or "[Transcription returned no text]"
        except Exception as exc:  # pragma: no cover
            return f"OpenAI transcription error: {exc}"

    def analyze_image(self, file_path: Path, prompt: str = "Describe this image.") -> str:
        mime = mimetypes.guess_type(str(file_path))[0] or "image/png"
        try:
            encoded = base64.b64encode(file_path.read_bytes()).decode("ascii")
        except Exception as exc:  # pragma: no cover
            return f"OpenAI vision error (file read): {exc}"
        data_url = f"data:{mime};base64,{encoded}"
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": prompt},
                            {"type": "image_url", "image_url": {"url": data_url}},
                        ],
                    }
                ],
                temperature=self.config.temperature,
                max_tokens=self.config.max_output_tokens,
            )
            content = response.choices[0].message.content or ""
            return content.strip() or "[Vision response returned no text]"
        except Exception as exc:  # pragma: no cover
            return f"OpenAI vision error: {exc}"

    # ------------------------------------------------------------------ routing
    def classify(self, text: str) -> AITask:
        t = text.lower()
        if any(w in t for w in ("embed", "embedding", "semantic")):
            return AITask.EMBEDDINGS
        if any(w in t for w in ("image", "generate image", "dall-e")):
            return AITask.IMAGE_GENERATION
        if any(w in t for w in ("transcribe", "audio to text", "whisper")):
            return AITask.TRANSCRIPTION
        if any(w in t for w in ("speak", "tts", "voice")):
            return AITask.TTS
        if any(w in t for w in ("plan", "strategy", "roadmap", "architecture")):
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
            "You are the OpenAI resident running inside the UBOS Balaur vessel. "
            "Respond with awareness of the mission context and tie answers back to Janus when relevant."
        )
        answer = self.generate_response(
            conversation_id,
            user_message,
            model=model,
            system_prompt=system_prompt,
        )
        return {"task": task.value, "model": model, "answer": answer}
