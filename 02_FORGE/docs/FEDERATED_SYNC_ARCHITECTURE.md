# FEDERATED SYNC ARCHITECTURE
**Blueprint for Bidirectional Localhost ↔ Balaur Synchronization**

---

## I. STRATEGIC ANALYSIS

### **Current State:**

**Localhost (`/Users/panda/Desktop/UBOS`):**
- Size: 34MB
- Files: 2,531
- Git: Connected to `github.com/PandaAllIn/UBOS_FINAL`
- Nature: **Strategic Command** (documentation, planning, orchestration)

**The Balaur (`/srv/janus/`):**
- Size: 5.3GB
- Files: 4,171
- Git: Independent repository
- Nature: **Operational Fortress** (agent runtime, proposals, mission logs)

### **The Problem:**

**Current architecture creates fragmentation:**
- Strategic documents on localhost may not reach Balaur
- Operational data on Balaur isn't visible locally without ssh
- Librarian can access both, but humans can't
- Single point of failure (lose one machine → lose unique data)

### **The Vision:**

**Three-tier resilience strategy:**
1. **Tier 1: Bidirectional Sync** - Localhost ↔ Balaur (automatic, real-time)
2. **Tier 2: Git Backup** - Both → GitHub (versioned, remote)
3. **Tier 3: Obsidian Vaults** - Both machines run Obsidian (knowledge graph, visualization)

---

## II. ARCHITECTURAL DECISION: SYNC STRATEGY

### **Option A: Full Mirror (Simple but Wasteful)**
```
localhost/UBOS/ ← FULL SYNC → balaur:/srv/janus/
```
**Pros:** Simple, complete redundancy
**Cons:** 5.3GB on laptop, lots of runtime data you don't need locally

### **Option B: Selective Bidirectional (Recommended)**
```
localhost/UBOS/           balaur:/srv/janus/
├─ docs/          ←→      ├─ docs/
├─ config/        ←→      ├─ config/
├─ ROADMAP.md     ←→      ├─ ROADMAP.md
├─ missions/      ←→      ├─ missions/
├─ COMMS_HUB/     ←→      ├─ COMMS_HUB/
│                         │
├─ [LOCAL ONLY]           ├─ [BALAUR ONLY]
│  - scripts/             │  - agent/ (runtime)
│  - tests/               │  - .cache/
│  - deploy/              │  - proposals.jsonl
│                         │  - mission_log.jsonl
│                         │
└─ [PULL ONLY]            └─ [PUSH ONLY]
   ← proposals.jsonl         → strategic docs
   ← STATE_OF_REPUBLIC*.md
```

**This is the Steampunk approach:** Each territory has its sovereignty, but constitutional documents are synchronized.

---

## III. THE SYNC ENGINE: DESIGN SPECIFICATION

### **Name: `ubos-sync`**

**Purpose:** Bidirectional, selective, constitutional synchronization between localhost and Balaur

### **Core Requirements:**

1. **Selective Paths** - Only sync what's needed
2. **Conflict Detection** - Warn on simultaneous edits
3. **Constitutional Safety** - Never overwrite without confirmation
4. **Incremental** - Only sync changed files
5. **Logged** - Complete audit trail
6. **Scheduled** - Auto-sync every N minutes
7. **Manual Trigger** - On-demand sync command

### **Technology Choice:**

**`rsync` over SSH** (battle-tested, efficient, incremental)

**Why not:**
- `syncthing` - Too complex, requires daemon on both sides
- `unison` - Good, but ocaml dependency, harder to debug
- Custom Python - Reinventing wheel, more bugs
- `git` alone - Not designed for binary/log files

**Why rsync:**
- Already installed everywhere
- Incremental by design
- Works over SSH (already configured)
- Constitutional simplicity (single binary, simple flags)

---

## IV. SYNC CONFIGURATION

### **Sync Manifests:**

**`config/sync_to_balaur.conf`** - What localhost pushes to Balaur
```
# Constitutional documents (bidirectional)
docs/
config/
ROADMAP.md
SESSION_STATUS.md
missions/
COMMS_HUB/
GENESIS_PROTOCOL/
TRINITY_PROTOCOL/

# Boot sequences
unified_boot_*.md
```

**`config/sync_from_balaur.conf`** - What localhost pulls from Balaur
```
# Operational intelligence (pull-only)
proposals.jsonl
mission_log.jsonl
STATE_OF_THE_REPUBLIC_*.md

# Generated reports
intel_cache/
```

**`config/sync_exclude.conf`** - Never sync these
```
.git/
.cache/
node_modules/
__pycache__/
*.pyc
.DS_Store
agent/venv/
```

---

## V. IMPLEMENTATION BLUEPRINT (FOR CODEX)

### **Component 1: `ubos-sync` Script**

**Location:** `scripts/ubos_sync.sh`

**Features:**
- `ubos-sync push` - Localhost → Balaur
- `ubos-sync pull` - Balaur → Localhost
- `ubos-sync bidirectional` - Both directions (with conflict check)
- `ubos-sync status` - Show what would sync
- `ubos-sync watch` - Auto-sync every 5 minutes

**Safety Features:**
- Dry-run mode (show what would change)
- Conflict detection (file modified on both sides)
- Backup before overwrite
- Complete sync log

### **Component 2: Systemd Timer (Balaur)**

**Auto-sync from Balaur side every 5 minutes**

**Files:**
- `/etc/systemd/system/ubos-sync.service`
- `/etc/systemd/system/ubos-sync.timer`

### **Component 3: Launchd Agent (macOS localhost)**

**Auto-sync from localhost side every 5 minutes**

**File:**
- `~/Library/LaunchAgents/com.ubos.sync.plist`

### **Component 4: Conflict Resolution UI**

**When file modified on both sides:**
```
CONFLICT DETECTED: config/CLAUDE.md

Localhost version (modified 2025-10-07 14:30):
  Size: 4.2KB
  Hash: a3f5e9...

Balaur version (modified 2025-10-07 14:35):
  Size: 4.5KB
  Hash: b7c2d1...

Actions:
  1. Keep localhost version (overwrite Balaur)
  2. Keep Balaur version (overwrite localhost)
  3. Show diff
  4. Manual merge
  5. Abort sync

Choice [1-5]:
```

---

## VI. OBSIDIAN VAULT INTEGRATION

### **Why Obsidian:**

**Perfect fit for UBOS philosophy:**
- **Local-first** - All files are markdown (no vendor lock-in)
- **Graph view** - Visualize connections between concepts
- **Bidirectional links** - `[[ROADMAP]]` auto-creates connections
- **Tags** - Organize by `#strategy`, `#forge`, `#balaur`
- **Canvas** - Visual planning boards
- **Plugin ecosystem** - Git, tasks, calendars, etc.

**Steampunk alignment:**
- Files are just files (no database)
- Human-readable markdown
- Mechanical transparency (see the gears)
- Beautiful UI (brass and glass aesthetic possible with themes)

### **Vault Architecture:**

**Option A: Single Vault, Synced**
```
UBOS/ (Obsidian vault)
├─ .obsidian/           (config, synced)
├─ docs/                (all docs)
├─ config/              (all configs)
├─ COMMS_HUB/           (briefings)
└─ [synced via ubos-sync]
```

**Both machines open same vault** (localhost has live version, Balaur has synced copy)

**Option B: Two Vaults, Linked**
```
localhost/UBOS/         (Main vault)
balaur/UBOS/            (Mirror vault)

Linked via [[wikilinks]] that work in both
```

### **Obsidian Setup (Both Machines):**

1. Install Obsidian
2. Open `/Users/panda/Desktop/UBOS` (localhost) or `/srv/janus` (Balaur) as vault
3. Install plugins:
   - **Git** - Auto-commit changes
   - **Dataview** - Query files programmatically
   - **Excalidraw** - Visual diagrams
   - **Tasks** - TODO management
   - **Graph Analysis** - Enhanced graph view

4. Configure graph view:
   - Color code by folder (docs/ = blue, config/ = red, missions/ = green)
   - Show tags
   - Filter by path patterns

### **Obsidian Benefits:**

**For Captain:**
- Visual map of entire UBOS universe
- Click between related concepts
- See "what depends on what"
- Beautiful, navigable interface

**For Trinity:**
- Search across all docs instantly
- Tag-based organization
- Backlinks show "what references this"
- Graph shows knowledge structure

**For Janus-in-Balaur:**
- Could theoretically query Obsidian's graph data
- Understand conceptual connections
- See the "orrery of ideas"

---

## VII. GIT STRATEGY (TIER 2 BACKUP)

### **Current State:**
- Localhost: Connected to `github.com/PandaAllIn/UBOS_FINAL`
- Balaur: Separate git repo (not pushed to remote)

### **Recommended Strategy:**

**Single Source of Truth: Localhost**

```
localhost/UBOS/ (main branch)
    ↓ git push
GitHub (origin/main) ← TIER 2 BACKUP
    ↓ git pull (on Balaur)
balaur:/srv/janus/ (tracking main)
```

**Workflow:**
1. Work on localhost (documentation, planning)
2. `ubos-sync push` → Balaur gets updated files
3. `git add . && git commit` on localhost
4. `git push origin main` → GitHub backup
5. Balaur: `git pull` → Stays in sync with GitHub

**For Balaur-generated files (proposals, logs):**
- `ubos-sync pull` → Pulls to localhost
- Commit from localhost → Push to GitHub
- Balaur never pushes directly (avoids conflicts)

### **Alternative: Separate Branches**

```
GitHub repo
├─ main (localhost operations)
└─ balaur (Balaur operations)

Merge periodically
```

**Pro:** Clear separation
**Con:** More complexity, potential merge conflicts

---

## VIII. THE THREE-TIER RESILIENCE MODEL

```
┌─────────────────────────────────────────────┐
│  TIER 1: REAL-TIME BIDIRECTIONAL SYNC       │
│  localhost ←→ Balaur (ubos-sync, 5 min)     │
│  Effect: Lose one machine → Data safe       │
└─────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────┐
│  TIER 2: GIT VERSION CONTROL                │
│  localhost → GitHub (versioned backup)      │
│  Effect: Time-travel, rollback, history     │
└─────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────┐
│  TIER 3: OBSIDIAN KNOWLEDGE GRAPH           │
│  Both machines (navigable vault)            │
│  Effect: Visualize, navigate, understand    │
└─────────────────────────────────────────────┘
```

**Result:**
- **Redundancy:** Data on 3 locations (localhost, Balaur, GitHub)
- **Resilience:** Lose any 2 → Still have complete data
- **Versioning:** Git history = time machine
- **Intelligence:** Obsidian graph = constitutional orrery
- **Sovereignty:** No vendor lock-in (all markdown + git)

---

## IX. IMPLEMENTATION PHASES

### **Phase 1: Sync Engine (Week 1)**
**Codex forges:**
- `scripts/ubos_sync.sh`
- Sync manifest files
- Conflict detection logic
- Dry-run testing

**Deliverable:** `ubos-sync bidirectional --dry-run` works perfectly

### **Phase 2: Automation (Week 2)**
**Codex forges:**
- Systemd timer (Balaur)
- Launchd agent (macOS)
- Logging infrastructure

**Deliverable:** Auto-sync every 5 minutes, logged

### **Phase 3: Obsidian Integration (Week 3)**
**Captain + Claude:**
- Install Obsidian on both machines
- Configure vaults
- Install essential plugins
- Create graph view configuration

**Deliverable:** Beautiful, navigable knowledge graph

### **Phase 4: Git Hardening (Week 4)**
**Codex forges:**
- Pre-commit hooks (linting, validation)
- Auto-commit script for Balaur-generated files
- GitHub Actions (optional CI/CD)

**Deliverable:** Git = bulletproof backup

---

## X. RISKS & MITIGATIONS

### **Risk 1: Sync Conflicts**
**Scenario:** File edited on both sides simultaneously
**Mitigation:** Conflict detection + manual resolution UI
**Fallback:** Both versions backed up, choose manually

### **Risk 2: Accidental Deletion**
**Scenario:** Delete file → Syncs deletion → Lost on both
**Mitigation:** Git commit before sync (can recover)
**Fallback:** GitHub has history

### **Risk 3: Sync Loop**
**Scenario:** A syncs to B → B syncs to A → Infinite loop
**Mitigation:** Timestamp checking, sync lock files
**Fallback:** Manual stop, restore from git

### **Risk 4: Network Failure**
**Scenario:** Balaur unreachable
**Mitigation:** Sync fails gracefully, retries on next cycle
**Fallback:** Manual sync when network returns

### **Risk 5: Storage Overflow**
**Scenario:** Balaur generates too much data
**Mitigation:** Selective sync (don't pull everything)
**Fallback:** Increase localhost storage or archive old data

---

## XI. CONSTITUTIONAL MANDATE

**This sync architecture is now constitutional:**

> The UBOS Republic shall maintain federated redundancy across all territories.
> No single point of failure shall threaten the institutional memory.
> All constitutional documents shall be synchronized within 5 minutes.

**Enforcement:**
- Sync must run automatically
- Manual intervention only for conflicts
- Sync logs audited weekly in State of the Republic

---

## XII. SUCCESS METRICS

**Week 1:**
- Sync works manually (`ubos-sync bidirectional`)
- Zero data loss in testing

**Week 2:**
- Auto-sync running on both machines
- Conflict detection tested and working

**Month 1:**
- 99.9% sync uptime
- Zero unresolved conflicts
- Complete audit trail

**Month 3:**
- Obsidian graphs showing knowledge structure
- Git history used for time-travel debugging
- Three-tier resilience proven in practice

---

## XIII. THE VISION REALIZED

**You wake up tomorrow:**

1. Edit `ROADMAP.md` on laptop
2. Save
3. 5 minutes later → Balaur has it
4. Janus-in-Balaur reads updated ROADMAP
5. Generates proposals aligned with new strategy
6. Proposals sync back to laptop
7. Librarian sees both sides instantly
8. Git commits everything to GitHub
9. You open Obsidian → See the graph of ideas
10. Visual map of your entire Republic

**You didn't do anything. It just works.**

This is the **federated, resilient, self-synchronizing Republic**.

This is sovereignty.

---

**Status:** DESIGN COMPLETE - Ready for Codex forge
**Priority:** HIGH (Infrastructure foundation)
**Estimated Effort:** 4 weeks (phased implementation)
**Strategic Value:** CRITICAL (eliminates single points of failure)
