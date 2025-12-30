# Autonomous Vessel Protocol

This document describes the deployment process for the Janus autonomous vessel
stack on The Balaur. Follow the sequence below after Phase 2.5 consecration.

## 1. Prepare directories and users

1. Create the `janus` system account:
   ```bash
   sudo useradd --system --create-home --home /srv/janus --shell /usr/sbin/nologin janus
   sudo mkdir -p /srv/janus/intel_cache /srv/janus/workspaces
   sudo chown -R janus:janus /srv/janus
   ```
2. Copy repository artifacts from the Cockpit to The Balaur:
   ```bash
   rsync -avz packages/janus_agent scripts/janus_agentd.py deploy/janus configs/janus_agent \
       balaur@10.215.33.26:/home/balaur/ubos-agent/
   ```

## 2. Install runtime dependencies

1. Install Python runtime and utilities (Ubuntu):
   ```bash
   sudo apt update
   sudo apt install -y python3 python3-venv python3-pip bubblewrap jq
   ```
2. Create a virtual environment for the harness:
   ```bash
   sudo -u janus python3 -m venv /srv/janus/venv
   sudo -u janus /srv/janus/venv/bin/pip install --upgrade pip
   sudo -u janus /srv/janus/venv/bin/pip install fastapi uvicorn
   ```

## 3. Configure security posture

1. Apply sudo policy:
   ```bash
   sudo cp /home/balaur/ubos-agent/deploy/janus/sudoers_balaur /etc/sudoers.d/01-balaur-nopasswd
   sudo chmod 440 /etc/sudoers.d/01-balaur-nopasswd
   ```
2. Configure UFW baseline:
   ```bash
   sudo /home/balaur/ubos-agent/deploy/janus/ufw_rules.sh
   ```

## 4. Deploy harness configuration

1. Place configuration files:
   ```bash
   sudo mkdir -p /etc/janus
   sudo cp /home/balaur/ubos-agent/configs/janus_agent/example_harness.json /etc/janus/harness.json
   sudo cp /home/balaur/ubos-agent/configs/janus_agent/example_policy.json /etc/janus/policy.json
   sudo chown -R janus:janus /etc/janus
   ```
2. Install systemd unit:
   ```bash
   sudo cp /home/balaur/ubos-agent/deploy/janus/systemd/janus_agentd.service /etc/systemd/system/
   sudo systemctl daemon-reload
   sudo systemctl enable janus_agentd
   ```

## 5. Start and verify service

1. Start the daemon:
   ```bash
   sudo systemctl start janus_agentd
   ```
2. Check status and logs:
   ```bash
   sudo systemctl status janus_agentd
   sudo journalctl -u janus_agentd --since "-5m"
   tail -f /srv/janus/mission_log.jsonl
   ```

## 6. Next steps

- Integrate Ollama and local LLM endpoints once documentation review is complete.
- Implement Fluent Bit or syslog forwarding from `/var/log/janus/` as defined in
  the logging framework.
- Extend `configs/janus_agent/example_harness.json` with the approved tool
  catalogue before enabling autonomous execution.

The harness, sandbox policy, and logging framework delivered in this commit form
the foundation for Janus-in-Balaur autonomy. Iterate on the configuration files
rather than modifying the code directly when adjusting operational posture.
