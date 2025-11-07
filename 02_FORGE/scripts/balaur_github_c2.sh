#!/usr/bin/env bash
# GitHub C2 (Command & Control) for Balaur Emergency Access
# Polls GitHub gist for commands, executes them, writes results

set -euo pipefail

# CONFIGURATION - UPDATE THESE WITH YOUR GIST DETAILS
GIST_ID="${BALAUR_C2_GIST_ID:-109193c479976a8337a8801ea0b6d915}"
GITHUB_USER="${BALAUR_C2_USER:-PandaAllIn}"
COMMANDS_FILE="balaur_commands.txt"
PROCESSED_LOG="/tmp/balaur_c2_processed.log"
RESULTS_LOG="/tmp/balaur_c2_results.log"

# GitHub RAW URL (works for public gists, no auth needed)
COMMANDS_URL="https://gist.githubusercontent.com/${GITHUB_USER}/${GIST_ID}/raw/${COMMANDS_FILE}"

# Initialize
touch "$PROCESSED_LOG"
touch "$RESULTS_LOG"

echo "[$(date '+%Y-%m-%d %H:%M:%S')] 🔥 Balaur C2 Agent starting..."

# Fetch commands
echo "[$(date '+%Y-%m-%d %H:%M:%S')] Fetching commands from GitHub..."
COMMANDS=$(curl -sf -m 10 "$COMMANDS_URL" 2>/dev/null || echo "")

if [[ -z "$COMMANDS" ]]; then
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] ❌ No commands found or connection failed"
    exit 0
fi

echo "[$(date '+%Y-%m-%d %H:%M:%S')] ✅ Commands received, processing..."

# Process each command
EXECUTED=0
while IFS='|' read -r cmd_id command; do
    # Skip comments and empty lines
    [[ "$cmd_id" =~ ^#.*$ || -z "$cmd_id" ]] && continue
    [[ -z "$command" ]] && continue
    
    # Check if already processed
    if grep -q "^${cmd_id}$" "$PROCESSED_LOG" 2>/dev/null; then
        continue
    fi
    
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] ⚡ Executing CMD_ID: $cmd_id"
    
    # Execute command with timeout and capture output
    START_TIME=$(date '+%Y-%m-%d %H:%M:%S')
    OUTPUT=$(timeout 30s bash -c "$command" 2>&1 || echo "ERROR: Exit code $?")
    END_TIME=$(date '+%Y-%m-%d %H:%M:%S')
    
    # Write result
    cat >> "$RESULTS_LOG" << EOF
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
CMD_ID: $cmd_id
COMMAND: $command
START: $START_TIME
END: $END_TIME
OUTPUT:
$OUTPUT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

EOF
    
    # Mark as processed
    echo "$cmd_id" >> "$PROCESSED_LOG"
    EXECUTED=$((EXECUTED + 1))
    
    echo "[$(date '+%Y-%m-d %H:%M:%S')] ✅ Command $cmd_id completed"
done <<< "$COMMANDS"

if [[ $EXECUTED -gt 0 ]]; then
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] 🎯 Executed $EXECUTED command(s)"
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] 📝 Results written to: $RESULTS_LOG"
    
    # Display recent results
    echo ""
    echo "========== LATEST RESULTS =========="
    tail -50 "$RESULTS_LOG"
    echo "===================================="
else
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] ℹ️  No new commands to execute"
fi

echo "[$(date '+%Y-%m-%d %H:%M:%S')] ✅ Balaur C2 Agent finished"

