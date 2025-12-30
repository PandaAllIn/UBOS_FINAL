"""Execution dispatcher for the Trinity Orchestrator."""
from __future__ import annotations

import os
from typing import Dict, Mapping

from config import APIKeys, TrinityPaths
from janus_orchestrator import DelegationPlan
from oracle_bridge import OracleBridge

_RESIDENTS = {}

def _get_resident(name: str):
    if name in _RESIDENTS:
        return _RESIDENTS[name]
    
    try:
        if name == "claude":
            from claude_resident import ResidentClaude
            instance = ResidentClaude()
        elif name == "gemini":
            from gemini_resident import GeminiResident
            instance = GeminiResident()
        elif name == "groq":
            from groq_resident import GroqResident
            instance = GroqResident()
        elif name == "openai":
            from openai_resident import ResidentOpenAI
            instance = ResidentOpenAI()
        else:
            return None
        
        _RESIDENTS[name] = instance
        return instance
    except Exception as e:
        return f"Error initializing resident {name}: {e}"

def _dispatch_to_resident(plan: DelegationPlan) -> str:
    resident = _get_resident(plan.target)
    if resident is None:
        return f"Error: Resident '{plan.target}' not found."
    if isinstance(resident, str):
        return resident # Error message from initialization

    try:
        # Standardize query method names across residents
        # All local resident classes implement `generate_response(conversation_id, user_message, model=..., ...)`
        
        conversation_id = "telegram_direct"
        
        if plan.target in ["claude", "gemini", "groq", "openai"]:
            return resident.generate_response(conversation_id, plan.query, model=plan.model)
        else:
            return f"Error: Unknown resident type {plan.target}"
            
    except Exception as exc:
        return f"Error executing query on {plan.target}: {exc}"


def execute_plan(plan: DelegationPlan, paths: TrinityPaths, keys: APIKeys) -> str:
    """Executes a delegation plan by routing it to the appropriate resident or oracle."""
    if plan.mode == "oracle":
        oracle_bridge = OracleBridge(keys)
        return oracle_bridge.query_oracle(plan.target, plan.query)

    return _dispatch_to_resident(plan)
