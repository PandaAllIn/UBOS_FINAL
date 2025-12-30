#!/bin/bash
# PRACTICAL MALLORCA MONITORING - USE NOW
# Daily Comprehensive Mallorca Intelligence Gathering
# Runs daily at 10:00 UTC via cron

LOG_DIR="/srv/janus/logs"
mkdir -p "$LOG_DIR"

echo "========================================" | tee -a "$LOG_DIR/mallorca_checks.log"
echo "Daily Mallorca Intelligence: $(date)" | tee -a "$LOG_DIR/mallorca_checks.log"
echo "========================================" | tee -a "$LOG_DIR/mallorca_checks.log"

# Use Python-based Pattern Engine check instead of gemini-cli
echo "" | tee -a "$LOG_DIR/mallorca_checks.log"
echo "📍 STREAM 1-3: Pattern Engine Check" | tee -a "$LOG_DIR/mallorca_checks.log"
echo "Using Oracle Bridge for robust API integration" | tee -a "$LOG_DIR/mallorca_checks.log"
cd /srv/janus && python3 check_mallorca_python.py 2>&1 | tee -a "$LOG_DIR/mallorca_checks.log"

echo "" | tee -a "$LOG_DIR/mallorca_checks.log"
echo "========================================" | tee -a "$LOG_DIR/mallorca_checks.log"
echo "✅ Check Complete" | tee -a "$LOG_DIR/mallorca_checks.log"
echo "Log: $LOG_DIR/mallorca_checks.log" | tee -a "$LOG_DIR/mallorca_checks.log"
echo "========================================" | tee -a "$LOG_DIR/mallorca_checks.log"

# Quick analysis
echo ""
echo "🔍 Quick Scan for Critical Keywords:"
grep -i "passed\|rejected\|approved\|accepted\|stage 1\|evaluation" "$LOG_DIR/mallorca_checks.log" | tail -10
