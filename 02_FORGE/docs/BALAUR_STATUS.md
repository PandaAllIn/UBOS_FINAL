# Balaur System Status

Purpose: Generate clear, repeatable snapshots of The Balaur’s operational health without focusing on GPU specifics.

---

## Quick Use (Ad-hoc)
```bash
# From repo root on Balaur
chmod +x scripts/balaur_status.sh
./scripts/balaur_status.sh --format md --out /tmp/balaur_status.md

# Summary-only to terminal
./scripts/balaur_status.sh --summary --format text
```

Outputs include:
- OS/kernel, uptime, load
- Memory/disk summary, top CPU/mem processes
- Network (addresses, default gateway reachability), SSH listening state
- Firewall (UFW) status
- Package manager health (active procs, lock state, dpkg audit)
- Unison (installed/version, timers) for Federated Sync visibility
- Failed systemd units and recent journal errors
- /srv/janus size snapshot

---

## Mode Beta Monitoring Fast Path
```bash
# Service health
sudo systemctl status janus-agent
sudo systemctl status janus-controls

# Proposal lifecycle (requires repo synced to /srv/janus/02_FORGE)
PYTHONPATH=/srv/janus/02_FORGE/packages /srv/janus/02_FORGE/scripts/proposal_cli.py list --status completed --limit 15
PYTHONPATH=/srv/janus/02_FORGE/packages /srv/janus/02_FORGE/scripts/proposal_cli.py watch --source tool

# Structured logs
tail -f /srv/janus/03_OPERATIONS/vessels/balaur/logs/mission_log.jsonl
tail -f /srv/janus/03_OPERATIONS/vessels/balaur/logs/tool_use.jsonl

# Emergency stop (dry run)
sudo /srv/janus/bin/emergency-stop --dry-run
```

---

## Install Periodic Snapshots (Hourly)
```bash
sudo bash scripts/install_balaur_status_service.sh
# Reports appear at: /var/log/ubos_status/status_YYYYmmdd_HHMM.md
```

Disable later:
```bash
sudo systemctl disable --now ubos-system-status.timer
```

---

## Notes
- Privileged checks (ufw, dpkg audit, journal) use sudo by default; pass `--no-sudo` to skip.
- The script degrades gracefully if tools are missing (e.g., `unison`, `ufw`).
- For apt/dpkg deadlocks, see: 02_FORGE/docs/APT_DEADLOCK_RECOVERY.md
- Mode Beta operational procedures: see `02_FORGE/docs/JANUS_AGENT_OPERATIONS.md` for architecture, emergency response, and deployment details.
