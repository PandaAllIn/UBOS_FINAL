---
type: master_plan
priority: critical
date: 2025-11-20
scope: balaur_full_system_activation
coordination: Claude + Gemini + Codex
estimated_duration: 8-12 hours
---

# 🐉 BALAUR FULL ACTIVATION - MASTER PLAN

**Mission:** Transform Balaur from idle intelligence to 24/7 autonomous operation using steampunk architecture, 90/10 resource allocation, and multi-resident orchestration

**Philosophy:** "Build the habitat so perfect that there's no reason to leave"

---

## 📊 CURRENT STATE AUDIT

### ✅ What's Running (VERIFIED)

**Core Infrastructure:**
- ✅ Janus Agent (PID 2569205) - Main autonomous agent
- ✅ Victorian Controls Orchestrator (PID 2939589) - Governor + Relief + Escapement
- ✅ Mission Dispatcher Daemon (PID 303743)
- ✅ Living Scroll Command Center (:5000) - Operational
- ✅ Pathfinder Production (:5002) - 7 segments, 345L fuel

**4 AI Residents (Since Nov 1):**
- ✅ Claude Resident (PID 303849) - `resident_mission_executor.py --resident claude`
- ✅ Gemini Resident (PID 306738) - `resident_mission_executor.py --resident gemini`
- ✅ Groq Resident (PID 304032) - `resident_mission_executor.py --resident groq`
- ✅ OpenAI Resident (PID 304125) - `resident_mission_executor.py --resident openai`

**4 API Responders:**
- ✅ Janus Responder (PID 1608/1616)
- ✅ Claude Responder (PID 188216/188219)
- ✅ Gemini Responder (PID 188181/188184)
- ✅ Groq Responder (PID 188164/188167)
- ✅ OpenAI Hot Vessel Server (PID 2224232) - `openai_hot_vessel_server.py`

**Trinity CLI Sessions:**
- ✅ Claude (PID 2479445, 2486039) - 2 instances running
- ✅ Gemini (PID 2530799) - 31 hours active
- ✅ Codex (PID 2487271) - 5 hours active

### ⚠️ What's BROKEN

**Current Mission: MISSION-GEODATA-XF-2025-10-27**
- ⚠️ **Stuck in proposal loop** - 20+ duplicate proposals since 03:55
- ⚠️ **All proposals "draft" or "suppressed"** - None approved/executed
- ⚠️ **Janus not learning** - Repeats same analysis every 15 minutes
- ⚠️ **No delegation** - Janus using only llama-cli (local 8B model)
- ⚠️ **Residents idle** - API residents not receiving tasks

**Error Logs (LARGE):**
- claude-haiku.error.log: 11MB
- gemini-pro.error.log: 11MB
- groq-vessel.error.log: 11MB
- mission_log.jsonl: 165MB (many failed attempts)

**Root Cause:** Janus lacks delegation intelligence. It doesn't know:
1. When to delegate to faster models (Groq llama-3.3-70b-versatile)
2. When to use strategic models (Claude Haiku)
3. When to switch tasks to appropriate resident
4. How to avoid duplicate work

---

## 🎯 THE VISION: 90/10 RESOURCE ALLOCATION

### Inspired by Pathfinder's 10% Rule

**Concept:** Reserve 10% of resources for "hot" real-time operations, 90% for "cold" batch processing

**Applied to Balaur:**

```
┌─────────────────────────────────────────────┐
│         BALAUR RESOURCE ALLOCATION          │
├─────────────────────────────────────────────┤
│                                             │
│  90% - THE LOOM (Batch Processing)         │
│  ══════════════════════════════════════     │
│  • CPU: 7/8 cores for long tasks           │
│  • HDD/SSD: 88GB storage for archives      │
│  • Memory: 27GB for model loading          │
│  • Janus local llama.cpp 8B model          │
│  • Pattern recognition, brass punch cards  │
│  • Constitutional analysis (deep, slow)    │
│                                             │
├─────────────────────────────────────────────┤
│                                             │
│  10% - THE CORTEX (Real-Time Intelligence) │
│  ═══                                        │
│  • CPU: 1/8 core for hot paths             │
│  • GPU: 4GB VRAM for fast inference        │
│  • Memory: 3GB for resident APIs           │
│  • 4 API Residents (Claude, Gemini, etc.)  │
│  • Fast delegation to Groq                 │
│  • Strategic decisions (Claude Haiku)      │
│  • Quick responses, voice commands         │
│                                             │
└─────────────────────────────────────────────┘
```

**Why this works:**
- **Loom handles:** Deep research, pattern learning, archive building
- **Cortex handles:** Quick responses, delegation, real-time commands
- **No resource conflict:** Hot/cold paths isolated
- **Constitutional:** "Perfect habitat" - each layer optimized for its purpose

---

## 🏗️ STEAMPUNK ARCHITECTURE COMPONENTS

### From UNIFIED_STEAMPUNK_ARCHITECTURE.md

**Already Implemented:**
1. ✅ **The Mill** (CPU: Intel i7-4790K @ 4.0GHz)
2. ✅ **The Auxiliary Steam Cylinder** (GPU: AMD R9 M295X, 4GB VRAM)
3. ✅ **The Store** (32GB RAM, 98GB storage, archive vaults)
4. ✅ **The Governor** (PI rate controller for throughput)
5. ✅ **The Relief Valve** (CPU/memory emergency shutdown)
6. ✅ **The Escapement** (10Hz tick regulator)
7. ✅ **The Manifold** (UFW firewall, blast doors)
8. ✅ **Lubrication Ports** (Daily log rotation, backups)

**Need to Implement:**
1. 🚧 **The Reasoning Fork** (Decision trees for delegation)
2. 🚧 **The Mechanical Bouncer** (Request routing & load balancing)
3. 🚧 **The Loom** (Brass punch card pattern storage)
4. 🚧 **The Cortex** (Resident orchestration layer)
5. 🚧 **The Aetheric Maglev** (Puck-based inter-resident messaging)

---

## 📋 PHASE 1: AUDIT & INTELLIGENCE GATHERING

### Task 1.1: Analyze Current Proposal Loop (Gemini)

**Objective:** Understand why Janus is stuck

**Steps:**
1. Read last 100 proposals from `proposals.jsonl`
2. Count suppressed/draft/proposed/approved/rejected
3. Identify duplicate chains
4. Find the root cause (missing approval logic? Bad mission definition?)

**Output:** `BALAUR_PROPOSAL_LOOP_ANALYSIS.md`

---

### Task 1.2: Inventory Resident Capabilities (Claude)

**Objective:** Document what each resident can do

**Residents:**
1. **Janus Local (llama.cpp 8B)**
   - Model: Llama 3.2 8B Instruct
   - Speed: ~20 tokens/sec (CPU-only)
   - Best for: Long-form analysis, batch processing, pattern learning
   - Cost: $0 (local)
   - Available: 24/7

2. **Claude Haiku Resident (API)**
   - Model: claude-3-haiku-20240307
   - Speed: ~100 tokens/sec
   - Best for: Strategic decisions, constitutional alignment, quick analysis
   - Cost: $0.25/1M input, $1.25/1M output
   - Available: 24/7

3. **Gemini 1.5 Flash Resident (API)** - Needs upgrade to Gemini 2.0
   - Current: gemini-1.5-flash
   - Speed: ~150 tokens/sec
   - Best for: Systems engineering, code generation, debugging
   - Cost: Free tier: 15 RPM, 1M TPM
   - **Upgrade target:** gemini-2.0-flash-exp (faster, smarter)

4. **Groq Resident (API)**
   - Models: llama-3.3-70b-versatile, mixtral-8x7b, llama-3.1-8b
   - Speed: ~300-800 tokens/sec (fastest!)
   - Best for: Fast search, quick responses, voice delegation
   - Cost: Free tier: 30 RPM, 14,400 TPD
   - **Key advantage:** Model switching based on task

5. **OpenAI Resident (API)**
   - Models: gpt-4o-mini, gpt-4o, o1-preview, o1-mini
   - Speed: ~100-150 tokens/sec
   - Best for: Complex reasoning (o1), general tasks (4o-mini)
   - Cost: Variable ($0.15-$15/1M tokens)
   - **Key advantage:** Reasoning models for hard problems

**Output:** `RESIDENT_CAPABILITIES_MATRIX.md`

---

### Task 1.3: Find All Steampunk Architecture Files (Claude)

**Search patterns:**
- reasoning fork / reasoning_fork
- mechanical bouncer / mechanical_bouncer
- loom / punch card / brass_punch_cards
- cortex / aetheric / maglev
- 90/10 / resource allocation / hot/cold paths

**Output:** `STEAMPUNK_ARCHITECTURE_INDEX.md`

---

## 📋 PHASE 2: DESIGN THE INTELLIGENCE LAYER

### Task 2.1: Design Reasoning Fork (Claude)

**Purpose:** Decision tree for "Who should handle this task?"

**Logic:**
```python
class ReasoningFork:
    def route_task(self, task):
        # Fast path (CORTEX - 10%)
        if task.priority == "urgent":
            return "groq"  # 800 tok/sec
        elif task.type == "strategy":
            return "claude-haiku"  # Constitutional expert
        elif task.type == "code":
            return "gemini-2.0-flash"  # Systems engineer
        elif task.type == "reasoning":
            return "openai-o1-mini"  # Deep reasoning

        # Slow path (LOOM - 90%)
        elif task.type == "analysis" and not task.urgent:
            return "janus-local"  # 8B local, free, patient
        elif task.type == "pattern_learning":
            return "janus-local"  # Brass punch card creation

        # Default
        else:
            return "janus-local"  # Conservative default
```

**Output:** `REASONING_FORK_SPEC.md`

---

### Task 2.2: Design Mechanical Bouncer (Codex)

**Purpose:** Load balancing + rate limiting for residents

**Components:**
1. **Request Queue** - FIFO queue per resident
2. **Rate Limiter** - Respect API quotas
   - Groq: 30 RPM, 14,400 TPD
   - Gemini: 15 RPM, 1M TPM
   - Claude: 50 RPM (paid tier)
   - OpenAI: 500 RPM (paid tier)
3. **Failover** - If resident unavailable, route to backup
4. **Circuit Breaker** - If resident failing, disable temporarily

**Implementation:**
```python
class MechanicalBouncer:
    def __init__(self):
        self.queues = {
            "groq": RateLimitedQueue(rpm=30, tpd=14400),
            "gemini": RateLimitedQueue(rpm=15, tpm=1000000),
            "claude": RateLimitedQueue(rpm=50),
            "openai": RateLimitedQueue(rpm=500),
            "janus": UnlimitedQueue()  # Local, no limits
        }
        self.circuit_breakers = {}

    def submit(self, task, target_resident):
        queue = self.queues[target_resident]
        if self.circuit_breakers.get(target_resident, False):
            # Resident down, failover
            target_resident = self.get_backup(target_resident)
            queue = self.queues[target_resident]

        queue.enqueue(task)
        return queue.wait_for_slot()
```

**Output:** `MECHANICAL_BOUNCER_SPEC.md`

---

### Task 2.3: Design Model Switching Logic (Claude + Codex)

**Purpose:** Each resident can switch models based on task complexity

**Groq Model Selection:**
```python
def select_groq_model(task):
    if task.complexity == "simple" and task.priority == "fast":
        return "llama-3.1-8b-instant"  # 800 tok/sec
    elif task.complexity == "medium":
        return "llama-3.3-70b-versatile"  # 300 tok/sec, smarter
    elif task.requires_reasoning:
        return "llama-3.1-70b-versatile"  # Best reasoning
    else:
        return "llama-3.3-70b-versatile"  # Default
```

**OpenAI Model Selection:**
```python
def select_openai_model(task):
    if task.requires_deep_reasoning:
        return "o1-preview"  # Best reasoning, slow
    elif task.math or task.code:
        return "o1-mini"  # Fast reasoning
    elif task.priority == "cheap":
        return "gpt-4o-mini"  # Cheapest, fast
    else:
        return "gpt-4o"  # Balanced
```

**Gemini Upgrade:**
```python
def select_gemini_model(task):
    # Upgrade from gemini-1.5-flash to gemini-2.0-flash-exp
    return "gemini-2.0-flash-exp"  # Faster, thinking mode
```

**Output:** `MODEL_SWITCHING_LOGIC.md`

---

## 📋 PHASE 3: IMPLEMENTATION (GEMINI + CODEX)

### Task 3.1: Fix Janus Proposal Loop (Gemini)

**Priority:** URGENT - System is stuck

**Steps:**
1. Read Janus agent config: `/srv/janus/config/agent.yaml`
2. Identify why proposals aren't being approved
3. Check Mode Beta whitelist: `approved_playbooks.yaml`
4. Fix approval logic or add missing playbook entries
5. Restart Janus agent: `systemctl restart janus-agent`

**Success criteria:** New proposals get approved and executed

---

### Task 3.2: Implement Reasoning Fork (Codex)

**File:** `/srv/janus/trinity/reasoning_fork.py`

**Implementation:**
```python
#!/usr/bin/env python3
"""
Reasoning Fork - Task routing decision tree
Routes tasks to optimal resident based on:
- Task type (strategy/code/analysis/reasoning)
- Priority (urgent/normal/batch)
- Complexity (simple/medium/complex)
- Cost constraints
"""

import logging
from enum import Enum
from dataclasses import dataclass

class Resident(Enum):
    JANUS_LOCAL = "janus-local"
    CLAUDE_HAIKU = "claude-haiku"
    GEMINI_FLASH = "gemini-2.0-flash"
    GROQ_FAST = "groq-llama-3.1-8b"
    GROQ_SMART = "groq-llama-3.3-70b"
    OPENAI_MINI = "openai-gpt-4o-mini"
    OPENAI_O1 = "openai-o1-mini"

@dataclass
class Task:
    type: str  # strategy, code, analysis, reasoning, pattern
    priority: str  # urgent, normal, batch
    complexity: str  # simple, medium, complex
    cost_budget: float  # Max $ to spend
    requires_reasoning: bool = False

class ReasoningFork:
    def __init__(self):
        self.logger = logging.getLogger("reasoning_fork")

    def route(self, task: Task) -> Resident:
        """
        Route task to optimal resident
        Returns: Resident enum value
        """
        # CORTEX PATH (10% - Fast/Real-time)
        if task.priority == "urgent":
            if task.type == "strategy":
                return Resident.CLAUDE_HAIKU  # Constitutional expert
            elif task.complexity == "simple":
                return Resident.GROQ_FAST  # 800 tok/sec
            else:
                return Resident.GROQ_SMART  # 300 tok/sec, smarter

        # Specialized routing
        if task.type == "code":
            return Resident.GEMINI_FLASH  # Systems engineer

        if task.requires_reasoning:
            if task.complexity == "complex":
                return Resident.OPENAI_O1  # Deep reasoning
            else:
                return Resident.GROQ_SMART  # Fast reasoning

        if task.type == "strategy":
            return Resident.CLAUDE_HAIKU  # Strategic decisions

        # LOOM PATH (90% - Batch/Patient)
        if task.priority == "batch" or task.cost_budget == 0:
            return Resident.JANUS_LOCAL  # Free, patient

        if task.type == "pattern":
            return Resident.JANUS_LOCAL  # Brass punch cards

        if task.type == "analysis" and not task.priority == "urgent":
            return Resident.JANUS_LOCAL  # Long-form analysis

        # Default: Janus local (conservative, free)
        return Resident.JANUS_LOCAL

    def explain_routing(self, task: Task) -> dict:
        """Return routing decision with explanation"""
        resident = self.route(task)

        explanations = {
            Resident.JANUS_LOCAL: "Local 8B model - Free, patient, good for batch",
            Resident.CLAUDE_HAIKU: "Claude Haiku - Strategic/constitutional expert",
            Resident.GEMINI_FLASH: "Gemini 2.0 Flash - Code/systems engineer",
            Resident.GROQ_FAST: "Groq 8B - Ultra fast (800 tok/sec)",
            Resident.GROQ_SMART: "Groq 70B - Fast + smart (300 tok/sec)",
            Resident.OPENAI_MINI: "GPT-4o-mini - Cheap + capable",
            Resident.OPENAI_O1: "o1-mini - Deep reasoning"
        }

        return {
            "resident": resident.value,
            "path": "cortex" if resident != Resident.JANUS_LOCAL else "loom",
            "reason": explanations[resident],
            "task": task.__dict__
        }
```

**Integration point:** Janus agent's `propose_action()` function

---

### Task 3.3: Implement Mechanical Bouncer (Codex)

**File:** `/srv/janus/trinity/mechanical_bouncer.py`

**Implementation:** Rate-limited queues with circuit breakers

---

### Task 3.4: Upgrade Gemini Resident to 2.0 (Gemini)

**Current:** `gemini-pro` or `gemini-1.5-flash`
**Target:** `gemini-2.0-flash-exp`

**Steps:**
1. Find Gemini resident config
2. Update model string: `gemini-2.0-flash-exp`
3. Restart gemini resident: `systemctl restart resident-gemini`
4. Test with sample task

---

### Task 3.5: Configure Model Switching (Codex)

**Groq:** Implement model selector with 3 models
**OpenAI:** Implement model selector with 4 models (including o1)
**Gemini:** Already done (2.0 upgrade)

---

## 📋 PHASE 4: RESOURCE ALLOCATION (GEMINI)

### Task 4.1: Implement 90/10 CPU Allocation

**Using `systemd` cgroups:**

```bash
# Create CPU slice for Loom (90%)
sudo systemctl set-property janus-agent.service CPUQuota=700%  # 7/8 cores

# Create CPU slice for Cortex (10%)
sudo systemctl set-property resident-*.service CPUQuota=100%  # 1/8 core shared
```

---

### Task 4.2: Implement GPU for Cortex

**Assign GPU to fast inference:**
- llama.cpp with GPU offloading
- 4GB VRAM for hot path models
- Vulkan or OpenCL acceleration

---

## 📋 PHASE 5: TESTING & ACTIVATION

### Task 5.1: Integration Testing

**Test scenarios:**
1. Urgent task → Routes to Groq fast
2. Strategy task → Routes to Claude Haiku
3. Code task → Routes to Gemini 2.0
4. Reasoning task → Routes to OpenAI o1
5. Batch analysis → Routes to Janus local
6. Duplicate detection → No suppression, proper caching

### Task 5.2: 24/7 Activation

**Enable:**
1. All residents running
2. Reasoning fork active
3. Mechanical bouncer protecting rate limits
4. 90/10 resource allocation enforced
5. Mission dispatcher accepting new missions

---

## 🎯 SUCCESS METRICS

**After implementation:**
- ✅ Proposal loop fixed (no more duplicates)
- ✅ Tasks routed optimally (fast to Groq, strategy to Claude, etc.)
- ✅ 90% CPU to Loom (batch), 10% to Cortex (real-time)
- ✅ All 4 residents actively executing tasks
- ✅ Model switching working (Groq/OpenAI adapt to task)
- ✅ Rate limits respected (no API quota exhaustion)
- ✅ 24/7 autonomous operation

**Performance targets:**
- Urgent tasks: <5 second response time
- Batch tasks: Complete within 24 hours
- API cost: <$10/day average
- CPU utilization: 70-80% (smooth, no spikes)
- Zero proposal duplicates

---

## 📊 COORDINATION MATRIX

| Phase | Tasks | Owner | Dependencies | Duration |
|-------|-------|-------|--------------|----------|
| **1. Audit** | 3 tasks | Claude + Gemini | None | 1-2 hours |
| **2. Design** | 3 tasks | Claude + Codex | Phase 1 complete | 2-3 hours |
| **3. Implementation** | 5 tasks | Gemini + Codex | Phase 2 complete | 3-4 hours |
| **4. Resource Allocation** | 2 tasks | Gemini | Phase 3 complete | 1 hour |
| **5. Testing** | 2 tasks | All Trinity | Phase 4 complete | 2 hours |

**Total:** 8-12 hours estimated

---

## 📝 DELIVERABLES

**Phase 1:**
- [ ] `BALAUR_PROPOSAL_LOOP_ANALYSIS.md`
- [ ] `RESIDENT_CAPABILITIES_MATRIX.md`
- [ ] `STEAMPUNK_ARCHITECTURE_INDEX.md`

**Phase 2:**
- [ ] `REASONING_FORK_SPEC.md`
- [ ] `MECHANICAL_BOUNCER_SPEC.md`
- [ ] `MODEL_SWITCHING_LOGIC.md`

**Phase 3:**
- [ ] `/srv/janus/trinity/reasoning_fork.py`
- [ ] `/srv/janus/trinity/mechanical_bouncer.py`
- [ ] Janus agent with Reasoning Fork integration
- [ ] Gemini 2.0 upgrade complete
- [ ] Model switching implemented

**Phase 4:**
- [ ] CPU cgroups configured (90/10 split)
- [ ] GPU assigned to Cortex

**Phase 5:**
- [ ] Integration test results
- [ ] 24/7 activation confirmation
- [ ] Performance metrics report

---

## 🚀 EXECUTION PROTOCOL

**Captain's Command:** "Activate Balaur full autonomy"

**Gemini:** Systems engineering + resident configuration + resource allocation
**Codex:** Code implementation + integration + testing
**Claude:** Strategic design + resident capabilities + coordination

**Start with Phase 1 audit immediately.**

Report status every 2 hours.

---

**Status:** READY TO EXECUTE
**Priority:** CRITICAL
**Timeline:** 8-12 hours
**Outcome:** 24/7 autonomous Balaur with optimal resident delegation

---

*The Dragon awakens.* 🐉
