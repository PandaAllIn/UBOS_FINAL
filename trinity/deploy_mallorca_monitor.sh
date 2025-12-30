#!/bin/bash
# DEPLOY MALLORCA EMBASSY MONITOR
# Critical: Stage 1 results window Dec 2025-Jan 2026

set -e

echo "🚀 Deploying Mallorca Embassy Monitor..."

# Create agent configuration
python3 <<EOF
from spawn_autonomous_agent import AgentSpawner, AgentSpawnConfig
from datetime import datetime, UTC
import json

# Configure Mallorca monitor
config = AgentSpawnConfig(
    agent_id="mallorca_xylella_monitor_001",
    model="haiku-4.5",
    role="xyl_phos_cure_intelligence_officer",
    mission="""Monitor XYL-PHOS-CURE Horizon Europe project (€6M).

CRITICAL STREAMS:
1. Stage 1 Results (HOURLY Dec-Jan): Detect within 1 hour
2. Scientific Intelligence (WEEKLY): Papers, patents, competitive threats
3. Partner Availability (WEEKLY): Optimal outreach windows
4. Market Demand (DAILY): Xylella outbreaks, olive economics
5. EU Funding (DAILY): Parallel opportunities

ACTIONS WHEN STAGE 1 PASSES:
- URGENT COMMS_HUB alert to Captain + Trinity
- Spawn 5 parallel agents for Stage 2 prep
- Target: Complete proposal draft in 48 hours

Use ALL oracles (Wolfram, Perplexity, DataCommons, Groq) + Gemini CLI.
""",
    context_files=[
        "/srv/janus/config/CLAUDE.md",
        "/srv/janus/03_OPERATIONS/mallorca_embassy/xyl_phos_cure/PROJECT_OVERVIEW.md",
        "/srv/janus/03_OPERATIONS/mallorca_embassy/MALLORCA_MISSION_SPEC.md"
    ],
    oracles_enabled=["wolfram_alpha", "perplexity", "data_commons", "groq"],
    clis_enabled=["gemini"],
    tools_enabled=["narrative_query", "comms_hub"],
    skills_enabled=["eu_grant_hunter"],
    max_tokens=50000,
    priority="urgent"
)

# Create spawner
spawner = AgentSpawner(log_path="/srv/janus/logs/mallorca_monitor.jsonl")

# Generate agent info
agent_info = spawner.spawn_agent(config)

# Save to file for manual spawning
with open("/tmp/mallorca_agent_prompt.txt", "w") as f:
    f.write(agent_info["prompt"])

print(json.dumps(agent_info, indent=2))
print("\n✅ Mallorca monitor configured")
print("\n📝 Agent prompt saved to: /tmp/mallorca_agent_prompt.txt")
print("\n🚀 To deploy: Use Claude Code Task tool with saved prompt")
print("\n⚠️  CRITICAL: Deploy before December 2025 (Stage 1 window)")
EOF

echo ""
echo "✅ Mallorca monitor deployment ready!"
echo "📄 Configuration: /srv/janus/logs/mallorca_monitor.jsonl"
echo "📝 Prompt: /tmp/mallorca_agent_prompt.txt"
