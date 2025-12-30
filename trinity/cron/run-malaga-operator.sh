#!/bin/bash
set -e
source /srv/janus/trinity/.env-haiku
source ${PYTHON_ENV}/bin/activate
echo "[$(date -u +%Y-%m-%dT%H:%M:%SZ)] Malaga Embassy Operator: Starting daily briefing" >> ${LOGS_DIR}/cron.log
cd ${SKILLS_DIR}/malaga-embassy-operator
python3 scripts/generate_daily_briefing.py 2>&1 | tee -a ${LOGS_DIR}/malaga_embassy_cron.log
if [ $? -eq 0 ]; then
    echo "[$(date -u +%Y-%m-%dT%H:%M:%SZ)] Malaga Embassy Operator: Completed successfully" >> ${LOGS_DIR}/cron.log
else
    echo "[$(date -u +%Y-%m-%dT%H:%M:%SZ)] Malaga Embassy Operator: FAILED (exit code $?)" >> ${LOGS_DIR}/cron.log
    echo "URGENT: Malaga Embassy Operator failed" | tee ${COMMS_HUB_DIR}/inbox/gemini/alert-$(date +%s).txt
fi
