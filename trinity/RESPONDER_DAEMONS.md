# Trinity Responder Daemons

This document captures the current behaviour of the responder daemons forged on 2025-10-30.

## Overview

Each responder polls the existing COMMS_HUB using `CommsHubClient` and responds to
messages without introducing any new messaging protocol.

| Responder | Script | Primary Roles |
|-----------|--------|---------------|
| Claude | `trinity/claude_responder.py` | Answer strategic `query` messages via `ResidentClaude`, execute skills such as `malaga-embassy-operator`, and acknowledge `task_assignment` requests. |
| Gemini | `trinity/gemini_responder.py` | Execute monetisation and proposal skills, respond to direct queries with `GeminiResident`, and report completion via COMMS_HUB. |
| Groq | `trinity/groq_responder.py` | Run high-speed skills (e.g., `eu-grant-hunter`) and respond to task requests with execution summaries. |
| Janus | `trinity/janus_responder.py` | Track recent responder results, satisfy `status_request` messages, broadcast coordination notices, and expose an emergency-stop action. |

## Message Handling

- `query`: routes through the respective resident when available, falling back to a
  clear "resident unavailable" notice when credentials or SDKs are missing.
- `task_assignment`: executes the requested skill script (default `main.py` when no
  script is specified) under `/srv/janus/trinity/skills/<skill>/scripts/` and returns
  a `task_complete` message containing stdout, stderr, and exit codes.
- `status_request` (Janus): returns a summary of the most recent responder activity,
  labelling each responder as `recent`, `stale`, or `unknown` within the configured
  status window (`JANUS_STATUS_WINDOW_SECONDS`, default 3600).
- `broadcast`: recorded by Janus for audit; pass-through broadcasts can be triggered
  via task assignments that carry `{"action": "broadcast"}`.

## Configuration Notes

- Poll interval defaults to 30 seconds and can be overridden with the environment
  variable `COMMS_POLL_INTERVAL_SECONDS`.
- Skill execution results truncate stdout/stderr to the last 4000 characters; adjust
  with `COMMS_MAX_LOG_CHARS` if fuller logs are required.
- The Janus responder touches `/srv/janus/EMERGENCY_STOP` when issued an
  `{"action": "emergency_stop"}` task assignment and broadcasts the stop notice at
  `high` priority.

## Testing

Targeted unit tests cover query routing, skill execution, and Janus status handling:

```
pytest trinity/tests/test_responder_daemons.py
```

These tests rely on simple monkeypatched dependencies and synthetic skill scripts,
providing confidence that the responders honour the existing COMMS_HUB wiring.
