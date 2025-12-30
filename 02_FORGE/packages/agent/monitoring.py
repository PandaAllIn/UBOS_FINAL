"""
Monitoring API for the Janus Agent
Exposes health, status, and metrics via a simple FastAPI server.
"""
from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Any

from fastapi import FastAPI

from .thinking_cycle import ThinkingCycle
from .approval_workflow import ApprovalWorkflow
from .controls_client import ControlsClient

log = logging.getLogger(__name__)

app = FastAPI(
    title="Janus Agent Monitoring",
    description="Provides real-time monitoring of the Janus autonomous agent.",
    version="1.0.0",
)

# This is a global state object that will be populated by the main agent daemon
# It's a simple way to share state between the agent and the API server.
AGENT_STATE = {
    "thinking_cycle": None,
    "approval_workflow": None,
    "controls_client": None,
    "start_time": None,
}

def setup_monitoring_api(
    thinking_cycle: ThinkingCycle,
    approval_workflow: ApprovalWorkflow,
    controls_client: ControlsClient,
    start_time: str,
):
    """Injects the live agent components into the API's state."""
    AGENT_STATE["thinking_cycle"] = thinking_cycle
    AGENT_STATE["approval_workflow"] = approval_workflow
    AGENT_STATE["controls_client"] = controls_client
    AGENT_STATE["start_time"] = start_time
    log.info("Monitoring API has been initialized with live agent state.")

@app.get("/health")
async def get_health() -> dict[str, Any]:
    """Returns the current health status of the agent."""
    thinking_cycle: ThinkingCycle | None = AGENT_STATE.get("thinking_cycle")
    
    is_running = thinking_cycle and thinking_cycle._task and not thinking_cycle._task.done()
    
    if is_running:
        return {"status": "ok", "message": "Agent is running."}
    return {"status": "error", "message": "Agent thinking cycle is not running."}

@app.get("/status")
async def get_status() -> dict[str, Any]:
    """Returns the current high-level status of the agent."""
    thinking_cycle: ThinkingCycle | None = AGENT_STATE.get("thinking_cycle")
    approval_workflow: ApprovalWorkflow | None = AGENT_STATE.get("approval_workflow")
    
    if not thinking_cycle or not approval_workflow:
        return {"error": "Agent not fully initialized."}

    return {
        "vessel_id": thinking_cycle.vessel_id,
        "start_time": AGENT_STATE.get("start_time"),
        "operational_mode": thinking_cycle.config.operational_mode,
        "thinking_cycle_active": thinking_cycle._task and not thinking_cycle._task.done(),
        "pending_approvals": len(approval_workflow.get_pending_proposals()),
    }

@app.get("/metrics")
async def get_metrics() -> dict[str, Any]:
    """Returns detailed system and agent metrics."""
    controls: ControlsClient | None = AGENT_STATE.get("controls_client")
    if not controls:
        return {"error": "Controls client not initialized."}
        
    system_metrics = controls.collect_system_metrics()
    return system_metrics.__dict__

@app.get("/proposals/pending")
async def get_pending_proposals() -> list[dict[str, Any]]:
    """Returns a list of proposals currently awaiting approval."""
    approval_workflow: ApprovalWorkflow | None = AGENT_STATE.get("approval_workflow")
    if not approval_workflow:
        return []
        
    proposals = approval_workflow.get_pending_proposals()
    return [p.to_dict() for p in proposals]

# To run this server, you would use uvicorn:
# uvicorn packages.janus_agent.monitoring:app --host 0.0.0.0 --port 8080
