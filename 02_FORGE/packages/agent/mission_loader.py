"""Mission loader for injecting study materials into LLM context.

Supports YAML or JSON mission definitions. Extracts limited-size excerpts from
listed source files to avoid exceeding prompt budgets.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import json


def _safe_load_yaml(path: Path) -> dict[str, Any]:
    try:
        import yaml  # type: ignore
    except Exception as exc:  # pragma: no cover - optional dependency
        raise RuntimeError("PyYAML is required to load YAML missions") from exc
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def _read_excerpt(p: Path, max_chars: int) -> str:
    try:
        text = p.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return ""
    if len(text) <= max_chars:
        return text
    # take head and tail slices to preserve context
    head = text[: max_chars // 2]
    tail = text[-max_chars // 2 :]
    return head + "\n...\n" + tail


def load_mission(path: Path, *, max_chars: int = 6000) -> dict[str, Any]:
    """Load mission spec and attach study material excerpts.

    Expected mission keys (best effort): mission_id, mission_name, objectives,
    sources/materials containing file paths or inline content.
    """
    if path.suffix.lower() in (".yaml", ".yml"):
        data = _safe_load_yaml(path)
    else:
        with path.open("r", encoding="utf-8") as f:
            data = json.load(f)

    mission: dict[str, Any] = {
        "mission_id": data.get("mission_id") or data.get("id") or path.stem,
        "mission_name": data.get("mission_name") or data.get("name") or "Unnamed Mission",
        "objectives": data.get("objectives") or data.get("goals") or [],
    }

    materials: list[dict[str, Any]] = []

    # Common fields that may point to files
    candidates: list[Any] = []
    for key in ("materials", "sources", "architecture_docs", "philosophy_docs"):
        val = data.get(key)
        if isinstance(val, list):
            candidates.extend(val)

    for item in candidates:
        # item may be a string path OR dict with 'path'/'content'
        if isinstance(item, str):
            p = Path(item)
            if not p.is_absolute():
                p = (path.parent / p).resolve()
            excerpt = _read_excerpt(p, max_chars=max_chars)
            materials.append({
                "name": p.name,
                "path": str(p),
                "kind": p.suffix.lower().lstrip("."),
                "length": len(excerpt),
                "excerpt": excerpt,
            })
        elif isinstance(item, dict):
            p_str = item.get("path")
            if p_str:
                p = Path(p_str)
                if not p.is_absolute():
                    p = (path.parent / p).resolve()
                excerpt = _read_excerpt(p, max_chars=max_chars)
                materials.append({
                    "name": item.get("name") or p.name,
                    "path": str(p),
                    "kind": p.suffix.lower().lstrip("."),
                    "length": len(excerpt),
                    "excerpt": excerpt,
                })
            elif item.get("content"):
                content = str(item["content"])[:max_chars]
                materials.append({
                    "name": item.get("name") or "inline",
                    "path": None,
                    "kind": "inline",
                    "length": len(content),
                    "excerpt": content,
                })

    mission["materials"] = materials
    return mission

