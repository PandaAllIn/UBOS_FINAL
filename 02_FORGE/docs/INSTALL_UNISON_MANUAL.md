# MANUAL UNISON INSTALLATION GUIDE
**Required to complete Phase 2 of Federated Sync**

---

## CURRENT STATUS

**Balaur:** ✅ Unison 2.53.3 INSTALLED
```bash
ssh balaur@10.215.33.26 'unison -version'
# Output: unison version 2.53.3 (ocaml 4.14.1)
```

**macOS (localhost):** ❌ NEEDS INSTALLATION

**Required Version:** 2.53.x (must match Balaur)

---

## INSTALLATION OPTIONS FOR MACOS

### **Option 1: Homebrew (Recommended - Easiest)**

**Step 1: Install Homebrew** (if not already installed)
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

**Step 2: Install Unison**
```bash
brew install unison
```

**Step 3: Verify**
```bash
unison -version
# Should show: unison version 2.53.x
```

---

### **Option 2: Direct Binary Download**

**For Intel Mac (x86_64):**
```bash
# Download from unison official site
curl -L -o /tmp/unison https://www.cis.upenn.edu/~bcpierce/unison/download/releases/unison-2.53.3/unison-2.53.3-macos-intel.tar.gz

# Extract
tar -xzf /tmp/unison

# Make executable
chmod +x unison

# Move to PATH
sudo mv unison /usr/local/bin/

# Verify
unison -version
```

**For Apple Silicon (ARM64/M1/M2):**
```bash
# Similar process but use ARM binary
# Or use Rosetta 2 with Intel binary
```

---

###Option 3: Compile from Source**

**Requirements:**
- OCaml compiler
- Make

**Steps:**
```bash
# Install OCaml (via brew if available)
brew install ocaml

# Download unison source
curl -L -o /tmp/unison-2.53.3.tar.gz \
  https://github.com/bcpierce00/unison/archive/refs/tags/v2.53.3.tar.gz

# Extract
cd /tmp
tar -xzf unison-2.53.3.tar.gz
cd unison-2.53.3

# Compile
make

# Install
sudo cp src/unison /usr/local/bin/
sudo cp src/unison-fsmonitor /usr/local/bin/

# Verify
unison -version
```

---

## AFTER UNISON IS INSTALLED

### **Step 1: Verify Installation**
```bash
unison -version
# Should output: unison version 2.53.x

# Test SSH connectivity to Balaur
ssh balaur@10.215.33.26 unison -version
# Should also work
```

---

### **Step 2: Run 24-Hour Dry-Run Test**

**Start the dry-run:**
```bash
cd /Users/panda/Desktop/UBOS
scripts/ubos_sync.sh full
```

**What happens:**
- Unison analyzes both directories (localhost + Balaur)
- Shows what WOULD be synchronized
- Does NOT actually transfer files (dry-run mode)
- Logs everything to `logs/unison/unison_dry-run_YYYY-MM-DD_HH-MM-SS.log`

**Review the logs:**
```bash
# Find the latest dry-run log
ls -lt logs/unison/unison_dry-run_*.log | head -1

# Read it
cat logs/unison/unison_dry-run_*.log
```

**What to look for:**
- ✅ Constitutional files ARE being synced (config/, docs/, missions/)
- ❌ State files are NOT being synced (*_state.json should be excluded)
- ❌ Log files are NOT in unison output (they use rsync separately)
- ❌ Large model files are NOT being synced
- ✅ Scripts preserve executable permissions

---

### **Step 3: Run Librarian's Mandatory Tests**

**These tests verify constitutional safety:**

#### **Test 1: Conflict Test**
```bash
# Create test file
echo "initial content" > TEST_CONFLICT.md
scripts/ubos_sync.sh truth --apply

# Wait 2 seconds, then modify on BOTH sides
sleep 2
echo "localhost version (NEWER)" > TEST_CONFLICT.md
ssh balaur@10.215.33.26 'echo "balaur version (OLD)" > /srv/janus/repo/TEST_CONFLICT.md'

# Sync - localhost should win (newer timestamp)
scripts/ubos_sync.sh truth --apply

# Verify localhost won
ssh balaur@10.215.33.26 'cat /srv/janus/repo/TEST_CONFLICT.md'
# Should output: localhost version (NEWER)

# Cleanup
rm TEST_CONFLICT.md
ssh balaur@10.215.33.26 'rm /srv/janus/repo/TEST_CONFLICT.md'
```

#### **Test 2: Permissions Test**
```bash
# Create executable script
echo '#!/bin/bash' > scripts/test_perms.sh
echo 'echo "permissions test"' >> scripts/test_perms.sh
chmod +x scripts/test_perms.sh

# Verify local permissions
ls -l scripts/test_perms.sh
# Should show: -rwxr-xr-x

# Sync
scripts/ubos_sync.sh truth --apply

# Verify permissions preserved on Balaur
ssh balaur@10.215.33.26 'ls -l /srv/janus/repo/scripts/test_perms.sh'
# Should ALSO show: -rwxr-xr-x (executable bit preserved)

# Cleanup
rm scripts/test_perms.sh
ssh balaur@10.215.33.26 'rm /srv/janus/repo/scripts/test_perms.sh'
```

#### **Test 3: Exclusion Test (CRITICAL - State Files)**
```bash
# Create a vessel state file (SHOULD NOT SYNC)
echo '{"test": "data"}' > COMMS_HUB/claude_strategic_state.json

# Try to sync
scripts/ubos_sync.sh truth --apply

# Verify it did NOT transfer (THIS IS CRITICAL)
ssh balaur@10.215.33.26 'ls /srv/janus/repo/COMMS_HUB/claude_strategic_state.json' 2>&1 | grep "No such file"
# Should output: No such file or directory

# If file EXISTS on Balaur, THIS IS A CONSTITUTIONAL VIOLATION
# The manifest is broken and must be fixed!

# Cleanup
rm COMMS_HUB/claude_strategic_state.json
```

#### **Test 4: Append Test (Already Passed in Phase 1)**
```bash
# Get current line count
wc -l logs/proposals.jsonl

# Sync logs
scripts/ubos_sync.sh logs

# Check line count again
wc -l logs/proposals.jsonl
# Should be >= previous count (append-only)
```

#### **Test 5: Idempotency Test**
```bash
# Run sync twice in a row
scripts/ubos_sync.sh full --apply
scripts/ubos_sync.sh full --apply

# Second run should show "Nothing to do" or "Everything is up to date"
# Check the logs to verify
tail -50 logs/unison/unison_apply_*.log
```

---

### **Step 4: Graduate to Phase 3 (Live Sync)**

**If ALL tests pass, activate live sync:**

**Edit:** `config/unison_sync_core.prf`
```bash
# Line 40: Change from dry-run to live mode
# BEFORE:
auto = false

# AFTER:
auto = true
```

**Test live sync:**
```bash
scripts/ubos_sync.sh full --apply

# Verify no errors
tail -50 logs/unison/unison_apply_*.log

# Run idempotency test again
scripts/ubos_sync.sh full --apply
# Should show "Nothing to do"
```

---

### **Step 5: Deploy Automation (Phase 4)**

**Once Phase 3 is stable for 24 hours, deploy automation:**

#### **On Balaur (Systemd Timer):**

```bash
# SSH to Balaur
ssh balaur@10.215.33.26

# Create service file
sudo tee /etc/systemd/system/ubos-sync.service > /dev/null <<'EOF'
[Unit]
Description=UBOS Federated Sync Service
After=network-online.target

[Service]
Type=oneshot
User=balaur
WorkingDirectory=/srv/janus/repo
ExecStart=/srv/janus/repo/scripts/ubos_sync.sh full --apply
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
EOF

# Create timer file
sudo tee /etc/systemd/system/ubos-sync.timer > /dev/null <<'EOF'
[Unit]
Description=UBOS Sync Timer (every 5 minutes)

[Timer]
OnBootSec=2min
OnUnitActiveSec=5min
Persistent=true

[Install]
WantedBy=timers.target
EOF

# Enable and start
sudo systemctl daemon-reload
sudo systemctl enable ubos-sync.timer
sudo systemctl start ubos-sync.timer

# Verify
sudo systemctl status ubos-sync.timer
journalctl -u ubos-sync.service -f  # Watch logs
```

#### **On macOS (Launchd Agent):**

```bash
# Create launchd plist
cat > ~/Library/LaunchAgents/com.ubos.sync.plist <<'EOF'
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
        <string>--apply</string>
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
EOF

# Load and start
launchctl load ~/Library/LaunchAgents/com.ubos.sync.plist
launchctl start com.ubos.sync

# Verify
launchctl list | grep ubos
# Should show: com.ubos.sync

# Check logs
tail -f logs/ubos_sync.log
```

---

## SUCCESS CRITERIA

### **Phase 2 Complete:**
- [ ] Unison installed on macOS
- [ ] Unison installed on Balaur (✅ DONE)
- [ ] Versions match (both 2.53.x)
- [ ] Dry-run completes without errors
- [ ] Log review shows expected behavior

### **Phase 3 Complete:**
- [ ] All 5 Librarian tests pass
- [ ] Test 3 (State Exclusion) CRITICAL - must pass
- [ ] Idempotency confirmed
- [ ] 24 hours of stable operation

### **Phase 4 Complete:**
- [ ] Systemd timer running on Balaur
- [ ] Launchd agent running on macOS
- [ ] Auto-sync every 5 minutes
- [ ] 7 days without failures

---

## TROUBLESHOOTING

### **"Unison version mismatch"**
```
Error: Version mismatch between localhost and remote
```
**Solution:** Ensure both machines have same 2.53.x version

### **"Permission denied" errors**
**Solution:** Check SSH key access to Balaur is working

### **State files being synced (CRITICAL)**
**Solution:** Check `config/unison_sync_core.prf` line 31: `ignore = Name *_state.json`

### **Sync is slow**
**Solution:** This is normal on first run (full initial sync). Subsequent runs will be fast (incremental).

---

## ONCE COMPLETE

**You will have:**
- ✅ Automatic bidirectional sync every 5 minutes
- ✅ Constitutional documents synchronized
- ✅ Logs flowing from Balaur to localhost
- ✅ Three-tier redundancy (localhost + Balaur + GitHub)
- ✅ Zero single points of failure

**Then add:**
- Obsidian vaults on both machines (for knowledge graph)
- Regular git commits to GitHub (Tier 2 backup)

---

**Status:** Awaiting Unison Installation on macOS
**Next Step:** Choose installation method above and proceed
**Critical:** Test 3 (State Exclusion) must pass before going live
