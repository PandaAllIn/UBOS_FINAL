# Trinity Autonomous Orchestration - Deployment Checklist

**Date:** 2025-11-06
**Version:** 1.0

---

## ✅ Pre-Deployment

- [x] Auto-orchestration system built and tested
- [x] Agent spawner built and tested
- [x] Mallorca monitor built and tested
- [x] Session closer skill implemented
- [x] Unified launcher created
- [x] Capability registry complete
- [x] Embassy agent specifications complete
- [x] COMMS_HUB integration working
- [x] All scripts made executable
- [x] Documentation written (15+ files)
- [x] Meta-building proven with Gemini CLI

---

## 🚀 Deployment Steps

### 1. Verify System Status

```bash
cd /srv/janus/trinity
./trinity_launcher.sh status
```

**Expected Output:**
```
✅ Auto-Orchestration: READY
✅ Agent Spawner: READY
✅ Mallorca Monitor: READY
✅ Session Closer: READY
✅ Capability Registry: READY
```

- [ ] All systems show READY

### 2. Test Core Functions

```bash
# Test orchestration
./trinity_launcher.sh orchestrate "Research quantum computing papers"

# Test Mallorca monitor
./trinity_launcher.sh mallorca

# Test spawner
./trinity_launcher.sh spawn

# Test COMMS_HUB
./trinity_launcher.sh comms
```

- [ ] Orchestration returns task analysis
- [ ] Mallorca monitor completes all 3 streams
- [ ] Spawner generates agent config
- [ ] COMMS_HUB shows inbox/outbox

### 3. Deploy Mallorca Cron Job

**CRITICAL: December 2025 - January 2026 requires HOURLY checks!**

```bash
# Edit crontab
crontab -e

# Add this line for hourly checks during evaluation window:
0 * * * * /srv/janus/trinity/check_mallorca_now.sh >> /srv/janus/logs/mallorca_cron.log 2>&1

# For rest of year, use daily:
# 0 9 * * * /srv/janus/trinity/check_mallorca_now.sh >> /srv/janus/logs/mallorca_cron.log 2>&1
```

- [ ] Cron job added
- [ ] Test: Wait 1 hour and check `/srv/janus/logs/mallorca_cron.log`

### 4. Set Up Log Monitoring

```bash
# Create log monitoring script
cat > /srv/janus/trinity/check_logs.sh << 'SCRIPT'
#!/bin/bash
echo "📊 Recent Mallorca Checks"
tail -20 /srv/janus/logs/mallorca_checks.log | grep -E "STREAM|PASS|FAIL|€"
SCRIPT

chmod +x /srv/janus/trinity/check_logs.sh
```

- [ ] Log monitoring script created

### 5. Configure Alerts (Optional)

For Stage 1 PASS detection:

```bash
# Add to check_mallorca_now.sh
if grep -qi "stage.*1.*pass" /srv/janus/logs/mallorca_checks.log; then
  # Send alert (email, notification, etc)
  echo "🚨 MALLORCA STAGE 1 PASSED - START STAGE 2 PREP!" | tee /srv/janus/logs/ALERT.log
fi
```

- [ ] Alert mechanism configured (if desired)

### 6. Test Trinity Coordination

```bash
# Send test message to Gemini via COMMS_HUB
cat > /srv/janus/03_OPERATIONS/COMMS_HUB/gemini/inbox/test_$(date +%s).json << 'EOF'
{
  "from": "claude",
  "to": "gemini",
  "subject": "Trinity deployment test",
  "body": "Testing COMMS_HUB after Trinity orchestration deployment",
  "timestamp": "$(date -u +%Y-%m-%dT%H:%M:%S+00:00)"
}
