#!/bin/bash
set -e
source /srv/janus/trinity/.env-haiku
source ${PYTHON_ENV}/bin/activate
echo "=== JANUS-HAIKU HEALTH CHECK ==="
echo "Date: $(date -u +%Y-%m-%dT%H:%M:%SZ)"
echo ""
echo "Skill #1: EU Grant Hunter"
if [ -f ${LOGS_DIR}/grant_hunter_cron.log ]; then
    tail -5 ${LOGS_DIR}/grant_hunter_cron.log
    echo "✅ Grant Hunter operational"
else
    echo "❌ Grant Hunter log not found"
fi
echo ""
echo "Skill #2: Malaga Embassy Operator"
if [ -f ${LOGS_DIR}/malaga_embassy_cron.log ]; then
    tail -5 ${LOGS_DIR}/malaga_embassy_cron.log
    cd ${SKILLS_DIR}/malaga-embassy-operator
    HEALTH=$(python3 scripts/calculate_health_score.py --json | jq '.score')
    echo "Current Health Score: ${HEALTH}/100"
    if (( $(echo "${HEALTH} < 70" | bc -l) )); then
        echo "⚠️  Health below 70, attention required"
        echo "WARNING: Malaga health ${HEALTH}/100" | tee ${COMMS_HUB_DIR}/inbox/claude/warning-$(date +%s).txt
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
du -sh ${LOGS_DIR}/*.log 2>/dev/null || echo "No logs yet"
echo ""
echo "=== Health check complete ==="
