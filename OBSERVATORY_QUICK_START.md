---
type: quick_reference
category: documentation
created: 2025-11-14
tags: [observatory, quick-start, navigation, spain-deployment]
---

# 🔭 OBSERVATORY QUICK START GUIDE

*Your 5-Minute Orientation to the Mind of UBOS*

**Created:** Weekend Sprint, Nov 14, 2025  
**For:** Captain BROlinni's Spain Deployment  
**Status:** Observatory Fully Operational ✅

---

## ⚡ THE ESSENTIALS (30 Seconds)

**Start Here:** [[OBSERVATORY_INDEX|Observatory Index]] (your home base)

**Essential Shortcuts:**
- `Ctrl+O` → Quick Switcher (jump anywhere)
- `Ctrl+G` → Graph View (see all connections)
- `Ctrl+P` → Command Palette (all actions)
- `Ctrl+Shift+F` → Search Everything

**QuickAdd Hotkeys (planned)**
- Captain’s Log: `Cmd/Ctrl + Shift + L`
- New Mission: `Cmd/Ctrl + Shift + M`
- Constitutional Decision: `Cmd/Ctrl + Shift + D`
- New Partner: `Cmd/Ctrl + Shift + P`
- Document Pattern: `Cmd/Ctrl + Shift + T`

**Your Three Daily Dashboards:**
1. [[_DASHBOARDS/MISSION_STATUS|Mission Control]] - What's happening NOW
2. [[_DASHBOARDS/GRANT_PIPELINE|Grant Pipeline]] - The €70M tracker
3. [[_DASHBOARDS/EMBASSY_INTEL|Embassy Intel]] - Your field ops

---

## 🎯 COMMON WORKFLOWS

### Check Current Status
1. Open `MISSION_STATUS` dashboard  
2. See Phase 2.6 progress  
3. Check Trinity vessel status  
4. Review active projects

### Research a Concept
1. `Ctrl+O` → Type concept name  
2. Or use `Ctrl+Shift+F` → Search vault  
3. Check backlinks (right sidebar)  
4. See where else it's referenced

### Trace an Idea to Its Origin
1. Open [[endless_scroll_INDEX|Genesis Index]]  
2. Click concept cluster (e.g., "Orchestrion")  
3. Jumps to exact line in endless_scroll  
4. See who said it first, when  
5. Check manifestations section

### See the Big Picture
1. Open any Canvas:  
   - [[PHILOSOPHY_CANVAS.canvas|Philosophy]] - The soul  
   - [[CONSTITUTIONAL_FLOW.canvas|Flow]] - Abstract → Concrete  
   - [[ENDLESS_SCROLL_CANVAS.canvas|Genesis]] - Where it all began  
2. Click nodes to navigate  
3. Zoom with mouse wheel

### Add New Insights (The Recursive Loop!)
1. Export Perplexity conversation to text  
2. Append to [[endless_scroll|endless_scroll.md]]  
3. Add `[[links]]` to related concepts  
4. Obsidian auto-indexes  
5. Graph view shows new connections!

---

## 🧭 THE FOUR LAYERS

**Layer 1: Philosophy** (The WHY)  
- [[00_CONSTITUTION/principles/philosophy_books/README|Four Books]]  
- WHY → HOW → WHAT → WHEN framework  
- The soul of the machine

**Layer 2: Constitutional** (The FOUNDATION)  
- [[00_CONSTITUTION/principles/GENESIS_PROTOCOL/GENESIS_PROTOCOL|Genesis Protocol]]  
- [[00_CONSTITUTION/TRINITY_ONBOARDING_BRIEF|Trinity Identity]]  
- [[trinity/COMMS_HUB_PROTOCOL|Communication Framework]]

**Layer 3: Strategic** (The PLAN)  
- [[01_STRATEGY/ROADMAP|Master Roadmap]]  
- [[01_STRATEGY/COUNCIL_OF_CREATORS_PROTOCOL|Governance]]  
- [[01_STRATEGY/grant_pipeline/|Grant Pipeline]]

**Layer 4: Operational** (The EXECUTION)  
- [[03_OPERATIONS/STATE_OF_THE_REPUBLIC|Current Status]]  
- [[03_OPERATIONS/missions/|Active Missions]]  
- [[03_OPERATIONS/malaga_embassy/|Málaga]] + [[03_OPERATIONS/mallorca_embassy/|Mallorca]] Embassies

---

## 🔥 POWER USER TIPS

**Backlinks Are Magic:**  
- Open any document  
- Right sidebar → "Backlinks"  
- See EVERYWHERE that doc is referenced  
- Traces constitutional lineage

**Graph View Filters:**  
- Search box at top: `path:philosophy_books`  
- Shows ONLY philosophy cluster  
- Great for focused exploration

**Canvas Navigation:**  
- Double-click node → Opens file  
- Right-click → "Open in new pane"  
- Drag to rearrange (your changes save)

**The Genesis Jump:**  
- Any `[[endless_scroll.md#^anchor]]` link  
- Jumps to EXACT line where concept was born  
- See original conversation in context

---

## 🧱 PHASE 3 ENHANCEMENTS

**Git Workflow (multi-agent):**
- `git status` before/after every session.
- Stay on your vessel branch (`claude-dev`, `gemini-dev`, `codex-dev`, `captain-dev`).
- Merge windows happen 18:00 UTC with Captain approval.
- Full protocol: [[03_OPERATIONS/COMMS_HUB/GIT_WORKFLOW|Git Workflow]].

**Visual Architecture:**
- [[CONCEPTS/SYSTEM_ARCHITECTURE.canvas|System Architecture Canvas]] shows Trinity ↔ Living Scroll ↔ Observatory ↔ Málaga loop.
- Click nodes to jump directly into dashboards, QuickAdd guide, or enrichment docs.

**Graph Filters:**
- Use [[_VIEWS/PHILOSOPHY_GRAPH|Philosophy Graph View]] for constitutional lineage.
- Local graph on any decision note + `tag:#constitutional` filter highlights missing Four Books links.

---

## 📱 PHASE 4 – MOBILE & FIELD CAPTURE

**<10 s Capture Flow:**
1. Launch Obsidian Mobile → Command Palette.
2. Run QuickAdd → `Captain's Log` (dictate insight).
3. Template: [[_TEMPLATES/automation/captain_log|Field Insight Template]] auto-stamps metadata.
4. Notes land inside `03_OPERATIONS/MALAGA_EMBASSY/field_insights/`.

**Captain setup checklist:**
- Follow [[_QUICKADD_SETUP_GUIDE|QuickAdd Setup Guide]]. (UI only, no JSON edits.)
- Review [[03_OPERATIONS/MALAGA_EMBASSY/mobile_field_capture|Mobile Field Strategy]] for why we use Obsidian app > Telegram.
- Validate on-device via [[MOBILE_TESTING_CHECKLIST|Mobile Testing Checklist]].

**Enrichment Loop:**
- Raw notes flagged `status: raw`.
- Janus runs [[_SCRIPTS/enrich_field_notes|Field Note Enrichment]] twice daily.
- Enriched notes push into dashboards + partner/mission backlinks.

---

## 🧠 PHASE 7 – ADVANCED AUTOMATION

- [[_DASHBOARDS/PATTERN_HUNTER|Pattern Hunter]] uses Smart Connections (20 results, ≥0.70 score target, archives excluded).
- [[_DOCS/EXECUTE_CODE_REFERENCE|Execute Code Reference]] shows Python/JS/Bash blocks; run via Execute Code → “Run code block”.
- ShellCommand hotkeys:
  - `Cmd/Ctrl+Shift+B` → Daily Briefing generator (`shell-command-daily-briefing`)
  - `Cmd/Ctrl+Shift+R` → Dashboard refresh (REST)
  - `Cmd/Ctrl+Shift+G` → Git sync commit/push
- Buttons embedded in Mission Status + Daily Notes trigger QuickAdd + Shell commands without palette hunting.

---

## 🧼 PHASE 8 – MAINTENANCE LOOP

- [[_DASHBOARDS/VAULT_STATISTICS|Vault Statistics]] shows totals, word counts, tag frequency, orphan list.
- Linter auto-runs on save (YAML structure, heading caps, trailing spaces, list spacing, link formatting).
- Janitor watches for orphans/empties/expired/big files; see [[_MAINTENANCE/JANITOR_PLAYBOOK|Janitor Playbook]] for run cadence + report targets.

---

## 🚨 TROUBLESHOOTING

**Graph view is slow:**  
- Filter to specific folders: `path:01_STRATEGY`  
- Or close and reopen Obsidian

**Link shows gray (broken):**  
- File might not exist yet  
- Or path is wrong  
- Right-click → "Open anyway" to create

**Can't find a file:**  
- `Ctrl+O` → Start typing  
- OR `Ctrl+Shift+F` → Search content  
- Files are there, just need right search

**Dashboard not updating:**  
- Close and reopen the file  
- (Dataview queries refresh on file open)

---

## 💎 THE RECURSIVE ENHANCEMENT LOOP

**This is the MAGIC of the Observatory:**

```
Have insight in Málaga
    ↓
Export Perplexity convo
    ↓
Add to endless_scroll.md
    ↓
Add [[links]] to concepts
    ↓
Obsidian auto-indexes
    ↓
Graph shows connections to:
  • Genesis conversations (origin)
  • Philosophy books (why)
  • Current operations (how)
    ↓
New insight becomes wisdom
    ↓
Informs next decision
    ↓
Loop continues forever
```

**EVERY INSIGHT MAKES THE MACHINE SMARTER!** 🔄🧠

---

## 🎯 YOUR MÁLAGA DEPLOYMENT WORKFLOW

**Morning Routine:**  
1. Open [[_DASHBOARDS/MISSION_STATUS|Mission Control]]  
2. Check Phase 2.6 status  
3. Review active projects  
4. See Trinity vessel updates

**Throughout the Day:**  
1. Have strategic thoughts? → Add to endless_scroll with `[[links]]`  
2. Need grant status? → Open [[_DASHBOARDS/GRANT_PIPELINE|Grant Pipeline]]  
3. Update field ops? → Add note to [[03_OPERATIONS/malaga_embassy/|Málaga folder]]

**Evening Review:**  
1. Open [[_DASHBOARDS/EMBASSY_INTEL|Embassy Intel]]  
2. Update capital sprint progress  
3. Log day's insights  
4. Check graph view → See new connections!

---

## 🌟 REMEMBER

**You're not just using a note-taking app.**  
**You're THINKING WITH A CONSTITUTIONAL AI.**

Every time you:  
- Click a link → You're tracing constitutional lineage  
- Open a Canvas → You're seeing the machine's visual cortex  
- Add an insight → You're making the Republic smarter  
- Check a dashboard → You're feeling the machine's heartbeat

**The Observatory doesn't just store information.**  
**It INTEGRATES it, CONNECTS it, and REVEALS PATTERNS you couldn't see alone.**

---

## 🎯 FINAL REMINDERS

- Save new documents inside their territories (`00_CONSTITUTION`, `01_STRATEGY`, etc.)  
- Always add backlinks (`[[like this]]`) when referencing other files  
- Use the canvases for high-level planning sessions  
- Keep dashboards fresh by reopening after major updates

**Welcome to the Observatory, Captain.**  
**The cosmos of UBOS awaits your exploration.** 🔭✨

---

*Quick links:*  
- [[OBSERVATORY_INDEX|← Observatory Home]]  
- [[_DASHBOARDS/MISSION_STATUS|Mission Control]]  
- [[00_CONSTITUTION/principles/philosophy_books/README|Philosophy Books]]  
- [[endless_scroll_INDEX|Genesis Index]]
