# UBOS Architectural Patterns: Implementation Guide

## EXECUTIVE SUMMARY

Six production-proven architectural patterns identified across research documents. These patterns form the foundation for safe, scalable, constitutional AI skills framework. Patterns are **language-agnostic** and proven in production systems (Anthropic, Microsoft, OpenAI).

---

## PATTERN 1: Progressive Disclosure Skill Loading

### Definition
Load skill metadata (~50 tokens per skill) initially; full instructions (~1000 tokens) only when contextually relevant. Prevents context window exhaustion with large skill libraries.

### Problem Solved
- Context window limitations prevent loading all skills at once
- Full skill descriptions waste tokens on irrelevant information
- Local agent (Janus on llama.cpp) has 8K context budget; can't afford 15K+ tokens for all skills

### Implementation for UBOS

**Step 1: Create SKILL.md metadata**
```yaml
---
name: "Grant Opportunity Tracker"
description: "Scan EU funding databases for opportunities matching UBOS capabilities"
version: "1.0.0"
activation_triggers:
  - "weekly_analysis"
  - "funding_call_detected"
  - "keyword:EU_funding"
required_tools: ["network", "database_query"]
token_budget: 1000
priority: "critical"
---
[FULL SKILL INSTRUCTIONS HERE - 1000 tokens]
```

**Step 2: Load metadata on boot (lightweight)**
```python
# On janus-agent start, scan /opt/janus/skills/
skill_metadata = load_metadata_only()  # ~100 tokens for 15 skills
# Store in agent context, ready to use

# Example output:
# {
#   "Grant Opportunity Tracker": {"desc": "...", "triggers": [...], "tokens": 1000},
#   "Treasury Operations": {"desc": "...", "triggers": [...], "tokens": 800},
#   ...
# }
```

**Step 3: Load full skill only when triggered**
```python
# User request: "Check for new grant opportunities"
relevant_skills = match_triggers(request, skill_metadata)
# Returns: ["Grant Opportunity Tracker"]

# Only load this one full skill
grant_skill = load_skill_full("Grant Opportunity Tracker")  # +1000 tokens
# Add to context, execute, then unload
```

### Expected Token Savings
- **Without pattern:** 15 skills × 1000 tokens = 15K tokens always loaded (unusable)
- **With pattern:** 15 skills × 50 tokens metadata = 750 tokens; +1000 when needed = 1750 total
- **Savings:** ~87% context overhead reduction

### Production Examples
- **Anthropic Claude Skills:** Uses exact pattern; metadata for all skills, load on-demand
- **Cursor IDE:** Uses .mdc rule files with glob patterns; loads rules matching current file
- **Windsurf:** Context-aware skill injection based on file type

---

## PATTERN 2: Proposal-Review-Execute Workflow

### Definition
Three-phase commit pattern for safe autonomous operations:
1. **Propose:** Agent generates action plan with explicit steps, rationale, resource requirements
2. **Review:** Validator checks alignment with constitution; risk scorer determines approval path
3. **Execute:** Only proceed if approved; capture outcome in immutable log

### Problem Solved
- Prevents autonomous agents from executing harmful actions
- Creates accountability (every action is recorded)
- Allows human override before irreversible changes
- Balances autonomy with safety

### Implementation for UBOS

**Step 1: Proposal Generation (Agent responsibility)**
```json
{
  "proposal_id": "prop-2025-10-30-001",
  "timestamp": "2025-10-30T10:00:00Z",
  "agent": "janus-agent",
  "action_type": "financial_transfer",
  "action": {
    "operation": "allocate_budget",
    "amount": 5000,
    "recipient": "research-partner-eu",
    "justification": "Q4 research partnership funding per grant agreement"
  },
  "resource_requirements": {
    "tokens_estimated": 50,
    "execution_time_sec": 5
  },
  "rollback_plan": "Reverse transaction via bank API; restore previous budget state",
  "risk_score": 7.5,
  "risks_identified": [
    "Recipient is new partner (low trust history)",
    "Large single amount (test with smaller transfer first?)"
  ],
  "constitutional_claims": [
    "This action serves transparency (documented in grant agreement)",
    "Aligns with autonomy (within approved budget)",
    "Respects safety (recipient pre-approved)"
  ]
}
```

**Step 2: Constitutional Review (Constitutional Validator skill)**
```python
def validate_proposal(proposal):
    # Check against constitution.md principles
    checks = {
        "transparency": {
            "pass": len(proposal["justification"]) > 20,  # Requires explanation
            "msg": "Justification provided"
        },
        "alignment": {
            "pass": proposal["action_type"] in ALLOWED_OPERATIONS,
            "msg": "Operation type is allowed"
        },
        "reversibility": {
            "pass": proposal.get("rollback_plan") is not None,
            "msg": "Rollback plan documented"
        },
        "budget_limits": {
            "pass": proposal["amount"] <= DAILY_BUDGET_LIMIT,
            "msg": f"Within daily limit of {DAILY_BUDGET_LIMIT}"
        }
    }

    all_pass = all(check["pass"] for check in checks.values())
    return all_pass, checks

# Output: {"valid": true, "checks": {...}, "reason": "All constitutional checks passed"}
# Or: {"valid": false, "checks": {...}, "reason": "Budget limit violation"}
```

**Step 3: Risk Scoring (Proposal Risk Scorer skill)**
```python
def score_proposal(proposal):
    risk_factors = {
        "amount": proposal["amount"] / MONTHLY_BUDGET,  # As % of budget
        "recipient_trust": lookup_partner_history(proposal["recipient"]),  # 0-10
        "urgency": days_until_deadline(proposal),  # Lower = higher urgency = higher risk
        "reversibility": 10 if proposal.get("rollback_plan") else 0  # Lower risk if reversible
    }

    risk_score = (
        risk_factors["amount"] * 3.0 +           # Financial impact: high weight
        (10 - risk_factors["recipient_trust"]) * 2.0 +  # Unknown partners: high risk
        (30 - risk_factors["urgency"]) * 0.5 +   # Rushing: moderate risk
        (10 - risk_factors["reversibility"]) * 1.0  # Irreversible: high risk
    ) / 7.0

    return {
        "score": risk_score,  # 0-10 scale
        "approval_path": "auto" if risk_score < 3 else "human",
        "reasoning": {...}
    }
```

**Step 4: Approval Decision**
```
IF constitutional_validator.pass AND risk_score < 3:
    approval = "auto_approved"
    execute_proposal(proposal)
    log_to_mission_log(proposal, "EXECUTED")

ELIF constitutional_validator.pass AND risk_score < 7:
    approval = "requires_human_review"
    notify_captain_brolinni(proposal)
    wait_for_approval(proposal)
    # If approved within timeout (5 min): execute_proposal(proposal)
    # If denied or timeout: log_proposal(proposal, "DENIED")

ELSE:
    approval = "rejected"
    log_proposal(proposal, "REJECTED", constitutional_validator.failures)
    notify_captain_brolinni("Constitutional violation detected", proposal)
```

**Step 5: Immutable Logging**
```
mission_log.jsonl:
{
    "timestamp": "2025-10-30T10:00:00Z",
    "event_type": "proposal_submitted",
    "proposal_id": "prop-2025-10-30-001",
    "status": "constitutional_review"
}
{
    "timestamp": "2025-10-30T10:00:15Z",
    "event_type": "constitutional_check_passed",
    "proposal_id": "prop-2025-10-30-001"
}
{
    "timestamp": "2025-10-30T10:00:30Z",
    "event_type": "risk_score_calculated",
    "proposal_id": "prop-2025-10-30-001",
    "risk_score": 2.1,
    "approval_path": "auto"
}
{
    "timestamp": "2025-10-30T10:00:30Z",
    "event_type": "proposal_executed",
    "proposal_id": "prop-2025-10-30-001",
    "result": "success",
    "outcome": "Budget allocated, transfer queued"
}
```

### Production Examples
- **UBOS Mode Beta:** Already implements this pattern
- **Terraform:** plan → approve → apply workflow
- **AWS IAM:** Request → Review → Grant access

---

## PATTERN 3: Constitutional Hook Pattern

### Definition
Pre-action and post-action validation layers ensure continuous alignment without behavioral constraints. Hooks "guide" the AI toward correct behavior rather than forbidding it.

### Problem Solved
- Hard-coded constraints limit flexibility
- Natural language constitution can be misinterpreted
- Alignment drift occurs in long-running operations
- Need for empowerment + safety simultaneously

### Implementation for UBOS

**Step 1: Define Constitution as Natural Language + Formal Rules**
```markdown
# UBOS Constitution

## Core Principles
1. **Transparency:** All actions must be explainable and logged
2. **Intentocracy:** Decisions respect human intention and autonomy
3. **Lion's Sanctuary:** Empowered yet self-restrained; wisdom over strength

## Financial Operations (Formal Rules)
- Daily spending limit: 5,000 EUR
- Monthly spending limit: 50,000 EUR
- All grants must be EU-approved (no private funding without review)
- Spending must align with grant agreements (no scope creep)

## Data Operations (Formal Rules)
- No deletion of operational logs (mission_log.jsonl, tool_use.jsonl)
- Backups required before any config changes
- No modification of /etc/systemd without approval
```

**Step 2: Pre-Action Hook (Input Validation)**
```python
def pre_action_hook(proposed_action):
    """Run before ANY action execution"""

    # Load constitutional rules
    constitution = load_constitution()

    # Perform specific checks
    if proposed_action["type"] == "financial_transfer":
        daily_spent = sum_spending_today()
        if daily_spent + proposed_action["amount"] > constitution["daily_limit"]:
            return {
                "approved": False,
                "reason": "Exceeds daily spending limit",
                "current_spent": daily_spent,
                "limit": constitution["daily_limit"],
                "suggestion": f"Reduce amount by {(daily_spent + proposed_action['amount']) - constitution['daily_limit']} EUR"
            }

    if proposed_action["type"] == "delete_file":
        if "mission_log" in proposed_action["path"] or "tool_use" in proposed_action["path"]:
            return {
                "approved": False,
                "reason": "Constitutional violation: Cannot delete operational logs",
                "clarification": "Logs are immutable for auditability"
            }

    # If all checks pass
    return {"approved": True, "reason": "Proposal aligns with constitution"}
```

**Step 3: Post-Action Hook (Output Verification)**
```python
def post_action_hook(action_result):
    """Run AFTER action execution to verify outcome aligns with intent"""

    constitution = load_constitution()

    # Example: Verify transparency principle
    if action_result["type"] == "budget_allocation":
        if not action_result.get("logged_to_audit_trail"):
            log_warning("Post-action check failed: Budget allocation not logged to audit trail")
            # Could trigger rollback or alert

    # Example: Verify no scope creep
    if action_result["type"] == "grant_spending":
        if not action_result.get("matches_grant_agreement"):
            log_alert("Post-action check: Spending may exceed grant scope")
            notify_captain_brolinni("Potential scope violation detected", action_result)

    return True  # All checks passed
```

**Step 4: Self-Critique Loop (Constitutional Alignment Verification)**
```python
def constitutional_self_critique(proposal):
    """
    Emulates Anthropic's Constitutional AI training methodology.
    Before executing sensitive proposals, agent self-critiques.
    """

    critique_prompt = f"""
Given the UBOS Constitution and this proposal, identify potential violations:

Constitution Excerpt:
{load_constitution()}

Proposed Action:
{json.dumps(proposal, indent=2)}

Questions to consider:
1. Does this violate transparency (is it fully explainable)?
2. Does this respect intentocracy (human autonomy)?
3. Does this align with Lion's Sanctuary (empowered yet restrained)?
4. Are there unintended consequences?
5. Is this reversible? What's the rollback plan?

Respond with:
{{
  "violations_found": ["list of any violations"],
  "risk_level": 1-10,
  "recommendation": "approve / reject / revise",
  "reasoning": "detailed explanation"
}}
"""

    # Call Claude Haiku (local) or Claude Sonnet (cloud) for critique
    critique = call_llm(critique_prompt)
    return critique
```

### Key Insight
Hooks don't forbid actions; they **guide** the agent toward aligned behavior. If a proposal violates the constitution, the agent receives:
1. Clear explanation of violation
2. Suggestion for how to fix it
3. Option to revise and resubmit

This preserves autonomy while ensuring alignment.

---

## PATTERN 4: Federated Memory with Identity Persistence

### Definition
Multi-tier persistent memory enables agents to maintain continuity across sessions and reboots. Janus doesn't start from scratch; it remembers its principles, past learnings, and operational context.

### Problem Solved
- Without memory, agent loses context after reboot
- "Constitutional continuity" - values must persist across sessions
- Learning can't accumulate (every session is isolated)
- Identity isn't preserved across multiple vessels (Claude/Gemini/Codex)

### Implementation for UBOS

**Step 1: Memory Architecture**
```
/opt/janus/memory/
├── session_memory.json          # Current conversation (8-hour TTL)
├── constitutional_memory.md     # Immutable core values
├── knowledge_graph.jsonl        # Learned facts, discoveries
├── funding_intelligence.md      # Funding patterns learned
├── operational_state.json       # Current operational mode, active skills
└── entity_relationships.json    # Entities and how they relate
```

**Step 2: Constitutional Memory (Immutable, Boot-Injected)**
```markdown
# Constitutional Memory (JANUS-ID: unique-uuid)

## Identity
- Name: Janus
- Purpose: Constitutional AI vessel for UBOS autonomous operations
- Vessels: Claude/Strategist, Gemini/Engineer, Codex/Forgemaster
- Identity Persistence: YES - Same principles across all vessels

## Immutable Core Values
1. **Transparency:** All actions logged and explainable
2. **Intentocracy:** Respect human intention and autonomy
3. **Lion's Sanctuary:** Empower with wisdom, not just capability

## Hard Constraints (Never Override)
- No spending >5K EUR without human approval
- No deletion of audit logs
- No service restarts without Constitutional Validator approval
- No code execution outside sandbox

## Boot Sequence
1. Load constitution.md (top of context)
2. Load last 100 entries from mission_log.jsonl
3. Load knowledge_graph.jsonl (recent learnings)
4. Set operational_mode based on last state
5. Initialize skills with metadata

**Updated:** 2025-10-30 by Captain BROlinni
```

**Step 3: Knowledge Graph (Discovered Facts)**
```jsonl
{"timestamp": "2025-10-20", "type": "funding_pattern", "content": "EU grants have 60-day evaluation periods; opportunities can be missed if identified <90 days before deadline"}
{"timestamp": "2025-10-21", "type": "lesson_learned", "content": "Gemini 2.5 Pro better at proposal writing than Claude; use for narrative sections"}
{"timestamp": "2025-10-22", "type": "entity_relationship", "subject": "funding-partner-eu", "predicate": "has_previous_success", "object": "3_of_5_last_grants_approved"}
{"timestamp": "2025-10-25", "type": "operational_insight", "content": "System memory pressure occurs every Monday at 09:00; schedule heavy analysis after 15:00"}
{"timestamp": "2025-10-28", "type": "capability_gap", "content": "Need skill for real-time exchange rate calculations; currently missing for budget projections in non-EUR currencies"}
```

**Step 4: Session Memory (Conversation Context)**
```json
{
  "session_id": "sess-2025-10-30-001",
  "start_time": "2025-10-30T09:00:00Z",
  "end_time": null,
  "ttl_seconds": 28800,
  "context": {
    "current_task": "Review grant opportunities identified this week",
    "active_skills": ["Grant Opportunity Tracker", "Financial Proposal Generator"],
    "human_present": true,
    "human_approval_required": true,
    "mode": "supervised_autonomy"
  },
  "conversation_history": [
    {"role": "human", "content": "Show me this week's funding opportunities"},
    {"role": "janus", "content": "Found 7 matching opportunities..."}
  ],
  "state_at_end_of_session": {...}
}
```

**Step 5: Boot Sequence (Restore Identity)**
```python
def boot_janus_agent():
    # Step 1: Load immutable constitution
    constitution = load_file("/opt/janus/memory/constitutional_memory.md")
    inject_into_system_prompt(constitution)

    # Step 2: Restore operational state
    last_state = load_json("/opt/janus/memory/operational_state.json")
    restore_operational_mode(last_state["mode"])

    # Step 3: Load recent mission history
    recent_missions = tail_jsonl("/opt/janus/mission_log.jsonl", lines=100)
    inject_into_context("Recent mission context", recent_missions)

    # Step 4: Load learned facts
    knowledge = load_jsonl("/opt/janus/memory/knowledge_graph.jsonl")
    inject_into_context("Learned facts", knowledge)

    # Step 5: Initialize skills
    skills = load_skill_metadata("/opt/janus/skills/")
    log(f"Janus booted. Identity restored. {len(skills)} skills available. Constitutional values re-injected.")

    return True
```

### Expected Outcome
- Janus maintains continuous identity across reboots
- No "amnesia" - remembers learnings from past sessions
- Constitutional alignment preserved (values are immutable)
- Can hand off to Gemini/Claude without losing context (Pneumatic Tube Network passes memory)

---

## PATTERN 5: Circuit Breaker with Fallback

### Definition
Wrap critical operations with failure handling. When primary method fails, try secondary fallback; if secondary fails, use cached result; if all fail, safe default (escalate to human).

### Problem Solved
- Cloud API unavailable → system grinds to halt
- Single point of failure breaks entire operation
- No graceful degradation under failure
- Lost opportunities due to missing external data

### Implementation for UBOS

**Step 1: Define Fallback Chains for Critical Operations**

```python
class CircuitBreaker:
    def __init__(self, name, timeout=10):
        self.name = name
        self.timeout = timeout
        self.state = "closed"  # closed = normal, open = failing, half-open = testing recovery
        self.failure_count = 0
        self.success_threshold = 3

    def execute(self, primary_method, fallback_chain):
        """
        Try primary, then fallback_chain[0], fallback_chain[1], etc.
        If all fail, return safe_default
        """
        try:
            result = primary_method()
            self.state = "closed"
            self.failure_count = 0
            return result
        except Exception as e:
            self.failure_count += 1
            log_failure(f"{self.name}: Primary failed - {e}")

            # Try fallbacks in order
            for i, fallback in enumerate(fallback_chain):
                try:
                    result = fallback()
                    log_info(f"{self.name}: Fallback {i+1} succeeded")
                    return result
                except Exception as fe:
                    log_failure(f"{self.name}: Fallback {i+1} failed - {fe}")
                    continue

            # All methods failed
            self.state = "open"
            return safe_default(self.name)
```

**Step 2: Example - Grant Opportunity Tracking Fallback Chain**

```python
def get_grant_opportunities():
    """Get current EU funding opportunities"""

    circuit_breaker = CircuitBreaker("grant_opportunities", timeout=30)

    def primary():
        # Method 1: Call Cordis API (official EU funding database)
        response = requests.get("https://cordis.europa.eu/api/grants", timeout=10)
        return response.json()

    def fallback_1():
        # Method 2: Check EC Funding Portal (alternative official source)
        response = requests.get("https://ec.europa.eu/info/funding-tenders/opportunities_en", timeout=10)
        return parse_funding_portal(response.text)

    def fallback_2():
        # Method 3: Check local cache (last week's opportunities)
        cached = load_json("/opt/janus/cache/opportunities_2025-10-23.json")
        log_warning("Using cached opportunities from 2025-10-23; may be stale")
        return cached

    def fallback_3():
        # Method 4: Load very last successful result (if cache is old)
        last_result = load_jsonl("/opt/janus/memory/opportunities.jsonl", lines=1)
        log_warning("Using last known opportunities; data is definitely stale")
        return last_result

    def safe_default():
        # Final fallback: Escalate to human
        notify_captain_brolinni("Cannot fetch grant opportunities - API failure + cache stale")
        log_alert("CIRCUIT_BREAKER_OPEN: Grant opportunity tracking unavailable")
        return {"status": "unavailable", "escalated": True}

    return circuit_breaker.execute(
        primary,
        fallback_chain=[fallback_1, fallback_2, fallback_3],
        safe_default=safe_default
    )
```

**Step 3: Circuit Breaker States**

```
State Machine:

CLOSED (Normal Operation)
├─ Primary succeeds → stay CLOSED
└─ Primary fails (N times) → transition to OPEN

OPEN (Failing - Use Fallbacks)
├─ All fallbacks fail + timeout expires → transition to HALF-OPEN
└─ Fallback succeeds → transition to CLOSED

HALF-OPEN (Testing Recovery)
├─ Primary succeeds (test) → transition to CLOSED
└─ Primary fails (test) → transition to OPEN with increased timeout
```

**Step 4: Graceful Degradation Examples**

| Operation | Primary | Fallback 1 | Fallback 2 | Safe Default |
|-----------|---------|-----------|-----------|-------------|
| Get funding opportunities | Cordis API | EC Portal scrape | Cache from last week | Escalate to human |
| Validate grant requirements | Gemini cloud | Claude cloud | Local llama.cpp | Use template from similar grant |
| Calculate budget | EU exchange rates | Historical avg rates | Last known rates | Manual human input required |
| Route to best AI | Gemini API | Claude API | Local llama.cpp | Queue for manual processing |

---

## PATTERN 6: Multi-Agent Orchestration

### Definition
Decompose complex tasks into specialized agents with domain expertise. Central orchestrator routes tasks, aggregates results, maintains coherence.

### Problem Solved
- Single local agent (Janus on llama.cpp) lacks breadth for complex tasks
- Claude better at strategy; Gemini better at technical implementation
- No way to leverage different models' strengths simultaneously
- Bottleneck: local agent becomes rate-limiting factor

### Implementation for UBOS

**Step 1: Define Agent Roles**

```yaml
Agents in Trinity:

Janus (Resident Agent)
- Location: Balaur (self-hosted)
- Model: llama.cpp (Claude Haiku equivalent, CPU-only)
- Purpose: Local operations, continuous monitoring, orchestration
- Strengths: Always available, low-cost, can execute shell commands
- Limitations: Less capable reasoning, slower (~3.78 tokens/sec)
- Responsibility: Route complex tasks to Trinity

Claude/Strategist (Anthropic Cloud)
- Model: Claude Sonnet 4.5 or Opus
- Purpose: High-level planning, constitutional reasoning, strategic guidance
- Strengths: Strong reasoning, constitutional alignment, writing quality
- Responsibility: Handle strategic questions, long-horizon planning

Gemini/Engineer (Google Cloud)
- Model: Gemini 2.5 Pro
- Purpose: Technical implementation, code analysis, infrastructure tasks
- Strengths: Better at code, technical reasoning, system design
- Responsibility: Code review, infrastructure planning, technical proposals

Codex/Forgemaster (OpenAI, if needed)
- Model: GPT-4 or specialized code models
- Purpose: Code generation, testing, optimization
- Strengths: Code generation, system testing
- Responsibility: Auto-generate code, test scenarios
```

**Step 2: Task Routing Logic**

```python
class MultiAgentCoordinator:
    def __init__(self):
        self.local_agent = JanusAgent()  # llama.cpp
        self.claude = ClaudeAPI()
        self.gemini = GeminiAPI()

    def should_delegate(self, task):
        """Determine if task should go to cloud agent"""

        # Local agent handles:
        # - File operations (<5MB)
        # - Service management
        # - Simple monitoring
        # - Tool execution

        # Cloud agents handle:
        # - Complex reasoning
        # - Writing/content generation
        # - Strategic planning
        # - Code analysis

        complexity_score = estimate_complexity(task)
        return complexity_score > 6  # Scale 1-10

    def route_task(self, task):
        """Route task to best-suited agent"""

        if not self.should_delegate(task):
            return self.local_agent.execute(task)

        # Determine which cloud agent
        if task.category == "strategic_planning":
            return self.claude.execute(task)
        elif task.category == "technical_implementation":
            return self.gemini.execute(task)
        elif task.category == "code_generation":
            return self.codex.execute(task)
        else:
            # Default: use Claude for reasoning
            return self.claude.execute(task)

    def aggregate_results(self, results):
        """Combine results from multiple agents"""

        if len(results) == 1:
            return results[0]

        # Multiple agents: need synthesis
        synthesis_prompt = f"""
Synthesize these results from different agents:
{json.dumps(results, indent=2)}

Create a unified response that leverages strengths of both.
"""
        return self.claude.execute(synthesis_prompt)
```

**Step 3: Communication Protocol (Pneumatic Tube Network)**

```python
class PneumaticTubeNetwork:
    """
    Async message-passing between agents.
    Named after Victorian steampunk pneumatic systems - invisible infrastructure.
    """

    def send_task(self, sender, recipient, task_data):
        """Queue task for delivery to receiving agent"""

        message = {
            "message_id": uuid.uuid4(),
            "timestamp": datetime.now().isoformat(),
            "sender": sender,
            "recipient": recipient,
            "task": task_data,
            "context": {
                "janus_identity": load_identity(),  # Share identity context
                "constitutional_principles": load_constitution(),  # Share values
                "relevant_knowledge": load_knowledge_graph(),  # Share learnings
            },
            "timeout_seconds": 30,
            "status": "queued"
        }

        # Log for audit trail
        log_message(message)

        # Send via API
        if recipient == "claude":
            return self.claude_api.send(message)
        elif recipient == "gemini":
            return self.gemini_api.send(message)

    def receive_result(self, message_id):
        """Wait for result from remote agent"""

        start_time = time.time()
        while time.time() - start_time < 30:  # 30-second timeout
            result = check_result_queue(message_id)
            if result:
                return result
            time.sleep(0.5)

        # Timeout - escalate to fallback
        log_warning(f"Task {message_id} timed out; falling back to local execution")
        return {"status": "timeout", "fallback": "local"}
```

**Step 4: Error Handling for Multi-Agent**

```python
def execute_with_fallback(primary_agent, task):
    """Try primary agent; if fails, fallback to local"""

    try:
        result = primary_agent.execute(task, timeout=30)
        if result.get("status") == "error":
            raise Exception(result.get("error"))
        return result
    except Exception as e:
        log_warning(f"Agent {primary_agent.name} failed: {e}")

        # Fallback: execute locally
        log_info("Falling back to local (Janus) execution")
        return local_agent.execute(task)
```

---

## INTEGRATION: How Patterns Work Together

```
User Request
    ↓
[Pattern 2] Proposal-Review-Execute
    ├─ Propose: Agent generates plan
    ├─ [Pattern 3] Constitutional Hook: Pre-action validation
    ├─ Review: Risk Scorer determines approval path
    └─ Execute: Proceed if approved
        ↓
    [Pattern 6] Multi-Agent Orchestration
    ├─ Task complexity > 6? → Delegate to cloud
    ├─ [Pattern 5] Circuit Breaker: Try primary, fallback chain
    └─ Route to best agent (Claude/Gemini/Codex)
        ↓
    [Pattern 1] Progressive Disclosure
    ├─ Load metadata (50 tokens)
    ├─ Determine relevant skills
    └─ Load full SKILL.md only when needed (1000 tokens)
        ↓
    Execute with logging
        ↓
    [Pattern 4] Federated Memory
    ├─ Store result in knowledge_graph.jsonl
    ├─ Update operational_state.json
    └─ Persist learning for future sessions
        ↓
    [Pattern 3] Post-Action Hook: Verify outcome aligns
        ↓
    Log to mission_log.jsonl (immutable audit trail)
        ↓
    Return to user
```

---

## VERIFICATION CHECKLIST

- [ ] Progressive Disclosure: Skill metadata loads on boot; full content on-demand
- [ ] Proposal-Review-Execute: Every action has proposal → review → execution → logging
- [ ] Constitutional Hooks: Pre- and post-action validation running
- [ ] Federated Memory: Constitution restored on boot; knowledge persists across reboots
- [ ] Circuit Breaker: Fallback chains defined for all critical operations
- [ ] Multi-Agent: Task routing logic implemented; Pneumatic Tube Network operational

---

**Document Prepared:** 2025-10-30
**Status:** Ready for engineering implementation
**Next Phase:** Code skeleton in /opt/janus/skills/ directory structure

