#!/bin/bash
set -e
source /srv/janus/trinity/.env-haiku
source ${PYTHON_ENV}/bin/activate
echo "[$(date -u +%Y-%m-%dT%H:%M:%SZ)] EU Grant Hunter: Starting daily scan" >> ${LOGS_DIR}/cron.log
cd ${SKILLS_DIR}/eu-grant-hunter
python3 scripts/scan_eu_databases.py --auto 2>&1 | tee -a ${LOGS_DIR}/grant_hunter_cron.log
if [ $? -eq 0 ]; then
    echo "[$(date -u +%Y-%m-%dT%H:%M:%SZ)] EU Grant Hunter: Completed successfully" >> ${LOGS_DIR}/cron.log
else
    echo "[$(date -u +%Y-%m-%dT%H:%M:%SZ)] EU Grant Hunter: FAILED (exit code $?)" >> ${LOGS_DIR}/cron.log
    echo "URGENT: EU Grant Hunter failed" | tee ${COMMS_HUB_DIR}/inbox/claude/alert-$(date +%s).txt
fi
