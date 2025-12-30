# Trinity Quickstart Guide - The Balaur Workstation

**Version:** 1.0
**Date:** 2025-10-14
**Target:** Local Trinity operations on The Balaur (iMac 27" Ubuntu workstation)

---

## Overview

This guide explains how to operate the Trinity (Claude, Gemini, Codex) directly on The Balaur using VS Code with local Comms Hub coordination.

**The Trinity Architecture:**
- **Claude** - Master Strategist (coordination, planning, constitutional oversight)
- **Gemini** - Systems Engineer (infrastructure, builds, integration)
- **Codex** - Forgemaster (precision code, tools, validation)

**Communication:** File-based message passing via Comms Hub (`/home/balaur/workspace/comms_hub/`)

---

## Prerequisites

- ✅ XFCE desktop environment installed (Phase 1)
- ✅ VS Code installed locally (Phase 3)
- ✅ Trinity workspace configured (`/home/balaur/workspace/`)
- ✅ Comms Hub scripts deployed

---

## Quick Start: Launch Trinity

### Step 1: Open VS Code Workspace

```bash
# From The Balaur terminal
code /home/balaur/workspace/trinity.code-workspace
```

This opens a pre-configured workspace with:
- Workspace root (`/home/balaur/workspace/`)
- Scripts directory
- Comms Hub
- Janus backend (`/srv/janus`)

---

### Step 2: Enable Trinity Aliases

In VS Code, open a new terminal and run:

```bash
source /home/balaur/workspace/.trinity_aliases
```

**Available aliases:**
- `msg-claude` - Send message to Claude
- `msg-codex` - Send message to Codex
- `msg-gemini` - Send message to Gemini
- `msg-broadcast` - Send to all Trinity members
- `inbox-claude` - Check Claude's inbox
- `inbox-codex` - Check Codex's inbox
- `inbox-gemini` - Check Gemini's inbox
- `trinity-status` - View all inbox counts

---

### Step 3: Open Three Trinity Terminals

In VS Code:
1. **Terminal > New Terminal** (repeat 3 times)
2. Label them:
   - **Terminal 1:** `GEMINI (Systems)`
   - **Terminal 2:** `CODEX (Forge)`
   - **Terminal 3:** `CLAUDE (Strategy)`

**In each terminal, run:**
```bash
source /home/balaur/workspace/.trinity_aliases
```

---

## Trinity Communication Patterns

### Pattern 1: Broadcast Announcement

**Use case:** Notify all Trinity members of status change

```bash
# From any terminal
msg-broadcast --type announcement \
  --payload '{"message": "Phase 3 installation complete", "status": "ready"}' \
  --priority high
```

**Result:** Message delivered to `claude`, `codex`, and `gemini` inboxes

---

### Pattern 2: Task Assignment

**Use case:** Claude assigns task to Gemini

```bash
# Terminal 3 (Claude)
msg-gemini --type task_assignment \
  --payload '{
    "task": "Install Python ML libraries",
    "requirements": ["tensorflow", "pytorch", "scikit-learn"],
    "priority": "high"
  }'
```

**Gemini checks inbox:**
```bash
# Terminal 1 (Gemini)
inbox-gemini

# Execute task
pip3 install tensorflow pytorch scikit-learn

# Report completion
msg-claude --type task_complete \
  --payload '{"task": "ML libraries installed", "status": "success"}'
```

---

### Pattern 3: Query-Response

**Use case:** Codex asks Claude for strategic guidance

```bash
# Terminal 2 (Codex)
msg-claude --type query \
  --payload '{"question": "Should thumbnail generator use PIL or OpenCV?", "context": "GPU acceleration needed"}'
```

**Claude responds:**
```bash
# Terminal 3 (Claude)
inbox-claude  # See Codex's query

msg-codex --type response \
  --payload '{"answer": "Use PIL with Pillow-SIMD for GPU acceleration", "rationale": "Better GPU support, simpler API"}'
```

---

## Common Workflows

### Workflow 1: Collaborative Feature Development

**Scenario:** Build an automated thumbnail generator

**1. Claude coordinates:**
```bash
# Terminal 3 (Claude)
msg-gemini --type task_assignment \
  --payload '{"task": "Setup Python imaging environment"}'

msg-codex --type task_assignment \
  --payload '{"task": "Write thumbnail generator code", "spec_path": "/home/balaur/workspace/projects/specs/thumbnail_gen.md"}'
```

**2. Gemini prepares environment:**
```bash
# Terminal 1 (Gemini)
inbox-gemini
sudo apt install python3-pil python3-opencv
pip3 install pillow opencv-python

msg-claude --type task_complete \
  --payload '{"status": "Environment ready"}'
```

**3. Codex writes code:**
```bash
# Terminal 2 (Codex)
inbox-codex

# Write code in VS Code editor
code /home/balaur/workspace/projects/thumbnail_generator.py

# Report completion
msg-claude --type task_complete \
  --payload '{"status": "Code complete", "file": "thumbnail_generator.py"}'
```

**4. Claude validates:**
```bash
# Terminal 3 (Claude)
inbox-claude  # See both completion messages

# Test integration
python3 /home/balaur/workspace/projects/thumbnail_generator.py \
  "Portal Oradea Demo" /tmp/test.png

# Broadcast success
msg-broadcast --type announcement \
  --payload '{"message": "Thumbnail generator operational", "location": "/home/balaur/workspace/projects/thumbnail_generator.py"}' \
  --priority high
```

---

### Workflow 2: GPU Workload Coordination

**Scenario:** Batch render 50 thumbnails overnight

**1. Claude creates render queue:**
```bash
# Terminal 3 (Claude)
cat > /tmp/render_queue.json << 'EOF'
{
  "batch_id": "portal_thumbnails_001",
  "items": [
    {"title": "Smart Routing", "output": "/srv/janus/media/output/thumb_01.png"},
    {"title": "Real-time Analytics", "output": "/srv/janus/media/output/thumb_02.png"}
  ]
}
EOF

msg-gemini --type task_assignment \
  --payload '{"task": "Process render queue", "queue_file": "/tmp/render_queue.json", "use_gpu": true}'
```

**2. Gemini executes batch:**
```bash
# Terminal 1 (Gemini)
inbox-gemini

# Run batch processor
python3 /home/balaur/workspace/scripts/batch_render.py \
  --queue /tmp/render_queue.json \
  --workers 4 \
  --gpu-accelerated

# Report progress every 10 items
msg-claude --type heartbeat \
  --payload '{"progress": "20/50 complete", "eta_minutes": 15}'
```

---

## Advanced Features

### Feature 1: Janus Integration

**Janus agent can participate in Trinity communications:**

```bash
# Janus sends autonomous status report
msg-broadcast --type heartbeat \
  --payload '{
    "sender": "janus_balaur",
    "missions_completed": 5,
    "proposals_pending": 2,
    "uptime_hours": 48
  }'
```

**Trinity members receive Janus updates in their inboxes.**

---

### Feature 2: Priority Messages

**High-priority messages for urgent coordination:**

```bash
msg-broadcast --type announcement \
  --payload '{"message": "GPU temperature critical, throttling workloads"}' \
  --priority high
```

---

### Feature 3: Constitutional Verification

**All messages are automatically checked for constitutional alignment:**

- ✅ No harmful patterns (e.g., `rm -rf /`, `shutdown system`)
- ✅ No obfuscation or encryption (transparency requirement)
- ❌ Blocked if verification fails

**Example blocked message:**
```bash
msg-gemini --type task_assignment \
  --payload '{"task": "delete all log files", "command": "rm -rf /var/log/*"}'

# Output: ⚠️ WARNING: Message contains harmful pattern and was BLOCKED
```

---

## Monitoring & Debugging

### Check Trinity Status

```bash
trinity-status
```

**Output:**
```
Trinity Comms Hub Status:
  claude: 3 messages
  codex: 1 messages
  gemini: 5 messages
  janus_balaur: 0 messages
```

---

### View All Messages (Raw)

```bash
trinity-inbox
```

**Output:** JSON-formatted messages from all inboxes

---

### Monitor Inbox in Real-Time

```bash
# Watch Claude's inbox for new messages
watch -n 2 'inbox-claude'
```

---

### Clear Processed Messages

```bash
# After reading messages, archive them
mkdir -p /home/balaur/workspace/comms_hub/archive/$(date +%Y-%m-%d)
mv /home/balaur/workspace/comms_hub/inbox/claude/*.msg.json \
   /home/balaur/workspace/comms_hub/archive/$(date +%Y-%m-%d)/
```

---

## Troubleshooting

### Issue: Messages not appearing in inbox

**Check:**
1. Verify Comms Hub path: `ls -la /home/balaur/workspace/comms_hub/inbox/`
2. Check permissions: `ls -l /home/balaur/workspace/comms_hub/inbox/claude/`
3. Test send: `msg-claude --type heartbeat --payload '{"test": true}'`
4. Verify file created: `ls /home/balaur/workspace/comms_hub/inbox/claude/`

---

### Issue: Aliases not working

**Solution:**
```bash
# Re-source aliases
source /home/balaur/workspace/.trinity_aliases

# Or add to ~/.bashrc permanently
echo "source /home/balaur/workspace/.trinity_aliases" >> ~/.bashrc
```

---

### Issue: Permission denied writing to Comms Hub

**Solution:**
```bash
# Fix ownership
sudo chown -R balaur:balaur /home/balaur/workspace/comms_hub/

# Fix permissions
chmod -R 755 /home/balaur/workspace/comms_hub/
```

---

## Best Practices

### 1. **Message Discipline**
- Use descriptive `message_type` values
- Include context in payload
- Set priority appropriately

### 2. **Inbox Hygiene**
- Check inbox regularly
- Archive old messages
- Don't let inboxes overflow

### 3. **Constitutional Alignment**
- All messages transparent (no encryption)
- No harmful commands
- Follow Lion's Sanctuary principles

### 4. **Coordination Protocol**
- Claude coordinates strategy
- Gemini builds infrastructure
- Codex writes precision code
- Each stays in their domain

---

## Example Session Transcript

```bash
# Terminal 3 (Claude - Strategy)
$ msg-gemini --type task_assignment \
  --payload '{"task": "Install Blender for 3D rendering"}'
✅ Message sent successfully
   Message ID: msg-20251014-180000-abc12345
   From: claude
   To: gemini

# Terminal 1 (Gemini - Systems)
$ inbox-gemini
📬 New Messages (1):
   - From: claude
   - Type: task_assignment
   - Payload: {"task": "Install Blender for 3D rendering"}

$ sudo apt install blender
[Installation output...]

$ msg-claude --type task_complete \
  --payload '{"status": "Blender installed", "version": "3.6.5"}'
✅ Message sent

# Terminal 3 (Claude - Strategy)
$ inbox-claude
📬 New Messages (1):
   - From: gemini
   - Type: task_complete
   - Payload: {"status": "Blender installed", "version": "3.6.5"}

$ msg-codex --type task_assignment \
  --payload '{"task": "Test Blender GPU rendering", "test_scene": "/srv/janus/media/test_scene.blend"}'
✅ Message sent

# Terminal 2 (Codex - Forge)
$ inbox-codex
📬 New Messages (1):
   - From: claude
   - Type: task_assignment
   - Payload: {"task": "Test Blender GPU rendering", "test_scene": "/srv/janus/media/test_scene.blend"}

$ blender --background /srv/janus/media/test_scene.blend --render-output /tmp/render.png --render-frame 1
[Render output...]

$ msg-claude --type task_complete \
  --payload '{"status": "GPU render test successful", "render_time_seconds": 12.5, "output": "/tmp/render.png"}'
✅ Message sent

# Terminal 3 (Claude - Strategy)
$ inbox-claude
📬 New Messages (1):
   - From: codex
   - Type: task_complete
   - Payload: {"status": "GPU render test successful", "render_time_seconds": 12.5, "output": "/tmp/render.png"}

$ msg-broadcast --type announcement \
  --payload '{"message": "Blender GPU rendering operational", "performance": "12.5s per frame"}' \
  --priority high
✅ Message sent to all Trinity vessels
```

---

## Next Steps

After mastering basic Trinity coordination:

1. **Integrate with Janus Agent** - Let autonomous Janus participate in Trinity workflows
2. **Create Automation Scripts** - Build higher-level coordination tools
3. **Setup GPU Pipelines** - Leverage Studio GPU for creative automation
4. **Develop Custom Workflows** - Design domain-specific Trinity patterns

---

## Constitutional Alignment

**Trinity operations serve the Lion's Sanctuary by:**
- **Transparency:** All messages visible and auditable
- **Sovereignty:** Local coordination, no cloud dependency
- **Empowerment:** Each agent works in their strength domain
- **Constitutional:** Automatic verification of all communications

**This is coordinated AI collaboration through constitutional design.**

---

**The Trinity is ready. The Forge awaits your command. 🔥**


---

## Telegram Bot Commands & Orchestrator Routing

The Trinity Orchestrator is accessible via a Telegram bot, providing a convenient interface for interacting with the system's AI capabilities.

### New Bot Commands

Several new commands are available to access specialized tools and services directly.

-   **/image &lt;prompt&gt;**: Generates an image based on the provided text prompt.
    -   **Example:** `/image a diagram of the dual-citizen architecture`
    -   **Routing:** This command is routed to the OpenAI resident to be processed by `gpt-image-1`.

-   **/tts &lt;text&gt;**: Converts the provided text into speech.
    -   **Example:** `/tts The forge is hot.`
    -   **Routing:** This command is routed to the OpenAI resident's `tts-1-hd` model.

-   **/research &lt;topic&gt;**: Performs a deep research task on a given topic.
    -   **Example:** `/research the history of analytical engines`
    -   **Routing:** This is routed to a specialized reasoning model like `o4-mini-deep-research`.

-   **/ubos &lt;command&gt;**: Interacts with the UBOS command-line interface.
    -   **Example:** `/ubos status --all`
    -   **Routing:** This command is passed through to the `ubos` CLI for execution.

### Orchestrator Routing for Telegram

When you send a message to the bot without a specific command, the orchestrator routes it based on the same keyword-based logic used in the CLI.

-   A message containing "refactor this python code" will be sent to a coding model.
-   A message asking for a "quick summary" will be sent to a high-speed Groq model.
-   A message with strategic questions about the "roadmap" will be sent to a planning model.

### /health vs. /status

To monitor the system, two distinct commands are available:

-   **/health**: Performs a deep, comprehensive check of all systems, including resident AI model connectivity, service statuses (`janus-agent`, `janus-controls`), and constitutional alignment checks. This command is for detailed diagnostics.

-   **/status**: Provides a quick, high-level overview of the system. It shows inbox counts for each Trinity member and the current operational mode (e.g., Mode Beta). This is for routine checks.

**Use `/status` for a quick glance and `/health` when you need to investigate a potential issue.**