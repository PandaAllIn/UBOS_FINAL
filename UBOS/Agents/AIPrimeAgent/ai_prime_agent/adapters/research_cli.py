"""
UBOS Blueprint: Research Agent CLI Adapter

Philosophy: Systems Over Willpower + Strategic Starting Points
Strategic Purpose: Invoke the Research Agent as an independent process and map
its JSON output to the Prime workflow schema.
"""

from __future__ import annotations

import json
import subprocess
from typing import Callable, Dict, Optional

from ai_prime_agent.bus import TaskMessage
from ai_prime_agent.bus.inproc_bus import Handler
from ai_prime_agent.registry import AgentCapability, AgentRecord, AgentRegistry, AgentStatus


CAPABILITY_NAME = "research.query"


def make_cli_research_handler(*, python_exe: str, agent_script: str, depth_to_command: Optional[Dict[str, str]] = None, timeout: float = 20.0) -> Handler:
    mapping = depth_to_command or {"quick": "quick", "medium": "pro", "deep": "deep"}

    def handler(msg: TaskMessage) -> dict:
        payload = msg.payload or {}
        query = str(payload.get("query", ""))
        depth = str(payload.get("depth", "medium"))
        command = mapping.get(depth, "pro")
        args = [python_exe, agent_script, command, query, "--format", "json", "--depth", depth]
        proc = subprocess.run(args, capture_output=True, text=True, timeout=timeout)
        if proc.returncode != 0:
            # Attempt to parse error payload if present
            try:
                err = json.loads(proc.stdout or proc.stderr or "{}")
            except Exception:
                err = {"error": True, "stderr": proc.stderr}
            raise RuntimeError(f"Research CLI failed: {err}")

        # The CLI prints banners and then JSON. Extract JSON from stdout robustly.
        raw = proc.stdout.strip()
        data = None
        # Try direct parse
        try:
            data = json.loads(raw)
        except Exception:
            # Fallback: find the first line that looks like JSON and parse from there
            for i, line in enumerate(raw.splitlines()):
                if line.lstrip().startswith("{"):
                    try:
                        candidate = "\n".join(raw.splitlines()[i:])
                        data = json.loads(candidate)
                        break
                    except Exception:
                        continue
        if data is None:
            raise RuntimeError("Research CLI output not valid JSON")
        return {
            "query": query,
            "depth": depth,
            "content": data.get("content", ""),
            "citations": data.get("citations", []),
            "analysis": data.get("query_analysis", {}),
            "confidence": 0.7,
        }

    return handler


def register_cli_with_prime(
    *,
    agent_id: str,
    registry: AgentRegistry,
    register_handler: Callable[[str, str, Handler], None],
    python_exe: str,
    agent_script: str,
    timeout: float = 20.0,
) -> AgentRecord:
    record = AgentRecord.create(
        agent_id=agent_id,
        agent_type="ResearchAgent",
        capabilities=[
            AgentCapability(
                name=CAPABILITY_NAME,
                version="1.0",
                description="External research via CLI",
                input_schema={"type": "object"},
                output_schema={"type": "object"},
            )
        ],
        status=AgentStatus.IDLE,
    )
    registry.register(record)
    handler = make_cli_research_handler(python_exe=python_exe, agent_script=agent_script, timeout=timeout)
    register_handler(agent_id=agent_id, task=CAPABILITY_NAME, handler=handler)
    return record


__all__ = ["register_cli_with_prime", "make_cli_research_handler", "CAPABILITY_NAME"]
