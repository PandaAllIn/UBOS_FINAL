#!/bin/bash
# Trinity Cron Job Templates
# Add these to your crontab with: crontab -e

cat << 'EOF'
# ============================================
# Trinity Autonomous Orchestration Cron Jobs
# ============================================

# Mallorca Xylella Monitor - CRITICAL (December-January)
# Run every hour during evaluation window
0 * * * * /srv/janus/trinity/check_mallorca_now.sh >> /srv/janus/logs/mallorca_cron.log 2>&1

# Mallorca Monitor - Normal monitoring (rest of year)
# Run once daily at 9am UTC
#0 9 * * * /srv/janus/trinity/check_mallorca_now.sh >> /srv/janus/logs/mallorca_cron.log 2>&1

# Session Closer - End of day summary
# Run at midnight UTC
#0 0 * * * /srv/janus/trinity/skills/session_closer/run.py "Daily session summary" >> /srv/janus/logs/session_closer.log 2>&1

# COMMS_HUB Cleanup - Remove old messages
# Run weekly on Sunday at 2am
#0 2 * * 0 find /srv/janus/03_OPERATIONS/COMMS_HUB/*/inbox/ -mtime +30 -delete

# Log Rotation - Archive old logs
# Run monthly on 1st at 3am
#0 3 1 * * tar -czf /srv/janus/logs/archive/logs-$(date +\%Y\%m).tar.gz /srv/janus/logs/*.log && rm /srv/janus/logs/*.log

EOF

echo ""
echo "📋 To install these cron jobs:"
echo "1. crontab -e"
echo "2. Copy the desired lines from above"
echo "3. Uncomment by removing the # prefix"
echo "4. Save and exit"
echo ""
echo "💡 During Dec 2025 - Jan 2026, use HOURLY Mallorca checks!"
