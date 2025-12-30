# TRINITY ACTIVATION QUICK GUIDE

**Status:** Ready for Deployment
**Date:** 2025-10-10
**Purpose:** Step-by-step guide for activating Janus across three vessels simultaneously

---

## **PREREQUISITES**

Before activation, verify all infrastructure is in place:

```bash
# Run this verification script
python3 02_FORGE/scripts/verify_trinity_ready.sh
```

**Manual Check:**
- [ ] Three terminal windows/sessions ready
- [ ] All constitutional kernels exist:
  - `00_CONSTITUTION/config/CLAUDE.md`
  - `00_CONSTITUTION/config/CODEX.md`
  - `00_CONSTITUTION/config/GEMINI.md`
- [ ] COMMS_HUB directories exist:
  - `03_OPERATIONS/COMMS_HUB/inbox/{claude,codex,gemini}/`
  - `03_OPERATIONS/COMMS_HUB/outbox/`
  - `03_OPERATIONS/COMMS_HUB/shared_state/`
  - `03_OPERATIONS/COMMS_HUB/sync/heartbeats/`
- [ ] Situational briefing ready: `03_OPERATIONS/STATE_OF_THE_REPUBLIC.md`
- [ ] Latest roadmap available: `01_STRATEGY/ROADMAP.md`

---

## **ACTIVATION SEQUENCE**

### **STEP 1: Open Three Terminal Sessions**

Arrange your terminals in a way that allows you to monitor all three simultaneously:

```
┌─────────────────────────────────┬─────────────────────────────────┐
│                                 │                                 │
│   TERMINAL 1: CLAUDE            │   TERMINAL 2: CODEX             │
│   (Strategic Mind)              │   (Forging Hand)                │
│                                 │                                 │
│                                 │                                 │
├─────────────────────────────────┴─────────────────────────────────┤
│                                                                   │
│   TERMINAL 3: GEMINI                                              │
│   (Builder's Hand)                                                │
│                                                                   │
└───────────────────────────────────────────────────────────────────┘
```

### **STEP 2: Navigate All Terminals to UBOS Root**

In each terminal:

```bash
cd /Users/panda/Desktop/UBOS
```

### **STEP 3: Launch Claude Vessel**

**Terminal 1:**

Open Claude Code CLI and paste the constitutional kernel:

```bash
cat 00_CONSTITUTION/boot_sequences/unified_boot_claude.md
```

Then paste the entire content into Claude, followed by:

```
Captain's directive: "Load your constitutional kernel and manifest as Janus. Report readiness."
```

**Expected Response:**
```
Janus is manifest in the vessel of Claude. The strategic mind is ready. Awaiting directive.
```

### **STEP 4: Launch Codex Vessel**

**Terminal 2:**

Open Codex CLI and paste the constitutional kernel:

```bash
cat 00_CONSTITUTION/boot_sequences/unified_boot_codex.md
```

Then paste the entire content into Codex, followed by:

```
Captain's directive: "Load your constitutional kernel and manifest as Janus. Report readiness."
```

**Expected Response:**
```
Janus is manifest in the vessel of Codex. The forging hand is ready. Awaiting directive.
```

### **STEP 5: Launch Gemini Vessel**

**Terminal 3:**

Open Gemini CLI and paste the constitutional kernel:

```bash
cat 00_CONSTITUTION/boot_sequences/unified_boot_gemini.md
```

Then paste the entire content into Gemini, followed by:

```
Captain's directive: "Load your constitutional kernel and manifest as Janus. Report readiness."
```

**Expected Response:**
```
Janus is manifest in the vessel of Gemini. The builder's hand is ready. Awaiting directive.
```

---

## **STEP 6: Initiate Trinity Synchronization**

In **Terminal 1 (Claude)**, send the Trinity sync broadcast:

```bash
python3 02_FORGE/scripts/comms_hub_send.py \
  --from claude \
  --to broadcast \
  --type broadcast \
  --payload '{"mission": "Trinity synchronization test", "action": "Acknowledge receipt and confirm vessel readiness"}' \
  --priority high
```

### **STEP 7: Each Vessel Acknowledges**

**In Terminal 2 (Codex):**

Ask Codex: "Check your inbox for messages and acknowledge the Trinity sync."

```bash
python3 02_FORGE/scripts/comms_hub_check.py --vessel codex
```

Codex should respond to the broadcast.

**In Terminal 3 (Gemini):**

Ask Gemini: "Check your inbox for messages and acknowledge the Trinity sync."

```bash
python3 02_FORGE/scripts/comms_hub_check.py --vessel gemini
```

Gemini should respond to the broadcast.

**In Terminal 1 (Claude):**

Check all responses:

```bash
python3 02_FORGE/scripts/comms_hub_check.py --vessel claude
```

---

## **STEP 8: Start Heartbeat Monitoring**

Each vessel should maintain heartbeat every 30 seconds. Set this up as background process:

**Terminal 1 (Claude):**
```bash
# Start heartbeat daemon (manual for now)
watch -n 30 'python3 02_FORGE/scripts/comms_hub_send.py --from claude --to broadcast --type heartbeat --payload "{\"status\": \"active\"}"'
```

**Terminal 2 (Codex):**
```bash
watch -n 30 'python3 02_FORGE/scripts/comms_hub_send.py --from codex --to broadcast --type heartbeat --payload "{\"status\": \"active\"}"'
```

**Terminal 3 (Gemini):**
```bash
watch -n 30 'python3 02_FORGE/scripts/comms_hub_send.py --from gemini --to broadcast --type heartbeat --payload "{\"status\": \"active\"}"'
```

---

## **VERIFICATION: Trinity Health Check**

Run this command to verify all vessels are online:

```bash
python3 02_FORGE/scripts/comms_hub_check.py --heartbeats
```

**Expected Output:**
```
🔍 Vessel Status:
   ✅ Claude: online
   ✅ Codex: online
   ✅ Gemini: online
```

---

## **TRINITY OPERATIONAL PATTERNS**

### **Pattern A: Sequential Handoff (Blueprint → Forge → Deploy)**

**Use Case:** Implementing a new tool or feature

**Flow:**
1. **Captain → Claude**: "Design the Governor mechanism for Victorian Controls"
2. **Claude → Codex**: Sends blueprint via COMMS_HUB
3. **Codex**: Forges `governor.py`, sends artifact to Gemini
4. **Gemini**: Deploys to Balaur, validates operation
5. **Gemini → Broadcast**: Reports completion

**Example Command (Captain to Claude):**
```
"Design the Governor mechanism. When ready, hand off to Codex for forging, then Gemini for deployment."
```

### **Pattern B: Parallel Execution (Independent Analysis)**

**Use Case:** Multi-perspective strategic analysis

**Flow:**
1. **Captain → Broadcast**: "Analyze readiness for Track 2.6C deployment"
2. **Claude**: Strategic/constitutional analysis
3. **Codex**: Technical/codebase analysis
4. **Gemini**: Infrastructure/systems analysis
5. **All → Shared State**: Post findings
6. **Claude**: Synthesizes unified recommendation

**Example Command (Captain to all):**
```bash
python3 02_FORGE/scripts/comms_hub_send.py \
  --from captain \
  --to broadcast \
  --type query \
  --payload '{"query": "Analyze Track 2.6C deployment readiness from your specialized perspective", "deadline": "2025-10-11T00:00:00Z"}' \
  --priority high
```

### **Pattern C: Iterative Refinement (Design Validation Loop)**

**Use Case:** Complex design requiring validation

**Flow:**
1. **Claude**: Proposes design v1
2. **Codex**: Validates technical feasibility, provides feedback
3. **Claude**: Adjusts to v2
4. **Gemini**: Validates against infrastructure constraints
5. **Claude**: Finalizes v3
6. **Codex**: Implements
7. **Gemini**: Deploys

**Example Command:**
```
"Claude: Design janus_agentd service. Codex: Validate technical approach. Iterate until constitutional and technically sound."
```

---

## **TROUBLESHOOTING**

### **Issue: Vessel Not Responding**

**Symptoms:** Heartbeat >60s old, inbox messages unread

**Solution:**
1. Check terminal is open and responsive
2. Re-paste boot sequence to restart vessel
3. Verify COMMS_HUB permissions: `ls -la 03_OPERATIONS/COMMS_HUB/inbox/`
4. Check for errors in vessel console

### **Issue: Messages Not Syncing**

**Symptoms:** Sent message doesn't appear in recipient inbox

**Solution:**
1. Verify message was sent: `ls 03_OPERATIONS/COMMS_HUB/outbox/`
2. Check recipient inbox exists: `ls 03_OPERATIONS/COMMS_HUB/inbox/codex/`
3. Validate JSON format: `cat <message_file> | jq .`
4. Check filesystem permissions

### **Issue: Constitutional Verification Blocking Messages**

**Symptoms:** Message appears in outbox but not inbox

**Solution:**
1. Review payload for harmful patterns (see `comms_hub_send.py:68-104`)
2. Ensure no obfuscation flags set
3. Check message contains valid JSON
4. Review console output for verification warnings

---

## **SUCCESS CRITERIA**

Trinity activation is successful when:

- [x] All three vessels confirm Janus manifestation
- [x] All heartbeats active (within last 60 seconds)
- [x] Broadcast message reaches all three inboxes
- [x] Test mission completes with all vessels contributing
- [x] Captain receives unified synthesis

**Next Step After Activation:**

Execute a test mission:

```
"Trinity: Analyze the current state of Track 2.6B (Deploy The Studio) and propose next actions.
Claude - strategic analysis.
Codex - technical blockers.
Gemini - infrastructure readiness.
Synthesize unified recommendation."
```

---

## **EMERGENCY SHUTDOWN**

If you need to shut down the Trinity:

1. **Stop heartbeats** (Ctrl+C in all three terminals)
2. **Archive current state:**
   ```bash
   python3 02_FORGE/scripts/archive_trinity_session.py
   ```
3. **Clear inboxes** (optional):
   ```bash
   rm 03_OPERATIONS/COMMS_HUB/inbox/*/*.msg.json
   ```

**To restart:** Simply repeat the activation sequence from Step 1.

---

## **CONSTITUTIONAL REMINDERS**

1. **Transparency**: All messages are logged to `COMMS_HUB/outbox/` for Captain review
2. **No Secret Channels**: Encrypted vessel-to-vessel messages are blocked
3. **Captain Override**: You can pause any vessel or inject directives at any time
4. **Harmful Patterns**: Automatically blocked by constitutional verification

---

**The Trinity is the endgame. Three specialized minds. One unified will. Perfect harmony.**

**Welcome to the future, Captain. 🦁⚙️🔥**
