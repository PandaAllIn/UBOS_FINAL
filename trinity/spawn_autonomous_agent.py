#!/usr/bin/env python3
"""
AUTONOMOUS AGENT SPAWNER
Spawns Haiku sub-agents with full tool/oracle/CLI access.

Integration: Uses Claude Code Task tool to spawn agents
Coordination: COMMS_HUB for Trinity communication
Cost Strategy: Haiku 4.5 (4x cheaper than Sonnet)
"""

import json
import subprocess
import sys
from datetime import datetime, UTC
from pathlib import Path
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict
import logging

# Setup logging
LOG_DIR = Path("/srv/janus/logs")
LOG_DIR.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("agent_spawner")


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
    priority: str  # "urgent", "high", "normal", "low"
    timeout_seconds: Optional[int] = None


class AgentSpawner:
    """
    Spawns and manages autonomous Haiku agents.

    Uses Claude Code's Task tool for agent spawning.
    Coordinates via COMMS_HUB for Trinity integration.
    """

    def __init__(self, log_path: Optional[Path] = None):
        self.log_path = log_path or LOG_DIR / "agent_spawner.jsonl"
        self.active_agents: Dict[str, Dict] = {}

    def spawn_agent(self, config: AgentSpawnConfig) -> Dict:
        """
        Spawn a single autonomous agent.

        Args:
            config: Agent configuration

        Returns:
            Dict with agent info and status
        """
        logger.info(f"Spawning agent: {config.agent_id}")

        # Log spawn event
        self._log_event({
            "event": "agent_spawn_initiated",
            "agent_id": config.agent_id,
            "model": config.model,
            "role": config.role,
            "timestamp": datetime.now(UTC).isoformat()
        })

        # Build agent prompt with full context
        agent_prompt = self._build_agent_prompt(config)

        # Build capability instructions
        capability_instructions = self._build_capability_instructions(config)

        # Complete prompt
        full_prompt = f"""{agent_prompt}

{capability_instructions}

**YOUR MISSION:**
{config.mission}

**GUIDELINES:**
- Use the tools/oracles/CLIs available to you
- Log all significant actions
- Report findings via COMMS_HUB when complete
- Stay within {config.max_tokens} tokens
- Priority level: {config.priority}

Begin your mission now.
"""

        # Prepare agent metadata
        agent_info = {
            "agent_id": config.agent_id,
            "model": config.model,
            "role": config.role,
            "spawned_at": datetime.now(UTC).isoformat(),
            "status": "running",
            "prompt_length": len(full_prompt),
            "config": asdict(config)
        }

        # Store active agent
        self.active_agents[config.agent_id] = agent_info

        # Log spawn success
        self._log_event({
            "event": "agent_spawned",
            "agent_id": config.agent_id,
            "status": "running",
            "timestamp": datetime.now(UTC).isoformat()
        })

        # Return agent info with prompt (caller uses Task tool to actually spawn)
        agent_info["prompt"] = full_prompt
        return agent_info

    def spawn_multiple(self, configs: List[AgentSpawnConfig]) -> List[Dict]:
        """
        Spawn multiple agents in parallel.

        Args:
            configs: List of agent configurations

        Returns:
            List of agent info dicts
        """
        logger.info(f"Spawning {len(configs)} agents in parallel")

        agents = []
        for config in configs:
            agent_info = self.spawn_agent(config)
            agents.append(agent_info)

        return agents

    def _build_agent_prompt(self, config: AgentSpawnConfig) -> str:
        """Build agent system prompt with identity and context"""

        # Load context files
        context_content = []
        for file_path in config.context_files:
            try:
                with open(file_path) as f:
                    context_content.append(f"## Context from {file_path}\\n{f.read()}")
            except Exception as e:
                logger.warning(f"Could not load context file {file_path}: {e}")

        context_section = "\\n\\n".join(context_content) if context_content else "No context files loaded."

        prompt = f"""You are an autonomous Haiku agent (Claude Haiku 4.5).

**IDENTITY:**
- Agent ID: {config.agent_id}
- Role: {config.role}
- Model: {config.model}
- Priority: {config.priority}

**CONTEXT:**
{context_section}
"""
        return prompt

    def _build_capability_instructions(self, config: AgentSpawnConfig) -> str:
        """Build instructions for available tools/oracles/CLIs"""

        instructions = ["**CAPABILITIES AVAILABLE TO YOU:**"]

        # Oracles
        if config.oracles_enabled:
            instructions.append(f"\\n**Oracles:** {', '.join(config.oracles_enabled)}")
            for oracle in config.oracles_enabled:
                if oracle == "wolfram_alpha":
                    instructions.append("  - Wolfram: Use for math, computation, chemistry")
                elif oracle == "perplexity":
                    instructions.append("  - Perplexity: Use for research, papers, citations")
                elif oracle == "data_commons":
                    instructions.append("  - DataCommons: Use for statistics, economics")
                elif oracle == "groq":
                    instructions.append("  - Groq: Use for fast thinking, quick analysis")

        # CLIs
        if config.clis_enabled:
            instructions.append(f"\\n**CLIs:** {', '.join(config.clis_enabled)}")
            for cli in config.clis_enabled:
                if cli == "gemini":
                    instructions.append("  - Gemini: Use `gemini 'your prompt'` for real-time search/analysis")
                elif cli == "codex":
                    instructions.append("  - Codex: Use for code generation tasks")

        # Tools
        if config.tools_enabled:
            instructions.append(f"\\n**Tools:** {', '.join(config.tools_enabled)}")
            for tool in config.tools_enabled:
                if tool == "narrative_query":
                    instructions.append("  - Narrative Query: python3 /srv/janus/02_FORGE/scripts/narrative_query_tool.py --query 'term'")
                elif tool == "comms_hub":
                    instructions.append("  - COMMS_HUB: Write JSON to /srv/janus/03_OPERATIONS/COMMS_HUB/[recipient]/inbox/")

        # Skills
        if config.skills_enabled:
            instructions.append(f"\\n**Skills:** {', '.join(config.skills_enabled)}")
            instructions.append("  - Load skill SKILL.md files for detailed instructions")

        return "\\n".join(instructions)

    def _log_event(self, event: Dict):
        """Log event to JSONL file"""
        try:
            with open(self.log_path, 'a') as f:
                f.write(json.dumps(event) + '\\n')
        except Exception as e:
            logger.error(f"Failed to log event: {e}")

    def get_agent_status(self, agent_id: str) -> Optional[Dict]:
        """Get status of an active agent"""
        return self.active_agents.get(agent_id)

    def list_active_agents(self) -> List[Dict]:
        """List all active agents"""
        return list(self.active_agents.values())


def main():
    """CLI interface for spawning agents"""
    import argparse

    parser = argparse.ArgumentParser(description="Spawn autonomous Haiku agents")
    parser.add_argument("--agent-type", required=True, help="Agent type (e.g., malaga_embassy_monitor)")
    parser.add_argument("--model", default="haiku-4.5", help="Model to use")
    parser.add_argument("--mission", required=True, help="Agent mission")
    parser.add_argument("--log", default=None, help="Log file path")

    args = parser.parse_args()

    # Create spawner
    spawner = AgentSpawner(log_path=Path(args.log) if args.log else None)

    # Create config
    config = AgentSpawnConfig(
        agent_id=f"{args.agent_type}_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
        model=args.model,
        role=args.agent_type,
        mission=args.mission,
        context_files=[],  # Can be extended
        oracles_enabled=["groq", "perplexity"],  # Default set
        clis_enabled=["gemini"],
        tools_enabled=["narrative_query"],
        skills_enabled=[],
        max_tokens=30000,
        priority="normal"
    )

    # Spawn agent
    agent_info = spawner.spawn_agent(config)

    print(json.dumps(agent_info, indent=2))
    print(f"\\n✅ Agent {agent_info['agent_id']} ready to spawn")
    print(f"\\n📝 Use Claude Code Task tool with this prompt:\\n")
    print(agent_info['prompt'][:500] + "..." if len(agent_info['prompt']) > 500 else agent_info['prompt'])


if __name__ == "__main__":
    main()
