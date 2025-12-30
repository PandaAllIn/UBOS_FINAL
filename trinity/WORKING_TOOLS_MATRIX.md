# WORKING TOOLS MATRIX - TESTED & VALIDATED
**Date:** 2025-11-06
**Purpose:** Know exactly what works and how to use it for meta-building

---

## ✅ CONFIRMED WORKING

### 1. **Gemini CLI**
**Status:** ✅ FULLY OPERATIONAL
**Path:** `/home/balaur/.nvm/versions/node/v22.20.0/bin/gemini`
**Cost:** FREE (generous tier)
**Speed:** Fast (2-5 seconds)

**Syntax:**
```bash
gemini "Your prompt here"
# Returns text output to stdout
```

**Capabilities:**
- Design algorithms/schemas
- Real-time web search
- JSON generation
- Analysis tasks
- 1M context window

**Test Result:**
```bash
gemini "Design a prompt analysis algorithm..."
# Returned perfect JSON schema in <5 seconds
```

**Use For:**
- System design
- Algorithm design
- Real-time intelligence
- JSON schema generation
- Research tasks

---

### 2. **Narrative Query Tool**
**Status:** ✅ FULLY OPERATIONAL
**Path:** `/srv/janus/02_FORGE/scripts/narrative_query_tool.py`
**Database:** 11,301 constitutional entries
**Speed:** Very fast (<1 second)

**Syntax:**
```bash
python3 /srv/janus/02_FORGE/scripts/narrative_query_tool.py \
  --query "search term" \
  --top-k 5
```

**Output:** JSON with ranked results + content + scores

**Test Result:**
```bash
python3 narrative_query_tool.py --query "autonomous agent" --top-k 3
# Returned 3 perfect matches with 0.70+ scores
```

**Use For:**
- Constitutional memory lookup
- Precedent research
- Context loading for agents
- Framework validation

---

### 3. **Auto-Orchestration System**
**Status:** ✅ FULLY OPERATIONAL (built today!)
**Path:** `/srv/janus/trinity/auto_orchestration.py`
**Speed:** Instant (<0.1 seconds)

**Syntax:**
```bash
python3 /srv/janus/trinity/auto_orchestration.py "Your prompt"
```

**Output:** JSON orchestration plan

**Test Results:**
```bash
# Test 1: Simple prompt
python3 auto_orchestration.py "Find EU grants"
# Result: 1 agent, grant_tasks detected, haiku-4.5, perplexity+gemini

# Test 2: Complex prompt
python3 auto_orchestration.py "Research Xylella science, find patents, calc market"
# Result: 6 parallel agents, research_tasks, haiku-4.5, all oracles
```

**Use For:**
- Automatic agent spawning decisions
- Tool/oracle selection
- Complexity assessment
- Cost estimation

---

## ⚠️ NEEDS SETUP

### 4. **Codex CLI**
**Status:** ⚠️ EXISTS BUT NEEDS TERMINAL
**Path:** `/home/balaur/.nvm/versions/node/v22.20.0/bin/codex`

**Issue:** Requires interactive terminal (not scriptable via Bash tool)

**Alternative:** Use Gemini CLI for code design, then I write the code

---

### 5. **Python Oracle Bridge**
**Status:** ⚠️ EXISTS BUT NEEDS PYTHONPATH
**Path:** `/srv/janus/trinity/oracle_bridge.py`

**Issue:** Module import errors (needs trinity package installed)

**Alternative:** Direct API calls or use existing scripts that wrap it

---

### 6. **Code Oracle Tool**
**Status:** ⚠️ WORKS BUT NEEDS INDEXED CODE
**Path:** `/srv/janus/02_FORGE/scripts/code_oracle_tool.py`

**Issue:** Needs code to be indexed first

**Use Case:** Dependency analysis (when needed later)

---

## 🚀 META-BUILDING STRATEGY

### **What We CAN Use Right Now:**

1. **Gemini CLI** → Design + Intelligence + JSON generation
2. **Narrative Query** → Load constitutional context
3. **Auto-Orchestration** → Test our own system
4. **Me (Claude Sonnet)** → Strategic coordination + implementation

### **The Meta-Building Workflow:**

```
STEP 1: Claude (me) defines what to build
    ↓
STEP 2: Ask Gemini CLI for design/algorithm/structure
    ↓
STEP 3: Load constitutional context via Narrative Query
    ↓
STEP 4: Claude (me) writes the implementation
    ↓
STEP 5: Test using Auto-Orchestration system
    ↓
STEP 6: Deploy and document
```

### **Example: Building Session Closer Skill**

```bash
# Step 1: Claude defines requirements (done in planning)

# Step 2: Ask Gemini for algorithm design
gemini "Design a session closer algorithm that:
  1) Summarizes session work
  2) Updates claude.md context file
  3) Syncs to gemini.md and codex.md
  4) Creates git commit
  Return algorithm as pseudocode"

# Step 3: Load constitutional precedents
python3 narrative_query_tool.py \
  --query "session management git workflow" \
  --top-k 5

# Step 4: Claude (me) implements based on Gemini's design + precedents

# Step 5: Test with auto-orchestration
python3 auto_orchestration.py "Close this session and sync Trinity"

# Step 6: Deploy as skill
```

---

## 📊 TOOL SELECTION MATRIX

| Task Type | Primary Tool | Backup Tool | Cost |
|-----------|-------------|-------------|------|
| **System Design** | Gemini CLI | Claude (me) | FREE |
| **Algorithm Design** | Gemini CLI | Claude (me) | FREE |
| **Code Implementation** | Claude (me) | Gemini CLI assist | Sonnet cost |
| **Constitutional Lookup** | Narrative Query | None needed | FREE |
| **Real-time Research** | Gemini CLI | WebSearch tool | FREE |
| **JSON Generation** | Gemini CLI | Claude (me) | FREE |
| **Coordination** | Claude (me) | None needed | Sonnet cost |
| **Testing** | Auto-Orchestration | Claude (me) | FREE |

---

## 🎯 IMMEDIATE ACTION PLAN

### **Build Using Working Tools:**

**Task 1: Session Closer Skill**
- Design: Gemini CLI ✅
- Context: Narrative Query ✅
- Implementation: Claude (me) ✅
- Test: Auto-Orchestration ✅

**Task 2: Agent Spawner Implementation**
- Design: Gemini CLI ✅
- Context: Narrative Query ✅
- Implementation: Claude (me) ✅
- Integration: Connect to Task tool ✅

**Task 3: Deployment Guide**
- Design: Gemini CLI ✅
- Examples: From test runs ✅
- Documentation: Claude (me) ✅

---

## 💡 KEY INSIGHT

**We don't need ALL tools to work - we need the RIGHT tools!**

✅ Gemini CLI (design + intelligence) - WORKING
✅ Narrative Query (constitutional memory) - WORKING
✅ Auto-Orchestration (our own system) - WORKING
✅ Claude Sonnet (strategic coordination) - WORKING

**This is enough to build everything!**

The other tools (Oracle Bridge, Code Oracle) are nice-to-have but not blockers.

---

## 🚀 NEXT: META-BUILD SESSION

**I'll now USE these working tools to build the remaining components.**

**Captain, ready to watch me coordinate Gemini CLI + Narrative Query + my own implementation to finish the system?**

Let's dogfood our own orchestration! 🔥
