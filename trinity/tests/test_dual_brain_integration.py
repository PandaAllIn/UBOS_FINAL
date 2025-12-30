from __future__ import annotations

from pathlib import Path

import mission_orchestrator as mo
import pytest
from data_commons_oracle import DataCommonsOracle
from dual_speed_brain import DualSpeedCognition, GroqUnavailableError


class StubGroqClient:
    def __init__(self, *, raise_error: bool = False) -> None:
        self.raise_error = raise_error
        self.calls: list[str] = []

    def is_available(self) -> bool:  # pragma: no cover - trivial
        return True

    def fast_think(self, prompt: str) -> str:
        self.calls.append(prompt)
        if self.raise_error:
            raise GroqUnavailableError("Groq unavailable")
        return "scout-result"


class DummyResponse:
    def __init__(self, payload: dict) -> None:
        self.payload = payload
        self.status_code = 200
        self.text = ""

    def json(self):  # pragma: no cover - simple passthrough
        return self.payload


class DummySession:
    def __init__(self, payload: dict) -> None:
        self.payload = payload
        self.requests: list[tuple[str, dict]] = []

    def get(self, url: str, params=None, headers=None, timeout=10):  # pragma: no cover - trivial
        self.requests.append((url, params or {}))
        return DummyResponse(self.payload)


def test_dual_speed_scout_falls_back_to_local(monkeypatch, tmp_path):
    stub = StubGroqClient(raise_error=True)
    monkeypatch.setattr(DualSpeedCognition, "_resolve_llama_cli", lambda self: Path("/bin/true"))

    def fake_local(self, prompt: str, *, temperature: float, tokens: int) -> str:
        return f"LOCAL({tokens}): {prompt}"

    monkeypatch.setattr(DualSpeedCognition, "_local_response", fake_local)

    brain = DualSpeedCognition(groq_client=stub, local_model_path=tmp_path / "model.gguf")
    result = brain.scout("Investigate fallback behavior")

    assert result.startswith("LOCAL")
    assert stub.calls == ["Investigate fallback behavior"]


def test_mission_orchestrator_reads_roadmap_and_delegates(monkeypatch, tmp_path):
    mission_file = tmp_path / "mission.yaml"
    mission_file.write_text("status: active\n", encoding="utf-8")
    entry = mo.MissionEntry("M-1", mission_file, None, None, None, 0)

    monkeypatch.setattr(mo, "load_config", lambda path: ([entry], 5, 15))
    monkeypatch.setattr(mo, "read_state", lambda: {"current_mission": None, "missions": {}})

    roadmap = tmp_path / "ROADMAP.md"
    roadmap.write_text("## Phase 4\n*   Craft final integration plan\n", encoding="utf-8")

    captured_plans = []

    def fake_execute(plan, paths, keys):
        captured_plans.append(plan)
        return "delegated"

    monkeypatch.setattr(mo, "execute_plan", fake_execute)

    orchestrator = mo.MissionOrchestrator(config_path=mission_file)
    orchestrator.roadmap_path = roadmap

    missions = orchestrator.read_roadmap_missions()
    assert missions[0]["phase"] == "Phase 4"
    assert "integration" in missions[0]["description"].lower()

    outcome = orchestrator.delegate_to_resident("Coordinate Phase 4", "claude")
    assert outcome == "delegated"
    assert captured_plans[0].target == "claude"


def test_data_commons_population_lookup():
    payload = {
        "series": [
            {"date": "2021", "value": 19000000},
            {"date": "2022", "value": 19100000},
        ]
    }
    oracle = DataCommonsOracle(api_key=None, session=DummySession(payload))
    summary = oracle.query_demographics("country/ROU")
    assert "country/ROU" in summary
    assert "19100000" in summary

