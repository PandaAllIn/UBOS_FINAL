"""
UBOS Blueprint: Master Librarian HTTP Adapter

Philosophy: Systems Over Willpower + Structure Over Control
Strategic Purpose: Call the Librarian's REST API in a decoupled way and map
the response to the Prime workflow schema.
"""

from __future__ import annotations

from typing import Callable, Dict, Optional

import requests

from ai_prime_agent.bus import TaskMessage
from ai_prime_agent.bus.inproc_bus import Handler
from ai_prime_agent.registry import AgentCapability, AgentRecord, AgentRegistry, AgentStatus


CAPABILITY_NAME = "librarian.consult"


def make_http_consult_handler(*, base_url: str, auth_token: Optional[str] = None, timeout: float = 10.0) -> Handler:
    session = requests.Session()
    if auth_token:
        session.headers.update({"Authorization": f"Bearer {auth_token}"})

    def handler(msg: TaskMessage) -> dict:
        payload = msg.payload or {}
        body = {
            "task_id": msg.message_id,
            "summary": payload.get("summary", ""),
            "context": payload.get("context", []) or [],
            "objectives": payload.get("objectives", []) or [],
            "constraints": payload.get("constraints", []) or [],
            "metadata": {**payload.get("metadata", {}), "correlation_id": msg.correlation_id},
        }
        resp = session.post(f"{base_url.rstrip('/')}/consult", json=body, timeout=timeout)
        resp.raise_for_status()
        data = resp.json()

        # Map Librarian response into our workflow schema
        return {
            "recommendations": data.get("recommendations", []),
            "alignment_notes": data.get("ubos_alignment_notes", []),
            "confidence": data.get("confidence", 0.0),
            "mermaid": data.get("mermaid_diagram"),
        }

    return handler


def register_http_with_prime(
    *,
    agent_id: str,
    registry: AgentRegistry,
    register_handler: Callable[[str, str, Handler], None],
    base_url: str,
    auth_token: Optional[str] = None,
    timeout: float = 10.0,
) -> AgentRecord:
    record = AgentRecord.create(
        agent_id=agent_id,
        agent_type="MasterLibrarian",
        capabilities=[
            AgentCapability(
                name=CAPABILITY_NAME,
                version="1.0",
                description="Alignment consultation via REST",
                input_schema={"type": "object"},
                output_schema={"type": "object"},
            )
        ],
        status=AgentStatus.IDLE,
    )
    registry.register(record)
    handler = make_http_consult_handler(base_url=base_url, auth_token=auth_token, timeout=timeout)
    register_handler(agent_id=agent_id, task=CAPABILITY_NAME, handler=handler)
    return record


__all__ = ["register_http_with_prime", "make_http_consult_handler", "CAPABILITY_NAME"]
