from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping, Optional

import jsonschema

from pucklib.cypher.bih_engine import BIHEngine
from .constitution import load_constitutional_markers
from .tone import tone_for_puck

SCHEMA_PATH = Path(__file__).resolve().parent / "mission_brief_schema.json"

with SCHEMA_PATH.open("r", encoding="utf-8") as handle:
    _SCHEMA = json.load(handle)

_CONSTITUTION = load_constitutional_markers()

@dataclass
class ValidationResult:
    ok: bool
    errors: list[str]
    round_trip_equivalent: bool | None = None
    symbol_check_ok: bool | None = None
    constitution_ok: bool | None = None

    def raise_if_invalid(self) -> None:
        if not self.ok:
            raise ValidationError(self.errors)

class ValidationError(Exception):
    def __init__(self, errors: list[str]) -> None:
        message = "; ".join(errors)
        super().__init__(message)
        self.errors = errors

def validate_mission_brief(
    puck: Mapping[str, Any],
    *,
    bih_engine: BIHEngine,
    original_plaintext: str | None = None,
) -> ValidationResult:
    errors: list[str] = []

    try:
        jsonschema.validate(puck, _SCHEMA)
    except jsonschema.ValidationError as exc:
        errors.append(f"schema: {exc.message}")

    tone = puck.get("metadata", {}).get("tone")
    allowed_tones = tone_for_puck("mission_brief")
    if tone and tone not in allowed_tones:
        errors.append(f"tone: '{tone}' not permitted for mission_brief")

    payload = puck.get("payload")
    recovered: Optional[str] = None
    symbol_ok: bool | None = None
    constitution_ok: bool | None = None

    if isinstance(payload, str):
        recovered = bih_engine.decompress(payload)

        unknown_symbols = _find_unknown_symbols(payload, bih_engine.allowed_symbols)
        symbol_ok = not unknown_symbols
        if unknown_symbols:
            missing = ", ".join(sorted(unknown_symbols))
            errors.append(f"layer4: unknown symbols present ({missing})")

        constitution_ok = _check_constitution(payload)
        if not constitution_ok and recovered is not None:
            constitution_ok = _check_constitution(recovered)
        if constitution_ok is False:
            errors.append("layer5: constitutional markers missing")

    round_trip_ok: bool | None = None
    if recovered is not None:
        if original_plaintext is not None:
            round_trip_ok = bih_engine.is_semantically_equivalent(recovered, original_plaintext)
        else:
            round_trip_ok = True
        if round_trip_ok is False:
            errors.append("layer2: decompressed payload diverges semantically")

    return ValidationResult(
        ok=not errors,
        errors=errors,
        round_trip_equivalent=round_trip_ok,
        symbol_check_ok=symbol_ok,
        constitution_ok=constitution_ok,
    )


def _find_unknown_symbols(payload: str, allowed_symbols: set[str]) -> set[str]:
    cleaned = payload
    for symbol in sorted(allowed_symbols, key=len, reverse=True):
        cleaned = cleaned.replace(symbol, "")
    return {char for char in cleaned if ord(char) > 127}


def _check_constitution(text: str) -> bool:
    symbols = {k: v for k, v in _CONSTITUTION.items() if isinstance(v, str) and v}
    rep_symbol = symbols.get("rep_symbol")
    lion_symbol = symbols.get("lion_sanctuary_symbol")

    text_symbols = set(text)
    canonical = text.lower()

    lion_present = (
        (lion_symbol and lion_symbol in text_symbols)
        or "lion's sanctuary" in canonical
    )
    rep_present = (
        (rep_symbol and rep_symbol in text_symbols)
        or "recursive enhancement protocol" in canonical
    )
    return lion_present and rep_present
