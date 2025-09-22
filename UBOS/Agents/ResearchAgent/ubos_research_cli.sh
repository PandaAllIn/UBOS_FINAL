#!/bin/bash
# UBOS Research Agent CLI Wrapper
# Makes the agent easily accessible from anywhere in the system

AGENT_DIR="/Users/apple/Desktop/UBOS_FINAL/UBOS/Agents/ResearchAgent"
AGENT_SCRIPT="$AGENT_DIR/ubos_research_agent.py"
RESEARCH_CLI="$AGENT_DIR/research_cli.py"

# Check if Python script exists
if [ ! -f "$AGENT_SCRIPT" ]; then
    echo "❌ UBOS Research Agent not found at $AGENT_SCRIPT"
    exit 1
fi

# If first argument is a management command, use research_cli.py
if [[ "$1" == "list" || "$1" == "search" || "$1" == "show" || "$1" == "stats" || "$1" == "export" ]]; then
    python3 "$RESEARCH_CLI" "$@"
else
    # Otherwise use the main research agent
    python3 "$AGENT_SCRIPT" "$@"
fi