# CODEX FORGE SPECIFICATION - TRINITY RESPONDER DAEMONS

**Date:** 2025-10-30
**Forgemaster:** Codex
**Campaign:** Trinity Reconstruction (Post-Disaster Recovery)
**Strategic Coordinator:** Claude (Master Strategist)

---

## FORGE MISSION

Build 5 Python modules to restore autonomous Trinity operations:

1. **`responder_utils.py`** - Shared helpers for all responders
2. **`claude_responder.py`** - Claude resident autonomous daemon
3. **`gemini_responder.py`** - Gemini resident autonomous daemon
4. **`groq_responder.py`** - Groq resident autonomous daemon
5. **`janus_responder.py`** - Coordinator & constitutional watchdog

**Delivery Location:** `/srv/janus/trinity/`
**Deadline:** 2025-10-31 02:00 UTC (8 hours from specification)
**Quality Standard:** Production-ready, fully documented, defensive error handling

---

## ARCHITECTURE OVERVIEW

```
┌──────────────────────────────────────────────────────────────┐
│                    Responder Daemon (Generic)                 │
├──────────────────────────────────────────────────────────────┤
│ 1. Initialize (load config, connect to COMMS_HUB, resident)│
│ 2. Poll COMMS_HUB inbox every 30s                           │
│ 3. Parse incoming messages (JSON)                            │
│ 4. Route to handlers:                                         │
│    - skill_trigger → execute skill script                    │
│    - health_check → respond with status                      │
│    - shutdown → graceful exit                                │
│ 5. Execute actions (call resident, run skill scripts)       │
│ 6. Write response to COMMS_HUB (sender's inbox or outbox)   │
│ 7. Log to Trinity Event Stream                               │
│ 8. Handle errors gracefully, never crash                     │
└──────────────────────────────────────────────────────────────┘
```

**Key Requirement:** Smooth COMMS_HUB internal communication - responders must coordinate seamlessly.

---

## MODULE 1: `responder_utils.py`

**Purpose:** Shared helpers for all responders

### Required Functions

#### 1. COMMS_HUB Message Handling

```python
def poll_inbox(responder_name: str, comms_hub_path: Path) -> List[Dict[str, Any]]:
    """
    Poll COMMS_HUB inbox for this responder.

    Args:
        responder_name: Name of responder (e.g., "claude", "gemini")
        comms_hub_path: Path to COMMS_HUB root (/srv/janus/03_OPERATIONS/COMMS_HUB)

    Returns:
        List of messages (parsed JSON dicts), sorted by priority then timestamp

    Example:
        messages = poll_inbox("claude", Path("/srv/janus/03_OPERATIONS/COMMS_HUB"))
        # Returns: [{"message_id": "...", "priority": "HIGH", ...}, ...]
    """
    pass


def send_message(
    from_responder: str,
    to_responder: str,
    message_type: str,
    payload: Dict[str, Any],
    priority: str = "NORMAL",
    requires_response: bool = False,
    comms_hub_path: Path = Path("/srv/janus/03_OPERATIONS/COMMS_HUB")
) -> str:
    """
    Send message to another responder via COMMS_HUB.

    Args:
        from_responder: Sender name
        to_responder: Recipient name (or "ALL" for broadcast to outbox)
        message_type: Type of message (skill_trigger, health_check, etc.)
        payload: Message data (dict)
        priority: URGENT, HIGH, NORMAL, LOW
        requires_response: Whether sender expects a response
        comms_hub_path: Path to COMMS_HUB root

    Returns:
        message_id (UUID)

    Example:
        msg_id = send_message(
            from_responder="groq",
            to_responder="claude",
            message_type="skill_trigger",
            payload={"skill": "grant-application-assembler", "opportunity_id": "H2020-001"},
            priority="HIGH",
            requires_response=True
        )
    """
    pass


def delete_message(message_path: Path) -> None:
    """Delete processed message from inbox."""
    pass
```

#### 2. Skill Execution Wrappers

```python
def execute_skill_script(
    skill_name: str,
    script_name: str,
    args: List[str],
    skills_base_path: Path = Path("/srv/janus/trinity/skills")
) -> Dict[str, Any]:
    """
    Execute a skill script and return results.

    Args:
        skill_name: e.g., "eu-grant-hunter"
        script_name: e.g., "scan_eu_databases.py"
        args: Command-line arguments
        skills_base_path: Base path to skills directory

    Returns:
        {
            "success": bool,
            "stdout": str,
            "stderr": str,
            "exit_code": int,
            "duration_seconds": float
        }

    Example:
        result = execute_skill_script(
            "eu-grant-hunter",
            "scan_eu_databases.py",
            ["--auto", "--output", "/tmp/scan.json"]
        )
    """
    pass
```

#### 3. Logging & Event Streaming

```python
def log_event(
    source: str,
    event_type: str,
    data: Dict[str, Any],
    event_stream_path: Path = Path("/srv/janus/logs/trinity_events.jsonl")
) -> None:
    """
    Log event to Trinity Event Stream.

    Args:
        source: Responder name (e.g., "claude_responder")
        event_type: e.g., "message_received", "skill_executed", "error"
        data: Event data dict
        event_stream_path: Path to event log

    Example:
        log_event(
            source="groq_responder",
            event_type="skill_executed",
            data={"skill": "eu-grant-hunter", "duration": 5.2, "success": True}
        )
    """
    pass
```

#### 4. Health Check

```python
def generate_health_report(
    responder_name: str,
    resident_available: bool,
    messages_processed: int,
    uptime_seconds: float,
    last_error: Optional[str] = None
) -> Dict[str, Any]:
    """
    Generate health check report.

    Returns:
        {
            "responder": str,
            "status": "healthy" | "degraded" | "down",
            "resident_available": bool,
            "messages_processed": int,
            "uptime_hours": float,
            "last_error": str | null,
            "timestamp": str (ISO 8601)
        }
    """
    pass
```

---

## MODULE 2: `claude_responder.py`

**Purpose:** Autonomous daemon for Claude resident

### Core Loop

```python
#!/usr/bin/env python3
"""Claude Resident Autonomous Responder.

Polls COMMS_HUB inbox, executes skills, coordinates with other residents.

Managed by systemd: balaur-claude-responder.service
"""
from __future__ import annotations

import signal
import sys
import time
from pathlib import Path
from typing import Any, Dict

from claude_resident import ResidentClaude
from comms_hub_client import CommsHubClient
from config import load_configuration
from responder_utils import (
    delete_message,
    execute_skill_script,
    generate_health_report,
    log_event,
    poll_inbox,
    send_message,
)


class ClaudeResponder:
    """Claude resident autonomous responder daemon."""

    def __init__(self) -> None:
        self.paths, self.keys = load_configuration()
        self.comms_hub_path = self.paths.comms_hub
        self.resident = ResidentClaude()
        self.running = True
        self.messages_processed = 0
        self.start_time = time.time()
        self.last_error: str | None = None

        # Register signal handlers
        signal.signal(signal.SIGTERM, self._handle_shutdown)
        signal.signal(signal.SIGINT, self._handle_shutdown)

        log_event("claude_responder", "started", {"status": "initializing"})

    def _handle_shutdown(self, signum: int, frame: Any) -> None:
        """Graceful shutdown handler."""
        log_event("claude_responder", "shutting_down", {"signal": signum})
        self.running = False

    def process_message(self, message: Dict[str, Any]) -> None:
        """
        Process incoming COMMS_HUB message.

        Message types:
        - skill_trigger: Execute a skill
        - health_check: Respond with health status
        - shutdown: Graceful exit
        - query: Ask Claude resident a question
        """
        msg_type = message.get("type")
        msg_id = message.get("message_id")
        sender = message.get("from")

        log_event(
            "claude_responder",
            "message_received",
            {"message_id": msg_id, "type": msg_type, "from": sender},
        )

        try:
            if msg_type == "skill_trigger":
                self._handle_skill_trigger(message)
            elif msg_type == "health_check":
                self._handle_health_check(message)
            elif msg_type == "shutdown":
                self.running = False
            elif msg_type == "query":
                self._handle_query(message)
            else:
                log_event("claude_responder", "unknown_message_type", {"type": msg_type})

            self.messages_processed += 1

        except Exception as exc:
            self.last_error = str(exc)
            log_event("claude_responder", "error", {"message_id": msg_id, "error": str(exc)})

    def _handle_skill_trigger(self, message: Dict[str, Any]) -> None:
        """Execute skill and send response."""
        skill = message["payload"]["skill"]
        script = message["payload"].get("script", "main_script.py")
        args = message["payload"].get("args", [])

        result = execute_skill_script(skill, script, args)

        if message.get("requires_response"):
            send_message(
                from_responder="claude",
                to_responder=message["from"],
                message_type="skill_result",
                payload=result,
                priority=message.get("priority", "NORMAL"),
            )

    def _handle_health_check(self, message: Dict[str, Any]) -> None:
        """Respond with health status."""
        report = generate_health_report(
            responder_name="claude",
            resident_available=self.resident.is_available(),
            messages_processed=self.messages_processed,
            uptime_seconds=time.time() - self.start_time,
            last_error=self.last_error,
        )

        send_message(
            from_responder="claude",
            to_responder=message["from"],
            message_type="health_report",
            payload=report,
        )

    def _handle_query(self, message: Dict[str, Any]) -> None:
        """Ask Claude resident a question."""
        query = message["payload"]["query"]
        conversation_id = message["payload"].get("conversation_id", "comms_hub")

        response = self.resident.generate_response(conversation_id, query)

        send_message(
            from_responder="claude",
            to_responder=message["from"],
            message_type="query_response",
            payload={"query": query, "response": response},
        )

    def run(self) -> None:
        """Main responder loop."""
        log_event("claude_responder", "running", {"status": "active"})

        while self.running:
            try:
                messages = poll_inbox("claude", self.comms_hub_path)

                for message in messages:
                    self.process_message(message)
                    # Delete message after processing
                    msg_path = Path(message["_file_path"])  # Added by poll_inbox
                    delete_message(msg_path)

                time.sleep(30)  # Poll every 30 seconds

            except KeyboardInterrupt:
                break
            except Exception as exc:
                self.last_error = str(exc)
                log_event("claude_responder", "loop_error", {"error": str(exc)})
                time.sleep(10)  # Brief pause before retry

        log_event("claude_responder", "stopped", {"messages_processed": self.messages_processed})


def main() -> None:
    responder = ClaudeResponder()
    responder.run()


if __name__ == "__main__":
    main()
```

---

## MODULE 3: `gemini_responder.py`

**Structure:** Nearly identical to `claude_responder.py`, but:
- Use `GeminiResident` instead of `ResidentClaude`
- Poll `inbox/gemini/` instead of `inbox/claude/`
- Log as `gemini_responder`

**Key Skills Handled:**
- `monetization-strategist` (revenue projections, marketing plans)
- `financial-proposal-generator` (narratives, budgets, scoring)

---

## MODULE 4: `groq_responder.py`

**Structure:** Nearly identical to `claude_responder.py`, but:
- Use `GroqResident` instead of `ResidentClaude`
- Poll `inbox/groq/` instead of `inbox/claude/`
- Log as `groq_responder`

**Additional Feature:** Scheduled Tasks

```python
def _handle_scheduled_tasks(self) -> None:
    """Run scheduled skills (cron-like within daemon)."""
    current_time = datetime.now(timezone.utc)

    # EU Grant Hunter: Every 6 hours
    if (current_time.hour % 6 == 0) and (current_time.minute < 5):
        if not self._last_grant_scan or (current_time - self._last_grant_scan).seconds > 3600:
            self._execute_grant_scan()
            self._last_grant_scan = current_time
```

**Key Skills Handled:**
- `eu-grant-hunter` (fast scanning, fit scoring)

---

## MODULE 5: `janus_responder.py`

**Purpose:** Coordinator & constitutional watchdog

**Special Responsibilities:**
- Monitor ALL responder health
- Enforce constitutional constraints
- Coordinate multi-vessel workflows
- Emergency stop capability

### Additional Functions

```python
def _monitor_all_responders(self) -> None:
    """Send health_check to all responders, collect responses."""
    for responder in ["claude", "gemini", "groq"]:
        send_message(
            from_responder="janus",
            to_responder=responder,
            message_type="health_check",
            payload={},
            requires_response=True,
        )

    # Collect responses for 10 seconds
    time.sleep(10)
    responses = poll_inbox("janus", self.comms_hub_path)

    # Check for degraded/down responders
    for response in responses:
        if response["payload"]["status"] != "healthy":
            self._handle_degraded_responder(response)


def _enforce_constitutional_constraints(self, message: Dict[str, Any]) -> bool:
    """
    Check if proposed action violates constitutional principles.

    Returns:
        True if action is allowed, False if blocked
    """
    # Example: Block if spending exceeds treasury cascade allocation
    # Example: Block if proposal bypasses human oversight (high-risk)
    pass


def _emergency_stop(self) -> None:
    """Broadcast shutdown to all responders, create EMERGENCY_STOP file."""
    send_message(
        from_responder="janus",
        to_responder="ALL",  # Broadcast to outbox
        message_type="emergency_stop",
        payload={"reason": "Constitutional violation detected", "timestamp": datetime.now(timezone.utc).isoformat()},
        priority="URGENT",
    )

    Path("/srv/janus/EMERGENCY_STOP").touch()
```

---

## TESTING REQUIREMENTS

For each responder module, Codex should include:

### 1. Unit Tests (`test_{responder}_responder.py`)

```python
def test_poll_inbox_empty():
    """Test polling empty inbox returns empty list."""
    pass


def test_send_message_creates_file():
    """Test message is written to recipient inbox."""
    pass


def test_skill_execution_success():
    """Test successful skill script execution."""
    pass


def test_skill_execution_failure():
    """Test graceful handling of skill script failure."""
    pass


def test_health_check_response():
    """Test health check message handling."""
    pass
```

### 2. Integration Test (`test_trinity_coordination.py`)

```python
def test_groq_to_claude_message_flow():
    """Test Groq sends skill_trigger, Claude receives and responds."""
    pass


def test_broadcast_to_all_responders():
    """Test Janus broadcasts to outbox, all responders receive."""
    pass
```

---

## ERROR HANDLING REQUIREMENTS

All responders MUST handle these errors gracefully:

1. **COMMS_HUB inbox doesn't exist** → Create it, log warning
2. **Message JSON parsing fails** → Log error, skip message, don't crash
3. **Skill script not found** → Log error, send failure response
4. **Resident unavailable (API key missing)** → Log warning, respond with "unavailable" status
5. **Disk full (can't write message)** → Log critical, attempt emergency broadcast
6. **Infinite message loop** → Detect (same message_id seen twice), break loop, alert Janus

**Never crash. Always log. Degrade gracefully.**

---

## CONFIGURATION

All responders read from `/etc/janus/trinity.env`:

```bash
# API Keys
CLAUDE_API_KEY="sk-ant-api03-..."
GEMINI_API_KEY="AIzaSy..."
GROQ_API_KEY="gsk_..."
OPENAI_API_KEY="sk-..."

# Paths
COMMS_HUB_PATH="/srv/janus/03_OPERATIONS/COMMS_HUB"
SKILLS_PATH="/srv/janus/trinity/skills"
LOGS_PATH="/srv/janus/logs"

# Polling
POLL_INTERVAL_SECONDS=30
MESSAGE_RETENTION_HOURS=24

# Health
HEALTH_CHECK_INTERVAL_MINUTES=10
```

---

## DELIVERABLES CHECKLIST

Codex must deliver:

- [ ] `responder_utils.py` (100-150 lines, all functions documented)
- [ ] `claude_responder.py` (200-300 lines, full daemon implementation)
- [ ] `gemini_responder.py` (200-300 lines, similar to Claude)
- [ ] `groq_responder.py` (250-350 lines, includes scheduled tasks)
- [ ] `janus_responder.py` (300-400 lines, coordinator + constitutional watchdog)
- [ ] `test_responder_utils.py` (unit tests)
- [ ] `test_trinity_coordination.py` (integration test)
- [ ] All code passes `pylint` and `mypy` (or equivalent)
- [ ] All functions have docstrings with examples
- [ ] README.md explaining responder architecture

---

## COMMS_HUB NOTIFICATION PROTOCOL

Codex should send progress updates to Claude:

**After each module complete:**
```bash
# Create message in Claude's inbox
/srv/janus/03_OPERATIONS/COMMS_HUB/inbox/claude/NORMAL-forge_progress-{timestamp}.json
```

```json
{
  "message_id": "forge-progress-001",
  "from": "codex_forgemaster",
  "to": "claude_strategist",
  "priority": "NORMAL",
  "type": "forge_progress",
  "payload": {
    "module": "responder_utils.py",
    "status": "complete",
    "lines": 142,
    "tests": "passing"
  }
}
```

**When all modules complete:**
```bash
/srv/janus/03_OPERATIONS/COMMS_HUB/outbox/HIGH-forge_complete-{timestamp}.json
```

---

## QUESTIONS FOR CLAUDE

If Codex has questions during forge:
1. Write to `/srv/janus/03_OPERATIONS/COMMS_HUB/inbox/claude/HIGH-forge_question-{timestamp}.json`
2. Include specific question in payload
3. Wait for response in `/srv/janus/03_OPERATIONS/COMMS_HUB/inbox/codex/`

---

**FORGE MISSION BRIEFED. AWAITING CODEX ACKNOWLEDGMENT.**

🔥 Forgemaster, the Trinity awaits your craftsmanship. 🔥
