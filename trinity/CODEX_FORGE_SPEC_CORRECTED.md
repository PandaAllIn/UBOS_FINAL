# CODEX FORGE SPECIFICATION - CORRECTED (Use Existing COMMS_HUB)

**URGENT CORRECTION:** Previous spec designed a new protocol. **USE EXISTING COMMS_HUB INSTEAD.**

---

## WHAT EXISTS (DON'T REBUILD)

✅ **CommsHubClient** - Already works (`trinity/comms_hub_client.py`)
✅ **comms_hub_send.py** - Already works (`02_FORGE/scripts/comms_hub_send.py`)
✅ **Message format** - `.msg.json` files with pucklib
✅ **Directory structure** - `{agent}/inbox/`, `inbox/{agent}/`, `outbox/`

---

## WHAT TO BUILD (SIMPLE)

Build 4 responder daemons that USE the existing COMMS_HUB:

### 1. `claude_responder.py`

```python
#!/usr/bin/env python3
"""Claude Responder - Polls COMMS_HUB, executes skills."""
import time
from pathlib import Path
from claude_resident import ResidentClaude
from comms_hub_client import CommsHubClient

resident = ResidentClaude()
comms = CommsHubClient("claude")

while True:
    # Read messages using EXISTING client
    messages = comms.unpack(mark_as_read=True)

    for msg in messages:
        msg_type = msg.get("message_type")
        payload = msg.get("payload", {})

        if msg_type == "query":
            # Ask Claude resident
            response = resident.generate_response("comms", payload["query"])

            # Send response using EXISTING protocol
            comms.pack(
                recipient=msg["from_vessel"],
                payload={"response": response},
                priority=msg.get("priority", "normal")
            )

        elif msg_type == "task_assignment":
            # Execute skill (if skill name in payload)
            skill = payload.get("skill")
            if skill == "malaga-embassy-operator":
                # Run daily briefing
                import subprocess
                subprocess.run([
                    "python3",
                    f"/srv/janus/trinity/skills/malaga-embassy-operator/scripts/generate_daily_briefing.py",
                    "--auto"
                ])

    time.sleep(30)  # Poll every 30s
```

### 2. `gemini_responder.py`

Same structure, uses `GeminiResident` instead.

### 3. `groq_responder.py`

Same structure, uses `GroqResident`, handles `eu-grant-hunter` skill.

### 4. `janus_responder.py`

Coordinator - monitors all responders, handles broadcasts.

---

## KEY SIMPLIFICATIONS

**DON'T create:**
- ❌ New message format
- ❌ New file naming convention
- ❌ New polling logic
- ❌ responder_utils.py (use existing clients)

**DO create:**
- ✅ Simple daemon loops
- ✅ Use `CommsHubClient.unpack()` to read
- ✅ Use `CommsHubClient.pack()` to send
- ✅ Call skill scripts with `subprocess.run()`

---

## TESTING

```bash
# Send test message
python3 /srv/janus/02_FORGE/scripts/comms_hub_send.py \
  --from gemini \
  --to claude \
  --type query \
  --payload '{"query": "What is Lion's Sanctuary?"}' \
  --priority high

# Check if Claude responds
ls /srv/janus/03_OPERATIONS/COMMS_HUB/gemini/inbox/
```

---

**USE WHAT EXISTS. KEEP IT SIMPLE.**

🔥 Codex, disregard previous complex spec. Build simple daemons using existing tools. 🔥
