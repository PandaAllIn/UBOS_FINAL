#!/bin/bash
# Trinity Autonomous Orchestration - Unified Launcher
# Usage: ./trinity_launcher.sh <command> [args]

TRINITY_HOME="/srv/janus/trinity"
LOG_DIR="/srv/janus/logs"

cd "$TRINITY_HOME" || exit 1

case "$1" in
  orchestrate)
    # Analyze prompt and recommend agents/tools
    echo "🎯 Trinity Auto-Orchestration"
    python3 auto_orchestration.py "$2"
    ;;

  spawn)
    # Generate agent configuration
    echo "🚀 Spawning Agent Configuration"
    python3 spawn_autonomous_agent.py
    ;;

  mallorca)
    # Run Mallorca monitor
    echo "🏝️ Mallorca Xylella Monitor"
    ./check_mallorca_now.sh
    ;;

  session-close)
    # Close session with analysis
    echo "📝 Session Closer"
    python3 skills/session_closer/run.py "$2"
    ;;

  test-all)
    # Run all tests
    echo "🧪 Testing All Systems..."
    echo ""
    echo "1️⃣ Testing Auto-Orchestration..."
    python3 auto_orchestration.py "Research Xylella fastidiosa cure approaches"
    echo ""
    echo "2️⃣ Testing Mallorca Monitor..."
    ./check_mallorca_now.sh | head -20
    echo ""
    echo "3️⃣ Testing Agent Spawner..."
    python3 spawn_autonomous_agent.py | head -30
    echo ""
    echo "✅ All tests complete"
    ;;

  comms)
    # Check COMMS_HUB
    echo "📬 COMMS_HUB Status"
    echo "Inbox:"
    ls -lh /srv/janus/03_OPERATIONS/COMMS_HUB/claude/inbox/ 2>/dev/null | tail -5
    echo ""
    echo "Outbox:"
    ls -lh /srv/janus/03_OPERATIONS/COMMS_HUB/claude/outbox/ 2>/dev/null | tail -5
    ;;

  status)
    # Show system status
    echo "🔍 Trinity System Status"
    echo ""
    echo "✅ Auto-Orchestration: $([ -f auto_orchestration.py ] && echo 'READY' || echo 'MISSING')"
    echo "✅ Agent Spawner: $([ -f spawn_autonomous_agent.py ] && echo 'READY' || echo 'MISSING')"
    echo "✅ Mallorca Monitor: $([ -f check_mallorca_now.sh ] && echo 'READY' || echo 'MISSING')"
    echo "✅ Session Closer: $([ -f skills/session_closer/run.py ] && echo 'READY' || echo 'MISSING')"
    echo "✅ Capability Registry: $([ -f AGENT_CAPABILITY_REGISTRY.json ] && echo 'READY' || echo 'MISSING')"
    echo ""
    echo "📊 Recent Logs:"
    ls -lht "$LOG_DIR"/*.log 2>/dev/null | head -5
    ;;

  help|*)
    echo "Trinity Autonomous Orchestration Launcher"
    echo ""
    echo "Usage: ./trinity_launcher.sh <command> [args]"
    echo ""
    echo "Commands:"
    echo "  orchestrate <prompt>  - Analyze prompt and recommend agents/tools"
    echo "  spawn                 - Generate agent configuration"
    echo "  mallorca              - Run Mallorca Xylella monitor"
    echo "  session-close <text>  - Close session with analysis"
    echo "  test-all              - Test all systems"
    echo "  comms                 - Check COMMS_HUB status"
    echo "  status                - Show system status"
    echo "  help                  - Show this help"
    echo ""
    echo "Examples:"
    echo "  ./trinity_launcher.sh orchestrate 'Research quantum computing papers'"
    echo "  ./trinity_launcher.sh mallorca"
    echo "  ./trinity_launcher.sh status"
    ;;
esac
