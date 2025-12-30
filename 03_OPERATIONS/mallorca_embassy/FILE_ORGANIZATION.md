# File Organization - Mallorca Embassy

**Purpose**: Clear map for future Claude sessions to find what they need

---

## 🎯 ENTRY POINTS (Start Here)

**For new sessions:**
1. `START_HERE.md` - 5-minute orientation, tells you where everything is
2. `operations/ACTION_ITEMS.md` - What needs doing right now
3. `README.md` - Full mission overview (reference)

**Don't start anywhere else.** These 3 files will point you to everything else.

---

## 📁 DIRECTORY STRUCTURE (What Each Folder Contains)

### `/xyl_phos_cure/` - PROJECT CORE
**Purpose**: Everything about the €6M Horizon Europe project

**Key files:**
- `PROJECT_OVERVIEW.md` - Project summary, tech approach
- `STAGE1_STATUS.md` - Current submission status
- `TECHNICAL_ASSESSMENT_EVALUATOR_GRADE.md` - Deep technical analysis
- `STRATEGIC_ANALYSIS.md` - Full 76-page strategic plan
- `CONSORTIUM_STRATEGY.md` - Partner approach
- `PARTNER_RECONNAISSANCE.md` - Partner profiles (UIB, CIHEAM, etc.)
- `MULTI_ACTOR_APPROACH.md` - Farmer involvement framework

**When to read:**
- Need project context? → `PROJECT_OVERVIEW.md`
- Current status? → `STAGE1_STATUS.md`
- Technical details for proposal? → `TECHNICAL_ASSESSMENT_EVALUATOR_GRADE.md`

---

### `/operations/` - EXECUTION & TRACKING
**Purpose**: Day-to-day task management and decision logging

**Key files:**
- `ACTION_ITEMS.md` - Prioritized TODO list ← **CHECK THIS OFTEN**
- `TIMELINE.md` - Critical dates and deadlines
- `CONTACT_LOG.md` - Partner outreach tracking
- `DECISION_LOG.md` - Decision audit trail

**When to read:**
- What should I do? → `ACTION_ITEMS.md`
- When are deadlines? → `TIMELINE.md`
- Who have we contacted? → `CONTACT_LOG.md`

**When to write:**
- Completed task → Update `ACTION_ITEMS.md`
- Made decision → Log in `DECISION_LOG.md`
- Contacted partner → Log in `CONTACT_LOG.md`

---

### `/strategic_intelligence/` - INTELLIGENCE & MONITORING
**Purpose**: Strategic reconnaissance and automated monitoring

**Key files:**
- `JANUS_PERPLEXITY_RECONNAISSANCE.md` - Syn's complete intel brief (UIB, CIHEAM, competitive landscape)
- `PATTERN_ENGINE_CONFIG.md` - Monitoring datastream specs (reference)
- `PATTERN_ENGINE_INTEGRATION.md` - Operational scenarios (reference)

**When to read:**
- Need intel on UIB capabilities? → `JANUS_PERPLEXITY_RECONNAISSANCE.md`
- Understand monitoring system? → Read Pattern Engine docs

---

### `/property_intelligence/` - MALLORCA ASSETS
**Purpose**: Information about friend's property and cooperative network

**Status**: ⏳ **PENDING DATA COLLECTION**

**Key files:**
- `FRIEND_PROPERTY_SPECS.md` - Property details (TODO: Captain to collect)
- `COOPERATIVE_NETWORK.md` - Cooperative structure (TODO)
- `UIB_CONNECTIONS.md` - Research connection via daughter (TODO)
- `LIVING_LAB_PROPOSAL.md` - Field trial site specs (TODO)

**When to update:**
- Captain provides property info → Update `FRIEND_PROPERTY_SPECS.md`
- Get cooperative details → Update `COOPERATIVE_NETWORK.md`

---

### `/integration_strategy/` - STRATEGIC POSITIONING
**Purpose**: High-level strategic thinking, long-term vision

**Key files:**
- `CONVERGENCE_THESIS.md` - Why Mallorca + XYL-PHOS-CURE makes sense
- `DUAL_BASE_STRATEGY.md` - Mallorca + Málaga coordination
- `COMMERCIALIZATION_PATHWAY.md` - TRL 6→9, licensing, EIC strategy

**When to read:**
- Why are we doing this? → `CONVERGENCE_THESIS.md`
- Long-term commercialization? → `COMMERCIALIZATION_PATHWAY.md`

---

### `/reference/` - CROSS-REFERENCES & COORDINATION
**Purpose**: Links to other systems, Trinity coordination, archives

**Key files:**
- `ARCHIVE_LINKS.md` - Pointers to original XF docs in UBOS_MIXED_ARCHIVE
- `JANUS_TRINITY_COORDINATION.md` - Trinity protocol docs
- `BPC_PATTERN_ENGINE_DISCOVERY.yaml` - Brass Punch Card archive

**When to read:**
- Need original XF project docs? → `ARCHIVE_LINKS.md`
- Trinity coordination question? → `JANUS_TRINITY_COORDINATION.md`

---

### `/_docs_archive/` - HISTORICAL DOCUMENTS
**Purpose**: Completed docs, corrections, historical context

**Contains:**
- `CORRECTED_IMPLEMENTATION_SUMMARY.md` - What got fixed (historical)
- `PATTERN_ENGINE_DEPLOYMENT_SUMMARY.md` - Old summary (superseded by PATTERN_ENGINE_INTEGRATION_README)
- `IMPLEMENTATION_COMPLETE.md` - Completion notice (historical)

**When to read:**
- Rarely. Only if you need historical context about why something was done.

---

## 🔧 MAIN DIRECTORY FILES (Root Level)

### Core Entry Points
- **START_HERE.md** ← **READ THIS FIRST**
- **README.md** - Full mission overview
- **FILE_ORGANIZATION.md** - This file

### Pattern Engine Integration
- **MALLORCA_PATTERN_ENGINE_ADAPTER.py** - Executable Python code
- **MALLORCA_MISSION_SPEC.md** - Config file
- **PATTERN_ENGINE_INTEGRATION_README.md** - How it works, testing guide

**When to use:**
- Test monitoring? → Run `MALLORCA_PATTERN_ENGINE_ADAPTER.py`
- Understand monitoring? → Read `PATTERN_ENGINE_INTEGRATION_README.md`
- Change thresholds? → Edit `MALLORCA_MISSION_SPEC.md`

---

## 🎯 COMMON TASKS → WHERE TO LOOK

### "Captain just gave me new info about the friend's property"
→ Update `/property_intelligence/FRIEND_PROPERTY_SPECS.md`  
→ Log in `/operations/DECISION_LOG.md`

### "Stage 1 results are in - it's POSITIVE!"
→ Check `/operations/ACTION_ITEMS.md` for pre-planned actions  
→ Read `/xyl_phos_cure/CONSORTIUM_STRATEGY.md` for outreach plan  
→ Update `/xyl_phos_cure/STAGE1_STATUS.md` with results

### "Need to prepare Stage 2 proposal"
→ Read `/xyl_phos_cure/TECHNICAL_ASSESSMENT_EVALUATOR_GRADE.md` for content  
→ Read `/xyl_phos_cure/PARTNER_RECONNAISSANCE.md` for consortium details  
→ Read `/xyl_phos_cure/MULTI_ACTOR_APPROACH.md` for farmer involvement

### "Captain asks about UIB capabilities"
→ Read `/strategic_intelligence/JANUS_PERPLEXITY_RECONNAISSANCE.md`  
→ Check `/xyl_phos_cure/PARTNER_RECONNAISSANCE.md`

### "Need competitive intelligence"
→ Read `/strategic_intelligence/JANUS_PERPLEXITY_RECONNAISSANCE.md` (BeXyl, XF-ACTORS)  
→ Read `/xyl_phos_cure/STRATEGIC_ANALYSIS.md` (competitive positioning)

### "What's the technical assessment?"
→ Read `/xyl_phos_cure/TECHNICAL_ASSESSMENT_EVALUATOR_GRADE.md`

### "What are the immediate priorities?"
→ Read `/operations/ACTION_ITEMS.md` ← **START HERE ALWAYS**

---

## 🚫 WHAT NOT TO DO

❌ **Don't read all 25 files** - You'll waste time  
❌ **Don't start with archive docs** - Start with START_HERE.md  
❌ **Don't ignore ACTION_ITEMS.md** - This tells you what's urgent  
❌ **Don't edit core infrastructure files** - Pattern Engine, Oracle Bridge are separate systems  
❌ **Don't create new organizational schemes** - This one works, use it

---

## ✅ WORKFLOW FOR NEW SESSIONS

**1. Orient (5 minutes):**
- Read `START_HERE.md`
- Read `operations/ACTION_ITEMS.md`
- Check `xyl_phos_cure/STAGE1_STATUS.md` for latest status

**2. Execute (variable):**
- Work on highest priority item from ACTION_ITEMS.md
- Update relevant files as you go
- Log decisions in DECISION_LOG.md

**3. Update (5 minutes):**
- Mark completed items in ACTION_ITEMS.md
- Add new items discovered
- Update STAGE1_STATUS.md if status changed

---

## 📊 FILE COUNT BY TYPE

**Entry Points**: 3 files (START_HERE, README, FILE_ORGANIZATION)  
**Executable Code**: 1 file (MALLORCA_PATTERN_ENGINE_ADAPTER.py)  
**Configuration**: 1 file (MALLORCA_MISSION_SPEC.md)  
**Operations**: 4 files (ACTION_ITEMS, TIMELINE, CONTACT_LOG, DECISION_LOG)  
**Project Core**: 7 files (xyl_phos_cure/)  
**Intelligence**: 3 files (strategic_intelligence/)  
**Property**: 4 files (property_intelligence/ - pending data)  
**Integration Strategy**: 3 files  
**Reference**: 3 files  
**Archived**: 3 files (_docs_archive/)

**Total**: ~30 files, but you only need 3-5 for most tasks

---

## 🎯 GOLDEN RULE

**When in doubt:**
1. Read `START_HERE.md`
2. Check `operations/ACTION_ITEMS.md`
3. Execute highest priority item

**Everything else is reference material to support execution.**

---

**STATUS**: File organization complete, clear paths established  
**MAINTENANCE**: Update ACTION_ITEMS.md as mission progresses  
**NEXT REORGANIZATION**: Only if structure stops working (unlikely)

—Claude, File Organization Architecture

