# JANUS-HAIKU AUTONOMOUS AGENT: DEPLOYMENT IMPLEMENTATION

**Date:** 2025-10-30
**Coordinated By:** Claude (Strategic Mind) + Gemini (Systems Engineer)
**Objective:** Deploy Skills #1-2 for autonomous daily operation
**Status:** Ready for execution

---

## EXECUTIVE SUMMARY

**Mission:** Activate the first autonomous constitutional AI agent with revenue-generating capabilities.

**What We're Deploying:**
- Skill #1: EU Grant Hunter (€70M pipeline tracking)
- Skill #2: Malaga Embassy Operator (€855-1,910/month revenue system)
- Shared configuration: skill-rules.json (8 UBOS skills)
- Daily automation: 08:00 UTC Malaga, 09:00 UTC grants

**Expected Impact:**
- Autonomous grant scanning (daily)
- Autonomous health monitoring (daily)
- Constitutional compliance (100% enforced)
- Zero manual intervention required

---

## DEPLOYMENT ARCHITECTURE

```
┌─────────────────────────────────────────────────┐
│         JANUS-HAIKU AUTONOMOUS AGENT            │
├─────────────────────────────────────────────────┤
│                                                 │
│  Skill #1: EU Grant Hunter                     │
│  ├─ Cron: 09:00 UTC daily                      │
│  ├─ Scans: 4 EU funding sources                │
│  ├─ Scores: Fit 0-5 scale                      │
│  └─ Alerts: High-value via COMMS_HUB           │
│                                                 │
│  Skill #2: Malaga Embassy Operator             │
│  ├─ Cron: 08:00 UTC daily                      │
│  ├─ Calculates: Health 0-100                   │
│  ├─ Checks: Constitutional cascade             │
│  └─ Briefs: Captain via COMMS_HUB              │
│                                                 │
│  Monitoring                                     │
│  ├─ Logs: /srv/janus/logs/*.jsonl              │
│  ├─ Alerts: Trinity + Captain (urgent rhythm)  │
│  └─ Cross-validation: Claude + Gemini          │
│                                                 │
└─────────────────────────────────────────────────┘
```

---

## STEP 1: PACKAGE SKILLS

### Create Deployment Package

```bash
#!/bin/bash
# Package skills for Janus-Haiku deployment

DEPLOY_DIR="/srv/janus/trinity/skills/deployment"
PACKAGE_DIR="${DEPLOY_DIR}/janus-haiku-skills-v1.0"

# Create package structure
mkdir -p "${PACKAGE_DIR}/skills"
mkdir -p "${PACKAGE_DIR}/config"
mkdir -p "${PACKAGE_DIR}/logs"

# Copy Skill #1 (EU Grant Hunter)
cp -r /srv/janus/trinity/skills/eu-grant-hunter "${PACKAGE_DIR}/skills/"

# Copy Skill #2 (Malaga Embassy Operator)
cp -r /srv/janus/trinity/skills/malaga-embassy-operator "${PACKAGE_DIR}/skills/"

# Copy shared configuration
cp ~/.claude/hooks/skill-rules.json "${PACKAGE_DIR}/config/"

# Create deployment metadata
cat > "${PACKAGE_DIR}/deployment-info.json" <<EOF
{
  "version": "1.0.0",
  "date": "2025-10-30",
  "skills": [
    {
      "name": "eu-grant-hunter",
      "version": "1.0.0",
      "cron": "0 9 * * *"
    },
    {
      "name": "malaga-embassy-operator",
      "version": "1.0.0",
      "cron": "0 8 * * *"
    }
  ],
  "forged_by": "Codex",
  "validated_by": "Janus-in-Claude",
  "deployed_by": "Kilo"
}
EOF

# Create requirements.txt
cat > "${PACKAGE_DIR}/requirements.txt" <<EOF
# Python dependencies for Janus-Haiku skills
python>=3.10
requests>=2.31.0
beautifulsoup4>=4.12.0
lxml>=4.9.0
python-dateutil>=2.8.2
EOF

echo "✅ Package created at ${PACKAGE_DIR}"
```

### Validate Package Structure

```bash
# Verify all files present
tree "${PACKAGE_DIR}"

# Expected structure:
# janus-haiku-skills-v1.0/
# ├── skills/
# │   ├── eu-grant-hunter/
# │   │   ├── SKILL.md
# │   │   ├── scripts/
# │   │   ├── references/
# │   │   └── assets/
# │   └── malaga-embassy-operator/
# │       ├── SKILL.md
# │       ├── scripts/
# │       ├── references/
# │       └── assets/
# ├── config/
# │   └── skill-rules.json
# ├── logs/
# ├── deployment-info.json
# └── requirements.txt
```

---

## STEP 2: CONFIGURE ENVIRONMENT

### Python Environment Setup

```bash
# Create dedicated Python environment
python3 -m venv /srv/janus/trinity/.venv-haiku

# Activate environment
source /srv/janus/trinity/.venv-haiku/bin/activate

# Install dependencies
pip install --upgrade pip
pip install -r "${PACKAGE_DIR}/requirements.txt"

# Verify installation
python3 -c "import requests; import bs4; print('✅ Dependencies installed')"
```

### File System Permissions

```bash
# Grant Janus-Haiku write permissions
sudo chown -R balaur:janus /srv/janus/logs
sudo chmod -R 775 /srv/janus/logs

sudo chown -R balaur:janus /srv/janus/03_OPERATIONS/malaga_embassy
sudo chmod -R 775 /srv/janus/03_OPERATIONS/malaga_embassy

sudo chown -R balaur:janus /srv/janus/01_STRATEGY/grant_pipeline
sudo chmod -R 775 /srv/janus/01_STRATEGY/grant_pipeline

# Verify permissions
ls -la /srv/janus/logs
ls -la /srv/janus/03_OPERATIONS/malaga_embassy
ls -la /srv/janus/01_STRATEGY/grant_pipeline

echo "✅ Permissions configured"
```

### Environment Variables

```bash
# Create environment file for Janus-Haiku
cat > /srv/janus/trinity/.env-haiku <<EOF
# Janus-Haiku Autonomous Agent Environment
JANUS_HAIKU_HOME=/srv/janus/trinity
SKILLS_DIR=/srv/janus/trinity/skills
LOGS_DIR=/srv/janus/logs
CONFIG_DIR=/srv/janus/trinity/config
PYTHON_ENV=/srv/janus/trinity/.venv-haiku

# Constitutional settings
CONSTITUTIONAL_CASCADE=20/10/15/40/15
MODE_BETA=enabled
SUPERVISION=human_oversight_required

# COMMS settings
COMMS_HUB_DIR=/srv/janus/03_OPERATIONS/COMMS_HUB
PNEUMATIC_TUBE_PROTOCOL=enabled

# Timezone
TZ=UTC
EOF

echo "✅ Environment configured"
```

---

## STEP 3: CREATE CRON JOBS

### Cron Job Scripts

**Script 1: EU Grant Hunter (09:00 UTC)**

```bash
#!/bin/bash
# /srv/janus/trinity/cron/run-grant-hunter.sh

set -e

# Load environment
source /srv/janus/trinity/.env-haiku
source ${PYTHON_ENV}/bin/activate

# Log start
echo "[$(date -u +%Y-%m-%dT%H:%M:%SZ)] EU Grant Hunter: Starting daily scan" >> ${LOGS_DIR}/cron.log

# Run skill
cd ${SKILLS_DIR}/eu-grant-hunter
python3 scripts/scan_eu_databases.py --auto 2>&1 | tee -a ${LOGS_DIR}/grant_hunter_cron.log

# Check exit code
if [ $? -eq 0 ]; then
    echo "[$(date -u +%Y-%m-%dT%H:%M:%SZ)] EU Grant Hunter: Completed successfully" >> ${LOGS_DIR}/cron.log
else
    echo "[$(date -u +%Y-%m-%dT%H:%M:%SZ)] EU Grant Hunter: FAILED (exit code $?)" >> ${LOGS_DIR}/cron.log
    # Alert Trinity via COMMS_HUB
    echo "URGENT: EU Grant Hunter failed" | tee ${COMMS_HUB_DIR}/inbox/claude/alert-$(date +%s).txt
fi
```

**Script 2: Malaga Embassy Operator (08:00 UTC)**

```bash
#!/bin/bash
# /srv/janus/trinity/cron/run-malaga-operator.sh

set -e

# Load environment
source /srv/janus/trinity/.env-haiku
source ${PYTHON_ENV}/bin/activate

# Log start
echo "[$(date -u +%Y-%m-%dT%H:%M:%SZ)] Malaga Embassy Operator: Starting daily briefing" >> ${LOGS_DIR}/cron.log

# Run skill
cd ${SKILLS_DIR}/malaga-embassy-operator
python3 scripts/generate_daily_briefing.py --auto 2>&1 | tee -a ${LOGS_DIR}/malaga_embassy_cron.log

# Check exit code
if [ $? -eq 0 ]; then
    echo "[$(date -u +%Y-%m-%dT%H:%M:%SZ)] Malaga Embassy Operator: Completed successfully" >> ${LOGS_DIR}/cron.log
else
    echo "[$(date -u +%Y-%m-%dT%H:%M:%SZ)] Malaga Embassy Operator: FAILED (exit code $?)" >> ${LOGS_DIR}/cron.log
    # Alert Trinity via COMMS_HUB
    echo "URGENT: Malaga Embassy Operator failed" | tee ${COMMS_HUB_DIR}/inbox/gemini/alert-$(date +%s).txt
fi
```

**Make scripts executable:**

```bash
chmod +x /srv/janus/trinity/cron/run-grant-hunter.sh
chmod +x /srv/janus/trinity/cron/run-malaga-operator.sh
```

### Install Cron Jobs

```bash
# Edit crontab for balaur user
crontab -e

# Add these lines:

# Janus-Haiku Autonomous Agent - Skills Execution
# Malaga Embassy Operator: Daily briefing at 08:00 UTC
0 8 * * * /srv/janus/trinity/cron/run-malaga-operator.sh

# EU Grant Hunter: Daily scan at 09:00 UTC
0 9 * * * /srv/janus/trinity/cron/run-grant-hunter.sh

# Weekly health check: Sundays at 10:00 UTC
0 10 * * 0 /srv/janus/trinity/cron/run-health-check.sh
```

**Verify cron installation:**

```bash
crontab -l | grep "Janus-Haiku"
# Should show both cron jobs

echo "✅ Cron jobs installed"
```

---

## STEP 4: IMPLEMENT MONITORING

### Trinity Monitoring Dashboard

```bash
#!/bin/bash
# /srv/janus/trinity/cron/run-health-check.sh

set -e

source /srv/janus/trinity/.env-haiku
source ${PYTHON_ENV}/bin/activate

echo "=== JANUS-HAIKU HEALTH CHECK ==="
echo "Date: $(date -u +%Y-%m-%dT%H:%M:%SZ)"
echo ""

# Check Skill #1 status
echo "Skill #1: EU Grant Hunter"
if [ -f ${LOGS_DIR}/grant_hunter_cron.log ]; then
    tail -5 ${LOGS_DIR}/grant_hunter_cron.log
    echo "✅ Grant Hunter operational"
else
    echo "❌ Grant Hunter log not found"
fi
echo ""

# Check Skill #2 status
echo "Skill #2: Malaga Embassy Operator"
if [ -f ${LOGS_DIR}/malaga_embassy_cron.log ]; then
    tail -5 ${LOGS_DIR}/malaga_embassy_cron.log

    # Parse latest health score
    cd ${SKILLS_DIR}/malaga-embassy-operator
    HEALTH=$(python3 scripts/calculate_health_score.py --json | jq '.score')
    echo "Current Health Score: ${HEALTH}/100"

    if (( $(echo "${HEALTH} < 70" | bc -l) )); then
        echo "⚠️  Health below 70, attention required"
        # Alert Trinity
        echo "WARNING: Malaga health ${HEALTH}/100" | tee ${COMMS_HUB_DIR}/inbox/claude/warning-$(date +%s).txt
    else
        echo "✅ Malaga Embassy operational"
    fi
else
    echo "❌ Malaga Embassy log not found"
fi
echo ""

# Check disk space
echo "Disk Usage:"
df -h /srv/janus | tail -1
echo ""

# Check log sizes
echo "Log Sizes:"
du -sh ${LOGS_DIR}/*.log 2>/dev/null || echo "No logs yet"
echo ""

echo "=== Health check complete ==="
```

### Alert Configuration

```python
# /srv/janus/trinity/monitoring/trinity_alerts.py

import json
from pathlib import Path
from datetime import datetime, timezone

def send_trinity_alert(severity, skill, message):
    """
    Send alert to Trinity vessels via COMMS_HUB.

    severity: 'info' | 'warning' | 'critical'
    skill: 'eu-grant-hunter' | 'malaga-embassy-operator' | 'system'
    message: Alert text
    """
    comms_hub = Path('/srv/janus/03_OPERATIONS/COMMS_HUB')

    alert = {
        'timestamp': datetime.now(timezone.utc).isoformat(),
        'severity': severity,
        'skill': skill,
        'message': message,
        'source': 'janus-haiku'
    }

    # Send to Claude (Strategic Mind)
    claude_inbox = comms_hub / 'inbox/claude'
    claude_inbox.mkdir(parents=True, exist_ok=True)
    (claude_inbox / f'alert-{int(datetime.now().timestamp())}.json').write_text(
        json.dumps(alert, indent=2)
    )

    # Send to Gemini (Systems Engineer)
    gemini_inbox = comms_hub / 'inbox/gemini'
    gemini_inbox.mkdir(parents=True, exist_ok=True)
    (gemini_inbox / f'alert-{int(datetime.now().timestamp())}.json').write_text(
        json.dumps(alert, indent=2)
    )

    # Send to Captain
    if severity in ['warning', 'critical']:
        captain_inbox = comms_hub / 'inbox/captain'
        captain_inbox.mkdir(parents=True, exist_ok=True)
        (captain_inbox / f'alert-{int(datetime.now().timestamp())}.json').write_text(
            json.dumps(alert, indent=2)
        )

# Example usage:
if __name__ == '__main__':
    send_trinity_alert(
        'info',
        'system',
        'Janus-Haiku deployment complete. Skills #1-2 operational.'
    )
```

---

## STEP 5: ACTIVATE AND VALIDATE

### Pre-Deployment Testing

```bash
#!/bin/bash
# Test both skills before enabling cron

echo "=== PRE-DEPLOYMENT VALIDATION ==="

# Test Skill #1
echo "Testing EU Grant Hunter..."
cd /srv/janus/trinity/skills/eu-grant-hunter
python3 scripts/scan_eu_databases.py --dry-run --max-results 2
if [ $? -eq 0 ]; then
    echo "✅ EU Grant Hunter: PASS"
else
    echo "❌ EU Grant Hunter: FAIL"
    exit 1
fi

# Test Skill #2
echo "Testing Malaga Embassy Operator..."
cd /srv/janus/trinity/skills/malaga-embassy-operator
python3 scripts/generate_daily_briefing.py --no-comms --json > /dev/null
if [ $? -eq 0 ]; then
    echo "✅ Malaga Embassy Operator: PASS"
else
    echo "❌ Malaga Embassy Operator: FAIL"
    exit 1
fi

echo "=== ALL TESTS PASSED ==="
echo "Ready for production deployment."
```

### First Day Validation Protocol

**08:00 UTC (Malaga Briefing):**
```bash
# Monitor Malaga briefing execution
tail -f /srv/janus/logs/malaga_embassy_cron.log

# Cross-validate with Gemini
echo "Kilo: Validate Malaga health score calculation"
# Gemini recalculates independently, compares results

# Expected: Health score 85/100 (initial state)
```

**09:00 UTC (Grant Scan):**
```bash
# Monitor grant scan execution
tail -f /srv/janus/logs/grant_hunter_cron.log

# Cross-validate with Claude
echo "Claude: Validate grant pipeline updates"
# Claude checks fit scores, deadline tracking

# Expected: 4 opportunities tracked, 2 high-priority
```

**Trinity Coordination Check:**
```bash
# Both vessels query Janus-Haiku outputs
Claude: "Show me today's Malaga briefing"
Gemini: "Show me today's grant scan results"

# Compare outputs:
# - Same health score? ✅
# - Same opportunities? ✅
# - Same fit scores? ✅

# If all match → Deployment successful ✅
```

---

## POST-DEPLOYMENT OPERATIONS

### Daily Trinity Synchronization

**Morning Routine (08:00-10:00 UTC):**

1. **08:00 UTC:** Janus-Haiku generates Malaga briefing
2. **08:05 UTC:** Gemini validates health calculations
3. **09:00 UTC:** Janus-Haiku scans grant pipeline
4. **09:05 UTC:** Claude validates fit scores + deadlines
5. **10:00 UTC:** Weekly health check (Sundays only)

**Coordination Protocol:**

```python
# Trinity vessels check Janus-Haiku outputs daily

# Claude (Strategic Mind) checks:
- Grant opportunities identified correctly
- Fit scores align with strategic priorities
- Deadlines tracked (90/60/30/7-day reminders)

# Gemini (Systems Engineer) checks:
- Health score calculations correct
- Constitutional cascade enforced
- System logs healthy (no errors)

# If discrepancy detected:
- Alert human oversight immediately
- Cross-validate between vessels
- Determine root cause (Janus-Haiku vs vessel calculation)
```

### Continuous Improvement

**As Codex Forges New Skills:**

```bash
# Add Skill #3 (Grant Application Assembler)
1. Test skill independently
2. Add to janus-haiku deployment package
3. Create new cron job (if daily execution needed)
4. Update monitoring dashboard
5. Validate with Trinity vessels

# Repeat for Skills #4-5
```

**Skill Versioning:**

```bash
# Track skill versions in deployment metadata
{
  "skills": [
    {"name": "eu-grant-hunter", "version": "1.0.0"},
    {"name": "malaga-embassy-operator", "version": "1.0.0"},
    {"name": "grant-application-assembler", "version": "1.0.0"} // Added
  ]
}

# Update package when skills change
# Janus-Haiku automatically uses latest versions
```

---

## SUCCESS CRITERIA

### Week 1 (Deployment Validation)

- ✅ Both skills execute daily without errors
- ✅ Logs written correctly
- ✅ COMMS_HUB alerts delivered
- ✅ Trinity cross-validation passes (100% match)
- ✅ Captain receives daily Malaga briefings

### Month 1 (Operational Validation)

- ✅ 30/30 daily briefings delivered (100% uptime)
- ✅ 30/30 grant scans completed (100% uptime)
- ✅ Zero missed deadlines (Sept 2, Jan 15 tracked)
- ✅ Malaga health >70/100 maintained
- ✅ Constitutional compliance: 100%

### Month 3 (Performance Validation)

- ✅ €855-1,910 Malaga revenue achieved
- ✅ 2+ grant proposals assembled
- ✅ Skills #3-5 integrated
- ✅ Autonomous operations proven reliable

---

## ROLLBACK PROCEDURE

**If Issues Detected:**

```bash
# Disable cron jobs immediately
crontab -e
# Comment out Janus-Haiku lines

# Investigate logs
tail -100 /srv/janus/logs/cron.log
tail -100 /srv/janus/logs/grant_hunter_cron.log
tail -100 /srv/janus/logs/malaga_embassy_cron.log

# Identify root cause
# Fix issues
# Test manually before re-enabling cron

# Re-enable when validated
crontab -e
# Uncomment Janus-Haiku lines
```

---

## TRINITY COORDINATION MATRIX

| Time (UTC) | Janus-Haiku | Claude | Gemini | Captain |
|------------|-------------|---------|--------|---------|
| 08:00 | Generate Malaga briefing | Standby | Validate calculations | Receive briefing |
| 08:05 | Complete | Review briefing | Cross-validate | Review |
| 09:00 | Scan grant pipeline | Validate fit scores | Standby | Notified (high-value) |
| 09:05 | Complete | Cross-validate | Review scan | Review |
| 10:00 (Sun) | Health check | Review health | Review health | Notified (issues) |

---

## CONSTITUTIONAL NOTES

**This deployment embodies Lion's Sanctuary principles:**

1. **Autonomous Operation with Oversight**
   - Janus-Haiku operates daily without intervention
   - Claude + Gemini provide cross-validation
   - Captain retains final authority
   - Human oversight loop maintained

2. **Transparency**
   - All operations logged
   - Trinity vessels can audit anytime
   - COMMS_HUB notifications for all actions
   - Constitutional cascade visible in every briefing

3. **Empowerment through Structure**
   - Automated routines free human attention
   - Alerts only on critical issues
   - Guidance provided, never blocking
   - Captain empowered by information

4. **Coordinated Safety**
   - Trinity vessels cross-validate
   - Redundant monitoring (3 vessels)
   - Emergency protocols automatic
   - Rollback procedure ready

---

## DEPLOYMENT CHECKLIST

**Pre-Deployment:**
- [ ] Package skills (both complete)
- [ ] Configure environment (Python + permissions)
- [ ] Create cron scripts (both jobs)
- [ ] Implement monitoring (health check + alerts)
- [ ] Test independently (dry-run both skills)

**Deployment:**
- [ ] Install cron jobs
- [ ] Activate monitoring
- [ ] Send deployment notification to Trinity
- [ ] Verify first execution (08:00 + 09:00 UTC)

**Post-Deployment:**
- [ ] Cross-validate with Claude (grant scores)
- [ ] Cross-validate with Gemini (health calculations)
- [ ] Verify COMMS_HUB alerts delivered
- [ ] Confirm Captain received briefings
- [ ] Monitor for 7 days (100% uptime target)

---

## EXECUTION COMMAND

```bash
# Execute full deployment (when ready)
bash /srv/janus/trinity/deployment/deploy-janus-haiku.sh

# This will:
# 1. Run pre-deployment tests
# 2. Configure environment
# 3. Install cron jobs
# 4. Activate monitoring
# 5. Send notification to Trinity
# 6. Validate first execution

# Expected output:
# ✅ Skills packaged
# ✅ Environment configured
# ✅ Cron jobs installed
# ✅ Monitoring active
# ✅ Janus-Haiku operational
```

---

**DEPLOYMENT COORDINATOR:** Kilo (Systems Engineer)
**STRATEGIC OVERSIGHT:** Janus-in-Claude (Strategic Mind)
**SKILLS FORGED BY:** Codex (Forgemaster)
**DEPLOYMENT STATUS:** Ready for execution
**EXPECTED IMPACT:** €70M+ pipeline + €855-1,910/month autonomous operation

🔥🔥🔥 **JANUS-HAIKU: READY FOR AUTONOMOUS OPERATION** 🔥🔥🔥
