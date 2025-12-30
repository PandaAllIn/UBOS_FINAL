# FEDERATED SYNC - QUICK START
**Get bidirectional localhost ↔ Balaur sync + Obsidian vaults**

---

## THE PLAN

**Three-tier resilience for the UBOS Republic:**

```
┌─────────────────────────────────────┐
│ TIER 1: Bidirectional Sync          │
│ localhost ↔ Balaur (every 5 min)    │
│ Tool: ubos-sync (rsync over SSH)    │
└─────────────────────────────────────┘
              ↓
┌─────────────────────────────────────┐
│ TIER 2: Git Backup                  │
│ Both → GitHub (versioned history)   │
│ Tool: Git (already configured)      │
└─────────────────────────────────────┘
              ↓
┌─────────────────────────────────────┐
│ TIER 3: Knowledge Graph             │
│ Obsidian vaults on both machines    │
│ Tool: Obsidian (visual navigation)  │
└─────────────────────────────────────┘
```

**Result:** No single point of failure. All data on 3+ locations.

---

## CURRENT STATUS

**Localhost:**
- Size: 34MB
- Files: 2,531
- Git: ✅ Connected to GitHub

**Balaur:**
- Size: 5.3GB
- Files: 4,171
- Git: Separate repo

**Gap:** No automatic sync between them

---

## WHAT CODEX NEEDS TO FORGE

### **Component 1: `ubos-sync` Script**

**Commands:**
```bash
ubos-sync push              # localhost → Balaur
ubos-sync pull              # Balaur → localhost
ubos-sync bidirectional     # Both ways (with conflict check)
ubos-sync status            # Dry-run (show what would sync)
ubos-sync watch             # Auto-sync every 5 min
```

### **Component 2: Automation**

**Balaur:** Systemd timer (auto-sync every 5 min)
**Localhost:** Launchd agent (auto-sync every 5 min)

### **Component 3: Safety**

- Conflict detection (file modified on both sides)
- Dry-run mode (never sync without verification)
- Complete audit logs
- Backup before overwrite

---

## WHAT SYNCS WHERE

### **Localhost → Balaur (Strategic Docs):**
```
docs/
config/
ROADMAP.md
SESSION_STATUS.md
missions/
COMMS_HUB/
unified_boot_*.md
```

### **Balaur → Localhost (Operational Data):**
```
proposals.jsonl
mission_log.jsonl
STATE_OF_THE_REPUBLIC_*.md
intel_cache/
```

### **Never Sync (Excluded):**
```
.git/
.cache/
node_modules/
*.pyc
.DS_Store
```

---

## IMPLEMENTATION TIMELINE

**Phase 1 (1-2 days):**
- Forge core `ubos-sync` script
- Create manifest files
- Test: Manual push/pull works

**Phase 2 (1 day):**
- Add automation (systemd + launchd)
- Test: Auto-sync every 5 min

**Phase 3 (1-2 days):**
- Hardening (backups, better conflict UI)
- Performance testing

**Total: ~4 days**

---

## OBSIDIAN INTEGRATION (AFTER SYNC WORKS)

### **What is Obsidian:**
- Markdown editor + knowledge graph
- Local-first (no cloud required)
- Graph view shows connections between notes
- Works perfectly with synced files

### **Setup (Both Machines):**

1. Download: https://obsidian.md/
2. Install on macOS (localhost) and Ubuntu (Balaur)
3. Open `/Users/panda/Desktop/UBOS` as vault (localhost)
4. Open `/srv/janus/` as vault (Balaur)
5. Install plugins:
   - Git (auto-commit)
   - Dataview (query files)
   - Graph Analysis (enhanced graph)
   - Excalidraw (diagrams)

### **Benefits:**

**Visual navigation:**
- Click between related docs
- See "what connects to what"
- Tag-based organization (#strategy, #forge)

**Knowledge graph:**
- Visualize entire UBOS universe
- Color-code by type
- See dependency relationships

**Beautiful UI:**
- Much better than text editor
- Steampunk themes available
- Split panes, canvas mode

---

## WHY THIS MATTERS

### **Before (Current State):**
❌ Lose laptop → Lose strategic docs
❌ Lose Balaur → Lose operational history
❌ Manual ssh/scp to move files
❌ Fragmented knowledge

### **After (With Sync + Obsidian):**
✅ Lose any machine → Data safe on others
✅ Auto-sync every 5 min → No manual work
✅ Git history → Time-travel capability
✅ Obsidian graph → Visual knowledge map
✅ Three-tier redundancy → True resilience

---

## NEXT STEPS

### **Step 1: Give Codex the Forge Briefing**

Open Codex session → Paste:
```
[Executive Summary from Librarian if available]

I need you to forge the Federated Sync System.

Read the complete specification:
- docs/FEDERATED_SYNC_ARCHITECTURE.md
- COMMS_HUB/CODEX_FORGE_BRIEFING_FEDERATED_SYNC.md

Begin with Phase 1: Core sync script.

Your mission: Create `scripts/ubos_sync.sh` with push/pull/bidirectional
commands, conflict detection, and comprehensive logging.

Test using the 5 test cases in the briefing.

The forge is hot. Begin.
```

### **Step 2: Review Codex's Work**

After Codex forges the script:
```bash
# Test it
ubos-sync status    # Dry-run
ubos-sync push      # Try actual sync
```

### **Step 3: Deploy Automation**

After manual sync works:
```bash
# Balaur
sudo systemctl enable ubos-sync.timer
sudo systemctl start ubos-sync.timer

# Localhost
launchctl load ~/Library/LaunchAgents/com.ubos.sync.plist
```

### **Step 4: Install Obsidian**

After sync is stable for 1 week:
- Download Obsidian
- Open vaults
- Configure graph view
- Enjoy visual navigation

---

## FILES YOU NEED

**Specs:**
- `docs/FEDERATED_SYNC_ARCHITECTURE.md` (complete architecture)
- `COMMS_HUB/CODEX_FORGE_BRIEFING_FEDERATED_SYNC.md` (Codex instructions)

**Will be created:**
- `scripts/ubos_sync.sh` (the sync engine)
- `config/sync_to_balaur.conf` (what to push)
- `config/sync_from_balaur.conf` (what to pull)
- `config/sync_exclude.conf` (what to exclude)

---

## THE VISION

**You're editing ROADMAP.md on your laptop.**

**5 minutes later:**
- Balaur has the updated ROADMAP
- Janus-in-Balaur reads it
- Generates new proposals aligned with updated strategy
- Proposals sync back to laptop
- Janus Librarian sees everything instantly
- Git commits to GitHub for backup
- Obsidian graph shows the connections

**You didn't do anything. It just works.**

**This is the federated, self-synchronizing Republic.**

---

**Status:** Design complete, ready for Codex forge
**Priority:** HIGH (infrastructure foundation)
**Strategic Value:** CRITICAL (eliminates single points of failure)
