"""Tests for the Research CLI adapter using a mocked subprocess.run."""

from pathlib import Path
import sys
import json

import pytest

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from ai_prime_agent.bus import TaskMessage
from ai_prime_agent.bus.inproc_bus import InProcBus
from ai_prime_agent.registry import AgentRegistry
from ai_prime_agent.adapters.research_cli import register_cli_with_prime


class DummyCompleted:
    def __init__(self, stdout: str, returncode: int = 0, stderr: str = ""):
        self.stdout = stdout
        self.returncode = returncode
        self.stderr = stderr


def test_research_cli_adapter(monkeypatch, tmp_path: Path):
    reg = AgentRegistry()
    bus = InProcBus(reg)

    import ai_prime_agent.adapters.research_cli as cli_mod

    def fake_run(args, capture_output, text, timeout):  # pylint: disable=unused-argument
        payload = {
            "content": "Findings about orchestration...",
            "citations": ["https://x"],
            "query_analysis": {"score": 3},
        }
        return DummyCompleted(stdout=json.dumps(payload))

    monkeypatch.setattr(cli_mod.subprocess, "run", fake_run)

    record = register_cli_with_prime(
        agent_id="A-re-cli",
        registry=reg,
        register_handler=lambda agent_id, task, handler: bus.register_handler(agent_id, task, handler),
        python_exe="python3",
        agent_script=str(tmp_path / "ubos_research_agent.py"),
    )

    msg = TaskMessage.new(
        source_agent_id="A-prime",
        destination_agent_id=record.agent_id,
        task="research.query",
        payload={"query": "UBOS orchestration", "depth": "medium"},
    )
    ack = bus.dispatch(msg)
    assert getattr(ack, "status", "") == "ACK"
    result = bus.last_result_for(msg.message_id)
    assert result and "content" in result and result["citations"]

