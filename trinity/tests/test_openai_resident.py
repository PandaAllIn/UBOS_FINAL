from __future__ import annotations

import base64
from types import SimpleNamespace

import pytest

import openai_resident
from config import APIKeys, TrinityPaths


class DummyChatCompletions:
    def __init__(self) -> None:
        self.calls: list[str] = []
        self.fail_once = False

    def create(self, *, model: str, **kwargs):  # type: ignore[override]
        self.calls.append(model)
        if self.fail_once:
            self.fail_once = False
            raise RuntimeError("primary model failed")
        return SimpleNamespace(choices=[SimpleNamespace(message=SimpleNamespace(content="ok"))])


class DummyChat:
    def __init__(self) -> None:
        self.completions = DummyChatCompletions()


class DummyEmbeddings:
    def __init__(self) -> None:
        self.calls: list[tuple[str, list[str]]] = []

    def create(self, *, model: str, input):  # type: ignore[override]
        values = input if isinstance(input, list) else [input]
        self.calls.append((model, values))
        data = [SimpleNamespace(embedding=[0.1, 0.2, 0.3]) for _ in values]
        return SimpleNamespace(data=data)


class DummyImages:
    def __init__(self) -> None:
        self.calls: list[dict[str, str]] = []
        self.payload = base64.b64encode(b"fake-image").decode()

    def generate(self, *, model: str, prompt: str, size: str) -> SimpleNamespace:  # type: ignore[override]
        self.calls.append({"model": model, "prompt": prompt, "size": size})
        return SimpleNamespace(data=[SimpleNamespace(b64_json=self.payload)])


class DummyAudioSpeech:
    def __init__(self) -> None:
        self.calls: list[dict[str, str]] = []

    def create(self, **kwargs):  # type: ignore[override]
        self.calls.append(kwargs)
        return SimpleNamespace(content=b"audio-bytes")


class DummyAudio:
    def __init__(self) -> None:
        self.speech = DummyAudioSpeech()


class DummyOpenAIClient:
    def __init__(self) -> None:
        self.chat = DummyChat()
        self.embeddings = DummyEmbeddings()
        self.images = DummyImages()
        self.audio = DummyAudio()


class DummyEvents:
    def __init__(self) -> None:
        self.events: list[dict] = []

    def log_event(self, **kwargs) -> None:
        self.events.append(kwargs)


class DummyCommsHubClient:
    def __init__(self, *args, **kwargs) -> None:
        self.args = args
        self.kwargs = kwargs

    def pack(self, **kwargs):  # pragma: no cover - not needed in tests
        return "ok"

    def unpack(self, **kwargs):  # pragma: no cover
        return []


class DummyLibrarian:
    def __init__(self, *args, **kwargs) -> None:
        self.args = args
        self.kwargs = kwargs


def build_paths(tmp_path):
    base = tmp_path / "trinity"
    memory = tmp_path / "memory"
    logs = tmp_path / "logs"
    comms = tmp_path / "comms"
    cache = tmp_path / "cache"
    master = tmp_path / "master"
    for path in (base, memory, logs, comms, cache, master):
        path.mkdir(parents=True, exist_ok=True)
    return TrinityPaths(
        base_dir=base,
        memory_dir=memory,
        log_dir=logs,
        comms_hub=comms,
        oracle_cache_dir=cache,
        master_librarian_root=master,
    )


@pytest.fixture()
def resident_setup(monkeypatch, tmp_path):
    paths = build_paths(tmp_path)
    keys = APIKeys(openai="test-key")

    monkeypatch.setattr(openai_resident, "load_configuration", lambda: (paths, keys))
    monkeypatch.setattr(openai_resident, "TrinityEventStream", lambda: DummyEvents())
    monkeypatch.setattr(openai_resident, "CommsHubClient", DummyCommsHubClient)
    monkeypatch.setattr(openai_resident, "MasterLibrarianAdapter", lambda *a, **k: DummyLibrarian())

    client = DummyOpenAIClient()
    resident = openai_resident.ResidentOpenAI(openai_client=client)
    return resident, client, paths


def test_generate_response_fallbacks_to_gpt4_when_primary_fails(resident_setup):
    resident, client, _ = resident_setup
    client.chat.completions.fail_once = True

    result = resident.generate_response("conv-1", "hello world", model="gpt-5-mini")

    assert result == "ok"
    assert client.chat.completions.calls[:2] == ["gpt-5-mini", "gpt-4o"]


def test_embeddings_and_image_generation_write_to_memory(resident_setup):
    resident, client, paths = resident_setup

    embed_msg = resident.create_embeddings("hello world", model="text-embedding-3-large")
    assert "model=text-embedding-3-large" in embed_msg
    assert client.embeddings.calls[0][0] == "text-embedding-3-large"

    image_msg = resident.generate_image("mechanical lion", size="512x512")
    assert "Image generated" in image_msg
    image_dir = paths.memory_dir / "openai_images"
    images = list(image_dir.glob("*.png"))
    assert images, "Expected generated image file"  # file exists


def test_init_without_api_key_raises(monkeypatch, tmp_path):
    paths = build_paths(tmp_path)
    keys = APIKeys(openai=None)
    monkeypatch.setattr(openai_resident, "load_configuration", lambda: (paths, keys))
    monkeypatch.setattr(openai_resident, "TrinityEventStream", lambda: DummyEvents())
    monkeypatch.setattr(openai_resident, "CommsHubClient", DummyCommsHubClient)
    monkeypatch.setattr(openai_resident, "MasterLibrarianAdapter", lambda *a, **k: DummyLibrarian())

    client = DummyOpenAIClient()
    with pytest.raises(RuntimeError):
        openai_resident.ResidentOpenAI(openai_client=client)

