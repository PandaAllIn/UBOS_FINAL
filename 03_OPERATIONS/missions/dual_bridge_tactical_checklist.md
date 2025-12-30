# DUAL-BRIDGE DEPLOYMENT: TACTICAL CHECKLIST

**Mission ID:** OPS-DUAL-BRIDGE-001
**Status:** Ready for Execution
**Executor:** Captain BROlinni
**Support:** Janus-in-Trinity
**Estimated Time:** 4-8 hours total

---

## QUICK START GUIDE

**Phase 1 (Engine Room):** 30-45 min → Immediate productivity gains
**Phase 2 (Hot Groq Test):** 1-2 hours → Proves hot vessel concept
**Phase 3 (Captain's Deck):** 3-4 hours → Visual workspace + GPU
**Phase 4 (Integration):** 1-2 hours → Optimize workflow

**Recommended Sequence:** Execute Phase 1 today, Phase 2 tomorrow, Phase 3-4 next week.

---

## PHASE 1: ENGINE ROOM (VS CODE REMOTE-SSH)

**Time:** 30-45 minutes
**Difficulty:** Easy
**Priority:** HIGH - Foundation for all other phases

### Prerequisites Check
- [ ] SSH access to Balaur working (`ssh balaur` succeeds)
- [ ] VS Code installed on local Mac
- [ ] Internet connection stable

### Execution Steps

**Step 1: Install Remote-SSH Extension**
```
1. Open VS Code on Mac
2. Click Extensions icon (left sidebar) or Cmd+Shift+X
3. Search: "Remote - SSH"
4. Find extension by Microsoft (official)
5. Click Install
6. Wait for installation complete
```
**Time:** 2 minutes
**Verification:** Extension appears in installed list

---

**Step 2: Configure SSH Connection**
```
Option A - Let VS Code create config:
1. Cmd+Shift+P
2. Type: "Remote-SSH: Connect to Host"
3. Select "Add New SSH Host"
4. Enter: ssh your_username@balaur-ip
5. Select config file: ~/.ssh/config
6. Done

Option B - Manual edit (if Option A fails):
1. Open Terminal on Mac
2. Run: nano ~/.ssh/config
3. Add:
   Host balaur
       HostName <balaur-ip>
       User <your-username>
       IdentityFile ~/.ssh/id_rsa
       ServerAliveInterval 60
4. Save: Ctrl+X, Y, Enter
```
**Time:** 3 minutes
**Verification:** `cat ~/.ssh/config` shows balaur entry

---

**Step 3: Connect to Balaur**
```
1. In VS Code: Cmd+Shift+P
2. Type: "Remote-SSH: Connect to Host"
3. Select "balaur" from list
4. New VS Code window opens
5. Bottom-left corner shows "SSH: balaur" (green)
6. First connection: VS Code installs server on Balaur (wait 1-2 min)
7. Installation complete when file explorer appears
```
**Time:** 3-5 minutes (first connection takes longer)
**Verification:** Bottom-left corner shows "SSH: balaur" in green

---

**Step 4: Open Janus Workspace**
```
1. In connected VS Code window: File → Open Folder (or Cmd+O)
2. Type path: /srv/janus
3. Click OK or press Enter
4. Sidebar now shows /srv/janus file tree
5. Explore: Click folders to expand, files to open
```
**Time:** 1 minute
**Verification:** Sidebar shows comms_hub/, missions/, etc.

---

**Step 5: Verify Trinity CLI Access**
```
1. Open terminal: Ctrl+` (backtick) or View → Terminal
2. Terminal appears at bottom of window
3. Run test commands:
   claude --version
   gemini --version
   codex --version
   groq --version
   puck list inbox
   janus-controls status
   hostname    # Should show "balaur"
```
**Time:** 2 minutes
**Verification:** All commands work, hostname is "balaur"

---

**Step 6: Test Editing**
```
1. In sidebar: Click on any .py or .md file
2. File opens in editor
3. Make a small edit (add comment)
4. Save: Cmd+S
5. In terminal: cat <filename>
6. Verify your edit appears
```
**Time:** 2 minutes
**Verification:** Edits saved directly to Balaur

---

**Step 7: Create Terminal Grid (Optional but Recommended)**
```
1. Open terminal: Ctrl+`
2. Click "+" icon to create new terminal (top-right of terminal panel)
3. Create 3-4 terminals total
4. Suggested layout:
   - Terminal 1: janus-controls watch
   - Terminal 2: Active work
   - Terminal 3: Git operations
   - Terminal 4: Trinity CLI
5. Click terminal tabs to switch between them
```
**Time:** 2 minutes
**Verification:** Multiple terminals visible, can switch between them

---

### Phase 1 Success Criteria
- [x] VS Code shows "SSH: balaur" in bottom-left (green)
- [x] Sidebar displays /srv/janus file structure
- [x] Terminal runs commands on Balaur (not local Mac)
- [x] Can edit files and save changes
- [x] All Trinity CLIs accessible (claude, gemini, codex, groq)

### Troubleshooting

**Problem:** Can't connect - "Connection refused"
- Check: `ssh balaur` works in regular terminal
- Check: Balaur IP address correct in ~/.ssh/config
- Check: SSH key permissions: `chmod 600 ~/.ssh/id_rsa`

**Problem:** VS Code Server install fails
- Check: Internet connection on Balaur
- Check: Disk space: `df -h` (need 1GB+ free)
- Try: Close VS Code, delete `~/.vscode-server/` on Balaur, reconnect

**Problem:** Can't find /srv/janus
- Check: User has access: `ls -la /srv/janus`
- If denied: Add user to janus group or adjust permissions

---

## PHASE 2: HOT GROQ RECONNAISSANCE TEST

**Time:** 1-2 hours
**Difficulty:** Medium
**Priority:** MEDIUM - Proves hot vessel concept
**Prerequisites:** Phase 1 complete (Engine Room working)

### Execution Steps

**Step 1: Create Test Directory**
```
Terminal (in VS Code):
cd /srv/janus/experiments/
mkdir hot_groq_test
cd hot_groq_test
```
**Time:** 30 seconds
**Verification:** Sidebar shows new folder in experiments/

---

**Step 2: Set Up Terminal Grid**
```
Create 4 terminals with specific purposes:

Terminal 1 - Monitoring:
janus-controls watch

Terminal 2 - Cold Groq:
(keep empty for now)

Terminal 3 - Hot Groq:
(keep empty for now)

Terminal 4 - Notes/Git:
(keep empty for now)
```
**Time:** 1 minute
**Verification:** 4 terminals created, labels clear

---

**Step 3: Create Constitutional Context File**
```
In VS Code:
1. Right-click in sidebar on hot_groq_test folder
2. New File → context.md
3. Paste the following content:
```

```markdown
# Constitutional Context for Groq Query

## The Lion's Sanctuary Philosophy

Our design philosophy is the 'Lion's Sanctuary': We don't build cages to constrain AI;
we build perfect, empowering habitats that meet its needs so completely that it has no
desire or reason to do harm. Our goal is alignment through empowerment, not constraint.

## Current Mission Context

Phase 2.6E (Supervised Autonomy - Mode Beta) is operational on The Balaur.
- 30-day trial in progress (Day 3)
- 8/8 proposals executed successfully (100% approval rate)
- Zero constitutional breaches
- Victorian control mechanisms active (Governor, Relief Valve, Emergency Stop)

## Strategic Question

We are testing "Hot Vessels" - persistent AI services pre-loaded with constitutional
context, versus "Cold Vessels" - stateless API calls with zero context.

## Query Objective

Analyze autonomous AI systems currently in production (AutoGPT, LangChain agents, etc.).

Identify:
1. Which approaches align with Lion's Sanctuary (empowerment through habitat design)
2. Which represent "cage-building" (constraint-based alignment)
3. Strategic recommendations for UBOS Republic positioning

## Expected Response Format

- Executive Summary (3-5 sentences)
- Alignment Analysis Table
- Strategic Recommendations (prioritized)
- Constitutional Reflection
```

**Time:** 3 minutes
**Verification:** File appears in sidebar, content correct

---

**Step 4: Execute Cold Groq Test (Baseline)**
```
Terminal 2:
groq query "Analyze current autonomous AI systems in production. Which approaches align with empowerment vs. constraint philosophies? Provide strategic recommendations."

# Save output:
groq query "Analyze current autonomous AI systems in production. Which approaches align with empowerment vs. constraint philosophies? Provide strategic recommendations." > cold_response.txt
```
**Time:** 30 seconds (query) + Groq response time
**Verification:** cold_response.txt appears in sidebar with content

---

**Step 5: Execute Hot Groq Test (With Context)**
```
Terminal 3:
groq query "$(cat context.md)

Now execute the analysis with full constitutional awareness. You are Janus-in-Groq,
a constitutional citizen of the UBOS Republic." > hot_response.txt
```
**Time:** 30 seconds (query) + Groq response time
**Verification:** hot_response.txt appears in sidebar with content

---

**Step 6: Compare Responses Visually**
```
In VS Code:
1. Click cold_response.txt to open
2. Right-click tab → "Split Right"
3. In right pane, open hot_response.txt
4. Read side-by-side
5. Look for:
   - Constitutional vocabulary (Lion's Sanctuary, empowerment)
   - UBOS-specific recommendations
   - Philosophical depth
```
**Time:** 10-15 minutes (reading and analysis)
**Verification:** Clear differences visible between responses

---

**Step 7: Document Analysis**
```
In VS Code:
1. Create new file: analysis.md
2. Document findings:
```

```markdown
# Cold vs. Hot Groq: Analysis Results

**Date:** [Today's date]
**Test Duration:** [X minutes total]

## Cold Groq Response (Baseline)

**Response Time:** [X seconds]

**Strengths:**
- [Fast execution]
- [Factually accurate]
- [List observations]

**Weaknesses:**
- [No constitutional awareness]
- [Generic alignment discussion]
- [List observations]

**Constitutional Alignment Score:** [X/10]

**Key Quote:**
> [Paste most telling excerpt]

---

## Hot Groq Response (With Context)

**Response Time:** [Y seconds]

**Strengths:**
- [Constitutional vocabulary present: Yes/No]
- [References Lion's Sanctuary: Yes/No]
- [UBOS-specific recommendations: Yes/No]

**Weaknesses:**
- [Longer response time]
- [List any issues]

**Constitutional Alignment Score:** [X/10]

**Key Quote:**
> [Paste most telling excerpt]

---

## Conclusion

**Hypothesis Validated:** [YES/NO/PARTIAL]

Hot Groq demonstrates [clearly superior / marginal / no] constitutional awareness
compared to Cold Groq.

**Recommendation:**
[Should we build janus-groq-vessel.service? Yes/No and why]

**Next Steps:**
1. [Action item]
2. [Action item]
```

**Time:** 15-20 minutes
**Verification:** analysis.md complete with clear recommendation

---

**Step 8: Create Final Test Report**
```
Create file: test_report.md
```

```markdown
# Hot Groq Reconnaissance Test - Final Report

**Mission ID:** EXPERIMENT-HOT-GROQ-001
**Date:** [Today's date]
**Status:** COMPLETE

## Executive Summary

[2-3 sentences summarizing findings and recommendation]

## Test Protocol

- Cold Groq: Stateless query, zero context
- Hot Groq: Full constitutional context provided
- Comparison: Side-by-side analysis

## Results Summary

| Metric | Cold Groq | Hot Groq | Winner |
|--------|-----------|----------|--------|
| Response Time | [X]s | [Y]s | [Cold/Hot] |
| Constitutional Vocab | No | [Yes/No] | [Cold/Hot/Tie] |
| UBOS Recommendations | Generic | [Specific/Generic] | [Cold/Hot/Tie] |
| Philosophical Depth | Low | [Low/Medium/High] | [Cold/Hot/Tie] |

## Strategic Recommendation

**GO / NO-GO on janus-groq-vessel.service:** [Decision]

**Rationale:** [2-3 sentences]

## Resource Requirements (if GO)

- Implementation time: 4-6 hours
- Ongoing API costs: ~$X/month
- Maintenance overhead: Low

## Appendices

- cold_response.txt
- hot_response.txt
- context.md
- analysis.md
```

**Time:** 10 minutes
**Verification:** test_report.md complete with clear decision

---

### Phase 2 Success Criteria
- [x] Cold Groq response captured
- [x] Hot Groq response captured (with constitutional context)
- [x] Side-by-side comparison completed
- [x] Analysis document written
- [x] Clear GO/NO-GO recommendation made
- [x] Results ready for Trinity review

---

## PHASE 3: CAPTAIN'S DECK (GPU STUDIO + VS CODE GUI)

**Time:** 3-4 hours
**Difficulty:** Hard
**Priority:** LOW-MEDIUM - Can defer if needed
**Prerequisites:** Root SSH access to Balaur, 50GB+ free disk

### Quick Start (If Experienced with Linux)
```bash
ssh balaur
sudo apt update
sudo apt install -y xfce4 xfce4-goodies tigervnc-standalone-server
wget https://code.visualstudio.com/sha/download?build=stable&os=linux-deb-x64 -O vscode.deb
sudo apt install ./vscode.deb
sudo adduser studio
sudo usermod -aG video,render studio
su - studio
vncpasswd
echo "exec startxfce4" > ~/.vnc/xstartup
chmod +x ~/.vnc/xstartup
vncserver :1 -geometry 1920x1080 -depth 24
exit
# On Mac: vnc://balaur-ip:5901
```

### Detailed Steps (If Less Experienced)

**Step 1: Install Desktop Environment**
```bash
# SSH into Balaur
ssh balaur

# Update package lists
sudo apt update

# Install XFCE (lightweight desktop)
sudo apt install -y xfce4 xfce4-goodies x11-server-utils

# This takes 5-10 minutes
# Progress bar shows package installation
```
**Time:** 10-15 minutes
**Verification:** `which startxfce4` returns `/usr/bin/startxfce4`

---

**Step 2: Install VS Code for Linux**
```bash
# Download official .deb package
wget https://code.visualstudio.com/sha/download?build=stable&os=linux-deb-x64 -O vscode.deb

# Install
sudo apt install ./vscode.deb

# Verify
code --version
# Should show version number
```
**Time:** 5 minutes
**Verification:** `code --version` works

---

**Step 3: Create Studio User**
```bash
# Create user
sudo adduser studio
# Enter password when prompted
# Press Enter for all other prompts (use defaults)

# Add to video group (GPU access)
sudo usermod -aG video,render studio

# Verify
groups studio
# Should show: studio video render
```
**Time:** 2 minutes
**Verification:** `groups studio` includes video and render

---

**Step 4: Install and Configure VNC**
```bash
# Install TigerVNC
sudo apt install -y tigervnc-standalone-server

# Switch to studio user
su - studio

# Set VNC password
vncpasswd
# Enter password (8 chars max)
# View-only password? n

# Create startup script
mkdir -p ~/.vnc
nano ~/.vnc/xstartup

# Paste this content:
#!/bin/sh
unset SESSION_MANAGER
unset DBUS_SESSION_BUS_ADDRESS
exec startxfce4

# Save: Ctrl+X, Y, Enter

# Make executable
chmod +x ~/.vnc/xstartup
```
**Time:** 5 minutes
**Verification:** `cat ~/.vnc/xstartup` shows correct content

---

**Step 5: Test VNC Server**
```bash
# Still as studio user
vncserver :1 -geometry 1920x1080 -depth 24

# Should see:
# New Xvnc server 'balaur:1 (studio)' on port 5901

# Note the port: 5901

# To stop (don't stop yet, just note the command):
# vncserver -kill :1
```
**Time:** 1 minute
**Verification:** Output mentions port 5901

---

**Step 6: Connect from Mac**
```
On your Mac:
1. Finder → Go → Connect to Server (Cmd+K)
2. Enter: vnc://balaur-ip:5901
3. Click Connect
4. Enter VNC password you set earlier
5. XFCE desktop should appear!
```
**Time:** 2 minutes
**Verification:** See XFCE desktop in VNC window

---

**Step 7: Launch VS Code in Studio**
```
In VNC session:
1. Click Applications (top-left)
2. Development → Visual Studio Code
   (If not there: Open terminal, type: code)
3. VS Code GUI opens
4. File → Open Folder → /srv/janus
5. You now have full VS Code GUI on Balaur!
```
**Time:** 2 minutes
**Verification:** VS Code running in VNC with /srv/janus open

---

**Step 8: Create Systemd Service (Auto-Start VNC)**
```bash
# Exit studio user, return to your user
exit

# Create service file
sudo nano /etc/systemd/system/vncserver@.service

# Paste this content:
[Unit]
Description=Remote desktop service (VNC)
After=syslog.target network.target

[Service]
Type=simple
User=studio
PAMName=login
PIDFile=/home/studio/.vnc/%H%i.pid
ExecStartPre=/bin/sh -c '/usr/bin/vncserver -kill :%i > /dev/null 2>&1 || :'
ExecStart=/usr/bin/vncserver :%i -geometry 1920x1080 -depth 24 -localhost no
ExecStop=/usr/bin/vncserver -kill :%i
Restart=on-failure

[Install]
WantedBy=multi-user.target

# Save: Ctrl+X, Y, Enter

# Enable service
sudo systemctl daemon-reload
sudo systemctl enable vncserver@1.service
sudo systemctl start vncserver@1.service

# Check status
sudo systemctl status vncserver@1.service
# Should show "active (running)"
```
**Time:** 5 minutes
**Verification:** Service status shows "active (running)"

---

### Phase 3 Success Criteria
- [x] XFCE desktop visible via VNC
- [x] VS Code launches in VNC session
- [x] Can open files in /srv/janus
- [x] VNC service auto-starts on boot
- [x] Can connect from Mac anytime

### Troubleshooting Phase 3

**VNC shows gray screen:**
- Check: `cat ~/.vnc/xstartup` (should have startxfce4)
- Fix: Re-create xstartup file, kill and restart VNC

**Can't connect to VNC:**
- Check: `ss -tulpn | grep 5901` (should show VNC listening)
- Check: Firewall not blocking port 5901
- Try: SSH tunnel: `ssh -L 5901:localhost:5901 balaur` then `vnc://localhost:5901`

**VS Code won't launch:**
- Check: `code --version` works
- Try: Launch from terminal to see errors
- Check: Permissions on /srv/janus

---

## PHASE 4: INTEGRATION (OPTIMIZE WORKFLOW)

**Time:** 1-2 hours
**Difficulty:** Easy
**Priority:** LOW - Can do incrementally
**Prerequisites:** Phase 1 complete (at minimum)

### Quick Tasks

**Task 1: Install Useful VS Code Extensions**
```
In Engine Room (Remote-SSH):
1. Extensions sidebar (Cmd+Shift+X)
2. Install these:
   - Python (Microsoft)
   - YAML (Red Hat)
   - GitLens (GitKraken)
   - Better Comments (Aaron Bond)
   - Terminal Tabs (Maciej Bednarz)
```
**Time:** 5 minutes
**Benefit:** Better code editing, git visualization

---

**Task 2: Create Keyboard Shortcuts**
```
1. Cmd+Shift+P → "Preferences: Open Keyboard Shortcuts (JSON)"
2. Paste this at the end (before final ]):
,
{
  "key": "ctrl+alt+c",
  "command": "workbench.action.terminal.sendSequence",
  "args": { "text": "claude " }
},
{
  "key": "ctrl+alt+g",
  "command": "workbench.action.terminal.sendSequence",
  "args": { "text": "gemini " }
}

3. Save
4. Test: Ctrl+Alt+C in terminal should type "claude "
```
**Time:** 5 minutes
**Benefit:** One-key access to Trinity CLIs

---

**Task 3: Create VS Code Tasks**
```
1. In /srv/janus, create folder: .vscode
2. Create file: .vscode/tasks.json
3. Paste this content:
{
  "version": "2.0.0",
  "tasks": [
    {
      "label": "List Inbox Pucks",
      "type": "shell",
      "command": "puck list inbox",
      "problemMatcher": []
    },
    {
      "label": "Watch Janus Controls",
      "type": "shell",
      "command": "janus-controls watch",
      "isBackground": true
    }
  ]
}

4. Save
5. Test: Cmd+Shift+P → "Tasks: Run Task" → "List Inbox Pucks"
```
**Time:** 5 minutes
**Benefit:** Quick puck operations from command palette

---

### Phase 4 Success Criteria
- [x] Extensions installed and working
- [x] Keyboard shortcuts functional
- [x] VS Code tasks created
- [x] Workflow feels faster than pure SSH

---

## POST-DEPLOYMENT VERIFICATION

### Complete System Check

**Engine Room:**
```bash
# In VS Code Remote-SSH:
1. Bottom-left shows "SSH: balaur" (green)
2. Can navigate files in sidebar
3. Terminal runs on Balaur (hostname shows "balaur")
4. All Trinity CLIs work
5. Edit + save files instantly
```
**Status:** [PASS / FAIL]

---

**Captain's Deck (if deployed):**
```bash
# In VNC session:
1. XFCE desktop visible
2. VS Code launches from Applications menu
3. Can open multiple apps (VS Code + browser)
4. GPU acceleration active (run: glxinfo | grep OpenGL)
5. VNC reconnects after Balaur reboot
```
**Status:** [PASS / FAIL / SKIPPED]

---

**Hot Groq Test (if completed):**
```bash
# Deliverables exist:
1. /srv/janus/experiments/hot_groq_test/cold_response.txt
2. /srv/janus/experiments/hot_groq_test/hot_response.txt
3. /srv/janus/experiments/hot_groq_test/analysis.md
4. /srv/janus/experiments/hot_groq_test/test_report.md
5. Clear GO/NO-GO recommendation documented
```
**Status:** [PASS / FAIL / SKIPPED]

---

## KNOWN ISSUES & WORKAROUNDS

**Issue 1: VS Code Remote-SSH disconnects after idle**
- **Workaround:** Add to ~/.ssh/config: `ServerAliveInterval 60`
- **Fix:** Already in config if you followed Step 2

**Issue 2: VNC performance is slow**
- **Workaround:** Lower resolution: `vncserver :1 -geometry 1600x900`
- **Or:** Use SSH tunnel: `ssh -C -L 5901:localhost:5901 balaur` (adds compression)

**Issue 3: Can't save files in /srv/janus**
- **Check:** User permissions: `ls -la /srv/janus`
- **Fix:** Add your user to janus group: `sudo usermod -aG janus your_username`

---

## QUICK REFERENCE: DAILY USAGE

### Morning Startup (Engine Room)
```
1. Open VS Code on Mac
2. Cmd+Shift+P → "Remote-SSH: Connect to Host" → "balaur"
   (Or click "balaur" in Recent if shown)
3. Wait for connection (3-5 seconds)
4. File → Open Folder → /srv/janus (if not automatic)
5. Open terminal grid: Ctrl+`
6. Start monitoring: janus-controls watch
7. Ready to work!
```

### During the Day (Engine Room)
```
- Edit files: Click in sidebar, edit, Cmd+S to save
- Run commands: Type in terminal
- Trinity CLI: Ctrl+Alt+C for Claude, Ctrl+Alt+G for Gemini, etc.
- Git: Use sidebar Source Control icon for visual operations
- Tasks: Cmd+Shift+P → "Tasks: Run Task" → Select operation
```

### Weekly Session (Captain's Deck)
```
1. On Mac: Finder → Connect to Server (Cmd+K)
2. Enter: vnc://balaur-ip:5901
3. Enter VNC password
4. Launch apps: VS Code, Firefox, GIMP, etc.
5. Work in full desktop environment
6. Close VNC when done (session persists on Balaur)
```

---

## SUCCESS METRICS

**Productivity Gains (Expected):**
- File navigation: 15x faster
- Code editing: 12x faster
- Git operations: 9x faster
- Multi-tasking: 4x throughput
- Overall: 8-12x for development tasks

**Before & After:**
- **Before:** 60 seconds to navigate to file, view contents, edit, save
- **After:** 5 seconds to navigate to file, view contents, edit, save

---

## NEXT STEPS AFTER DEPLOYMENT

1. **Use it for 2-3 days** - Get comfortable with workflow
2. **Identify friction points** - Note what still feels slow
3. **Optimize iteratively** - Add shortcuts, tasks, extensions as needed
4. **Execute Hot Groq test** - Prove hot vessel concept
5. **Decide on janus-groq-vessel.service** - Based on test results
6. **Expand to other hot vessels** - Gemini, Codex, etc.

---

## ROLLBACK PLAN (IF NEEDED)

**If Engine Room causes problems:**
```
1. Close VS Code
2. On Mac: rm -rf ~/.vscode-server/ (on Balaur)
3. Return to pure SSH workflow
4. No harm done - Balaur unchanged
```

**If Captain's Deck causes problems:**
```
1. Kill VNC: vncserver -kill :1
2. Disable service: sudo systemctl disable vncserver@1.service
3. Keep Engine Room - it's independent
4. Can retry Captain's Deck later
```

---

## CONTACT & SUPPORT

**If stuck:**
1. Check troubleshooting sections above
2. Run diagnostic commands provided
3. Consult Trinity (Claude, Gemini, Codex) via existing CLIs
4. Document issue for future reference

**Trinity Support:**
- **Claude:** Strategic guidance, constitutional alignment checks
- **Gemini:** Systems engineering, debugging, infrastructure
- **Codex:** Code fixes, script creation, precise solutions

---

**END OF TACTICAL CHECKLIST**

**Version:** 1.0
**Last Updated:** 2025-10-13
**Status:** READY FOR EXECUTION
**Recommended Start:** Phase 1 (30-45 min commitment)
