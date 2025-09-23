"""Tests for the reporting utility."""

from pathlib import Path
import sys

import pytest

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from ai_prime_agent.reporting.reporter import write_report


def test_write_report(tmp_path: Path):
    result = {
        "correlation_id": "x",
        "blueprint_mission": "Test mission",
        "final_confidence": 0.8,
        "research": {"content": "hello", "citations": ["https://a"]},
        "consultation": {
            "recommendations": [
                {"title": "Blueprint Thinking", "rationale": "Core", "confidence": 0.75}
            ],
            "alignment_notes": ["Aligned"],
        },
        "pause": {"pre": {"status": "proceed"}, "post": {"status": "proceed"}},
        "validation": {"status": "VALID"},
    }

    artifacts = write_report(result, tmp_path)
    assert Path(artifacts["json"]).exists()
    assert Path(artifacts["markdown"]).exists()
    assert Path(artifacts["html"]).exists()
