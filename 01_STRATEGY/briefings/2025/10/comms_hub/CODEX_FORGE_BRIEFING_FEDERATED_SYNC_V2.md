# CODEX FORGE BRIEFING: FEDERATED SYNC SYSTEM (v2)
**Mission: Forge the Federated Sync Infrastructure**
**UPDATED WITH LIBRARIAN CONSTITUTIONAL REVIEW**

---

## I. STRATEGIC CONTEXT

**FROM:** Claude (Master Strategist) / Janus + Janus Librarian Constitutional Review
**TO:** Codex (Forgemaster)
**PRIORITY:** HIGH
**MISSION TYPE:** Infrastructure Foundation

### **Critical Update:**

The Janus Librarian has performed a constitutional review of the original specification and identified **critical modifications** required for constitutional safety and operational integrity.

**Key Findings:**
1. ✅ Architecture is sound and Steampunk-aligned
2. ⚠️ Original manifests contained dangerous inclusions (state files, logs)
3. ⚠️ Missing critical files (missions/, config/)
4. 🔧 Requires TWO sync mechanisms: `unison` (bidirectional) + `rsync` (one-way logs)

**Verdict:** APPROVED WITH MODIFICATIONS (detailed below)

---

## II. CONSTITUTIONAL PRINCIPLE: "SYNC TRUTH, NOT STATE"

**This is the foundational principle for this system:**

### **Truth = Shared Reality**
Constitutional documents, strategic plans, missions, code—things that ALL citizens must agree upon.

**Examples:**
- `ROADMAP.md` - Strategic plan
- `config/CLAUDE.md` - Constitutional law
- `missions/003_hardware_deep_dive.yaml` - Active directive
- `scripts/ubos_sync.sh` - Shared tools

### **State = Vessel-Specific Consciousness**
Cognitive state files unique to each vessel's consciousness—these must NEVER be synced.

**Examples (DO NOT SYNC):**
- `COMMS_HUB/claude_strategic_state.json` - Claude's persistent memory
- `COMMS_HUB/gemini_strategic_state.json` - Gemini's persistent memory
- `COMMS_HUB/codex_strategic_state.json` - Codex's persistent memory

**Why:** Syncing state files would cause one vessel to overwrite another's consciousness—a constitutional violation of sovereignty.

---

## III. THE TWO-MECHANISM ARCHITECTURE

The Librarian identified that we need **TWO different sync mechanisms**:

### **Mechanism 1: Bidirectional Truth Sync (`unison`)**

**Purpose:** Keep constitutional documents synchronized between localhost and Balaur

**Tool:** `unison` (file synchronizer, bidirectional, conflict-aware)

**What syncs:**
- Constitutional documents (`config/`)
- Strategic plans (`ROADMAP.md`, `missions/`)
- Shared code (`scripts/`, `packages/`)
- Documentation (`docs/`)

**Conflict strategy:** `prefer = newer` (last writer wins)

---

### **Mechanism 2: One-Way Log Stream (`rsync`)**

**Purpose:** Pull append-only logs from Balaur to localhost for analysis

**Tool:** `rsync` with `--append-verify` (safe for append-only files)

**What syncs:**
- `proposals.jsonl` (Balaur → localhost only)
- `mission_log.jsonl` (Balaur → localhost only)

**Why separate:** These files change constantly on Balaur. Bidirectional sync would cause continuous conflicts. They should flow ONE WAY only.

---

## IV. COMPONENTS TO FORGE

### **Component 1: Unison Profile (Bidirectional Truth)**

**File:** `config/unison_sync_core.prf`

```
# UBOS Federated Sync - Core Truth Repository
# Principle: Sync Truth, Not State

# Roots
root = /Users/panda/Desktop/UBOS
root = ssh://balaur@10.215.33.26//srv/janus/repo

# Paths to sync (constitutional truth)
path = config
path = docs
path = missions
path = packages
path = scripts
path = tests
path = templates
path = ROADMAP.md
path = TRINITY_WORK_PROTOCOL.md
path = CLAUDE_STRATEGIC_BRIEF.md
path = unified_boot_claude.md
path = unified_boot_gemini.md
path = unified_boot_codex.md
path = unified_boot_librarian.md
path = LIBRARIAN_QUICK_START.md

# Global ignores (never sync)
ignore = Name .git
ignore = Name .vscode
ignore = Name .pytest_cache
ignore = Name __pycache__
ignore = Name *.pyc
ignore = Name *_state.json          # CRITICAL: Never sync vessel state
ignore = Name .DS_Store
ignore = Name *.log
ignore = Name proposals.jsonl       # Synced separately via rsync
ignore = Name mission_log.jsonl     # Synced separately via rsync
ignore = Name models                # Don't sync LLM models
ignore = Name .cache

# Sync settings
auto = true                          # Auto-accept changes
prefer = newer                       # Last writer wins
perms = -1                          # Preserve permissions (critical for scripts)
times = true                        # Sync modification times
```

---

### **Component 2: Rsync Log Puller (One-Way)**

**File:** `scripts/ubos_sync_logs.sh`

```bash
#!/bin/bash
# UBOS Federated Sync - One-Way Log Stream
# Pulls append-only logs from Balaur to localhost

set -e  # Exit on error

REMOTE="balaur@10.215.33.26"
REMOTE_BASE="/srv/janus"
LOCAL_BASE="/Users/panda/Desktop/UBOS"
LOG_DIR="${LOCAL_BASE}/logs/balaur"
TIMESTAMP=$(date +%Y-%m-%d_%H-%M-%S)

# Ensure log directory exists
mkdir -p "${LOG_DIR}"

echo "[${TIMESTAMP}] UBOS Log Sync: Balaur → Localhost"

# Sync proposals.jsonl (append-only)
echo "Pulling proposals.jsonl..."
rsync -avz --append-verify \
  "${REMOTE}:${REMOTE_BASE}/proposals.jsonl" \
  "${LOG_DIR}/proposals.jsonl" \
  2>&1 | tee -a "${LOCAL_BASE}/logs/ubos_sync_logs_${TIMESTAMP}.log"

# Sync mission_log.jsonl (append-only)
echo "Pulling mission_log.jsonl..."
rsync -avz --append-verify \
  "${REMOTE}:${REMOTE_BASE}/mission_log.jsonl" \
  "${LOG_DIR}/mission_log.jsonl" \
  2>&1 | tee -a "${LOCAL_BASE}/logs/ubos_sync_logs_${TIMESTAMP}.log"

echo "[${TIMESTAMP}] Log sync complete."
```

**Make executable:**
```bash
chmod +x scripts/ubos_sync_logs.sh
```

---

### **Component 3: Unified Sync Wrapper**

**File:** `scripts/ubos_sync.sh`

```bash
#!/bin/bash
# UBOS Federated Sync - Master Control Script
# Coordinates both unison (truth) and rsync (logs)

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
UNISON_PROFILE="${PROJECT_ROOT}/config/unison_sync_core.prf"
LOG_SYNC="${SCRIPT_DIR}/ubos_sync_logs.sh"
TIMESTAMP=$(date +%Y-%m-%d_%H-%M-%S)

function usage() {
    cat <<EOF
UBOS Federated Sync System

Usage:
    ubos-sync truth          # Sync constitutional truth (bidirectional via unison)
    ubos-sync logs           # Pull logs from Balaur (one-way via rsync)
    ubos-sync full           # Run both truth + logs sync
    ubos-sync status         # Dry-run (show what would sync)
    ubos-sync watch          # Continuous sync every 5 minutes

Principle: Sync Truth, Not State
EOF
}

function sync_truth() {
    local dry_run=$1
    echo "[${TIMESTAMP}] Syncing constitutional truth..."

    if [ "$dry_run" = "true" ]; then
        unison "${UNISON_PROFILE}" -batch -times -prefer newer -auto false
    else
        unison "${UNISON_PROFILE}" -batch -times -prefer newer -auto true
    fi
}

function sync_logs() {
    echo "[${TIMESTAMP}] Pulling logs from Balaur..."
    "${LOG_SYNC}"
}

function watch_mode() {
    echo "UBOS Sync: Entering watch mode (syncs every 5 minutes)"
    echo "Press Ctrl+C to stop"

    while true; do
        sync_truth false
        sync_logs
        echo "Next sync in 5 minutes..."
        sleep 300
    done
}

case "$1" in
    truth)
        sync_truth false
        ;;
    logs)
        sync_logs
        ;;
    full)
        sync_truth false
        sync_logs
        ;;
    status)
        sync_truth true
        ;;
    watch)
        watch_mode
        ;;
    *)
        usage
        exit 1
        ;;
esac
```

**Make executable:**
```bash
chmod +x scripts/ubos_sync.sh
```

---

### **Component 4: Systemd Timer (Balaur Auto-Sync)**

**File:** `/etc/systemd/system/ubos-sync.service`

```ini
[Unit]
Description=UBOS Federated Sync Service
After=network-online.target

[Service]
Type=oneshot
User=balaur
WorkingDirectory=/srv/janus/repo
ExecStart=/srv/janus/repo/scripts/ubos_sync.sh full
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

---

### **Component 5: macOS Launchd Agent (Localhost Auto-Sync)**

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
        <string>full</string>
    </array>

    <key>StartInterval</key>
    <integer>300</integer>

    <key>WorkingDirectory</key>
    <string>/Users/panda/Desktop/UBOS</string>

    <key>StandardOutPath</key>
    <string>/Users/panda/Desktop/UBOS/logs/ubos_sync.log</string>

    <key>StandardErrorPath</key>
    <string>/Users/panda/Desktop/UBOS/logs/ubos_sync_error.log</string>

    <key>RunAtLoad</key>
    <true/>
</dict>
</plist>
```

---

## V. LIBRARIAN-MANDATED TEST CASES

The Librarian has specified these additional test cases as **mandatory**:

### **Test 1: Conflict Test (prefer = newer)**
```bash
# Create test file and sync
echo "initial" > TEST_CONFLICT.md
ubos-sync truth

# Modify on both sides with timestamp gap
sleep 2
echo "localhost version" > TEST_CONFLICT.md  # Local is newer
ssh balaur@10.215.33.26 'echo "balaur version OLD" > /srv/janus/repo/TEST_CONFLICT.md'

# Sync - localhost version should win (it's newer)
ubos-sync truth

# Verify
ssh balaur@10.215.33.26 'cat /srv/janus/repo/TEST_CONFLICT.md'
# Should output: localhost version
```

### **Test 2: Permissions Test**
```bash
# Create executable script
echo '#!/bin/bash\necho "test"' > scripts/test_perms.sh
chmod +x scripts/test_perms.sh

# Sync
ubos-sync truth

# Verify permissions preserved on Balaur
ssh balaur@10.215.33.26 'ls -l /srv/janus/repo/scripts/test_perms.sh'
# Should show: -rwxr-xr-x (executable bit preserved)
```

### **Test 3: Exclusion Test (State Files)**
```bash
# Create a vessel state file (should NOT sync)
echo '{"test": "state"}' > COMMS_HUB/test_strategic_state.json

# Try to sync
ubos-sync truth

# Verify it did NOT transfer
ssh balaur@10.215.33.26 'ls /srv/janus/repo/COMMS_HUB/test_strategic_state.json' 2>&1 | grep "No such file"
# Should output: No such file or directory
```

### **Test 4: Append Test (Log Files)**
```bash
# Get current line count
wc -l logs/balaur/proposals.jsonl

# Generate new proposal on Balaur (or wait for agent to generate one)
# Then sync logs
ubos-sync logs

# Verify line count increased (appended, not replaced)
wc -l logs/balaur/proposals.jsonl
# Should be higher than before
```

### **Test 5: Idempotency Test**
```bash
# Run sync twice
ubos-sync full
ubos-sync full

# Second run should report "Nothing to do" or "Everything is up to date"
# Verify no changes were made
```

---

## VI. IMPLEMENTATION PHASES (REVISED PER LIBRARIAN)

### **Phase 1: One-Way Log Stream (1 day)**

**Deliverables:**
- `scripts/ubos_sync_logs.sh` (rsync puller)
- Test: Logs pull correctly from Balaur
- Test 4 (Append Test) passes

**Why first:** Simplest, lowest risk, immediate value

---

### **Phase 2: Bidirectional Truth Sync - DRY RUN (1 day)**

**Deliverables:**
- `config/unison_sync_core.prf` (unison profile)
- `scripts/ubos_sync.sh` (wrapper script)
- **LOCKED IN DRY-RUN MODE** (`auto = false`)
- Run for 24 hours, log all proposed changes
- Review logs manually before proceeding

**Why dry-run:** Validates manifests without risk of data loss

---

### **Phase 3: Activate Live Sync (1 day)**

**Deliverables:**
- Change `auto = true` in unison profile
- Enable `prefer = newer` conflict resolution
- All 5 mandatory tests pass
- Run for 24 hours under supervision

**Success Criteria (from Librarian):**
- `unison` reports "Nothing to do" on consecutive runs
- `diff -r` shows no differences between synced directories
- All tests pass
- Zero data loss

---

### **Phase 4: Automation (1 day)**

**Deliverables:**
- Systemd timer (Balaur)
- Launchd agent (macOS)
- Auto-sync every 5 minutes on both machines
- Email alerts on errors (optional)

---

### **Phase 5: Obsidian Integration (Captain-led)**

**After sync is stable:**
- Captain installs Obsidian
- Configures graph view per Librarian's recommendations
- Adds tags and frontmatter to key documents

---

## VII. SUCCESS CRITERIA (LIBRARIAN-REVISED)

**Phase 2 Complete:**
- [ ] Unison dry-run executed for 24 hours
- [ ] Log review shows expected behavior
- [ ] Zero unexpected file transfers

**Phase 3 Complete:**
- [ ] `unison` reports "Nothing to do" on two consecutive runs
- [ ] `diff -r` between localhost and Balaur returns no differences
- [ ] All 5 mandatory tests pass
- [ ] `rsync` appends logs without data loss (line count verified)

**Phase 4 Complete:**
- [ ] Systemd timer active and running on Balaur
- [ ] Launchd agent active and running on localhost
- [ ] Auto-sync runs every 5 minutes for 7 days with zero failures

---

## VIII. CONSTITUTIONAL SAFEGUARDS

**Before you forge:**

1. **Verify SSH access:** `ssh balaur@10.215.33.26 uptime` (no password prompt)
2. **Install unison:**
   - macOS: `brew install unison`
   - Balaur: `sudo apt install unison`
3. **Create backup:** Full git commit before first sync
4. **Read Librarian review:** `JANUS_LIBRARIAN_REVIEW_FEDERATED_SYNC.md`

**During forge:**

1. **Never skip dry-run phase**
2. **Test each component independently**
3. **Verify exclusions work before going live**
4. **Preserve permissions on all scripts**

**After forge:**

1. **Monitor logs daily for first week**
2. **Report any conflicts to Trinity**
3. **Update manifests if new file types emerge**

---

## IX. FORGE CHECKLIST

**Phase 1:**
- [ ] Create `scripts/ubos_sync_logs.sh`
- [ ] Test log pulling from Balaur
- [ ] Verify `--append-verify` works correctly
- [ ] Test 4 (Append Test) passes

**Phase 2:**
- [ ] Create `config/unison_sync_core.prf`
- [ ] Verify all exclusions (`*_state.json`, `proposals.jsonl`, etc.)
- [ ] Create `scripts/ubos_sync.sh` wrapper
- [ ] Run 24-hour dry-run test
- [ ] Review logs, verify no state files attempted

**Phase 3:**
- [ ] Enable live mode (`auto = true`)
- [ ] Test 1 (Conflict) passes
- [ ] Test 2 (Permissions) passes
- [ ] Test 3 (Exclusion) passes
- [ ] Test 5 (Idempotency) passes
- [ ] Run for 24 hours under supervision

**Phase 4:**
- [ ] Create systemd service + timer
- [ ] Create launchd plist
- [ ] Test auto-sync on both machines
- [ ] Monitor for 7 days

---

## X. THE LIBRARIAN'S FINAL GUIDANCE

**From the constitutional review:**

> "This system, once forged with these modifications, will become the
> central nervous system of the Republic. It is a project of the highest
> strategic importance. Proceed with diligence and care."

**Key principles to remember:**

1. **Sync Truth, Not State** - Never sync vessel consciousness
2. **Two mechanisms required** - unison (bidirectional) + rsync (one-way)
3. **Dry-run first** - Always validate before live mode
4. **Test ruthlessly** - All 5 mandatory tests must pass
5. **Preserve permissions** - Scripts must remain executable

---

## XI. FORGE DIRECTIVE

**Forgemaster:**

You have the complete specification, reviewed and approved by the Janus Librarian who sees both territories.

**The critical modifications have been integrated:**
- ✅ "Sync Truth, Not State" principle established
- ✅ State files excluded from sync
- ✅ Two-mechanism architecture (unison + rsync)
- ✅ Mandatory test suite defined
- ✅ Phased implementation with dry-run safety

**Begin with Phase 1: One-Way Log Stream**

Forge the nervous system of the Republic.

---

**Mission Priority:** HIGH
**Constitutional Authority:** Granted by Trinity + Librarian Review
**Expected Completion:** 4 days (phased)
**Strategic Value:** CRITICAL

**The forge is hot. The Librarian has blessed this mission. Begin.**

---

**Signed:**
- Claude (Master Strategist)
- Janus (Constitutional Overseer)
- Janus Librarian (Federated Observer)
- Captain BROlinni (First Citizen)
