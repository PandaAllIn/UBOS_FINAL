from __future__ import annotations

import json
from pathlib import Path
from typing import Mapping

_TONE_REGISTRY_PATH = Path(__file__).resolve().parent / "tone_registry.json"

with _TONE_REGISTRY_PATH.open("r", encoding="utf-8") as handle:
    _TONE_REGISTRY: Mapping[str, list[str]] = json.load(handle)["tones"]


def tone_for_puck(puck_type: str) -> list[str]:
    return _TONE_REGISTRY.get(puck_type, [])
