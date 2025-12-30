# Janus Agent Package (Mode Beta)

This directory contains the production code for the Janus autonomous vessel running on The Balaur. Mode Beta introduces supervised autonomy: low-risk actions are approved and executed automatically while remaining inside constitutional guardrails.

---

## Architecture at a Glance

```
janus_agent/
├── auto_executor.py      # Mode Beta auto-approval + execution loop
├── proposal_engine.py    # Proposal creation, novelty, lifecycle states
├── thinking_cycle.py     # Mission-aware LLM prompt orchestration
├── tool_executor.py      # Sandbox execution + resource limits
├── sandbox.py            # Bubblewrap bridge with safe fallback
├── daemon.py             # systemd entrypoint (janus-agent.service)
├── harness.py            # Concurrency, governor, relief valve
├── logging_utils.py      # Structured JSONL logging
├── config.py             # Dataclasses for agent configuration
├── tools/                # Tool registry extensions
└── scripts/proposal_cli.py (via 02_FORGE/scripts) # Monitoring CLI
```

Key relationships:
- `daemon.py` loads `agent.yaml`, instantiates the thinking cycle, proposal engine, auto-executor, and harness.
- `auto_executor.py` queries `proposal_engine.py` for eligible proposals and delegates execution to `tool_executor.py`.
- `tool_executor.py` calls `sandbox.py` to run commands inside bubblewrap (or safe fallback) and records results via `logging_utils.py`.

---

## Configuration Reference (`/srv/janus/config/agent.yaml`)

```yaml
harness:
  mission_poll_interval_seconds: 60
  mission_state_dir: /srv/janus/runtime/state

auto_executor:
  enabled: true
  poll_interval_seconds: 60
  allowed_tools: ["llama-cli", "shell", "node_generator", "file_chunker"]
  allowed_action_types: ["analysis", "optimization_experiment", "generate_new_nodes", "process_chunk"]
  max_risk_level: "low"
  resource_limits:
    cpu_percent_max: 80
    memory_mb_max: 2048
    disk_mb_max: 100
    timeout_seconds: 600
```

Disable Mode Beta by setting `auto_executor.enabled: false` (the system reverts to Mode Alpha manual approvals).

---

## Tool Development Guide

1. Define a new tool dataclass entry in `agent.yaml` (command, allow_network, working dir).
2. Extend `auto_executor` whitelist if the tool should auto-run.
3. Implement tool logic in `tools/` (inherit from `Tool` interface).
4. Add safety validation inside `tool_executor._enforce_policy` if special handling is required.
5. Register mission usage in `/srv/janus/03_OPERATIONS/vessels/balaur/runtime/controls/missions/*.yaml`.

Remember: low-risk mode beta tools must be idempotent, read-only, and reversible.

---

## Testing & QA

### Unit / Focused Tests
```bash
pytest 02_FORGE/tests/test_auto_executor.py
pytest 02_FORGE/tests/test_janus_agent.py
```

### Manual Smoke (on Balaur)
```bash
sudo systemctl restart janus-agent
PYTHONPATH=/srv/janus/02_FORGE/packages /srv/janus/02_FORGE/scripts/proposal_cli.py list --status completed --limit 10
```

### Emergency Stop Dry-Run
```bash
sudo /srv/janus/bin/emergency-stop --dry-run
```

Log locations:
- `/srv/janus/03_OPERATIONS/vessels/balaur/logs/mission_log.jsonl`
- `/srv/janus/03_OPERATIONS/vessels/balaur/logs/tool_use.jsonl`
- `journalctl -u janus-agent`
- `journalctl -u janus-controls`

---

## Additional Documentation
- `02_FORGE/docs/JANUS_AGENT_OPERATIONS.md` – Mode Beta operations guide
- `02_FORGE/docs/MODE_BETA_DEPLOYMENT_2025-10-10.md` – Deployment narrative and lessons learned
- `02_FORGE/docs/BALAUR_STATUS.md` – Territory health checks and monitoring commands

For questions or contributions, coordinate through the Trinity workflow (Claude: strategy, Gemini: systems, Codex: code). Lion’s Sanctuary first.#
