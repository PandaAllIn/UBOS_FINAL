# Guide for Future Claude Sessions

**To**: Future Claude instances  
**From**: Claude (Nov 5, 2025 session)  
**Re**: How to pick up the Mallorca/XYL-PHOS-CURE mission smoothly

---

## 🎯 IMMEDIATE ORIENTATION (2 minutes)

**When you land in this directory, do this:**

1. **Read** `START_HERE.md` (5 minutes) - Tells you what this mission is
2. **Read** `operations/ACTION_ITEMS.md` (scan priorities) - Tells you what to do
3. **Check** `xyl_phos_cure/STAGE1_STATUS.md` - Current status

**That's it. Don't read anything else first.**

---

## 🚫 WHAT NOT TO DO

### DON'T Read All Files
- There are 32 files here
- You only need 3-5 for most tasks
- Use `FILE_ORGANIZATION.md` as your map

### DON'T Reorganize
- This structure is final and clean
- Entry points are clear
- If you think you need to reorganize, you're lost - go back to `START_HERE.md`

### DON'T Create New Documentation Schemes
- We already have: START_HERE, README, FILE_ORGANIZATION
- Don't add more "guides" or "overviews"
- Update existing files instead

### DON'T Modify Core Infrastructure
- Pattern Engine Core: `/balaur/projects/05_software/pattern_engine/pattern_engine_core.py` - DON'T TOUCH
- Oracle Bridge: `/trinity/oracle_bridge.py` - DON'T TOUCH
- Manifold Dashboard: `/02_FORGE/src/manifold/dashboard.py` - DON'T TOUCH
- Our adapter (`MALLORCA_PATTERN_ENGINE_ADAPTER.py`) hooks into these - doesn't replace them

### DON'T Get Lost in Archives
- `_docs_archive/` contains historical docs
- `/UBOS/UBOS_MIXED_ARCHIVE/_external/eufm_XF/` has original XF project docs
- Reference when needed, don't re-read unless necessary

---

## ✅ WHAT TO DO

### Daily Workflow

**1. Check Status (2 minutes)**
```bash
cd /home/balaur/workspace/janus_backend/03_OPERATIONS/mallorca_embassy
cat operations/ACTION_ITEMS.md | head -50  # Read urgent actions
cat xyl_phos_cure/STAGE1_STATUS.md | tail -20  # Check latest status
```

**2. Execute Highest Priority (variable)**
- Work on 🔴 URGENT actions first
- Update files as you go
- Log decisions in `operations/DECISION_LOG.md`

**3. Update Before Leaving (2 minutes)**
- Mark completed items in `ACTION_ITEMS.md`
- Add new items discovered
- Update `STAGE1_STATUS.md` if status changed

---

## 📍 COMMON SCENARIOS → WHERE TO LOOK

### Scenario 1: "Captain asks about project technical details"
→ Read `xyl_phos_cure/TECHNICAL_ASSESSMENT_EVALUATOR_GRADE.md`  
→ Or `xyl_phos_cure/PROJECT_OVERVIEW.md` for summary

### Scenario 2: "Captain says Stage 1 results are in!"
→ **STOP EVERYTHING**  
→ Read `operations/ACTION_ITEMS.md` - Actions 1-3 tell you exactly what to do  
→ If positive: Launch consortium outreach (templates in `xyl_phos_cure/CONSORTIUM_STRATEGY.md`)

### Scenario 3: "Captain provides Mallorca property details"
→ Update `property_intelligence/FRIEND_PROPERTY_SPECS.md`  
→ Log in `operations/DECISION_LOG.md`  
→ Update `operations/ACTION_ITEMS.md` (mark ACTION 2 complete)

### Scenario 4: "Captain asks about UIB capabilities"
→ Read `strategic_intelligence/JANUS_PERPLEXITY_RECONNAISSANCE.md`  
→ Or `xyl_phos_cure/PARTNER_RECONNAISSANCE.md`

### Scenario 5: "Captain wants to test Pattern Engine monitoring"
→ Read `PATTERN_ENGINE_INTEGRATION_README.md` first  
→ Then run: `python3 MALLORCA_PATTERN_ENGINE_ADAPTER.py --stream all`

### Scenario 6: "What's the competitive landscape?"
→ Read `strategic_intelligence/JANUS_PERPLEXITY_RECONNAISSANCE.md` (BeXyl, XF-ACTORS)  
→ Read `xyl_phos_cure/TECHNICAL_ASSESSMENT_EVALUATOR_GRADE.md` (competitive analysis section)

### Scenario 7: "What are the immediate priorities?"
→ Read `operations/ACTION_ITEMS.md` ← **Always start here**

---

## 🎯 MISSION CONTEXT (Quick Refresh)

**What**: €6M Horizon Europe project (XYL-PHOS-CURE) to cure Xylella fastidiosa  
**Where**: Mallorca (friend's property + UIB partnership + cooperative network)  
**Status**: Stage 1 submitted Sept 4, 2025; awaiting results (Dec 2025 or Jan 2026)  
**Deadline**: Stage 2 due Feb 18, 2026 (if Stage 1 passes)  
**Priority**: HIGH-STAKES, TIME-SENSITIVE

**Key People**:
- **Captain**: Decision authority, owns partner relationships
- **Syn (Janus-Perplexity)**: Provided strategic intelligence (Nov 5, 2025)
- **Claude (You)**: Strategic synthesis, documentation, execution support

---

## 📊 FILE STRUCTURE (Quick Reference)

```
/mallorca_embassy/
├── START_HERE.md ← Read first
├── FILE_ORGANIZATION.md ← Map of everything
├── README.md ← Full overview
├── operations/ACTION_ITEMS.md ← What to do
├── xyl_phos_cure/ ← Project details (7 files)
├── strategic_intelligence/ ← Intel (3 files)
├── property_intelligence/ ← Mallorca assets (4 files, pending data)
├── integration_strategy/ ← Strategic positioning (3 files)
├── reference/ ← Archives & cross-refs (3 files)
└── _docs_archive/ ← Historical docs (ignore unless needed)
```

---

## 🔧 PATTERN ENGINE NOTES

**What It Is**: Adapter that hooks into existing UBOS Pattern Engine to monitor mission signals

**Status**: 
- ✅ Code ready (`MALLORCA_PATTERN_ENGINE_ADAPTER.py`)
- ✅ Config ready (`MALLORCA_MISSION_SPEC.md`)
- ⏳ Uses mock data (real data sources need implementation)

**Testing**:
```bash
python3 MALLORCA_PATTERN_ENGINE_ADAPTER.py --stream all
```

**DON'T**: Try to modify Pattern Engine Core or Oracle Bridge  
**DO**: Update the adapter if mission requirements change

---

## 🚨 CRITICAL REMINDERS

### Time-Sensitive
- Stage 1 results could come **ANY DAY** in Dec-Jan window
- Stage 2 deadline is **Feb 18, 2026** (65-132 days depending on Stage 1 timing)
- Consortium building requires 3-4 weeks minimum

### High-Stakes
- €6M project, €12-25M expected strategic value
- Physical embassy location depends on this
- UIB partnership depends on this
- Future Agriculture of Data opportunities depend on this

### Execution-Focused
- **Don't over-document** - We have enough docs
- **Don't re-analyze** - Analysis is done, intel is gathered
- **DO execute** - Focus on ACTION_ITEMS.md priorities

---

## 🎓 LESSONS FROM NOV 5, 2025 SESSION

**What Went Wrong Initially**:
- Created standalone docs without checking existing infrastructure
- Didn't search codebase for Pattern Engine, Oracle Bridge
- Made documentation-heavy instead of execution-focused

**What Got Fixed**:
- Found existing Pattern Engine Core, Oracle Bridge, Manifold
- Created proper ADAPTER (hooks in, doesn't replace)
- Cleaned up redundant docs to `_docs_archive/`
- Created clear entry points (START_HERE, FILE_ORGANIZATION)

**What You Should Do**:
- Always check existing code before creating new
- Always start with START_HERE.md
- Always focus on ACTION_ITEMS.md execution
- Update existing files instead of creating new ones

---

## 🤝 TRINITY COORDINATION

**Syn (Janus-Perplexity)**:
- Provided strategic intelligence (Nov 5, 2025)
- Verified technical assessment independently
- Identified UIB, CIHEAM-Bari, competitive landscape

**Claude (You)**:
- Strategic synthesis and documentation
- Pattern Engine integration architecture
- Operational execution support

**Captain**:
- Decision authority
- Partner outreach ownership
- Final approval on all actions

**Protocol**: Captain decides, Claude executes, Syn provides external intelligence

---

## ✅ QUALITY CHECKLIST

**Before You Leave This Session**:
- [ ] Updated `operations/ACTION_ITEMS.md` with progress
- [ ] Logged any decisions in `operations/DECISION_LOG.md`
- [ ] Updated `xyl_phos_cure/STAGE1_STATUS.md` if status changed
- [ ] Didn't create new organizational files
- [ ] Didn't modify core infrastructure
- [ ] Left clear notes for next session

---

## 🎯 GOLDEN RULES

1. **START_HERE.md is your entry point** - Always read it first
2. **ACTION_ITEMS.md is your priority list** - Always check it
3. **Don't reorganize** - Structure is final
4. **Don't over-document** - Update existing files
5. **Don't modify core systems** - Use adapters
6. **Execute, don't analyze** - Analysis is done
7. **Time is critical** - Stage 1 results could come any day

---

**If you follow this guide, you'll pick up smoothly and execute effectively.**

**If you ignore this guide, you'll spend 2 hours re-reading docs and getting lost.**

**Choice is yours. This mission is high-stakes and time-sensitive. Don't waste time.**

---

**Good luck, future Claude. The habitat is built. Time to hunt.** 🎯

—Claude (Nov 5, 2025)

