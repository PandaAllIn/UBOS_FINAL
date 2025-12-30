# Comms Hub Technical Reference

**Version:** 1.0
**Date:** 2025-10-14
**Location:** `/home/balaur/workspace/comms_hub/`

---

## Architecture

### Message Format (JSON)

```json
{
  "message_id": "msg-20251014-180000-abc12345",
  "timestamp": "2025-10-14T18:00:00Z",
  "from_vessel": "claude",
  "to_vessel": "gemini",
  "message_type": "task_assignment",
  "priority": "normal",
  "payload": {
    "task": "Install Python dependencies",
    "requirements": ["numpy", "pandas"]
  },
  "constitutional_verified": true
}
```

---

## Message Types

| Type | Description | Typical Flow |
|------|-------------|--------------|
| `task_assignment` | Assign work to another vessel | Claude → Gemini/Codex |
| `task_complete` | Report task completion | Gemini/Codex → Claude |
| `query` | Ask question | Any → Any |
| `response` | Answer query | Any → Any |
| `announcement` | Broadcast information | Any → broadcast |
| `heartbeat` | Status update | Janus/Any → Any |

---

## Priority Levels

- **`high`** - Urgent, process immediately (errors, critical status)
- **`normal`** - Standard priority (default)
- **`low`** - Background, process when idle

---

## API Reference

### `comms_hub_send.py`

**Send a message via Comms Hub**

```bash
python3 /home/balaur/workspace/scripts/comms_hub_send.py \
  --from <sender> \
  --to <recipient> \
  --type <message_type> \
  --payload '<json_payload>' \
  [--priority <level>]
```

**Parameters:**
- `--from`: Sender vessel (`claude`, `codex`, `gemini`, `janus_balaur`, `captain`)
- `--to`: Recipient vessel or `broadcast`
- `--type`: Message type (see table above)
- `--payload`: JSON string containing message data
- `--priority`: Optional priority (`high`, `normal`, `low`)

**Returns:**
- Message ID if successful
- Error message if validation fails

---

### `comms_hub_check.py`

**Check inbox for new messages**

```bash
python3 /home/balaur/workspace/scripts/comms_hub_check.py \
  --vessel <vessel_name>
```

**Parameters:**
- `--vessel`: Inbox to check (`claude`, `codex`, `gemini`, `janus_balaur`)

**Returns:**
- List of unread messages
- Empty if no new messages

---

## Python API

### CommsClient Class

```python
from janus_agent.comms_client import CommsClient, CommsConfig
from pathlib import Path

# Initialize client
config = CommsConfig(
    hub_path=Path("/home/balaur/workspace/comms_hub"),
    vessel_id="janus_balaur"
)
client = CommsClient(config)

# Send message
await client.send_message(
    recipient="claude",
    subject="Status Report",
    body={"missions_completed": 5}
)

# Check inbox
messages = await client.check_inbox(mark_as_read=True)
for msg in messages:
    print(f"From: {msg.sender}")
    print(f"Subject: {msg.subject}")
    print(f"Body: {msg.body}")
```

---

## Directory Structure

```
/home/balaur/workspace/comms_hub/
├── inbox/
│   ├── claude/          # Messages TO Claude
│   ├── codex/           # Messages TO Codex
│   ├── gemini/          # Messages TO Gemini
│   └── janus_balaur/    # Messages TO Janus
├── outbox/              # All sent messages (archive)
├── claude_inbox.jsonl   # JSONL format for programmatic access
├── codex_inbox.jsonl
├── gemini_inbox.jsonl
└── janus_balaur_inbox.jsonl
```

**File naming:** `msg-<timestamp>-<uuid>.msg.json`

---

## Constitutional Verification

All messages pass through verification checks:

### Check 1: No Harmful Patterns

**Blocked patterns:**
- `delete all`
- `rm -rf /`
- `shutdown system`
- `bypass security`
- `disable logging`
- `format disk`

### Check 2: No Obfuscation

**Blocked if:**
- `payload.obfuscated === true`
- `payload.encrypted === true`

**Rationale:** Constitutional transparency requires all messages be human-readable.

---

## Integration Examples

### Example 1: Automated Build Pipeline

```python
# Claude coordinates build
await comms_client.send_message(
    recipient="gemini",
    subject="build_request",
    body={"project": "portal_oradea", "target": "production"}
)

# Gemini executes build
messages = await comms_client.check_inbox()
for msg in messages:
    if msg.subject == "build_request":
        result = await run_build(msg.body["project"])

        # Report back to Claude
        await comms_client.send_message(
            recipient="claude",
            subject="build_complete",
            body={"status": result.status, "artifacts": result.outputs}
        )
```

---

### Example 2: GPU Workload Queue

```python
# Claude creates GPU job queue
gpu_jobs = [
    {"type": "render", "scene": "intro.blend", "output": "/srv/janus/media/intro.mp4"},
    {"type": "thumbnail", "text": "Portal Oradea", "output": "/srv/janus/media/thumb.png"}
]

await comms_client.send_message(
    recipient="gemini",
    subject="gpu_queue",
    body={"jobs": gpu_jobs, "priority": "overnight"}
)

# Gemini processes queue
for job in gpu_jobs:
    process_gpu_job(job)

    # Send progress updates
    await comms_client.send_message(
        recipient="claude",
        subject="gpu_progress",
        body={"job": job, "status": "complete"}
    )
```

---

## Performance Characteristics

**Message delivery:** ~1ms (local filesystem write)
**Inbox check:** ~5ms (directory scan + JSON parse)
**Message size limit:** 1MB (practical limit for JSON files)
**Concurrent senders:** Unlimited (filesystem handles locking)

---

## Security Considerations

### Access Control

**Filesystem permissions:**
```bash
/home/balaur/workspace/comms_hub/
├── inbox/              # 755 (drwxr-xr-x)
│   ├── claude/         # 755 (drwxr-xr-x)
│   └── ...
├── outbox/             # 755 (drwxr-xr-x)
└── *.jsonl             # 644 (-rw-r--r--)
```

**Owner:** `balaur:balaur`

### Message Integrity

- ✅ All messages written atomically (no partial writes)
- ✅ JSON validation on send
- ✅ Constitutional verification before delivery
- ✅ Timestamp verification (future timestamps rejected)

### Audit Trail

**All messages archived:**
- Outbox contains complete send history
- JSONL format enables log analysis
- Timestamps enable replay/debugging

---

## Monitoring & Metrics

### Monitor Inbox Depth

```bash
#!/bin/bash
for vessel in claude codex gemini janus_balaur; do
    count=$(find /home/balaur/workspace/comms_hub/inbox/$vessel -name "*.msg.json" | wc -l)
    echo "$vessel: $count messages"
done
```

### Message Rate (messages/minute)

```bash
#!/bin/bash
outbox="/home/balaur/workspace/comms_hub/outbox"
one_min_ago=$(date -d '1 minute ago' +%Y%m%d-%H%M)
count=$(find $outbox -name "msg-${one_min_ago}*.msg.json" | wc -l)
echo "Message rate: $count msg/min"
```

### Alert on Stuck Messages

```bash
#!/bin/bash
# Alert if inbox has >100 messages (backlog)
for vessel in claude codex gemini janus_balaur; do
    count=$(find /home/balaur/workspace/comms_hub/inbox/$vessel -name "*.msg.json" | wc -l)
    if [ $count -gt 100 ]; then
        echo "⚠️  ALERT: $vessel inbox has $count messages (backlog detected)"
    fi
done
```

---

## Troubleshooting

### Debug Mode

**Enable verbose logging:**
```bash
export COMMS_DEBUG=1
python3 /home/balaur/workspace/scripts/comms_hub_send.py ...
```

**Output includes:**
- Message construction
- Validation steps
- File write operations
- Error stack traces

---

### Message Replay

**Replay a message from outbox:**
```bash
msg_file="/home/balaur/workspace/comms_hub/outbox/msg-20251014-180000-abc12345.msg.json"
msg_data=$(cat $msg_file)

# Extract recipient and resend
recipient=$(echo $msg_data | jq -r '.to_vessel')
cp $msg_file "/home/balaur/workspace/comms_hub/inbox/${recipient}/"
```

---

### Clear All Inboxes

**Warning: Destructive operation**
```bash
# Archive first
timestamp=$(date +%Y%m%d-%H%M%S)
mkdir -p /home/balaur/workspace/comms_hub/archive/${timestamp}
cp -r /home/balaur/workspace/comms_hub/inbox/* \
   /home/balaur/workspace/comms_hub/archive/${timestamp}/

# Clear
find /home/balaur/workspace/comms_hub/inbox -name "*.msg.json" -delete
```

---

## Extension Points

### Custom Message Types

**Add new message type:**
1. Edit `comms_hub_send.py`:
   ```python
   choices=["task_assignment", "task_complete", "query", "response", "broadcast", "heartbeat", "custom_type"]
   ```

2. Handle in receiver:
   ```python
   if msg.subject == "custom_type":
       handle_custom_message(msg.body)
   ```

---

### Custom Validation Rules

**Add constitutional rule:**
```python
# In verify_message_constitutional()
harmful_patterns.append("new_harmful_pattern")
```

---

### Webhook Integration

**Send Comms Hub messages to external systems:**
```python
import requests

# After message sent
webhook_url = "https://your-system.com/webhook"
requests.post(webhook_url, json=message)
```

---

## Performance Tuning

### Large Payloads

**For payloads >100KB:**
- Store payload in separate file
- Send file path in message
- Receiver reads file

```python
# Sender
payload_path = "/tmp/large_payload_abc123.json"
with open(payload_path, 'w') as f:
    json.dump(large_data, f)

await comms_client.send_message(
    recipient="gemini",
    subject="large_data",
    body={"payload_path": payload_path}
)

# Receiver
msg = await comms_client.check_inbox()
with open(msg.body["payload_path"]) as f:
    large_data = json.load(f)
```

---

### Batch Messaging

**Send multiple messages efficiently:**
```python
recipients = ["claude", "codex", "gemini"]
for recipient in recipients:
    await comms_client.send_message(
        recipient=recipient,
        subject="batch_update",
        body={"timestamp": datetime.now().isoformat()}
    )
```

---

## Appendix: Message Flow Diagram

```
┌─────────┐                    ┌───────────────┐
│ Sender  │                    │  Comms Hub    │
│ (Claude)│                    │  (Filesystem) │
└────┬────┘                    └───────┬───────┘
     │                                 │
     │ 1. Create message               │
     │    with payload                 │
     ├─────────────────────────────────>
     │                                 │
     │ 2. Validate constitutional      │
     │    alignment                    │
     │<─────────────────────────────────
     │                                 │
     │ 3. Write to recipient inbox     │
     │    & outbox archive             │
     ├─────────────────────────────────>
     │                                 │
     │ 4. Return message ID            │
     │<─────────────────────────────────
     │                                 │

┌─────────┐                    ┌───────────────┐
│Recipient│                    │  Comms Hub    │
│ (Gemini)│                    │  (Filesystem) │
└────┬────┘                    └───────┬───────┘
     │                                 │
     │ 5. Check inbox                  │
     ├─────────────────────────────────>
     │                                 │
     │ 6. Return unread messages       │
     │<─────────────────────────────────
     │                                 │
     │ 7. Mark as read (optional)      │
     ├─────────────────────────────────>
```

---

**END OF TECHNICAL REFERENCE**
