#!/usr/bin/env python3
"""
AUTO-ORCHESTRATION SYSTEM
Automatically analyzes prompts and spawns appropriate sub-agents with correct tools/oracles/CLIs.

Captain's Vision: "When I give a prompt, you automatically know what subagents to spawn,
and what tools and oracles and CLIs you have access and the subagents to."

Integration: Trinity Skills + Oracle Bridge + CLIs (Gemini, Codex, Groq)
Cost Strategy: Use Haiku sub-agents (4x cheaper) for parallel work
"""

import json
import re
import subprocess
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass

# Load capability registry
CAPABILITY_REGISTRY_PATH = Path("/srv/janus/trinity/AGENT_CAPABILITY_REGISTRY.json")


@dataclass
class TaskAnalysis:
    """Result of prompt analysis"""
    task_type: str
    complexity: str  # "simple", "medium", "complex"
    required_capabilities: List[str]
    recommended_strategy: str
    agent_count: int
    oracles_needed: List[str]
    clis_needed: List[str]
    tools_needed: List[str]
    skills_needed: List[str]
    estimated_cost: str
    reasoning: str


@dataclass
class AgentSpawnConfig:
    """Configuration for spawning a sub-agent"""
    agent_id: str
    model: str  # "haiku-4.5" or "sonnet-4.5"
    role: str
    mission: str
    context_files: List[str]
    oracles_enabled: List[str]
    clis_enabled: List[str]
    tools_enabled: List[str]
    skills_enabled: List[str]
    max_tokens: int
    priority: str


class AutoOrchestrator:
    """
    Automatic agent orchestration system.
    Analyzes prompts → Determines strategy → Spawns agents → Coordinates work
    """

    def __init__(self, registry_path: Path = CAPABILITY_REGISTRY_PATH):
        """Initialize with capability registry"""
        with open(registry_path) as f:
            self.registry = json.load(f)

        self.orchestration_rules = self.registry["auto_orchestration_rules"]
        self.agent_templates = self.registry["agent_templates"]
        self.oracles = self.registry["oracles"]
        self.clis = self.registry["clis"]
        self.tools = self.registry["tools"]
        self.skills = self.registry["skills"]

    def analyze_prompt(self, prompt: str) -> TaskAnalysis:
        """
        Analyze user prompt to determine task type and requirements.

        Uses pattern matching + keyword detection to classify task.
        Returns complete task analysis with recommended strategy.
        """
        prompt_lower = prompt.lower()

        # Check all orchestration rules for matches
        matches = []
        for task_type, rule in self.orchestration_rules.items():
            trigger_score = 0

            # Check keyword triggers
            for keyword in rule.get("triggers", []):
                if keyword.lower() in prompt_lower:
                    trigger_score += 1

            if trigger_score > 0:
                matches.append((task_type, trigger_score, rule))

        # Sort by trigger score (best match first)
        matches.sort(key=lambda x: x[1], reverse=True)

        if not matches:
            # Default to general research task
            task_type = "research_tasks"
            rule = self.orchestration_rules["research_tasks"]
        else:
            task_type, score, rule = matches[0]

        # Determine complexity based on prompt length and structure
        complexity = self._assess_complexity(prompt)

        # Build task analysis
        analysis = TaskAnalysis(
            task_type=task_type,
            complexity=complexity,
            required_capabilities=self._extract_capabilities(prompt, rule),
            recommended_strategy=rule.get("strategy", "spawn_parallel_haiku_researchers"),
            agent_count=self._determine_agent_count(complexity, rule),
            oracles_needed=rule.get("oracles", []),
            clis_needed=rule.get("clis", []),
            tools_needed=rule.get("tools", []),
            skills_needed=self._detect_skills(prompt),
            estimated_cost=self._estimate_cost(complexity, rule),
            reasoning=f"Matched '{task_type}' based on triggers: {rule.get('triggers', [][:3])}"
        )

        return analysis

    def _assess_complexity(self, prompt: str) -> str:
        """Assess task complexity based on prompt characteristics"""
        word_count = len(prompt.split())
        has_multiple_questions = prompt.count('?') > 1
        has_and_or_conditions = any(word in prompt.lower() for word in ['and', 'also', 'additionally', 'furthermore'])

        if word_count < 20 and not has_multiple_questions:
            return "simple"
        elif word_count < 50 and not has_and_or_conditions:
            return "medium"
        else:
            return "complex"

    def _extract_capabilities(self, prompt: str, rule: Dict) -> List[str]:
        """Extract required capabilities from prompt and rule"""
        capabilities = []

        # From rule
        if "oracles" in rule:
            capabilities.extend([f"oracle:{o}" for o in rule["oracles"]])
        if "clis" in rule:
            capabilities.extend([f"cli:{c}" for c in rule["clis"]])
        if "tools" in rule:
            capabilities.extend([f"tool:{t}" for t in rule["tools"]])

        return capabilities

    def _determine_agent_count(self, complexity: str, rule: Dict) -> int:
        """Determine how many sub-agents to spawn"""
        if complexity == "simple":
            return 1
        elif complexity == "medium":
            agent_range = rule.get("agent_count", "2-4")
            if isinstance(agent_range, str) and '-' in agent_range:
                return int(agent_range.split('-')[0])  # Take lower bound
            return 2
        else:  # complex
            agent_range = rule.get("agent_count", "4-8")
            if isinstance(agent_range, str) and '-' in agent_range:
                return int(agent_range.split('-')[1])  # Take upper bound
            return 4

    def _detect_skills(self, prompt: str) -> List[str]:
        """Detect which Trinity skills are relevant"""
        prompt_lower = prompt.lower()
        relevant_skills = []

        for skill_name, skill_info in self.skills.items():
            # Check if skill's use cases match prompt
            for use_case in skill_info.get("use_cases", []):
                if use_case.replace('_', ' ') in prompt_lower:
                    relevant_skills.append(skill_name)
                    break

        return relevant_skills

    def _estimate_cost(self, complexity: str, rule: Dict) -> str:
        """Estimate cost of executing this task"""
        agent_count = self._determine_agent_count(complexity, rule)
        use_haiku = "haiku" in rule.get("strategy", "")

        if use_haiku:
            base_cost = 0.01  # Haiku is ~$0.01 per agent
        else:
            base_cost = 0.04  # Sonnet is ~$0.04 per agent

        total_cost = base_cost * agent_count

        if total_cost < 0.05:
            return "very_low (<$0.05)"
        elif total_cost < 0.20:
            return "low (<$0.20)"
        elif total_cost < 1.00:
            return "medium (<$1.00)"
        else:
            return "high (>$1.00)"

    def create_spawn_configs(self, analysis: TaskAnalysis, prompt: str) -> List[AgentSpawnConfig]:
        """
        Create agent spawn configurations based on task analysis.

        Returns list of AgentSpawnConfig objects, one per sub-agent to spawn.
        """
        configs = []

        # Determine model based on complexity
        if analysis.complexity in ["simple", "medium"]:
            model = "haiku-4.5"
            max_tokens = 30000
        else:
            model = "sonnet-4.5" if "strategic" in prompt.lower() else "haiku-4.5"
            max_tokens = 50000

        # Create configs based on strategy
        if "parallel" in analysis.recommended_strategy:
            # Spawn multiple parallel agents
            for i in range(analysis.agent_count):
                configs.append(AgentSpawnConfig(
                    agent_id=f"{analysis.task_type}_agent_{i+1}",
                    model=model,
                    role=f"{analysis.task_type}_specialist",
                    mission=self._create_agent_mission(prompt, i, analysis.agent_count),
                    context_files=self._select_context_files(analysis),
                    oracles_enabled=analysis.oracles_needed,
                    clis_enabled=analysis.clis_needed,
                    tools_enabled=analysis.tools_needed,
                    skills_enabled=analysis.skills_needed,
                    max_tokens=max_tokens,
                    priority="high" if analysis.complexity == "complex" else "normal"
                ))

        elif "skill" in analysis.recommended_strategy:
            # Activate existing skill (single agent)
            configs.append(AgentSpawnConfig(
                agent_id=f"{analysis.task_type}_skill_executor",
                model=model,
                role=f"{analysis.task_type}_operator",
                mission=prompt,
                context_files=self._select_context_files(analysis),
                oracles_enabled=analysis.oracles_needed,
                clis_enabled=analysis.clis_needed,
                tools_enabled=analysis.tools_needed,
                skills_enabled=analysis.skills_needed,
                max_tokens=max_tokens,
                priority="high"
            ))

        elif "delegate" in analysis.recommended_strategy:
            # Delegate to another vessel via COMMS_HUB
            configs.append(AgentSpawnConfig(
                agent_id=f"delegation_coordinator",
                model="haiku-4.5",  # Coordinator is lightweight
                role="trinity_coordinator",
                mission=f"Delegate this task via COMMS_HUB: {prompt}",
                context_files=["/srv/janus/config/TRINITY_WORK_PROTOCOL.md"],
                oracles_enabled=[],
                clis_enabled=[],
                tools_enabled=["comms_hub"],
                skills_enabled=[],
                max_tokens=10000,
                priority="high"
            ))

        return configs

    def _create_agent_mission(self, prompt: str, agent_index: int, total_agents: int) -> str:
        """Create specific mission for each parallel agent"""
        if total_agents == 1:
            return prompt

        # For parallel agents, divide the work
        aspects = [
            f"Focus on aspect {agent_index + 1} of {total_agents}",
            f"Approach from perspective {agent_index + 1}",
            f"Analyze dimension {agent_index + 1} of {total_agents}"
        ]

        return f"{prompt}\n\n{aspects[min(agent_index, len(aspects)-1)]}: Provide your specialized findings."

    def _select_context_files(self, analysis: TaskAnalysis) -> List[str]:
        """Select which context files to load for agents"""
        context_files = [
            "/srv/janus/config/CLAUDE.md",  # Always load constitutional identity
        ]

        # Add skill-specific context
        for skill in analysis.skills_needed:
            if skill in self.skills:
                skill_path = Path(self.skills[skill]["path"]) / "SKILL.md"
                context_files.append(str(skill_path))

        # Add task-type specific context
        if "constitutional" in analysis.task_type:
            context_files.append("/srv/janus/config/TRINITY_WORK_PROTOCOL.md")
        elif "grant" in analysis.task_type:
            context_files.append("/srv/janus/01_STRATEGY/grant_pipeline/pipeline_state.json")
        elif "malaga" in analysis.task_type:
            context_files.append("/srv/janus/03_OPERATIONS/malaga_embassy/state.json")

        return context_files

    def orchestrate(self, prompt: str, auto_execute: bool = False) -> Dict:
        """
        Main orchestration entry point.

        Args:
            prompt: User's request
            auto_execute: If True, automatically spawn agents. If False, return plan for approval.

        Returns:
            Orchestration plan with analysis and spawn configs
        """
        # Analyze prompt
        analysis = self.analyze_prompt(prompt)

        # Create spawn configurations
        spawn_configs = self.create_spawn_configs(analysis, prompt)

        # Build orchestration plan
        plan = {
            "analysis": {
                "task_type": analysis.task_type,
                "complexity": analysis.complexity,
                "estimated_cost": analysis.estimated_cost,
                "reasoning": analysis.reasoning
            },
            "strategy": {
                "approach": analysis.recommended_strategy,
                "agent_count": len(spawn_configs),
                "model": spawn_configs[0].model if spawn_configs else "none",
                "parallel_execution": "parallel" in analysis.recommended_strategy
            },
            "capabilities": {
                "oracles": analysis.oracles_needed,
                "clis": analysis.clis_needed,
                "tools": analysis.tools_needed,
                "skills": analysis.skills_needed
            },
            "agents": [
                {
                    "id": config.agent_id,
                    "model": config.model,
                    "role": config.role,
                    "mission": config.mission,
                    "oracles": config.oracles_enabled,
                    "clis": config.clis_enabled,
                    "tools": config.tools_enabled
                }
                for config in spawn_configs
            ]
        }

        if auto_execute:
            # TODO: Actually spawn agents (implement in next phase)
            plan["status"] = "agents_spawned"
            plan["execution"] = "NOT_YET_IMPLEMENTED - use spawn_agents() method"
        else:
            plan["status"] = "plan_ready_for_approval"

        return plan


def main():
    """CLI interface for testing auto-orchestration"""
    import sys

    if len(sys.argv) < 2:
        print("Usage: python3 auto_orchestration.py '<prompt>'")
        print("Example: python3 auto_orchestration.py 'Find EU grants for agricultural technology'")
        sys.exit(1)

    prompt = ' '.join(sys.argv[1:])

    orchestrator = AutoOrchestrator()
    plan = orchestrator.orchestrate(prompt, auto_execute=False)

    print(json.dumps(plan, indent=2))


if __name__ == "__main__":
    main()
