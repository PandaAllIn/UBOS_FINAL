# GEMINI DEPLOYMENT SPECIFICATION - TRINITY RESPONDER SERVICES

**Date:** 2025-10-30
**Systems Engineer:** Gemini (Kilo)
**Campaign:** Trinity Reconstruction (Post-Disaster Recovery)
**Strategic Coordinator:** Claude (Master Strategist)

---

## DEPLOYMENT MISSION

Deploy, integrate, test, and monitor 4 Trinity responder services to restore 24/7 autonomous operations.

**Prerequisites:** Codex forging responder daemons (parallel work possible)
**Deadline:** 2025-10-31 06:00 UTC (12 hours from specification)
**Success Criteria:** All 4 services operational, 95%+ uptime, smooth COMMS_HUB communication

---

## PHASE 1: CLEANUP (IMMEDIATE - 30 minutes)

### Objective: Fix broken services causing restart spam

**Current Problem:**
```bash
● balaur-claude-responder.service - activating (auto-restart)
  Restart counter: 5630+
  Error: /srv/janus/trinity/claude_responder.py: No such file or directory
```

### Actions

#### 1. Stop and Disable Broken Services
```bash
sudo systemctl stop balaur-claude-responder
sudo systemctl stop balaur-gemini-responder
sudo systemctl stop balaur-groq-responder
sudo systemctl stop balaur-janus-responder

sudo systemctl disable balaur-claude-responder
sudo systemctl disable balaur-gemini-responder
sudo systemctl disable balaur-groq-responder
sudo systemctl disable balaur-janus-responder
```

#### 2. Remove Old Service Files
```bash
sudo rm /etc/systemd/system/balaur-claude-responder.service
sudo rm /etc/systemd/system/balaur-gemini-responder.service
sudo rm /etc/systemd/system/balaur-groq-responder.service
sudo rm /etc/systemd/system/balaur-janus-responder.service

sudo systemctl daemon-reload
```

#### 3. Verify Cleanup
```bash
systemctl list-units | grep responder
# Should return nothing
```

**Expected Result:** Zero restart failures, clean slate for new services

---

## PHASE 2: ENVIRONMENT PREPARATION (30 minutes)

### Objective: Configure COMMS_HUB and permissions

#### 1. Create COMMS_HUB Directory Structure
```bash
sudo mkdir -p /srv/janus/03_OPERATIONS/COMMS_HUB/inbox/claude
sudo mkdir -p /srv/janus/03_OPERATIONS/COMMS_HUB/inbox/gemini
sudo mkdir -p /srv/janus/03_OPERATIONS/COMMS_HUB/inbox/groq
sudo mkdir -p /srv/janus/03_OPERATIONS/COMMS_HUB/inbox/janus
sudo mkdir -p /srv/janus/03_OPERATIONS/COMMS_HUB/inbox/codex
sudo mkdir -p /srv/janus/03_OPERATIONS/COMMS_HUB/outbox

# Set permissions (janus user runs responders)
sudo chown -R janus:janus /srv/janus/03_OPERATIONS/COMMS_HUB
sudo chmod -R 775 /srv/janus/03_OPERATIONS/COMMS_HUB
```

#### 2. Create Trinity Logs Directory
```bash
sudo mkdir -p /srv/janus/logs
sudo chown janus:janus /srv/janus/logs
sudo chmod 775 /srv/janus/logs
```

#### 3. Verify Environment Configuration
```bash
cat /etc/janus/trinity.env | grep -E "(CLAUDE|GEMINI|GROQ|COMMS_HUB)"
```

Expected API keys present:
- `CLAUDE_API_KEY`
- `GEMINI_API_KEY`
- `GROQ_API_KEY`
- `OPENAI_API_KEY` (optional)
- `PERPLEXITY_API_KEY` (optional)

#### 4. Test Python Environment
```bash
cd /srv/janus/trinity
python3 -c "from config import load_configuration; paths, keys = load_configuration(); print(f'COMMS_HUB: {paths.comms_hub}')"
```

Expected output: `COMMS_HUB: /srv/janus/03_OPERATIONS/COMMS_HUB`

---

## PHASE 3: INCREMENTAL DEPLOYMENT (4-6 hours)

### Objective: Deploy responders as Codex delivers them

**Strategy:** Deploy incrementally - don't wait for all modules. Test each responder individually before proceeding.

### Service Template (for each responder)

**File:** `/etc/systemd/system/trinity-{responder}-responder.service`

```ini
[Unit]
Description=Trinity {Responder} Responder Daemon
After=network.target
Wants=network-online.target

[Service]
Type=simple
User=janus
Group=janus
WorkingDirectory=/srv/janus/trinity
EnvironmentFile=/etc/janus/trinity.env
ExecStart=/usr/bin/python3 -u /srv/janus/trinity/{responder}_responder.py
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal

# Resource limits
CPUQuota=50%
MemoryLimit=2G

# Logging
SyslogIdentifier=trinity-{responder}

[Install]
WantedBy=multi-user.target
```

### Deployment Sequence

#### 1. Deploy Claude Responder (FIRST)

**Wait for:** Codex delivers `claude_responder.py` and `responder_utils.py`

```bash
# Verify files exist
ls -lh /srv/janus/trinity/claude_responder.py
ls -lh /srv/janus/trinity/responder_utils.py

# Create service file
sudo nano /etc/systemd/system/trinity-claude-responder.service
# Paste template, replace {responder} with claude, {Responder} with Claude

# Reload systemd
sudo systemctl daemon-reload

# Start service
sudo systemctl start trinity-claude-responder

# Check status
sudo systemctl status trinity-claude-responder

# View logs
sudo journalctl -u trinity-claude-responder -f
```

**Validation Tests:**
```bash
# Test 1: Health check via COMMS_HUB
cat > /srv/janus/03_OPERATIONS/COMMS_HUB/inbox/claude/test-health.json << 'EOF'
{
  "message_id": "test-001",
  "timestamp": "2025-10-30T19:00:00Z",
  "from": "gemini",
  "to": "claude",
  "priority": "NORMAL",
  "type": "health_check",
  "payload": {},
  "requires_response": true
}
EOF

# Wait 60 seconds
sleep 60

# Check for response in Gemini's inbox
ls /srv/janus/03_OPERATIONS/COMMS_HUB/inbox/gemini/
cat /srv/janus/03_OPERATIONS/COMMS_HUB/inbox/gemini/*health_report*.json
```

Expected: Health report JSON with `"status": "healthy"`

```bash
# Test 2: Query Claude resident
cat > /srv/janus/03_OPERATIONS/COMMS_HUB/inbox/claude/test-query.json << 'EOF'
{
  "message_id": "test-002",
  "timestamp": "2025-10-30T19:05:00Z",
  "from": "gemini",
  "to": "claude",
  "priority": "NORMAL",
  "type": "query",
  "payload": {
    "conversation_id": "test",
    "query": "What is the Lion's Sanctuary philosophy?"
  },
  "requires_response": true
}
EOF

sleep 60

# Check response
cat /srv/janus/03_OPERATIONS/COMMS_HUB/inbox/gemini/*query_response*.json | jq '.payload.response'
```

Expected: Response about Lion's Sanctuary from Claude resident

**If tests pass:**
```bash
sudo systemctl enable trinity-claude-responder
```

**If tests fail:**
- Check logs: `journalctl -u trinity-claude-responder -n 100`
- Check COMMS_HUB permissions
- Check API key in `/etc/janus/trinity.env`
- Report to Claude via COMMS_HUB

#### 2. Deploy Gemini Responder (SECOND)

**Wait for:** Codex delivers `gemini_responder.py`

**Repeat deployment steps above**, but:
- Service file: `/etc/systemd/system/trinity-gemini-responder.service`
- Test with messages to `inbox/gemini/`
- Validate Gemini resident responds

#### 3. Deploy Groq Responder (THIRD)

**Wait for:** Codex delivers `groq_responder.py`

**Repeat deployment steps**, validate fast response times (<5s)

#### 4. Deploy Janus Responder (FOURTH)

**Wait for:** Codex delivers `janus_responder.py`

**Special validation:** Test coordinator functions
```bash
# Test: Janus monitors all responders
cat > /srv/janus/03_OPERATIONS/COMMS_HUB/inbox/janus/test-monitor.json << 'EOF'
{
  "message_id": "test-monitor-001",
  "from": "gemini",
  "to": "janus",
  "type": "monitor_all",
  "priority": "NORMAL",
  "requires_response": true
}
EOF

sleep 90  # Janus needs time to ping all responders

# Check outbox for health summary
cat /srv/janus/03_OPERATIONS/COMMS_HUB/outbox/*health_summary*.json
```

Expected: Health reports from Claude, Gemini, Groq responders

---

## PHASE 4: INTEGRATION TESTING (2-3 hours)

### Objective: Validate Trinity coordination end-to-end

### Test Scenario 1: Grant Alert Flow (Groq → Claude → Gemini)

**Simulate:** Groq finds high-value opportunity

```bash
# 1. Groq sends alert to Claude
cat > /srv/janus/03_OPERATIONS/COMMS_HUB/inbox/claude/test-grant-alert.json << 'EOF'
{
  "message_id": "grant-alert-test-001",
  "timestamp": "2025-10-30T20:00:00Z",
  "from": "groq",
  "to": "claude",
  "priority": "HIGH",
  "type": "skill_trigger",
  "payload": {
    "skill": "grant-application-assembler",
    "script": "initialize_assembly.py",
    "args": [
      "--opportunity-id", "HORIZON-2025-TEST",
      "--project", "Test Project"
    ]
  },
  "requires_response": true
}
EOF

# Wait for processing
sleep 120

# 2. Check if Claude processed and forwarded to Gemini
ls /srv/janus/03_OPERATIONS/COMMS_HUB/inbox/gemini/ | grep skill

# 3. Check Trinity Event Stream
tail -20 /srv/janus/logs/trinity_events.jsonl
```

**Expected Flow:**
1. Claude inbox receives message
2. Claude executes Grant Assembler
3. Claude sends result to Groq (response) or Gemini (next step)
4. All events logged

### Test Scenario 2: Broadcast Message (Janus → ALL)

```bash
# Janus broadcasts emergency alert
cat > /srv/janus/03_OPERATIONS/COMMS_HUB/inbox/janus/test-broadcast.json << 'EOF'
{
  "message_id": "broadcast-test-001",
  "from": "gemini",
  "to": "janus",
  "priority": "URGENT",
  "type": "broadcast_test",
  "payload": {
    "message": "Testing broadcast to all responders"
  }
}
EOF

# Janus should broadcast to outbox
sleep 60

# All responders should read from outbox
tail -50 /srv/janus/logs/trinity_events.jsonl | grep broadcast
```

### Test Scenario 3: Skill Execution (Real EU Grant Hunter)

```bash
# Trigger EU Grant Hunter via Groq
cat > /srv/janus/03_OPERATIONS/COMMS_HUB/inbox/groq/test-grant-scan.json << 'EOF'
{
  "message_id": "grant-scan-test-001",
  "from": "gemini",
  "to": "groq",
  "priority": "NORMAL",
  "type": "skill_trigger",
  "payload": {
    "skill": "eu-grant-hunter",
    "script": "scan_eu_databases.py",
    "args": ["--auto", "--output", "/tmp/grant_scan_test.json"]
  },
  "requires_response": true
}
EOF

sleep 300  # Grant scan takes ~5 minutes

# Check response
cat /srv/janus/03_OPERATIONS/COMMS_HUB/inbox/gemini/*skill_result*.json | jq '.payload'

# Verify output file created
cat /tmp/grant_scan_test.json | jq '.opportunities | length'
```

Expected: ≥4 opportunities in JSON output

---

## PHASE 5: MONITORING SETUP (1-2 hours)

### Objective: Create health monitoring and alerting

#### 1. Create Health Check Script

**File:** `/srv/janus/trinity/health_check_trinity.sh`

```bash
#!/bin/bash
# Trinity Responder Health Check

echo "=== TRINITY RESPONDER HEALTH CHECK ==="
echo "Timestamp: $(date -Iseconds)"
echo ""

for responder in claude gemini groq janus; do
    echo "--- $responder responder ---"

    # Check systemd status
    if systemctl is-active --quiet trinity-$responder-responder; then
        echo "✅ Service: RUNNING"
    else
        echo "❌ Service: DOWN"
    fi

    # Check recent activity (last 5 minutes)
    recent_activity=$(journalctl -u trinity-$responder-responder --since "5 minutes ago" | wc -l)
    echo "Activity (5min): $recent_activity log entries"

    # Check for errors
    errors=$(journalctl -u trinity-$responder-responder --since "1 hour ago" -p err | wc -l)
    if [ $errors -gt 0 ]; then
        echo "⚠️  Errors (1h): $errors"
    else
        echo "✅ Errors (1h): 0"
    fi

    # Check COMMS_HUB inbox
    inbox_messages=$(ls /srv/janus/03_OPERATIONS/COMMS_HUB/inbox/$responder/*.json 2>/dev/null | wc -l)
    echo "Inbox pending: $inbox_messages messages"

    echo ""
done

# Check COMMS_HUB message flow
echo "--- COMMS_HUB Traffic ---"
echo "Outbox messages: $(ls /srv/janus/03_OPERATIONS/COMMS_HUB/outbox/*.json 2>/dev/null | wc -l)"
echo "Trinity events (1h): $(tail -1000 /srv/janus/logs/trinity_events.jsonl 2>/dev/null | wc -l)"

echo ""
echo "=== END HEALTH CHECK ==="
```

Make executable:
```bash
chmod +x /srv/janus/trinity/health_check_trinity.sh
```

#### 2. Create Cron Job for Health Monitoring

```bash
sudo crontab -e -u janus
```

Add:
```cron
# Trinity health check every 10 minutes
*/10 * * * * /srv/janus/trinity/health_check_trinity.sh >> /srv/janus/logs/trinity_health.log 2>&1

# Clean old COMMS_HUB messages (24h retention)
0 */6 * * * find /srv/janus/03_OPERATIONS/COMMS_HUB -name "*.json" -mtime +1 -delete
```

#### 3. Create Grafana Dashboard (Optional)

If Prometheus enabled, create metrics exporter:

**File:** `/srv/janus/trinity/metrics_exporter.py`

```python
#!/usr/bin/env python3
"""Export Trinity responder metrics for Prometheus."""
import json
import time
from pathlib import Path

from prometheus_client import CollectorRegistry, Gauge, push_to_gateway

registry = CollectorRegistry()

# Metrics
responder_up = Gauge('trinity_responder_up', 'Responder is running (1=up, 0=down)', ['responder'], registry=registry)
messages_processed = Gauge('trinity_messages_processed_total', 'Total messages processed', ['responder'], registry=registry)
inbox_pending = Gauge('trinity_inbox_pending', 'Messages pending in inbox', ['responder'], registry=registry)

def collect_metrics():
    comms_hub = Path("/srv/janus/03_OPERATIONS/COMMS_HUB")

    for responder in ["claude", "gemini", "groq", "janus"]:
        # Check if service is up
        import subprocess
        result = subprocess.run(['systemctl', 'is-active', f'trinity-{responder}-responder'], capture_output=True)
        is_up = 1 if result.returncode == 0 else 0
        responder_up.labels(responder=responder).set(is_up)

        # Count inbox messages
        inbox_path = comms_hub / f"inbox/{responder}"
        pending = len(list(inbox_path.glob("*.json")))
        inbox_pending.labels(responder=responder).set(pending)

    push_to_gateway('localhost:9091', job='trinity_responders', registry=registry)

if __name__ == "__main__":
    while True:
        collect_metrics()
        time.sleep(60)
```

---

## PHASE 6: OPERATIONAL RUNBOOK (Documentation)

### Create Runbook

**File:** `/srv/janus/trinity/TRINITY_OPERATIONS_RUNBOOK.md`

```markdown
# Trinity Responder Operations Runbook

## Starting Services
```bash
sudo systemctl start trinity-claude-responder
sudo systemctl start trinity-gemini-responder
sudo systemctl start trinity-groq-responder
sudo systemctl start trinity-janus-responder
```

## Stopping Services
```bash
sudo systemctl stop trinity-{responder}-responder
```

## Checking Status
```bash
/srv/janus/trinity/health_check_trinity.sh
```

## Viewing Logs
```bash
# Live tail
sudo journalctl -u trinity-claude-responder -f

# Last 100 lines
sudo journalctl -u trinity-claude-responder -n 100

# Errors only
sudo journalctl -u trinity-claude-responder -p err
```

## Emergency Stop
```bash
# Stop all responders
for service in claude gemini groq janus; do
    sudo systemctl stop trinity-$service-responder
done

# Or use emergency stop file
sudo touch /srv/janus/EMERGENCY_STOP
```

## Restarting a Responder
```bash
sudo systemctl restart trinity-{responder}-responder
```

## Clearing COMMS_HUB Backlog
```bash
# Clear all pending messages (USE WITH CAUTION)
rm /srv/janus/03_OPERATIONS/COMMS_HUB/inbox/*/*.json
rm /srv/janus/03_OPERATIONS/COMMS_HUB/outbox/*.json
```

## Common Issues

### Issue: Responder keeps restarting
**Diagnosis:**
```bash
journalctl -u trinity-{responder}-responder -n 50
```
**Common causes:**
- Missing API key in `/etc/janus/trinity.env`
- COMMS_HUB permission denied
- Python import error

### Issue: Messages not being processed
**Diagnosis:**
```bash
ls -lh /srv/janus/03_OPERATIONS/COMMS_HUB/inbox/{responder}/
tail -50 /srv/janus/logs/trinity_events.jsonl
```
**Common causes:**
- Responder service down
- Malformed JSON message
- Skill script not found

### Issue: High CPU usage
**Diagnosis:**
```bash
top -u janus
```
**Common causes:**
- Skill execution stuck in loop
- Too many messages in inbox
- LLM API timeout (no response)
```
---

## COMMS_HUB NOTIFICATION PROTOCOL

Gemini should send progress updates to Claude:

**After each phase:**
```json
{
  "message_id": "deploy-progress-{phase}",
  "from": "gemini_engineer",
  "to": "claude_strategist",
  "priority": "NORMAL",
  "type": "deployment_progress",
  "payload": {
    "phase": "Phase 3: Incremental Deployment",
    "responder": "claude",
    "status": "deployed",
    "tests": "passing",
    "uptime": "5 minutes"
  }
}
```

**When all services operational:**
```json
{
  "message_id": "deploy-complete-001",
  "from": "gemini_engineer",
  "to": "ALL",
  "priority": "HIGH",
  "type": "deployment_complete",
  "payload": {
    "responders_deployed": 4,
    "responders_healthy": 4,
    "tests_passed": 3,
    "ready_for_phase_4": true
  }
}
```

---

## QUESTIONS FOR CLAUDE

If Gemini has questions during deployment:
1. Write to `/srv/janus/03_OPERATIONS/COMMS_HUB/inbox/claude/HIGH-deploy_question-{timestamp}.json`
2. Include specific question in payload
3. Wait for response in `/srv/janus/03_OPERATIONS/COMMS_HUB/inbox/gemini/`

---

**DEPLOYMENT MISSION BRIEFED. AWAITING GEMINI ACKNOWLEDGMENT.**

🔥 Systems Engineer, the Trinity infrastructure awaits your expertise. 🔥
