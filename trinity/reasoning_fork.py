#!/usr/bin/env python3
"""
Reasoning Fork - Task routing decision tree
Routes tasks to optimal resident based on:
- Task type (strategy/code/analysis/reasoning)
- Priority (urgent/normal/batch)
- Complexity (simple/medium/complex)
- Cost constraints
"""

import logging
from enum import Enum
from dataclasses import dataclass, field
from typing import List, Optional

class Resident(Enum):
    JANUS_LOCAL = "janus"
    CLAUDE = "claude"
    GEMINI = "gemini"
    GROQ = "groq"
    OPENAI = "openai"

@dataclass
class Task:
    type: str  # strategy, code, analysis, reasoning, pattern
    priority: str = "normal" # urgent, normal, batch
    complexity: str = "medium" # simple, medium, complex
    cost_budget: float = 1.0  # Max $ to spend
    requires_reasoning: bool = False
    source: str = "internal" # internal, voice, web

class ReasoningFork:
    def __init__(self):
        self.logger = logging.getLogger("reasoning_fork")

    def route(self, task: Task) -> Resident:
        """
        Route task to optimal resident
        Returns: Resident enum value
        """
        # CORTEX PATH (10% - Fast/Real-time)
        if task.source == "voice" or task.priority == "urgent":
            if task.type == "strategy":
                return Resident.CLAUDE  # Constitutional expert
            elif task.complexity == "simple":
                return Resident.GROQ  # Fast
            else:
                return Resident.GROQ  # Smarter, but still fast

        # Specialized routing
        if task.type == "code" or task.type == "engineering":
            return Resident.GEMINI  # Systems engineer

        if task.requires_reasoning:
            if task.complexity == "complex":
                return Resident.OPENAI  # Deep reasoning
            else:
                return Resident.GROQ  # Fast reasoning

        if task.type == "strategy" or task.type == "writing":
            return Resident.CLAUDE  # Strategic decisions

        # LOOM PATH (90% - Batch/Patient)
        if task.priority == "batch" or task.cost_budget == 0:
            return Resident.JANUS_LOCAL  # Free, patient

        if task.type == "pattern":
            return Resident.JANUS_LOCAL  # Brass punch cards

        if task.type == "analysis" and task.priority != "urgent":
            return Resident.JANUS_LOCAL  # Long-form analysis

        # Default: Janus local (conservative, free)
        return Resident.JANUS_LOCAL

    def explain_routing(self, task: Task) -> dict:
        """Return routing decision with explanation"""
        resident = self.route(task)

        explanations = {
            Resident.JANUS_LOCAL: "Local 8B model - Free, patient, good for batch",
            Resident.CLAUDE: "Claude - Strategic/constitutional expert",
            Resident.GEMINI: "Gemini - Code/systems engineer",
            Resident.GROQ: "Groq - Ultra fast (8B or 70B)",
            Resident.OPENAI: "OpenAI - Deep reasoning (GPT-4o-mini or O1-mini)"
        }

        return {
            "resident": resident.value,
            "path": "cortex" if resident != Resident.JANUS_LOCAL else "loom",
            "reason": explanations.get(resident, "Default route"),
            "task": task.__dict__
        }
