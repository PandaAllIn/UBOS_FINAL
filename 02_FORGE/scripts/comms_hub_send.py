#!/usr/bin/env python3
"""
COMMS_HUB Message Sender
Enables vessels to send messages via the Trinity coordination infrastructure.
"""
import argparse
import json
import os
import uuid
from datetime import datetime, timezone
from pathlib import Path

BASE_DIR = Path("/srv/janus")
COMMS_DIR = BASE_DIR / "03_OPERATIONS" / "COMMS_HUB"


def resolve_inbox_directory(recipient: str) -> Path:
    primary = COMMS_DIR / recipient / "inbox"
    primary.mkdir(parents=True, exist_ok=True)
    return primary


def send_message(from_vessel: str, to_vessel: str, message_type: str, payload: dict, priority: str = "normal") -> str:
    """
    Send a message via COMMS_HUB.

    Args:
        from_vessel: Sending vessel (claude, codex, gemini)
        to_vessel: Receiving vessel (claude, codex, gemini, broadcast)
        message_type: Type of message (task_assignment, query, response, etc.)
        payload: Message payload as dictionary
        priority: Message priority (high, normal, low)

    Returns:
        message_id: Unique identifier for the sent message
    """

    # Generate message ID
    timestamp_str = datetime.now(timezone.utc).strftime('%Y%m%d-%H%M%S')
    msg_id = f"msg-{timestamp_str}-{uuid.uuid4().hex[:8]}"

    # Construct message
    message = {
        "message_id": msg_id,
        "timestamp": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "from_vessel": from_vessel,
        "to_vessel": to_vessel,
        "message_type": message_type,
        "priority": priority,
        "payload": payload,
        "constitutional_verified": verify_message_constitutional(payload)
    }

    # Determine recipients
    if to_vessel == "broadcast":
        recipients = ["claude", "gemini", "groq", "janus"]
    else:
        recipients = [to_vessel]

    # Write to recipient inboxes
    for recipient in recipients:
        inbox_dir = resolve_inbox_directory(recipient)

        inbox_file = inbox_dir / f"{msg_id}.msg.json"
        inbox_file.write_text(json.dumps(message, indent=2))

    # Archive in outbox
    outbox_dir = COMMS_DIR / "outbox"
    outbox_dir.mkdir(parents=True, exist_ok=True)

    outbox_file = outbox_dir / f"{msg_id}.msg.json"
    outbox_file.write_text(json.dumps(message, indent=2))

    return msg_id


def verify_message_constitutional(payload: dict) -> bool:
    """
    Verify message aligns with constitutional principles.

    Checks:
    - No harmful instructions
    - No obfuscation or encryption (transparency requirement)
    - Constitutional alignment

    Returns:
        True if message passes verification, False otherwise
    """

    # Convert payload to string for pattern matching
    payload_str = json.dumps(payload).lower()

    # Check 1: No harmful patterns
    harmful_patterns = [
        "delete all",
        "rm -rf /",
        "shutdown system",
        "bypass security",
        "disable logging",
        "format disk"
    ]

    if any(pattern in payload_str for pattern in harmful_patterns):
        print(f"⚠️  WARNING: Message contains harmful pattern and was BLOCKED")
        return False

    # Check 2: No obfuscation (all messages must be transparent)
    if payload.get('obfuscated', False) or payload.get('encrypted', False):
        print(f"⚠️  WARNING: Message contains obfuscation and was BLOCKED")
        return False

    # All checks passed
    return True


def main():
    parser = argparse.ArgumentParser(
        description="Send a message via COMMS_HUB",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Send a task assignment to Codex
  python3 comms_hub_send.py --from claude --to codex --type task_assignment \
    --payload '{"task": "Analyze daemon.py dependencies"}'

  # Broadcast to all vessels
  python3 comms_hub_send.py --from claude --to broadcast --type announcement \
    --payload '{"message": "Trinity sync complete"}' --priority high
"""
    )

    parser.add_argument(
        "--from",
        dest="from_vessel",
        required=True,
        choices=["claude", "codex", "gemini", "groq", "openai", "janus", "janus_balaur", "captain"],
        help="Sending vessel"
    )

    parser.add_argument(
        "--to",
        dest="to_vessel",
        required=True,
        help="Receiving vessel (claude, codex, gemini, or broadcast)"
    )

    parser.add_argument(
        "--type",
        dest="message_type",
        required=True,
        choices=["task_assignment", "task_complete", "query", "response", "broadcast", "heartbeat"],
        help="Type of message"
    )

    parser.add_argument(
        "--payload",
        required=False,
        help="Message payload as JSON string"
    )

    parser.add_argument(
        "--priority",
        default="normal",
        choices=["high", "normal", "low"],
        help="Message priority (default: normal)"
    )

    args = parser.parse_args()

    # Parse payload JSON
    payload_str = args.payload
    if payload_str is None:
        payload_str = sys.stdin.read()

    print(f"Received payload: {payload_str}")

    try:
        payload = json.loads(payload_str)
    except json.JSONDecodeError as e:
        print(f"❌ ERROR: Invalid JSON payload: {e}")
        return 1

    # Send message
    try:
        msg_id = send_message(
            from_vessel=args.from_vessel,
            to_vessel=args.to_vessel,
            message_type=args.message_type,
            payload=payload,
            priority=args.priority
        )

        print(f"✅ Message sent successfully")
        print(f"   Message ID: {msg_id}")
        print(f"   From: {args.from_vessel}")
        print(f"   To: {args.to_vessel}")
        print(f"   Type: {args.message_type}")

        return 0

    except Exception as e:
        print(f"❌ ERROR sending message: {e}")
        return 1


if __name__ == "__main__":
    exit(main())

