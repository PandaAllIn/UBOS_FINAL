# COMMS_HUB Protocol

**Date:** 2025-10-30
**Version:** 1.0
**Purpose:** Smooth internal communication between Trinity residents

## 🔗 Related Systems
- Trinity Identity: [[00_CONSTITUTION/config/CLAUDE|Claude]] | [[00_CONSTITUTION/config/CODEX|Codex]] | [[00_CONSTITUTION/config/GEMINI|Gemini]]
- Strategic Context: [[01_STRATEGY/ROADMAP|Roadmap]]
- Active Operations: [[03_OPERATIONS/STATE_OF_THE_REPUBLIC|Current State]]

---

## OVERVIEW

COMMS_HUB is the pneumatic tube network for Trinity resident coordination. All responders communicate via file-based JSON messages for reliability, auditability, and constitutional alignment.

**Path:** `/srv/janus/03_OPERATIONS/COMMS_HUB`

**Key Principle:** **Fire-and-forget messaging with optional responses.** No blocking waits, no complex queues, just simple file I/O.

---

## DIRECTORY STRUCTURE

```
/srv/janus/03_OPERATIONS/COMMS_HUB/
├── inbox/
│   ├── claude/           # Messages for Claude responder
│   ├── gemini/           # Messages for Gemini responder
│   ├── groq/             # Messages for Groq responder
│   ├── janus/            # Messages for Janus coordinator
│   └── codex/            # Messages for Codex (manual processing)
└── outbox/               # Broadcast messages (all responders read)
```

**Permissions:**
- Owner: `janus:janus`
- Mode: `775` (rwxrwxr-x)
- All responders run as `janus` user

---

## MESSAGE FORMAT

### Standard Message (JSON)

```json
{
  "message_id": "uuid-v4-string",
  "timestamp": "2025-10-30T18:30:00Z",
  "from": "sender_responder_name",
  "to": "recipient_responder_name",
  "priority": "URGENT|HIGH|NORMAL|LOW",
  "type": "message_type",
  "payload": {
    "key": "value",
    "...": "..."
  },
  "requires_response": true,
  "response_deadline": "2025-10-30T19:00:00Z"
}
```

### Field Descriptions

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `message_id` | string | ✅ | Unique identifier (UUID v4) |
| `timestamp` | string | ✅ | ISO 8601 timestamp (UTC) |
| `from` | string | ✅ | Sender responder name (e.g., "groq", "claude") |
| `to` | string | ✅ | Recipient ("claude", "gemini", "groq", "janus", "ALL" for broadcast) |
| `priority` | string | ✅ | URGENT, HIGH, NORMAL, LOW |
| `type` | string | ✅ | Message type (see types below) |
| `payload` | object | ✅ | Message-specific data |
| `requires_response` | bool | ❌ | Whether sender expects a response (default: false) |
| `response_deadline` | string | ❌ | ISO 8601 timestamp for response |

---

## MESSAGE TYPES

### 1. `skill_trigger`

**Purpose:** Request execution of a skill

**Payload:**
```json
{
  "skill": "eu-grant-hunter",
  "script": "scan_eu_databases.py",
  "args": ["--auto", "--output", "/tmp/scan.json"]
}
```

**Example:**
```json
{
  "message_id": "550e8400-e29b-41d4-a716-446655440000",
  "timestamp": "2025-10-30T09:00:00Z",
  "from": "janus",
  "to": "groq",
  "priority": "NORMAL",
  "type": "skill_trigger",
  "payload": {
    "skill": "eu-grant-hunter",
    "script": "scan_eu_databases.py",
    "args": ["--auto"]
  },
  "requires_response": true
}
```

**Response Type:** `skill_result`

---

### 2. `skill_result`

**Purpose:** Return result of skill execution

**Payload:**
```json
{
  "skill": "eu-grant-hunter",
  "script": "scan_eu_databases.py",
  "success": true,
  "stdout": "Found 5 opportunities...",
  "stderr": "",
  "exit_code": 0,
  "duration_seconds": 12.5
}
```

---

### 3. `health_check`

**Purpose:** Request health status

**Payload:** `{}` (empty)

**Response Type:** `health_report`

**Example:**
```json
{
  "message_id": "health-check-001",
  "timestamp": "2025-10-30T10:00:00Z",
  "from": "janus",
  "to": "claude",
  "priority": "NORMAL",
  "type": "health_check",
  "payload": {},
  "requires_response": true
}
```

---

### 4. `health_report`

**Purpose:** Return health status

**Payload:**
```json
{
  "responder": "claude",
  "status": "healthy|degraded|down",
  "resident_available": true,
  "messages_processed": 142,
  "uptime_hours": 8.5,
  "last_error": null,
  "timestamp": "2025-10-30T10:00:05Z"
}
```

---

### 5. `query`

**Purpose:** Ask a resident a question (conversational)

**Payload:**
```json
{
  "conversation_id": "string",
  "query": "What is the Lion's Sanctuary philosophy?"
}
```

**Response Type:** `query_response`

---

### 6. `query_response`

**Purpose:** Return answer to query

**Payload:**
```json
{
  "conversation_id": "string",
  "query": "What is the Lion's Sanctuary philosophy?",
  "response": "The Lion's Sanctuary is a design philosophy..."
}
```

---

### 7. `shutdown`

**Purpose:** Request graceful shutdown

**Payload:**
```json
{
  "reason": "Maintenance window",
  "timestamp": "2025-10-30T22:00:00Z"
}
```

---

### 8. `emergency_stop`

**Purpose:** Immediate halt of all operations (constitutional violation, critical error)

**Payload:**
```json
{
  "reason": "Constitutional violation detected",
  "violated_principle": "Human oversight bypassed",
  "timestamp": "2025-10-30T18:30:00Z"
}
```

**Sent by:** Janus coordinator only
**Priority:** Always URGENT
**Target:** ALL (broadcast to outbox)

---

## FILE NAMING CONVENTION

**Format:** `{priority}-{type}-{timestamp}-{message_id_short}.json`

**Examples:**
```
HIGH-skill_trigger-20251030T090000Z-550e8400.json
URGENT-emergency_stop-20251030T183000Z-a1b2c3d4.json
NORMAL-health_check-20251030T100000Z-f7e6d5c4.json
```

**Rules:**
1. Priority prefix ensures correct processing order (URGENT first)
2. Type helps with debugging/monitoring
3. Timestamp is ISO 8601 compact format (no colons, for filesystem compatibility)
4. Message ID short = first 8 chars of UUID

---

## POLLING PROTOCOL

### Responder Inbox Polling

**Frequency:** Every 30 seconds
**Process:**
1. List all `.json` files in responder's inbox
2. Sort by filename (priority first, then timestamp)
3. Process URGENT messages immediately
4. Process HIGH messages within 5 minutes
5. Process NORMAL messages within 30 minutes
6. Process LOW messages when idle
7. Delete message after successful processing

**Pseudocode:**
```python
while running:
    messages = list_inbox_messages(responder_name)
    messages.sort(key=lambda m: (priority_rank(m), m.timestamp))

    for message in messages:
        process_message(message)
        delete_message(message)

    sleep(30)
```

---

### Outbox Polling (Broadcasts)

**Frequency:** Every 60 seconds
**Process:**
1. List all `.json` files in outbox
2. Read messages not seen before (track by message_id)
3. Process if relevant to this responder
4. Don't delete (outbox messages cleaned by cron after 24h)

---

## PRIORITY HANDLING

| Priority | Processing | Use Cases |
|----------|------------|-----------|
| **URGENT** | Immediate, interrupt current work | Emergency stop, critical constitutional violation |
| **HIGH** | Within 5 minutes | Grant deadline alert, health degradation |
| **NORMAL** | Within 30 minutes | Regular skill execution, queries |
| **LOW** | When idle | Maintenance tasks, optional optimizations |

---

## RESPONSE PROTOCOL

### If `requires_response: true`

1. **Sender writes message** to recipient's inbox
2. **Recipient processes** and generates response
3. **Recipient writes response** to sender's inbox
4. **Sender polls inbox**, finds response, processes

**Example Flow:**
```
1. Groq → Claude inbox: skill_trigger (requires_response: true)
2. Claude processes skill
3. Claude → Groq inbox: skill_result
4. Groq reads result from inbox
```

### If `requires_response: false`

Fire-and-forget. Sender doesn't wait for response.

---

## BROADCAST PROTOCOL

### When to Broadcast

- **Emergency stop** (Janus)
- **System-wide alerts** (Janus)
- **Completion notifications** (any responder)
- **Status updates** (any responder)

### How to Broadcast

1. Write message to `outbox/` with `to: "ALL"`
2. All responders poll outbox every 60s
3. Responders read but don't delete outbox messages
4. Cron job cleans outbox messages >24h old

**Example:**
```json
{
  "message_id": "broadcast-001",
  "timestamp": "2025-10-30T20:00:00Z",
  "from": "gemini",
  "to": "ALL",
  "priority": "HIGH",
  "type": "deployment_complete",
  "payload": {
    "responders_deployed": 4,
    "all_healthy": true
  }
}
```

File: `/srv/janus/03_OPERATIONS/COMMS_HUB/outbox/HIGH-deployment_complete-20251030T200000Z-broadcast001.json`

---

## MESSAGE RETENTION

### Inbox Messages
- **Processed:** Deleted immediately after successful processing
- **Failed:** Retained for 24 hours, then deleted by cron
- **Unprocessed:** Retained for 24 hours, then moved to `inbox/archive/`

### Outbox Messages
- **All:** Retained for 24 hours, then deleted by cron

### Cron Job
```bash
# Clean old COMMS_HUB messages
0 */6 * * * find /srv/janus/03_OPERATIONS/COMMS_HUB -name "*.json" -mtime +1 -delete
```

---

## ERROR HANDLING

### Malformed JSON

**Problem:** Message file contains invalid JSON

**Handling:**
1. Log error to Trinity Event Stream
2. Move message to `inbox/malformed/`
3. Don't crash, continue processing other messages

### Missing Required Fields

**Problem:** Message missing `message_id`, `from`, `to`, or `type`

**Handling:**
1. Log error with available fields
2. Move message to `inbox/invalid/`
3. Don't respond (can't identify sender)

### Unknown Message Type

**Problem:** `type` field not recognized

**Handling:**
1. Log warning
2. Send response (if `requires_response: true`):
```json
{
  "type": "error",
  "payload": {
    "error": "Unknown message type",
    "original_type": "unknown_type"
  }
}
```

### Disk Full

**Problem:** Can't write message to inbox/outbox

**Handling:**
1. Log critical error
2. Attempt emergency broadcast to Janus
3. If broadcast fails, write to stdout (systemd journal)
4. Gracefully degrade: continue reading messages, but no responses

---

## MESSAGE LOOP PREVENTION

### Problem

Responder A sends message to B → B responds to A → A responds to B → infinite loop

### Solution

**Track processed message IDs:**
```python
processed_messages = set()

def process_message(message):
    msg_id = message["message_id"]

    if msg_id in processed_messages:
        log_warning("Duplicate message detected, skipping")
        return

    processed_messages.add(msg_id)

    # Process message...

    # Limit set size (keep last 1000 IDs)
    if len(processed_messages) > 1000:
        processed_messages.pop(oldest_id)
```

---

## CONSTITUTIONAL ALIGNMENT

### Transparency

✅ All messages logged to Trinity Event Stream
✅ Message files auditable (filesystem, not ephemeral queue)
✅ Timestamps enable full reconstruction of event sequence

### Human Oversight

✅ Captain can read COMMS_HUB manually (filesystem access)
✅ High-risk actions require Captain approval (not automated)
✅ Emergency stop always available

### Graceful Degradation

✅ If responder down, messages queue in inbox (not lost)
✅ If COMMS_HUB full, responders log locally and degrade
✅ Janus coordinator monitors health, alerts on degradation

---

## EXAMPLES

### Example 1: Grant Scan Coordination

**Step 1:** Janus triggers Groq to scan
```json
{
  "message_id": "grant-scan-001",
  "timestamp": "2025-10-30T09:00:00Z",
  "from": "janus",
  "to": "groq",
  "priority": "NORMAL",
  "type": "skill_trigger",
  "payload": {
    "skill": "eu-grant-hunter",
    "script": "scan_eu_databases.py",
    "args": ["--auto"]
  },
  "requires_response": true
}
```

**Step 2:** Groq scans, finds high-value opportunity
```json
{
  "message_id": "grant-alert-001",
  "timestamp": "2025-10-30T09:05:00Z",
  "from": "groq",
  "to": "claude",
  "priority": "HIGH",
  "type": "skill_trigger",
  "payload": {
    "skill": "grant-application-assembler",
    "opportunity": {
      "id": "HORIZON-2025-GEOTHERMAL-01",
      "fit_score": 4.3,
      "deadline": "2025-09-02T17:00:00Z"
    }
  },
  "requires_response": true
}
```

**Step 3:** Claude validates strategy, sends to Gemini
```json
{
  "message_id": "proposal-gen-001",
  "timestamp": "2025-10-30T09:10:00Z",
  "from": "claude",
  "to": "gemini",
  "priority": "HIGH",
  "type": "skill_trigger",
  "payload": {
    "skill": "financial-proposal-generator",
    "script": "generate_narrative.py",
    "args": [
      "--assembly", "geodatacenter-phase-1",
      "--section", "excellence"
    ]
  },
  "requires_response": true
}
```

**Step 4:** Gemini generates narrative, broadcasts completion
```json
{
  "message_id": "proposal-complete-001",
  "timestamp": "2025-10-30T09:20:00Z",
  "from": "gemini",
  "to": "ALL",
  "priority": "HIGH",
  "type": "proposal_milestone",
  "payload": {
    "opportunity_id": "HORIZON-2025-GEOTHERMAL-01",
    "milestone": "Excellence narrative complete",
    "score": 4.32,
    "next_step": "Generate Impact narrative"
  }
}
```

---

### Example 2: Health Monitoring

**Janus checks all responders:**
```bash
# Send health check to Claude
cat > inbox/claude/health-check-001.json

# Send health check to Gemini
cat > inbox/gemini/health-check-001.json

# Send health check to Groq
cat > inbox/groq/health-check-001.json

# Wait 60 seconds

# Collect responses from Janus inbox
cat inbox/janus/*health_report*.json
```

---

## TESTING PROTOCOL

### Unit Test: Message Parsing
```python
def test_parse_valid_message():
    msg = {
        "message_id": "test-001",
        "timestamp": "2025-10-30T10:00:00Z",
        "from": "test",
        "to": "claude",
        "priority": "NORMAL",
        "type": "health_check",
        "payload": {}
    }
    assert is_valid_message(msg) == True
```

### Integration Test: End-to-End Flow
```bash
# Write test message
cat > inbox/claude/test-001.json << EOF
{...}
EOF

# Wait for processing
sleep 60

# Check response
cat inbox/test/*response*.json
```

---

**COMMS_HUB PROTOCOL COMPLETE. SMOOTH INTERNAL COMMUNICATION ENABLED.** 🔥
