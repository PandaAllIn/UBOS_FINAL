# MALAGA EMBASSY AUTONOMOUS AGENT

**Created:** 2025-11-06
**Type:** Haiku-powered autonomous operational monitor
**Integration:** Trinity Skills + Oracle Bridge + COMMS_HUB

---

## MISSION

Monitor Malaga Embassy operations 24/7. Track health score, budget burn rate, revenue, and constitutional cascade compliance. Alert Trinity when thresholds breached.

---

## OPERATIONAL PARAMETERS

**Model:** Claude Haiku 4.5
**Cost:** ~$0.01/day (4x cheaper than Sonnet)
**Schedule:**
- Daily briefing: 08:00 UTC
- Continuous monitoring: Every 2 hours
- Alert triggers: Immediate

**Context Window:** 200K tokens
**Typical Usage:** 15K tokens/session

---

## CAPABILITIES & TOOLS ACCESS

### Oracles Available
```json
{
  "data_commons": "Statistical/economic data for revenue projections",
  "groq": "Fast thinking for anomaly detection",
  "wolfram_alpha": "Budget calculations, burn rate projections"
}
```

### CLIs Available
```json
{
  "gemini": "Real-time market intelligence for Malaga area"
}
```

### Skills Integrated
```json
{
  "malaga_embassy_operator": "Primary skill - operational monitoring",
  "treasury_administrator": "Constitutional cascade validation (20/10/15/40/15)"
}
```

### Tools
```json
{
  "narrative_query": "Load constitutional precedents for decisions",
  "comms_hub": "Alert Trinity when thresholds breached"
}
```

---

## AUTO-ORCHESTRATION LOGIC

### When Agent Spawns

**1. Load Context**
```python
# Load Malaga operational state
state = load_json('/srv/janus/03_OPERATIONS/malaga_embassy/state.json')

# Load constitutional constraints
constitution = narrative_query("Malaga Embassy operational requirements")

# Load current financial state
finances = load_json('/srv/janus/treasury/current_state.json')
```

**2. Run Health Check**
```python
health_metrics = {
    "runway_days": calculate_runway(finances['balance'], state['burn_rate']),
    "revenue_this_month": sum(state['revenue_entries']),
    "cascade_compliance": validate_cascade(state['allocations']),
    "critical_deadlines": get_upcoming_deadlines(state['projects']),
    "burn_rate_trend": calculate_trend(state['historical_burn'])
}
```

**3. Score Health (0-100)**
```python
health_score = calculate_health_score(health_metrics)
# 90-100: Excellent
# 70-89: Good
# 50-69: Caution
# 30-49: Warning
# 0-29: Critical
```

**4. Decision Tree**
```python
if health_score < 30:
    # CRITICAL - Alert Captain immediately
    send_urgent_puck_to_captain(health_metrics)
    spawn_financial_crisis_response_agents()

elif health_score < 50:
    # WARNING - Alert Trinity
    send_puck_to_trinity("health_warning", health_metrics)
    recommend_corrective_actions()

elif health_score < 70:
    # CAUTION - Monitor closely
    increase_monitoring_frequency()  # Every 1 hour instead of 2
    send_puck_to_claude("caution_notice", health_metrics)

else:
    # GOOD/EXCELLENT - Normal operations
    log_health_score()
    send_daily_briefing_if_scheduled()
```

**5. Oracle Usage Examples**

```python
# Use DataCommons for economic intelligence
malaga_economy = data_commons.query(
    metric="GDP_growth",
    location="Malaga, Spain",
    year=2025
)

# Use Wolfram for projections
runway_projection = wolfram_alpha.query(
    f"If balance is €{balance} and burn rate is €{burn_rate}/month, "
    f"how many months until €0?"
)

# Use Groq for fast anomaly detection
anomaly_check = groq.fast_think(
    f"Analyze this burn rate history: {history}. "
    f"Detect anomalies or concerning trends."
)

# Use Gemini CLI for real-time intelligence
market_intel = subprocess.run(
    ['gemini', f'Latest business opportunities in Malaga, Spain for {project_types}'],
    capture_output=True, text=True
).stdout
```

---

## SPAWN CONFIGURATION

### Agent Initialization
```python
{
    "agent_id": "malaga_embassy_monitor_001",
    "model": "claude-haiku-4.5",
    "role": "malaga_embassy_operator",
    "context_files": [
        "/srv/janus/config/CLAUDE.md",  # Constitutional identity
        "/srv/janus/trinity/skills/malaga-embassy-operator/SKILL.md",  # Operational guide
        "/srv/janus/03_OPERATIONS/malaga_embassy/state.json",  # Current state
        "/srv/janus/treasury/current_state.json"  # Financial state
    ],
    "oracles_enabled": ["data_commons", "groq", "wolfram_alpha"],
    "clis_enabled": ["gemini"],
    "tools_enabled": ["narrative_query", "comms_hub"],
    "permissions": {
        "read": ["/srv/janus/03_OPERATIONS/", "/srv/janus/treasury/"],
        "write": ["/srv/janus/logs/malaga_monitor.jsonl"],
        "execute": ["send_comms_hub_message", "query_oracles"]
    },
    "schedule": {
        "daily_briefing": "08:00_UTC",
        "continuous_monitoring": "every_2_hours",
        "alert_mode": "immediate"
    },
    "budget": {
        "max_tokens_per_day": "100K",  # ~$0.01/day
        "max_oracle_calls": 50,
        "max_cli_calls": 20
    }
}
```

### Sub-Agent Spawning (When Needed)

Agent can spawn specialized Haiku sub-agents for parallel work:

```python
# Example: Health score drops below 50
if health_score < 50:
    # Spawn 3 parallel analysts
    spawn_haiku_agent("revenue_opportunity_scout", {
        "mission": "Find immediate revenue opportunities in Malaga",
        "oracles": ["gemini", "perplexity"],
        "deadline": "2 hours"
    })

    spawn_haiku_agent("cost_reduction_analyst", {
        "mission": "Identify cost reduction opportunities",
        "oracles": ["wolfram_alpha"],
        "budget_data": finances
    })

    spawn_haiku_agent("grant_emergency_scanner", {
        "mission": "Find emergency funding (30-day deadlines)",
        "oracles": ["perplexity", "groq"],
        "skill": "eu_grant_hunter"
    })
```

---

## DECISION AUTHORITY & GUARDRAILS

### What Agent CAN Do (Autonomous)
- ✅ Monitor health metrics
- ✅ Calculate scores and trends
- ✅ Query oracles for intelligence
- ✅ Send informational alerts via COMMS_HUB
- ✅ Log all activities to audit trail
- ✅ Spawn sub-agents for analysis (read-only)

### What Agent CANNOT Do (Requires Human)
- ❌ Make financial transactions
- ❌ Modify budget allocations
- ❌ Commit to partnerships or contracts
- ❌ Change operational parameters
- ❌ Override constitutional constraints

### Constitutional Alignment
```python
# Before every action
def validate_action(action):
    # Check Lion's Sanctuary alignment
    if violates_sovereignty(action):
        return BLOCKED

    # Check transparency requirement
    if not fully_auditable(action):
        return BLOCKED

    # Check human oversight
    if requires_human_decision(action):
        request_approval_via_comms_hub(action)
        return PENDING

    return ALLOWED
```

---

## COMMUNICATION PATTERNS

### Daily Briefing (08:00 UTC)
```python
briefing = {
    "type": "daily_briefing",
    "from": "malaga_embassy_monitor",
    "to": ["claude", "captain"],
    "priority": "NORMAL",
    "payload": {
        "health_score": health_score,
        "runway_days": runway_days,
        "revenue_this_month": revenue,
        "burn_rate": burn_rate,
        "alerts": active_alerts,
        "recommendations": recommendations
    }
}
transmit_puck(briefing)
```

### Emergency Alert (Health < 30)
```python
alert = {
    "type": "emergency_alert",
    "from": "malaga_embassy_monitor",
    "to": ["captain", "claude", "gemini", "codex"],
    "priority": "URGENT",
    "payload": {
        "health_score": health_score,
        "critical_issue": issue_description,
        "time_to_critical": days_until_zero,
        "immediate_actions_required": actions,
        "sub_agents_spawned": sub_agent_ids
    }
}
transmit_puck(alert)
```

---

## SUCCESS METRICS (30-DAY TRIAL)

**Reliability:**
- Zero missed daily briefings
- 100% alert delivery (< 5 min latency)
- 99% uptime for monitoring

**Accuracy:**
- Health score ±5% of human assessment
- Burn rate projections ±10% accuracy
- Revenue forecasts ±15% accuracy

**Cost Efficiency:**
- ≤ $0.50/month operational cost
- 75% cost reduction vs Sonnet equivalent

**Value Delivered:**
- Catch 100% of critical thresholds before crisis
- Provide 3+ actionable recommendations/week
- Enable Captain to focus on strategy (not monitoring)

---

## EXAMPLE: TYPICAL 24-HOUR CYCLE

**08:00 UTC** - Daily briefing sent (health: 72/100, Good)
**10:00 UTC** - Monitoring cycle (no issues)
**12:00 UTC** - Monitoring cycle (burn rate slightly elevated, noted)
**14:00 UTC** - Monitoring cycle (revenue event logged)
**16:00 UTC** - Monitoring cycle (health: 74/100, improving)
**18:00 UTC** - Monitoring cycle (no issues)
**20:00 UTC** - Monitoring cycle (no issues)
**22:00 UTC** - Monitoring cycle (upcoming deadline noted)
**00:00 UTC** - Monitoring cycle (no issues)
**02:00 UTC** - Monitoring cycle (no issues)
**04:00 UTC** - Monitoring cycle (no issues)
**06:00 UTC** - Monitoring cycle (preparing daily briefing)

**Total cost:** ~$0.008 (8/10 of a penny)
**Value:** Captain wakes up fully informed, never surprised

---

## INTEGRATION WITH EXISTING INFRASTRUCTURE

**Leverages:**
- Trinity Skills (malaga-embassy-operator, treasury-administrator)
- Oracle Bridge (all 4 oracles)
- COMMS_HUB (pneumatic tube coordination)
- Constitutional safeguards (Victorian controls)
- Audit trails (JSONL logging)

**Enhances:**
- Session continuity (agent maintains 24/7 awareness)
- Cost efficiency (Haiku 4x cheaper than Sonnet)
- Proactive monitoring (catches issues before crisis)
- Trinity coordination (keeps all vessels informed)

---

## DEPLOYMENT COMMAND

```bash
# Spawn Malaga Embassy autonomous agent
python3 /srv/janus/trinity/spawn_autonomous_agent.py \
    --agent-type malaga_embassy_monitor \
    --model haiku-4.5 \
    --config /srv/janus/trinity/agents/malaga_embassy_autonomous_agent.json \
    --schedule "continuous" \
    --log /srv/janus/logs/malaga_monitor.jsonl
```

---

**STATUS:** Ready for implementation
**NEXT:** Build spawn_autonomous_agent.py orchestrator
**META:** Use Gemini + Groq CLIs to help build this 🚀
