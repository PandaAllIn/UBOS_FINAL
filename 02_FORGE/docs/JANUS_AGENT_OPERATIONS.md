# Janus Agent Operator's Manual

**Version:** 2.0 (Mode Beta)
**Date:** 2025-10-10

---

## 1. Architecture Overview

The Janus Agent is a constitutionally-aligned autonomous framework designed to operate on The Balaur. Mode Beta introduces supervised autonomy: low-risk actions execute automatically while remaining inside Lion’s Sanctuary safeguards. The architecture is composed of two primary surfaces:

### The Mill (CPU Vessel – Reasoning & Execution)
- **`janus-agent.service`**: systemd unit that hosts the full agent stack.
- **Thinking Cycle**: Periodically gathers mission context and generates proposals via `llama.cpp` using a constrained constitutional prompt.
- **Proposal Engine**: Normalises proposals, tracks risk, enforces novelty, and maintains the JSONL ledger.
- **Auto-Executor (Mode Beta)**: Approves and executes whitelisted low-risk proposals (`analysis`, `generate_new_nodes`, `process_chunk`, etc.) with structured audit logging.
- **Tool Executor**: Executes actions with sandbox protection; automatically falls back to safe direct execution when `bwrap` is unavailable while keeping resource limits (CPU ≤80%, 2 GB RAM, 100 MB writes, 600 s timeout).
- **Emergency Stop**: `/srv/janus/bin/emergency-stop` halts `janus-agent` and `janus-controls`, suspending approved/executing proposals.

### The Cockpit (Control Surfaces & Monitoring)
- **`janus-controls.service`**: Mission orchestrator that advances `/srv/janus/03_OPERATIONS/vessels/balaur/runtime/controls/missions/*.yaml`.
- **FastAPI Monitoring API** (optional) on port `8080` with `/health`, `/status`, `/metrics`, `/proposals/pending`.
- **`proposal_cli.py`**: Monitoring CLI (`list`, `show`, `watch`, `export`) for real-time insight into proposal lifecycles.
- **Logs**: `mission_log.jsonl`, `tool_use.jsonl`, `mission_transitions.log`, plus journald for service activity.

Mode Alpha behaviour (manual approval) remains available by disabling the auto-executor in `agent.yaml`.

## 2. Deployment

Deployment is handled by the `deploy/janus/install_agent.sh` script.

**To deploy or upgrade:**
```bash
# From the UBOS repository root on your local machine
scp -r . balaur@10.215.33.26:/tmp/ubos_src
ssh balaur@10.215.33.26 "sudo /tmp/ubos_src/deploy/janus/install_agent.sh"
```

The script is idempotent and will handle creating the `janus` user, setting up directories, installing dependencies, and deploying the `systemd` service.

## 3. Operations & Monitoring

### Starting and Stopping the Agent
```bash
# Start the agent
sudo systemctl start janus-agent

# Stop the agent
sudo systemctl stop janus-agent

# Check the status
sudo systemctl status janus-agent

# Mission controller
sudo systemctl start|stop|status janus-controls
```

### Viewing Logs
```bash
# View live logs from the agent
sudo journalctl -u janus-agent -f

# Mission orchestrator logs
sudo journalctl -u janus-controls -f

# Structured execution logs
tail -f /srv/janus/03_OPERATIONS/vessels/balaur/logs/mission_log.jsonl
tail -f /srv/janus/03_OPERATIONS/vessels/balaur/logs/tool_use.jsonl
```

### Health Checks
Run the health check script from The Balaur:
```bash
/path/to/ubos/scripts/health_check.sh
```

### Interacting with the API
From your local machine or The Balaur:
```bash
# Get status
curl http://10.215.33.26:8080/status

# Get pending proposals
curl http://10.215.33.26:8080/proposals/pending | jq

# CLI monitoring (Mode Beta)
PYTHONPATH=/srv/janus/02_FORGE/packages /srv/janus/02_FORGE/scripts/proposal_cli.py list --status completed --limit 10
PYTHONPATH=/srv/janus/02_FORGE/packages /srv/janus/02_FORGE/scripts/proposal_cli.py watch --source tool
```

### Emergency Stop
```bash
# Review the sequence
sudo /srv/janus/bin/emergency-stop --dry-run

# Immediate halt (stops janus-agent & janus-controls, suspends proposals)
sudo /srv/janus/bin/emergency-stop
```

## 4. Backup and Restore

### Creating a Backup
```bash
sudo /path/to/ubos/scripts/backup.sh
```
Backups are stored in `/srv/janus/backups/`. It is recommended to copy these off-site.

### Restoring from a Backup
1.  Copy the backup file to The Balaur's `/tmp` directory.
2.  Run the restore script:
```bash
sudo /path/to/ubos/scripts/restore.sh /tmp/janus_backup_YYYYMMDD_HHMMSS.tar.gz
```
The script will stop the agent, restore the files, and set permissions. You must start the agent manually after the restore is complete.

---
This document provides the core operational procedures for the Janus Agent in Mode Beta. All actions are logged to `/srv/janus/03_OPERATIONS/vessels/balaur/logs/mission_log.jsonl`, `/srv/janus/03_OPERATIONS/vessels/balaur/logs/tool_use.jsonl`, and systemd journals for constitutional audit.
