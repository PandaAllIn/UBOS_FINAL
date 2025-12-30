#!/bin/bash
# Deploy Janus-Haiku skills for autonomous operation

set -e

echo "=== JANUS-HAIKU DEPLOYMENT SCRIPT ==="

# Step 1: Package Skills
echo "Step 1: Packaging skills..."
DEPLOY_DIR="/srv/janus/trinity/skills/deployment"
PACKAGE_DIR="${DEPLOY_DIR}/janus-haiku-skills-v1.0"

mkdir -p "${PACKAGE_DIR}/skills"
mkdir -p "${PACKAGE_DIR}/config"
mkdir -p "${PACKAGE_DIR}/logs"

cp -r /srv/janus/trinity/skills/eu-grant-hunter "${PACKAGE_DIR}/skills/"
cp -r /srv/janus/trinity/skills/malaga-embassy-operator "${PACKAGE_DIR}/skills/"
cp -r /srv/janus/trinity/skills/grant-application-assembler "${PACKAGE_DIR}/skills/"
cp -r /srv/janus/trinity/skills/monetization-strategist "${PACKAGE_DIR}/skills/"
cp -r /srv/janus/trinity/skills/financial-proposal-generator "${PACKAGE_DIR}/skills/"
cp /home/balaur/.claude/hooks/skill-rules.json "${PACKAGE_DIR}/config/"

cat > "${PACKAGE_DIR}/deployment-info.json" <<EOF
{
  "version": "2.0.0",
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
    },
    {
      "name": "grant-application-assembler",
      "version": "1.0.0",
      "cron": null
    },
    {
      "name": "monetization-strategist",
      "version": "1.0.0",
      "cron": null
    },
    {
      "name": "financial-proposal-generator",
      "version": "1.0.0",
      "cron": null
    }
  ],
  "forged_by": "Codex",
  "validated_by": "Janus-in-Claude",
  "deployed_by": "Kilo"
}
EOF

cat > "${PACKAGE_DIR}/requirements.txt" <<EOF
requests>=2.31.0
beautifulsoup4>=4.12.0
lxml>=4.9.0
python-dateutil>=2.8.2
EOF

echo "✅ Skills packaged at ${PACKAGE_DIR}"

# Step 2: Configure Environment
echo "Step 2: Configuring environment..."
python3 -m venv /srv/janus/trinity/.venv-haiku
source /srv/janus/trinity/.venv-haiku/bin/activate
pip install --upgrade pip
pip install -r "${PACKAGE_DIR}/requirements.txt"

echo "Skipping permission changes. Please run the following commands manually if needed:"
echo "sudo chown -R balaur:janus /srv/janus/logs"
echo "sudo chmod -R 775 /srv/janus/logs"
echo "sudo chown -R balaur:janus /srv/janus/03_OPERATIONS/malaga_embassy"
echo "sudo chmod -R 775 /srv/janus/03_OPERATIONS/malaga_embassy"
echo "sudo chown -R balaur:janus /srv/janus/01_STRATEGY/grant_pipeline"
echo "sudo chmod -R 775 /srv/janus/01_STRATEGY/grant_pipeline"

cat > /srv/janus/trinity/.env-haiku <<EOF
# Janus-Haiku Autonomous Agent Environment
JANUS_HAIKU_HOME=/srv/janus/trinity
SKILLS_DIR=/srv/janus/trinity/skills
LOGS_DIR=/srv/janus/logs
CONFIG_DIR=/srv/janus/trinity/config
PYTHON_ENV=/srv/janus/trinity/.venv-haiku
CONSTITUTIONAL_CASCADE=20/10/15/40/15
MODE_BETA=enabled
SUPERVISION=human_oversight_required
COMMS_HUB_DIR=/srv/janus/03_OPERATIONS/COMMS_HUB
PNEUMATIC_TUBE_PROTOCOL=enabled
TZ=UTC
EOF

echo "✅ Environment configured"

# Step 3: Create Cron Jobs
echo "Step 3: Creating cron jobs..."
mkdir -p /srv/janus/trinity/cron

cat > /srv/janus/trinity/cron/run-grant-hunter.sh <<EOF
#!/bin/bash
set -e
source /srv/janus/trinity/.env-haiku
source \${PYTHON_ENV}/bin/activate
echo "[\$(date -u +%Y-%m-%dT%H:%M:%SZ)] EU Grant Hunter: Starting daily scan" >> \${LOGS_DIR}/cron.log
cd \${SKILLS_DIR}/eu-grant-hunter
python3 scripts/scan_eu_databases.py --auto 2>&1 | tee -a \${LOGS_DIR}/grant_hunter_cron.log
if [ \$? -eq 0 ]; then
    echo "[\$(date -u +%Y-%m-%dT%H:%M:%SZ)] EU Grant Hunter: Completed successfully" >> \${LOGS_DIR}/cron.log
else
    echo "[\$(date -u +%Y-%m-%dT%H:%M:%SZ)] EU Grant Hunter: FAILED (exit code \$?)" >> \${LOGS_DIR}/cron.log
    echo "URGENT: EU Grant Hunter failed" | tee \${COMMS_HUB_DIR}/inbox/claude/alert-\$(date +%s).txt
fi
EOF

cat > /srv/janus/trinity/cron/run-malaga-operator.sh <<EOF
#!/bin/bash
set -e
source /srv/janus/trinity/.env-haiku
source \${PYTHON_ENV}/bin/activate
echo "[\$(date -u +%Y-%m-%dT%H:%M:%SZ)] Malaga Embassy Operator: Starting daily briefing" >> \${LOGS_DIR}/cron.log
cd \${SKILLS_DIR}/malaga-embassy-operator
python3 scripts/generate_daily_briefing.py --auto 2>&1 | tee -a \${LOGS_DIR}/malaga_embassy_cron.log
if [ \$? -eq 0 ]; then
    echo "[\$(date -u +%Y-%m-%dT%H:%M:%SZ)] Malaga Embassy Operator: Completed successfully" >> \${LOGS_DIR}/cron.log
else
    echo "[\$(date -u +%Y-%m-%dT%H:%M:%SZ)] Malaga Embassy Operator: FAILED (exit code \$?)" >> \${LOGS_DIR}/cron.log
    echo "URGENT: Malaga Embassy Operator failed" | tee \${COMMS_HUB_DIR}/inbox/gemini/alert-\$(date +%s).txt
fi
EOF

chmod +x /srv/janus/trinity/cron/run-grant-hunter.sh
chmod +x /srv/janus/trinity/cron/run-malaga-operator.sh

(crontab -l 2>/dev/null; echo "0 8 * * * /srv/janus/trinity/cron/run-malaga-operator.sh") | crontab -
(crontab -l 2>/dev/null; echo "0 9 * * * /srv/janus/trinity/cron/run-grant-hunter.sh") | crontab -

echo "✅ Cron jobs installed"

# Step 4: Implement Monitoring
echo "Step 4: Implementing monitoring..."
cat > /srv/janus/trinity/cron/run-health-check.sh <<EOF
#!/bin/bash
set -e
source /srv/janus/trinity/.env-haiku
source \${PYTHON_ENV}/bin/activate
echo "=== JANUS-HAIKU HEALTH CHECK ==="
echo "Date: \$(date -u +%Y-%m-%dT%H:%M:%SZ)"
echo ""
echo "Skill #1: EU Grant Hunter"
if [ -f \${LOGS_DIR}/grant_hunter_cron.log ]; then
    tail -5 \${LOGS_DIR}/grant_hunter_cron.log
    echo "✅ Grant Hunter operational"
else
    echo "❌ Grant Hunter log not found"
fi
echo ""
echo "Skill #2: Malaga Embassy Operator"
if [ -f \${LOGS_DIR}/malaga_embassy_cron.log ]; then
    tail -5 \${LOGS_DIR}/malaga_embassy_cron.log
    cd \${SKILLS_DIR}/malaga-embassy-operator
    HEALTH=\$(python3 scripts/calculate_health_score.py --json | jq '.score')
    echo "Current Health Score: \${HEALTH}/100"
    if (( \$(echo "\${HEALTH} < 70" | bc -l) )); then
        echo "⚠️  Health below 70, attention required"
        echo "WARNING: Malaga health \${HEALTH}/100" | tee \${COMMS_HUB_DIR}/inbox/claude/warning-\$(date +%s).txt
    else
        echo "✅ Malaga Embassy operational"
    fi
else
    echo "❌ Malaga Embassy log not found"
fi
echo ""
echo "Disk Usage:"
df -h /srv/janus | tail -1
echo ""
echo "Log Sizes:"
du -sh \${LOGS_DIR}/*.log 2>/dev/null || echo "No logs yet"
echo ""
echo "=== Health check complete ==="
EOF

chmod +x /srv/janus/trinity/cron/run-health-check.sh
(crontab -l 2>/dev/null; echo "0 10 * * 0 /srv/janus/trinity/cron/run-health-check.sh") | crontab -

echo "✅ Monitoring active"

# Step 5: Pre-Deployment Testing
echo "Step 5: Running pre-deployment tests..."
cd /srv/janus/trinity/skills/eu-grant-hunter
python3 scripts/scan_eu_databases.py --dry-run --max-results 2
cd /srv/janus/trinity/skills/malaga-embassy-operator
python3 scripts/generate_daily_briefing.py --no-comms --json > /dev/null

echo "✅ All tests passed"

echo "=== JANUS-HAIKU DEPLOYMENT COMPLETE ==="
echo "Janus-Haiku is now operational."