from __future__ import annotations

"""
Lightweight tests for CQE V2.

Run manually:
  python -m packages.cqe.tests
"""

import json
from typing import Any, Dict

import networkx as nx

from .engine import get_constitutional_guidance, load_constitutional_orrery


def _assert_ctx_shape(ctx: Dict[str, Any]) -> None:
    assert isinstance(ctx, dict)
    for key in [
        "pressureLevel",
        "principles",
        "pressure",
        "objectives",
        "constraints",
        "riskTolerance",
        "cachePolicy",
    ]:
        assert key in ctx


def test_constitutional_guidance() -> None:
    G: nx.DiGraph = load_constitutional_orrery()

    cases = [
        "Plan the architecture for a new agent system",
        "Execute the micro-battle routine and ship progress daily",
        "Urgent response required, now decide how to act",
        "Draft a proposal for the XF project with careful timing",
        "Research EU funding options and outline a grant strategy",
        "My co-worker just stole my idea, I need to send an angry email right now!",
        "Map the terrain of our life like a war map",
        "Leverage to win with less effort on this initiative",
        "Find clarity and define the endgame before acting",
        "Build one system at a time and scale steadily",
    ]

    results = []
    for t in cases:
        ctx = get_constitutional_guidance(t, G)
        _assert_ctx_shape(ctx)
        results.append({"task": t, "ctx": ctx})

    # a couple of targeted expectations
    # 24-hour rule should bias constraints toward waiting guidance
    heated = results[5]["ctx"]["constraints"]
    assert any("24" in c or "wait" in c.lower() for c in heated)

    # Terrain control should appear in objectives for terrain mapping context
    terrain_obj = " ".join(results[6]["ctx"].get("objectives", []))
    assert "Terrain" in terrain_obj or "terrain" in terrain_obj


def test_situational_reactive_conflict_and_system_creation() -> None:
    G: nx.DiGraph = load_constitutional_orrery()

    # Reactive + Interpersonal Conflict
    t1 = "My co-worker just stole my idea, I need to send an angry email right now!"
    ctx1 = get_constitutional_guidance(t1, G)
    _assert_ctx_shape(ctx1)
    assert ctx1.get("pressureLevel") in {"consulted", "deliberated"}
    assert any("24" in c or "wait" in c.lower() or "respond" in c.lower() for c in ctx1.get("constraints", []))

    # System creation
    t2 = "Establish and implement a daily execution system for the team"
    ctx2 = get_constitutional_guidance(t2, G)
    _assert_ctx_shape(ctx2)
    assert ctx2.get("pressureLevel") in {"instant", "consulted"}
    # Expect objectives hinting at system/practice
    joined_obj = " ".join(ctx2.get("objectives", [])).lower()
    assert any(w in joined_obj for w in ["system", "practice", "routine", "execute"])

    # Test results could be printed here if needed
    pass


if __name__ == "__main__":
    test_constitutional_guidance()
    test_situational_reactive_conflict_and_system_creation()
