# Trinity Autonomous Orchestration - Quick Start Guide

**Version:** 1.0
**Date:** 2025-11-06
**Status:** ✅ Production Ready

---

## 🚀 5-Minute Start

### 1. Test Everything
```bash
cd /srv/janus/trinity
./trinity_launcher.sh test-all
```

### 2. Run Mallorca Monitor
```bash
./trinity_launcher.sh mallorca
# Check logs: cat /srv/janus/logs/mallorca_checks.log
```

### 3. Analyze a Task
```bash
./trinity_launcher.sh orchestrate "Research quantum computing applications in drug discovery"
```

---

## 📚 Main Commands

| Command | Purpose | Example |
|---------|---------|---------|
| `orchestrate` | Analyze prompt, recommend agents/tools | `./trinity_launcher.sh orchestrate "your task"` |
| `mallorca` | Run Xylella project monitor | `./trinity_launcher.sh mallorca` |
| `spawn` | Generate agent configuration | `./trinity_launcher.sh spawn` |
| `session-close` | Analyze and close session | `./trinity_launcher.sh session-close "summary"` |
| `status` | System health check | `./trinity_launcher.sh status` |
| `comms` | Check COMMS_HUB messages | `./trinity_launcher.sh comms` |

---

## 🎯 Common Workflows

### Research Task with Auto-Orchestration
```bash
# 1. Analyze the task
./trinity_launcher.sh orchestrate "Find latest papers on CRISPR gene editing"

# 2. Review recommendations (agents, tools, oracles)

# 3. Use recommended CLI directly
gemini "Latest CRISPR gene editing research papers 2024-2025"
```

### Deploy Mallorca Monitoring
```bash
# 1. Test manually
./trinity_launcher.sh mallorca

# 2. Review output
cat /srv/janus/logs/mallorca_checks.log

# 3. Install cron job (for hourly checks during Dec-Jan)
cat cron_templates.sh
# Copy the hourly cron line to: crontab -e
```

### Close a Session
```bash
./trinity_launcher.sh session-close "Built Trinity orchestration system with auto-orchestration, agent spawner, and Mallorca monitor"
# This updates claude.md, gemini.md, codex.md and creates git commit
```

---

## 🔧 Individual Tools

### Auto-Orchestration (Direct)
```bash
python3 auto_orchestration.py "Implement user authentication with OAuth2"
```

Output:
- Task type
- Complexity
- Recommended agents
- Required tools/oracles
- Cost estimate

### Agent Spawner (Direct)
```bash
python3 spawn_autonomous_agent.py
```

Generates complete agent configuration with all capabilities.

### Session Closer (Direct)
```bash
python3 skills/session_closer/run.py "Today we built the orchestration system"
```

Updates context files and creates git commit.

---

## 🏝️ Mallorca Xylella Monitor

### What it monitors:
1. **Stream 1:** Stage 1 evaluation results (PROJECT 101157977)
2. **Stream 2:** Competing research (phosphate starvation approaches)
3. **Stream 3:** Market demand (Xylella outbreak economics)

### Critical Window:
**December 2025 - January 2026:** HOURLY checks required!

### Latest Test Results (2025-11-06):
- ✅ Results expected December 2025
- ✅ **NO competing phosphate research found** (EXCELLENT!)
- ✅ Market demand €5.5B+ annually

### Emergency Alert Setup:
```bash
# Add to check_mallorca_now.sh to send alerts
if grep -q "PASS" /srv/janus/logs/mallorca_checks.log; then
  # Send email/notification
  echo "🚨 Stage 1 PASSED! Start Stage 2 prep!" | mail -s "Mallorca Alert" you@example.com
fi
```

---

## 🔗 Trinity Coordination

### COMMS_HUB Messages
```bash
# Check inbox
ls /srv/janus/03_OPERATIONS/COMMS_HUB/claude/inbox/

# Check outbox
ls /srv/janus/03_OPERATIONS/COMMS_HUB/claude/outbox/

# Send message to Gemini
cat > /srv/janus/03_OPERATIONS/COMMS_HUB/gemini/inbox/task_$(date +%s).json << 'EOF'
{
  "from": "claude",
  "to": "gemini",
  "task": "Design error handling for agent spawner",
  "priority": "medium"
}
EOF
```

### Direct CLI Use
```bash
# Gemini for research/design
gemini "Design a caching strategy for agent configurations"

# Groq for fast inference
groq "Summarize this text: [...]"

# Narrative Query for code understanding
narrative-query "How does the orchestration system work?"
```

---

## 📊 Logs and Monitoring

All logs in: `/srv/janus/logs/`

- `mallorca_checks.log` - Xylella monitor results
- `mallorca_monitor.jsonl` - Agent spawn events
- `auto_orchestration.log` - Task analysis history
- `session_closer.log` - Session summaries

**View logs:**
```bash
# Latest Mallorca checks
tail -100 /srv/janus/logs/mallorca_checks.log

# Watch live
tail -f /srv/janus/logs/mallorca_checks.log
```

---

## 🎓 Advanced: Meta-Building

Use Trinity vessels to help build Trinity itself!

```bash
# Ask Gemini to design a feature
gemini "Design a critic agent system that reviews code quality and suggests improvements. Return as Python class structure."

# Use output to implement
# This is how we built the session closer!
```

---

## 🆘 Troubleshooting

### "Command not found"
```bash
chmod +x trinity_launcher.sh
chmod +x check_mallorca_now.sh
chmod +x skills/session_closer/run.py
```

### Gemini API errors
The `Error generating JSON content` messages are **HARMLESS**. Gemini still returns excellent results in text mode.

### Auto-orchestration not analyzing
```bash
# Check Python is available
python3 --version

# Run with debug
python3 -v auto_orchestration.py "test prompt"
```

---

## 📦 Files Overview

```
/srv/janus/trinity/
├── trinity_launcher.sh          # Main unified launcher
├── auto_orchestration.py        # Task analyzer
├── spawn_autonomous_agent.py    # Agent config generator
├── check_mallorca_now.sh        # Xylella monitor
├── AGENT_CAPABILITY_REGISTRY.json  # All tools/oracles
├── agents/
│   ├── mallorca_embassy_autonomous_agent.md
│   └── malaga_embassy_autonomous_agent.md
├── skills/
│   └── session_closer/
│       ├── SKILL.md
│       ├── config.json
│       └── run.py
└── designs/
    ├── prompt_analysis_schema.json
    ├── session_closer_algorithm.py
    └── agent_spawner_architecture.txt
```

---

## ✅ System Status

Run anytime:
```bash
./trinity_launcher.sh status
```

---

## 🚀 Next Steps

1. **Deploy Mallorca monitoring:** Add cron job for hourly checks
2. **Test workflows:** Try orchestrating different task types
3. **Integrate with projects:** Use auto-orchestration for daily tasks
4. **Expand monitoring:** Add more embassy agents as needed

---

**Documentation:** See `FINAL_DEPLOYMENT_STATUS.md` for complete system overview

**Support:** Check `/srv/janus/trinity/` for all documentation and logs
