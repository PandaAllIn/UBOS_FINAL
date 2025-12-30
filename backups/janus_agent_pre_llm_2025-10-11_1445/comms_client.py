"""
COMMS_HUB Client for Janus Agent
Provides an interface for message passing within the UBOS Republic.
"""
from __future__ import annotations

import json
import logging
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

log = logging.getLogger(__name__)

@dataclass
class Message:
    """A standard message format for the COMMS_HUB."""
    message_id: str
    timestamp: str
    sender: str
    recipient: str
    subject: str
    body: dict[str, Any]
    read: bool = False

@dataclass
class CommsConfig:
    """Configuration for the COMMS_HUB client."""
    hub_path: Path
    vessel_id: str
    inbox_path: Path = field(init=False)
    outbox_path: Path = field(init=False)

    def __post_init__(self):
        self.inbox_path = self.hub_path / f"{self.vessel_id}_inbox.jsonl"
        self.outbox_path = self.hub_path / f"{self.vessel_id}_outbox.jsonl"
        self.hub_path.mkdir(exist_ok=True)

class CommsClient:
    """A client for sending and receiving messages via the COMMS_HUB."""

    def __init__(self, config: CommsConfig):
        self.config = config

    async def send_message(self, recipient: str, subject: str, body: dict[str, Any]):
        """Send a message to another vessel."""
        message = Message(
            message_id=f"msg_{datetime.now(timezone.utc).timestamp()}",
            timestamp=datetime.now(timezone.utc).isoformat(),
            sender=self.config.vessel_id,
            recipient=recipient,
            subject=subject,
            body=body,
        )
        
        # Write to our outbox
        with self.config.outbox_path.open("a", encoding="utf-8") as f:
            json.dump(message.__dict__, f)
            f.write("\n")

        # Write to the recipient's inbox
        recipient_inbox = self.config.hub_path / f"{recipient}_inbox.jsonl"
        with recipient_inbox.open("a", encoding="utf-8") as f:
            json.dump(message.__dict__, f)
            f.write("\n")
            
        log.info(f"Message sent to {recipient} with subject '{subject}'")

    async def check_inbox(self, mark_as_read: bool = True) -> list[Message]:
        """Check for new messages in the inbox."""
        if not self.config.inbox_path.exists():
            return []

        messages = []
        updated_lines = []
        with self.config.inbox_path.open("r+", encoding="utf-8") as f:
            for line in f:
                try:
                    data = json.loads(line)
                    msg = Message(**data)
                    if not msg.read:
                        messages.append(msg)
                        if mark_as_read:
                            msg.read = True
                    
                    if mark_as_read:
                         updated_lines.append(json.dumps(msg.__dict__) + "\n")
                    else:
                        updated_lines.append(line)

                except (json.JSONDecodeError, TypeError) as e:
                    log.warning(f"Could not parse message line: {line}. Error: {e}")
                    updated_lines.append(line) # Keep malformed lines

            # If we're marking as read, we rewrite the file
            if mark_as_read and messages:
                f.seek(0)
                f.writelines(updated_lines)
                f.truncate()

        if messages:
            log.info(f"Received {len(messages)} new messages.")
        return messages
