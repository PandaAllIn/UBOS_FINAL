"""Autonomous delegation loop for Janus."""
from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List

import yaml

from config import load_configuration
from janus_orchestrator import DelegationPlan
from orchestrator_executor import execute_plan


@dataclass
class Task:
    resident: str
    prompt: str
    model: str | None = None


def parse_roadmap(roadmap_path: Path) -> List[str]:
    """Parses the ROADMAP.md file to extract Phase 2.5 priorities."""
    with open(roadmap_path, "r", encoding="utf-8") as f:
        content = f.read()

    phase_2_5_content = content.split("## Phase 2.5: The Fortification Protocol (CURRENT PRIORITY)")
    missions = []
    if len(phase_2_5_content) > 1:
        relevant_content = phase_2_5_content[1]
        next_phase_idx = relevant_content.find("## Phase")
        if next_phase_idx != -1:
            relevant_content = relevant_content[:next_phase_idx]
        if "GeoDataCenter proposal" in relevant_content:
            missions.append("GeoDataCenter €50M proposal")
        if "Portal Oradea MVP" in relevant_content:
            missions.append("Portal Oradea €6K MRR")
    return missions


def break_down_mission(mission: str) -> List[Task]:
    """Breaks down a mission into tasks for each resident."""
    if mission == "GeoDataCenter €50M proposal":
        return [
            Task(
                resident="claude",
                prompt="Draft the strategic narrative for the GeoDataCenter proposal. Use Perplexity to research the EU funding landscape for data centers.",
                model="claude-haiku-4-5",
            ),
            Task(
                resident="openai",
                prompt="Generate the technical section of the GeoDataCenter proposal. Use Data Commons to get statistics for Romania.",
                model="gpt-5",
            ),
        ]
    elif mission == "Portal Oradea €6K MRR":
        return [
            Task(
                resident="gemini",
                prompt="Deploy the infrastructure plan for the Portal Oradea MVP. Use Wolfram Alpha to calculate the costs.",
                model="gemini-2.5-pro",
            ),
            Task(
                resident="groq",
                prompt="Generate a quick executive summary for the Portal Oradea pitch deck.",
                model="llama-3.1-8b-instant",
            ),
        ]
    return []


def main():
    """Main autonomous loop."""
    paths, keys = load_configuration()
    roadmap_path = Path("/srv/janus/01_STRATEGY/ROADMAP.md")
    missions = parse_roadmap(roadmap_path)
    delegation_log_path = paths.log_dir / "autonomous_delegations.jsonl"

    for mission in missions:
        tasks = break_down_mission(mission)
        for task in tasks:
            plan = DelegationPlan(
                mode="keyword",
                target=task.resident,
                query=task.prompt,
                model=task.model,
            )
            response = execute_plan(plan, paths, keys)
            with open(delegation_log_path, "a", encoding="utf-8") as f:
                log_entry = {
                    "mission": mission,
                    "task": task.__dict__,
                    "response": response,
                }
                f.write(json.dumps(log_entry) + "\n")


if __name__ == "__main__":
    main()
