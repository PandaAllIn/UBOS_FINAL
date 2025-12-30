# CODEX FORGE BRIEFING: FEDERATED SYNC SYSTEM
**Mission: Forge the `ubos-sync` Infrastructure**

---

## I. STRATEGIC CONTEXT

**FROM:** Claude (Master Strategist) / Janus
**TO:** Codex (Forgemaster)
**PRIORITY:** HIGH
**MISSION TYPE:** Infrastructure Foundation

### **The Strategic Problem:**

The UBOS Republic currently has a **single point of failure**:
- Critical docs only on localhost → Lose laptop = lose strategy
- Operational data only on Balaur → Lose Balaur = lose history
- Janus Librarian can see both, but humans can't without ssh

**We need federated resilience.**

### **The Strategic Solution:**

**Three-tier resilience:**
1. **Tier 1:** Bidirectional localhost ↔ Balaur sync (every 5 min)
2. **Tier 2:** Git backup to GitHub (versioned history)
3. **Tier 3:** Obsidian vaults on both machines (knowledge graph)

**Your mission: Forge Tier 1 (the sync engine)**

---

## II. TECHNICAL SPECIFICATION

### **Component Name:** `ubos-sync`

**Purpose:** Selective, bidirectional, conflict-aware synchronization

**Technology:** `rsync` over SSH (battle-tested, incremental, simple)

**Core Requirements:**
1. Selective paths (only sync what's needed)
2. Conflict detection (warn on simultaneous edits)
3. Incremental transfer (only changed files)
4. Complete audit log
5. Dry-run mode (safety first)
6. Manual + automatic modes

---

## III. COMPONENTS TO FORGE

### **Component 1: `scripts/ubos_sync.sh`**

**Main sync script**

**Commands:**
```bash
ubos-sync push              # localhost → Balaur
ubos-sync pull              # Balaur → localhost
ubos-sync bidirectional     # Both directions (with conflict check)
ubos-sync status            # Show what would sync (dry-run)
ubos-sync watch             # Continuous sync every 5 min
```

**Implementation Details:**

**Function 1: Load Config**
```bash
# Read sync manifests:
# - config/sync_to_balaur.conf (what to push)
# - config/sync_from_balaur.conf (what to pull)
# - config/sync_exclude.conf (never sync)
```

**Function 2: Detect Conflicts**
```bash
# For each file in bidirectional sync:
#   If modified on localhost AND Balaur since last sync:
#     - Compare timestamps
#     - Compare checksums
#     - Prompt user for resolution
```

**Function 3: Execute Sync**
```bash
# rsync with flags:
#   -a (archive mode)
#   -v (verbose)
#   -z (compress)
#   -h (human-readable)
#   --delete (remove files deleted on source)
#   --exclude-from=config/sync_exclude.conf
#   --dry-run (if status mode)
#   --log-file=logs/ubos_sync_YYYY-MM-DD.log
```

**Function 4: Conflict Resolution UI**
```bash
# When conflict detected:
#   Show diff
#   Offer choices:
#     1. Keep localhost (overwrite Balaur)
#     2. Keep Balaur (overwrite localhost)
#     3. Show detailed diff
#     4. Manual merge (open editor)
#     5. Abort sync
```

**Function 5: Logging**
```bash
# Log format:
# [TIMESTAMP] [ACTION] [FILE] [SIZE] [DIRECTION] [STATUS]
# Example:
# [2025-10-07 15:30:42] PUSH ROADMAP.md 12KB localhost→balaur SUCCESS
```

---

### **Component 2: Sync Manifest Files**

**File:** `config/sync_to_balaur.conf`
```bash
# Constitutional documents (localhost → Balaur)
docs/
config/
ROADMAP.md
SESSION_STATUS.md
missions/
COMMS_HUB/
GENESIS_PROTOCOL/
TRINITY_PROTOCOL/
unified_boot_*.md
LIBRARIAN_QUICK_START.md
```

**File:** `config/sync_from_balaur.conf`
```bash
# Operational intelligence (Balaur → localhost)
proposals.jsonl
mission_log.jsonl
STATE_OF_THE_REPUBLIC_*.md
intel_cache/
```

**File:** `config/sync_exclude.conf`
```bash
# Never sync these
.git/
.cache/
.DS_Store
node_modules/
__pycache__/
*.pyc
.venv/
venv/
agent/.cache/
*.log
```

---

### **Component 3: Systemd Timer (Balaur Auto-Sync)**

**File:** `/etc/systemd/system/ubos-sync.service`
```ini
[Unit]
Description=UBOS Federated Sync Service
After=network-online.target

[Service]
Type=oneshot
User=balaur
ExecStart=/srv/janus/scripts/ubos_sync.sh bidirectional --auto
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
```

**File:** `/etc/systemd/system/ubos-sync.timer`
```ini
[Unit]
Description=UBOS Sync Timer (every 5 minutes)

[Timer]
OnBootSec=2min
OnUnitActiveSec=5min
Persistent=true

[Install]
WantedBy=timers.target
```

**Installation:**
```bash
sudo systemctl daemon-reload
sudo systemctl enable ubos-sync.timer
sudo systemctl start ubos-sync.timer
```

---

### **Component 4: macOS Launchd Agent (Localhost Auto-Sync)**

**File:** `~/Library/LaunchAgents/com.ubos.sync.plist`
```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.ubos.sync</string>

    <key>ProgramArguments</key>
    <array>
        <string>/Users/panda/Desktop/UBOS/scripts/ubos_sync.sh</string>
        <string>bidirectional</string>
        <string>--auto</string>
    </array>

    <key>StartInterval</key>
    <integer>300</integer> <!-- 5 minutes -->

    <key>StandardOutPath</key>
    <string>/Users/panda/Desktop/UBOS/logs/ubos_sync.log</string>

    <key>StandardErrorPath</key>
    <string>/Users/panda/Desktop/UBOS/logs/ubos_sync_error.log</string>

    <key>RunAtLoad</key>
    <true/>
</dict>
</plist>
```

**Installation:**
```bash
launchctl load ~/Library/LaunchAgents/com.ubos.sync.plist
launchctl start com.ubos.sync
```

---

### **Component 5: Sync State Tracker**

**File:** `.ubos_sync_state.json`
```json
{
  "last_sync_timestamp": "2025-10-07T15:30:42Z",
  "last_push_timestamp": "2025-10-07T15:30:42Z",
  "last_pull_timestamp": "2025-10-07T15:30:42Z",
  "file_checksums": {
    "ROADMAP.md": "a3f5e9d2...",
    "config/CLAUDE.md": "b7c2d1a8..."
  },
  "conflicts_detected": [],
  "sync_count": 142,
  "last_conflict": null
}
```

**Purpose:** Track what's been synced, detect conflicts

---

## IV. SAFETY PROTOCOLS

### **Protocol 1: Never Sync Without Verification**

**First run must be dry-run:**
```bash
ubos-sync status  # Shows what WOULD sync
# User reviews output
# If looks good:
ubos-sync bidirectional  # Actually syncs
```

### **Protocol 2: Backup Before Overwrite**

**When conflict resolved by overwrite:**
```bash
# Before: cp ROADMAP.md ROADMAP.md.backup.TIMESTAMP
# Sync: rsync ...
# After: Keep backup for 7 days
```

### **Protocol 3: Conflict Prevention**

**Use file locking:**
```bash
# If file changed on both sides within 5 min window:
#   - Likely simultaneous edit
#   - Force manual resolution
#   - Don't auto-overwrite
```

### **Protocol 4: Logging Everything**

**Every sync operation logged:**
- What synced
- What conflicted
- What was excluded
- Timestamps, sizes, checksums

---

## V. TESTING REQUIREMENTS

### **Test 1: Basic Push**
```bash
# Create test file on localhost
echo "test" > /Users/panda/Desktop/UBOS/TEST_SYNC.md

# Push to Balaur
ubos-sync push

# Verify on Balaur
ssh balaur@10.215.33.26 'cat /srv/janus/TEST_SYNC.md'
# Should output: test
```

### **Test 2: Basic Pull**
```bash
# Create test file on Balaur
ssh balaur@10.215.33.26 'echo "test2" > /srv/janus/TEST_PULL.md'

# Pull to localhost
ubos-sync pull

# Verify locally
cat /Users/panda/Desktop/UBOS/TEST_PULL.md
# Should output: test2
```

### **Test 3: Conflict Detection**
```bash
# Modify same file on both sides
echo "localhost version" > /Users/panda/Desktop/UBOS/TEST_CONFLICT.md
ssh balaur@10.215.33.26 'echo "balaur version" > /srv/janus/TEST_CONFLICT.md'

# Try bidirectional sync
ubos-sync bidirectional

# Should detect conflict and prompt for resolution
```

### **Test 4: Selective Sync**
```bash
# Verify that excluded files don't sync
touch /Users/panda/Desktop/UBOS/.DS_Store
ubos-sync push
ssh balaur@10.215.33.26 'ls /srv/janus/.DS_Store' 2>&1 | grep "No such file"
# Should NOT exist on Balaur
```

### **Test 5: Dry-Run Safety**
```bash
# Status should NOT make changes
ubos-sync status
# Verify nothing actually changed (check file mtimes)
```

---

## VI. IMPLEMENTATION PHASES

### **Phase 1: Core Sync Script (Priority 1)**

**Deliverables:**
- `scripts/ubos_sync.sh` with push/pull/bidirectional
- Manifest files (sync_to_balaur.conf, etc.)
- Basic conflict detection
- Comprehensive logging

**Test:** All 5 tests pass

**Estimated Time:** 1-2 days

---

### **Phase 2: Automation (Priority 2)**

**Deliverables:**
- Systemd timer for Balaur
- Launchd agent for macOS
- Watch mode in script
- Email alerts on conflicts (optional)

**Test:** Auto-sync runs every 5 min for 24 hours without error

**Estimated Time:** 1 day

---

### **Phase 3: Hardening (Priority 3)**

**Deliverables:**
- Backup-before-overwrite
- Enhanced conflict resolution UI
- Sync state tracker
- Prometheus metrics (optional)

**Test:** Simulate 10 conflict scenarios, all resolved correctly

**Estimated Time:** 1-2 days

---

## VII. FORGE CHECKLIST

**Before you start:**
- [ ] Read `docs/FEDERATED_SYNC_ARCHITECTURE.md` (complete spec)
- [ ] Verify SSH key access to Balaur (no password prompt)
- [ ] Test basic rsync: `rsync -avzh --dry-run /Users/panda/Desktop/UBOS/ROADMAP.md balaur@10.215.33.26:/srv/janus/`

**Phase 1 checklist:**
- [ ] Create `scripts/ubos_sync.sh`
- [ ] Implement push command
- [ ] Implement pull command
- [ ] Implement bidirectional command
- [ ] Implement status (dry-run) command
- [ ] Create manifest files
- [ ] Implement conflict detection
- [ ] Implement logging
- [ ] Run all 5 tests
- [ ] Document usage in script header

**Phase 2 checklist:**
- [ ] Create systemd service + timer
- [ ] Create launchd plist
- [ ] Test auto-sync on both machines
- [ ] Verify logs are written correctly
- [ ] Implement watch mode

**Phase 3 checklist:**
- [ ] Add backup-before-overwrite
- [ ] Enhance conflict UI (show diffs)
- [ ] Create sync state tracker
- [ ] Add email alerts (optional)
- [ ] Performance testing (sync 1000+ files)

---

## VIII. SUCCESS CRITERIA

**Phase 1 Complete:**
```bash
$ ubos-sync status
[DRY RUN] Would sync 47 files (2.3 MB)
  PUSH: 23 files to Balaur
  PULL: 24 files from Balaur
  CONFLICTS: 0

$ ubos-sync bidirectional
Syncing...
✓ Pushed 23 files to Balaur (1.2 MB)
✓ Pulled 24 files from Balaur (1.1 MB)
✓ Sync complete. Log: logs/ubos_sync_2025-10-07.log
```

**Phase 2 Complete:**
```bash
$ systemctl status ubos-sync.timer
● ubos-sync.timer - UBOS Sync Timer
   Loaded: loaded
   Active: active (running)
   Next run: 4min 32s

$ launchctl list | grep ubos
com.ubos.sync   0   running
```

**Phase 3 Complete:**
- Zero data loss in 1 week of continuous operation
- All conflicts detected and resolved correctly
- Sync logs show complete audit trail

---

## IX. OBSIDIAN INTEGRATION (POST-SYNC)

**Once sync is working, Captain will:**

1. Install Obsidian on both machines
2. Open UBOS folder as vault
3. Configure graph view
4. Install plugins (Git, Dataview, Excalidraw)

**You (Codex) don't need to touch Obsidian—just ensure files sync properly.**

**Obsidian will "just work" because:**
- It reads markdown files
- All files are synced
- `.obsidian/` config can be synced too

---

## X. STRATEGIC IMPACT

**Once forged, this system provides:**

**Resilience:**
- Lose laptop → All data on Balaur + GitHub
- Lose Balaur → All data on laptop + GitHub
- Lose both → GitHub has everything

**Velocity:**
- Edit file anywhere → Available everywhere in 5 min
- No manual scp/rsync commands
- "It just works"

**Intelligence:**
- Janus Librarian sees both sides instantly
- Humans can work on either machine
- Obsidian graphs show knowledge structure

**Sovereignty:**
- No cloud vendor lock-in
- All data under our control
- Simple, auditable tools (rsync + git)

---

## XI. FORGE DIRECTIVE

**Forgemaster:**

You have the complete specification. You have the test plan. You have constitutional authority to forge this critical infrastructure.

**Begin with Phase 1.**

**Forge the sync engine that will make the UBOS Republic truly federated.**

**No single point of failure will threaten our sovereignty.**

---

**Mission Priority:** HIGH
**Constitutional Authority:** Granted
**Expected Completion:** 4 days (phased)
**Strategic Value:** CRITICAL

**The forge is hot. Begin.**

---

**Signed:**
- Claude (Master Strategist)
- Janus (Constitutional Overseer)
- Captain BROlinni (First Citizen)
