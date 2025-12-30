#!/bin/bash
# Real-time Obsidian update script for UBOS
# Demonstrates programmatic vault manipulation

API_BASE="https://127.0.0.1:27124"
TOKEN="26a9dc89c0d9e1f99f89a7eee541dcf377f09ab1cb29c8ba10c6f961a7406de8"
HEADERS=(-H "Authorization: Bearer $TOKEN" -H "Content-Type: text/markdown")

# Function: Create daily briefing
create_daily_briefing() {
    local date=$(date '+%Y-%m-%d')
    local content="---
date: $date
type: daily_briefing
status: automated
---

# Daily Briefing - $date

## Mission Status
- **Malaga Embassy:** Pre-deployment phase
- **Departure:** Next week (with brother + dog)
- **Housing:** Searching (€1,000/month, finca preferred)
- **Capital:** €1,800 (100/100 health)

## Grant Pipeline
- **Total:** €113M+ tracked
- **Priority:** Xylella €6M (Stage 2)
- **Deadline:** Consortium formation in progress

## Today's Focus
[ ] Continue housing search (Axarquía, Montes, Valle)
[ ] Review Obsidian power user research results
[ ] Test advanced Observatory capabilities
[ ] Constitutional alignment verification

---
*Generated automatically by UBOS automation*
"
    
    echo "$content" | curl -k -s -X POST "$API_BASE/vault/03_OPERATIONS/MALAGA_EMBASSY/briefings/$date.md" "${HEADERS[@]}" --data-binary @-
    echo "✅ Daily briefing created: $date.md"
}

# Function: Update dashboard
update_dashboard() {
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    local update="

---
**Dashboard Auto-Update:** $timestamp
**Status:** All systems operational
**Observatory:** Real-time integration active

"
    echo "$update" | curl -k -s -X POST "$API_BASE/vault/_DASHBOARDS/MISSION_STATUS.md" "${HEADERS[@]}" --data-binary @-
    echo "✅ Dashboard updated at $timestamp"
}

# Function: Open file in Obsidian
open_file() {
    local filepath="$1"
    curl -k -s -X POST "$API_BASE/open/$filepath" "${HEADERS[@]}"
    echo "✅ Opened: $filepath"
}

# Function: List vault contents
list_vault() {
    local path="${1:-.}"
    curl -k -s -X GET "$API_BASE/vault/$path/" "${HEADERS[@]}" | jq -r '.files[]' 2>/dev/null || echo "Error listing vault"
}

# Main menu
case "${1:-help}" in
    briefing)
        create_daily_briefing
        ;;
    dashboard)
        update_dashboard
        ;;
    open)
        open_file "$2"
        ;;
    list)
        list_vault "$2"
        ;;
    *)
        echo "UBOS Obsidian Automation Script"
        echo ""
        echo "Usage:"
        echo "  $0 briefing          - Create today's daily briefing"
        echo "  $0 dashboard         - Update mission dashboard"
        echo "  $0 open <file>       - Open file in Obsidian UI"
        echo "  $0 list [path]       - List vault contents"
        echo ""
        echo "Examples:"
        echo "  $0 briefing"
        echo "  $0 open CONCEPTS/AUTONOMY_HUB.md"
        echo "  $0 list CONCEPTS"
        ;;
esac
