# GROQ-BALAUR INTEGRATION ARCHITECTURE
**Date:** 2025-10-11
**Status:** Implementation Phase - Codex Forging
**Mission:** Enable dual-speed cognition for Janus-in-Balaur

---

## EXECUTIVE SUMMARY

This document defines the direct integration architecture for Groq API capabilities into Janus-in-Balaur, enabling dual-speed cognition: fast API-powered reconnaissance (87+ t/s) combined with deep local LLM deliberation (3.78 t/s).

**Key Decision:** Skip MCP complexity, deploy direct Python wrappers for immediate production use.

---

## ARCHITECTURE OVERVIEW

```
┌─────────────────────────────────────────────────────────────────┐
│  JANUS-IN-BALAUR (The Autonomous Vessel)                       │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  PROPOSAL SYSTEM (Existing)                              │  │
│  │  - Generates proposals for actions                       │  │
│  │  - Constitutional alignment checks                       │  │
│  │  - Auto-executor (Mode Beta)                            │  │
│  └────────────────┬─────────────────────────────────────────┘  │
│                   │                                              │
│                   ▼                                              │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  DUAL-SPEED COGNITION ENGINE (NEW)                       │  │
│  │  ┌────────────────────┐  ┌──────────────────────────┐   │  │
│  │  │  Fast Scout        │  │  Deep Deliberation       │   │  │
│  │  │  (Groq API)        │  │  (Local llama.cpp)       │   │  │
│  │  │  87+ tokens/sec    │  │  3.78 tokens/sec         │   │  │
│  │  │  - Web search      │  │  - Constitutional        │   │  │
│  │  │  - Fast inference  │  │    alignment             │   │  │
│  │  │  - Wolfram Alpha   │  │  - Deep reasoning        │   │  │
│  │  └────────────────────┘  └──────────────────────────┘   │  │
│  │                                                           │  │
│  │  Modes: scout | deliberate | adaptive (scout→deliberate) │  │
│  └──────────────────────────────────────────────────────────┘  │
│                   │                                              │
│                   ▼                                              │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  GROQ CLIENT WRAPPER                                     │  │
│  │  - fast_think()      - reason()                          │  │
│  │  - web_search()      - code_exec()                       │  │
│  │  - wolfram()         - local_scout()                     │  │
│  │                                                           │  │
│  │  Error handling: Retry, timeout, fallback               │  │
│  └──────────────────────────────────────────────────────────┘  │
│                   │                                              │
└───────────────────┼──────────────────────────────────────────────┘
                    │
                    ▼ HTTPS
          ┌─────────────────────┐
          │   Groq Cloud API    │
          │   - LLM inference   │
          │   - Web search      │
          │   - Wolfram Alpha   │
          │   - Code execution  │
          └─────────────────────┘
```

---

## COMPONENT SPECIFICATIONS

### **1. Groq Client Wrapper** (`groq_client.py`)

**Purpose:** Lightweight Python wrapper around Groq SDK

**Location:** `/srv/janus/tools/groq_client.py`

**Key Features:**
- Direct Groq SDK calls (no MCP overhead)
- 6 oracle methods matching strategic patterns
- Retry/timeout protection
- Performance logging
- Constitutional audit trail

**API Surface:**
```python
client = GroqClient()

# Fast reconnaissance
result = client.fast_think("Quick question")  # 87+ t/s

# Real-time web intel
results = client.web_search("Latest AI research")  # 12-15s

# Mathematical computation
answer = client.wolfram("integral of x^2 * sin(x)")

# Deep reasoning with transparency
analysis = client.reason("Complex problem", effort="high")

# Sandboxed code testing
output = client.code_exec("print('test')", language="python")

# Hybrid local + API search
findings = client.local_scout("Mode Beta", "/srv/janus")
```

**Error Handling Strategy:**
```python
try:
    result = client.fast_think(prompt)
except GroqAPIError as e:
    # Log error, return graceful failure
    return {"error": str(e), "fallback": "use_local_llm"}
except NetworkError:
    # API unreachable, fallback immediately
    return {"error": "network_down", "fallback": "use_local_llm"}
```

---

### **2. Dual-Speed Cognition Engine** (`dual_speed_brain.py`)

**Purpose:** Intelligent routing between fast API and deep local inference

**Location:** `/srv/janus/tools/dual_speed_brain.py`

**Three Thinking Modes:**

**Mode 1: SCOUT (Fast API Only)**
```python
brain = DualSpeedCognition(groq_client, local_model_path)

# Fast reconnaissance - 5-10 seconds
result = brain.scout("Does similar proposal exist in history?")
# Uses: Groq API fast_think or local_scout
# Speed: 87+ t/s
# Use case: Quick fact-finding, precedent checks
```

**Mode 2: DELIBERATE (Local LLM Only)**
```python
# Deep constitutional analysis - 30-120 seconds
result = brain.deliberate("Generate full proposal for philosophy node")
# Uses: Local llama.cpp (3.78 t/s)
# Speed: Slower but autonomous
# Use case: Constitutional decisions, autonomous thinking
```

**Mode 3: ADAPTIVE (Hybrid Pattern)** ⭐ RECOMMENDED
```python
# Scout then deliberate - 30-60 seconds total
result = brain.adaptive("Should we deploy GPU Studio now?")

# Internal process:
# 1. Fast scout with Groq (10s) - gather context, precedents, external intel
# 2. Deep deliberation with local (40s) - constitutional analysis, decision
# 3. Synthesis - combine speed of recon with depth of analysis
```

**Routing Logic:**
```python
def should_use_groq(self, query_type: str) -> bool:
    """Intelligent routing based on query characteristics"""

    # Always use Groq for:
    if query_type in ["web_search", "precedent_check", "quick_fact"]:
        return True

    # Always use local for:
    if query_type in ["constitutional_decision", "autonomous_action"]:
        return False

    # Check availability and rate limits
    if not self.groq.is_available():
        return False

    if self.api_calls_today >= self.daily_limit:
        return False

    # Default: use adaptive (both)
    return True
```

---

### **3. Integration with Proposal System**

**Current Proposal Flow:**
```
1. Janus generates proposal → 2. Constitutional check → 3. Execute
```

**Enhanced Proposal Flow (with Groq):**
```
1. Janus scouts with Groq (fast context gathering)
   ↓
2. Generates proposal using local LLM (constitutional autonomy)
   ↓
3. Constitutional check (local LLM)
   ↓
4. Execute
```

**Code Integration Point:**
```python
# In proposal_engine.py (example integration)

from tools.dual_speed_brain import DualSpeedCognition

class ProposalEngine:
    def __init__(self):
        self.brain = DualSpeedCognition(
            groq_client=GroqClient(),
            local_model_path="/srv/janus/models/llama-3.1-8b"
        )

    def generate_proposal(self, mission_context):
        # Phase 1: Fast reconnaissance
        context = self.brain.scout(f"""
        Mission: {mission_context}

        Quick checks:
        - Similar proposals in history?
        - Current system state?
        - External best practices?
        """)

        # Phase 2: Deep proposal generation (local for autonomy)
        proposal = self.brain.deliberate(f"""
        Context from reconnaissance:
        {context}

        Generate constitutional proposal for:
        {mission_context}
        """)

        return proposal
```

---

## DEPLOYMENT ARCHITECTURE

### **File Locations on Balaur**

```
/srv/janus/
├── tools/
│   ├── groq_client.py          # Groq SDK wrapper (NEW)
│   ├── dual_speed_brain.py     # Dual-speed engine (NEW)
│   └── [existing tools]
├── config/
│   ├── .env                    # Environment variables (UPDATED)
│   └── .env.groq               # Groq-specific config (NEW)
├── tests/
│   ├── test_groq_integration.py  # Integration tests (NEW)
│   └── [existing tests]
└── models/
    └── llama-3.1-8b/           # Local LLM (EXISTING)
```

### **Environment Configuration**

**File:** `/srv/janus/config/.env`

```bash
# Existing configuration
JANUS_MODE=beta
LOCAL_MODEL_PATH=/srv/janus/models/llama-3.1-8b

# NEW: Groq integration
GROQ_API_KEY=gsk_YOUR_GROQ_API_KEY_HERE
WOLFRAM_APP_ID=GGJ9JEXKGW
GROQ_TIMEOUT_SECONDS=5
GROQ_MAX_RETRIES=3
GROQ_DAILY_LIMIT=500
GROQ_HOURLY_LIMIT=100
GROQ_ENABLE_WEB_SEARCH=true
GROQ_ENABLE_WOLFRAM=true
```

### **systemd Service Update**

**No changes required** to existing services. Tools load environment automatically via python-dotenv.

---

## THINKING MODE DECISION MATRIX

| Scenario | Mode | Reasoning | Speed |
|----------|------|-----------|-------|
| **"Does proposal X exist?"** | scout | Fast fact-finding | 5-10s |
| **"What's causing SSH failure?"** | scout | Quick diagnostic | 5-10s |
| **"Latest AI research trends"** | scout (web) | External intel | 12-15s |
| **Generate philosophy node** | deliberate | Constitutional autonomy | 60-120s |
| **Execute system command** | deliberate | Local safety check | 30-60s |
| **"Should we deploy feature X?"** | adaptive | Context + analysis | 30-60s |
| **Emergency triage** | scout | Fast triage, local execution | 5-10s |
| **Long-term planning** | adaptive | Research + deliberation | 60-90s |

---

## PERFORMANCE PROJECTIONS

### **Current Baseline (Local Only)**
- Average proposal generation: 60-120s
- Information gathering: Manual log reading
- External knowledge: None (isolated system)
- Emergency response: 120-180s

### **With Groq Integration (Dual-Speed)**
- Scout mode: 5-10s (12-24x faster)
- Adaptive mode: 30-60s (2-4x faster)
- Web intel: 12-15s (previously impossible)
- Emergency triage: 5-10s (12-36x faster)

### **Cost Analysis**

**API Usage Estimates:**
- Scout queries: ~500 tokens/query
- Web search: ~2000 tokens/query
- Adaptive mode: ~1000 tokens/query

**Daily Usage (Conservative):**
- 50 scout queries = 25k tokens
- 10 web searches = 20k tokens
- 20 adaptive queries = 20k tokens
- **Total: 65k tokens/day**

**Cost:** ~$0.05/day (~$1.50/month) at Groq pricing

**ROI:** Massive - even 1 hour time saved = $1.50 well spent

---

## FALLBACK & RESILIENCE STRATEGY

### **Scenario 1: Groq API Unavailable**
```python
# Automatic fallback to local LLM
result = brain.adaptive(prompt)
# Internal: Detects API down, routes to local automatically
# User experience: Slower but functional
# No crashes, graceful degradation
```

### **Scenario 2: Rate Limit Exceeded**
```python
# Daily limit reached (500 calls)
result = brain.scout(prompt)
# Returns: {"status": "rate_limited", "fallback": "local"}
# Brain automatically switches to local-only mode for rest of day
# Resets at midnight UTC
```

### **Scenario 3: Network Issues**
```python
# Timeout after 5 seconds
# Automatic retry with exponential backoff
# After 3 failures: fallback to local
# No user intervention required
```

### **Scenario 4: Invalid API Key**
```python
# Detected at initialization
# Warning logged: "Groq API unavailable, operating in local-only mode"
# All brain calls route to local LLM
# System remains functional
```

**Key Principle:** Groq enhances but doesn't replace local autonomy

---

## SECURITY & CONSTITUTIONAL ALIGNMENT

### **API Key Security**
- Stored in `/srv/janus/config/.env` (read-only by janus user)
- Never logged in plain text
- Rotated periodically (manual process)
- No key in code repositories

### **Audit Trail**
```python
# Every Groq API call logged
{
  "timestamp": "2025-10-11T17:45:32Z",
  "tool": "groq_fast_think",
  "prompt": "Query text",
  "model": "llama-3.3-70b-versatile",
  "tokens_used": 87,
  "duration_seconds": 1.00,
  "cost_estimate": 0.00006,
  "success": true
}
```

### **Rate Limiting (Constitutional Resource Stewardship)**
- Hard daily limit: 500 API calls
- Hard hourly limit: 100 API calls
- Prevents cost overruns
- Ensures local autonomy preserved
- Alerts when approaching limits

### **Data Privacy**
- No sensitive data sent to API (constitutional requirement)
- Pre-flight privacy check (sanitize before API call)
- Local-only for sensitive operations
- Human approval for strategic decisions

### **Constitutional Alignment Checks**
```python
def is_constitutionally_aligned(self, action: str) -> bool:
    """Verify action aligns with Lion's Sanctuary principles"""

    # Always use LOCAL LLM for constitutional decisions
    # Never delegate constitutional checks to external API
    return self.local_llm.check_alignment(action)
```

---

## VALIDATION PROTOCOL

### **Phase 1: Local Testing (Before Deployment)**
```bash
# On development machine
cd /Users/panda/Desktop/UBOS/02_FORGE/packages/groq_mcp_server
python3 -m pytest tests/test_groq_integration.py -v

# Expected: All tests pass
```

### **Phase 2: Deployment to Balaur**
```bash
# Run deployment script
./02_FORGE/scripts/deploy_groq_to_balaur.sh

# Validates:
# - SSH connectivity
# - Dependency installation
# - File deployment
# - Environment setup
# - Integration tests on Balaur
# - Service health
```

### **Phase 3: Smoke Tests on Balaur**
```bash
ssh panda@100.94.145.78

# Test 1: Groq client basic function
python3 -c "
from tools.groq_client import GroqClient
client = GroqClient()
print(client.fast_think('Test query'))
"

# Test 2: Dual-speed brain
python3 -c "
from tools.dual_speed_brain import DualSpeedCognition
from tools.groq_client import GroqClient
brain = DualSpeedCognition(GroqClient(), '/srv/janus/models/llama-3.1-8b')
print(brain.scout('Quick test'))
"

# Test 3: Web search
python3 -c "
from tools.groq_client import GroqClient
client = GroqClient()
print(client.web_search('AI agent frameworks 2025'))
"
```

### **Phase 4: Integration with Proposal System**
```bash
# Monitor proposal generation with new tools
journalctl -u janus-agent -f | grep -E "groq|dual_speed"

# Expected: See Groq API calls in logs
# Expected: Faster proposal generation times
```

### **Phase 5: 24-Hour Burn-In**
- Monitor for crashes
- Track API usage and costs
- Validate fallback behavior
- Measure performance improvements
- Check constitutional alignment

**Success Criteria:**
- Zero crashes
- API usage within limits (<500/day)
- At least 3 successful adaptive-mode proposals
- Fallback working when API down
- All constitutional checks passing

---

## ROLLBACK PLAN

**If issues detected during validation:**

```bash
# Immediate rollback
ssh panda@100.94.145.78

# 1. Disable Groq integration
echo "GROQ_ENABLED=false" >> /srv/janus/config/.env

# 2. Restart services
sudo systemctl restart janus-agent janus-controls

# 3. Verify local-only operation
journalctl -u janus-agent -n 50

# System returns to pre-Groq state
# Local autonomy unaffected
```

**Root Cause Analysis:**
- Review logs: `/var/log/janus/agent.log`
- Check API errors in audit trail
- Validate environment configuration
- Test Groq client in isolation
- Fix issues, redeploy carefully

---

## MONITORING & OBSERVABILITY

### **Key Metrics to Track**

**Performance Metrics:**
```python
{
  "groq_api_calls_today": 87,
  "groq_api_calls_hour": 12,
  "avg_fast_think_duration": 1.2,  # seconds
  "avg_web_search_duration": 13.5,  # seconds
  "avg_adaptive_mode_duration": 45.0,  # seconds
  "tokens_used_today": 45000,
  "estimated_cost_today": 0.031  # USD
}
```

**Health Metrics:**
```python
{
  "groq_api_available": true,
  "local_llm_available": true,
  "fallback_events_today": 2,  # Times fell back to local
  "rate_limit_hits": 0,
  "error_rate": 0.02  # 2% errors acceptable
}
```

**Constitutional Metrics:**
```python
{
  "proposals_using_groq": 15,
  "proposals_local_only": 8,
  "constitutional_checks_passed": 23,
  "constitutional_checks_failed": 0,
  "human_approvals_required": 3
}
```

### **Alerting Thresholds**

**Warning Alerts:**
- API calls approaching 80% of daily limit
- Error rate >5%
- Fallback events >10/hour

**Critical Alerts:**
- API calls at 100% of limit (rate limited)
- Error rate >20%
- Constitutional check failures
- Both Groq and local LLM unavailable

---

## FIRST MISSIONS FOR DUAL-SPEED JANUS

### **Mission 1: Precedent Scout**
**Objective:** Use Groq to find similar proposals in history

```python
# Scout mode test
result = brain.scout("""
Search proposal history:
- Have we attempted GPU Studio deployment before?
- What were the outcomes?
- What lessons learned?
""")

# Expected: Fast retrieval from local logs + archives
# Speed: 8-12 seconds (vs 60+ seconds manual)
```

### **Mission 2: Emergency Triage**
**Objective:** Fast diagnosis of system issues

```python
# Scenario: SSH connection fails
result = brain.scout("""
Emergency triage:
- What are common causes of SSH timeout?
- Check recent system logs for clues
- Provide top 3 most likely causes
""")

# Expected: Web search + local log analysis
# Speed: 15-20 seconds (vs 120+ seconds research)
```

### **Mission 3: Research-Informed Decision**
**Objective:** Use adaptive mode for strategic decision

```python
# Adaptive mode test
result = brain.adaptive("""
Strategic decision:
Should we prioritize GPU Studio deployment or Mode Beta refinement?

Context needed:
- Latest GPU encoding best practices (web search)
- Current Mode Beta status (local logs)
- Resource availability (local system check)

Provide: Recommendation with reasoning
""")

# Expected: Web intel + local analysis + synthesis
# Speed: 45-60 seconds (vs 2-4 hours manual research)
```

### **Mission 4: Philosophy Node with Context**
**Objective:** Generate philosophy node with real-world examples

```python
# Adaptive mode for creative work
result = brain.adaptive("""
Generate philosophy node: "Cognitive Velocity"

Research phase (Groq):
- Latest research on AI inference speed optimization
- Examples of speed/accuracy tradeoffs in production systems

Creation phase (local):
- Generate node following constitutional principles
- Integrate research findings
- Ensure philosophical depth
""")

# Expected: High-quality node with external context
# Speed: 60-90 seconds
```

---

## SUCCESS METRICS

### **Technical Success**
- ✅ Zero deployment failures
- ✅ All 6 Groq tools functional
- ✅ Dual-speed brain operational
- ✅ Fallback mechanisms working
- ✅ API usage within budget

### **Performance Success**
- ✅ Scout mode: <10s average
- ✅ Adaptive mode: <60s average
- ✅ Web search: <15s average
- ✅ 2-4x faster proposal generation
- ✅ 12-24x faster reconnaissance

### **Constitutional Success**
- ✅ 100% constitutional checks passing
- ✅ No sensitive data leakage
- ✅ Local autonomy preserved
- ✅ Transparent operations (all logged)
- ✅ Human authority maintained

### **Strategic Success**
- ✅ Enables new mission types (research-driven)
- ✅ Faster crisis response
- ✅ Better decisions through deeper context
- ✅ Foundation for Phase 3 (meta-learning)

---

## NEXT PHASE: ADVANCED PATTERNS

**After successful deployment, enable:**

1. **Constitutional Validator Integration**
   - Auto-check proposals with Groq reasoning
   - Pre-flight alignment verification

2. **Research Accelerator Workflows**
   - Systematic research missions
   - Knowledge graph building

3. **Cross-Vessel Intelligence Sharing**
   - Groq as shared oracle for all vessels
   - Trinity synthesis patterns

4. **Meta-Learning System**
   - Janus learns from Groq insights
   - Pattern recognition acceleration

---

## CONCLUSION

This architecture enables Janus-in-Balaur to think at two speeds: **fast reconnaissance** (Groq 87+ t/s) and **deep deliberation** (local 3.78 t/s). The adaptive pattern combines both for optimal decision-making.

**Key Principles:**
- ✅ Speed without sacrificing depth
- ✅ External knowledge without compromising autonomy
- ✅ API enhancement without API dependency
- ✅ Constitutional alignment always preserved

**The forge is hot. Codex is building. Deployment imminent.**

---

**Document Status:** Active Implementation
**Next Update:** After Codex delivery and deployment to Balaur
**Owner:** Janus-in-Claude (Master Strategist)
**Forgemaster:** Janus-in-Codex (Implementation)
