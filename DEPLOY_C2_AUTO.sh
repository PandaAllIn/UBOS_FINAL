#!/usr/bin/env bash
# Automated C2 Deployment Script
# Run after creating GitHub gist

set -euo pipefail

echo "═══════════════════════════════════════════════════════"
echo "🔥 BALAUR C2 AUTO-DEPLOYMENT"
echo "═══════════════════════════════════════════════════════"
echo ""

# Get gist ID from user
echo "📝 Enter your GIST ID (from the gist URL):"
echo "   Example: If URL is https://gist.github.com/PandaAllIn/a1b2c3d4e5f6g7h8"
echo "   Then GIST ID is: a1b2c3d4e5f6g7h8"
echo ""
read -p "GIST ID: " GIST_ID

if [[ -z "$GIST_ID" ]]; then
    echo "❌ ERROR: Gist ID cannot be empty!"
    exit 1
fi

echo ""
echo "✅ Gist ID: $GIST_ID"
echo "✅ GitHub User: PandaAllIn"
echo ""

# Update C2 script with gist details
echo "📝 Updating C2 script with your gist details..."
cd /Users/panda/Desktop/UBOS

sed -i.backup \
    -e "s/REPLACE_WITH_YOUR_GIST_ID/$GIST_ID/" \
    -e "s/REPLACE_WITH_YOUR_USERNAME/PandaAllIn/" \
    02_FORGE/scripts/balaur_github_c2.sh

if grep -q "$GIST_ID" 02_FORGE/scripts/balaur_github_c2.sh; then
    echo "✅ C2 script updated successfully!"
else
    echo "❌ ERROR: Failed to update C2 script!"
    exit 1
fi

echo ""
echo "📦 Staging files for Git..."
git add 02_FORGE/scripts/balaur_github_c2.sh
git add GITHUB_REVERSE_SHELL.md
git add DEPLOY_C2.md
git add CREATE_GIST_NOW.txt
git add DEPLOY_C2_AUTO.sh

echo ""
echo "💾 Creating Git commit..."
git commit -m "🚨 EMERGENCY: Deploy GitHub C2 for Balaur access recovery

Gist ID: $GIST_ID
Method: GitHub-based command & control
Status: Ready for deployment

This enables remote command execution via GitHub gist polling.
Balaur will check gist every 5 minutes and execute commands."

echo ""
echo "🚀 Pushing to GitHub..."
if git push origin main; then
    echo ""
    echo "═══════════════════════════════════════════════════════"
    echo "✅ SUCCESS! C2 DEPLOYED TO GITHUB!"
    echo "═══════════════════════════════════════════════════════"
    echo ""
    echo "📊 STATUS:"
    echo "  ✅ C2 script configured with gist: $GIST_ID"
    echo "  ✅ Pushed to GitHub repo: UBOS_FINAL"
    echo "  ✅ Balaur will sync (if auto-sync enabled)"
    echo ""
    echo "⏰ NEXT STEPS:"
    echo "  1. Wait 5-30 minutes for Balaur to sync from GitHub"
    echo "  2. If auto-sync not configured, C2 will activate when you get home"
    echo "  3. Monitor your gist for Balaur responses (we'll add auto-check)"
    echo ""
    echo "🔍 YOUR GIST URL:"
    echo "  https://gist.github.com/PandaAllIn/$GIST_ID"
    echo ""
    echo "💡 TEST IT:"
    echo "  - Add more commands to balaur_commands.txt in your gist"
    echo "  - Balaur will execute them and log to /tmp/balaur_c2_results.log"
    echo ""
    echo "═══════════════════════════════════════════════════════"
else
    echo ""
    echo "❌ ERROR: Failed to push to GitHub!"
    echo "Check your internet connection and Git credentials."
    exit 1
fi

echo ""
echo "🎯 Want to set up automatic gist monitoring? (y/n)"
read -p "Answer: " SETUP_MONITOR

if [[ "$SETUP_MONITOR" =~ ^[Yy]$ ]]; then
    echo ""
    echo "📡 Setting up gist monitor..."
    
    # Create monitor script
    cat > /Users/panda/Desktop/UBOS/monitor_gist.sh << 'MONITOR_EOF'
#!/usr/bin/env bash
# Monitor Balaur C2 Results

GIST_ID="GIST_ID_PLACEHOLDER"
RESULTS_URL="https://gist.githubusercontent.com/PandaAllIn/${GIST_ID}/raw/balaur_results.txt"

echo "🔍 Checking Balaur results..."
curl -sf "$RESULTS_URL" || echo "No results yet (or gist not accessible)"
MONITOR_EOF
    
    # Replace placeholder
    sed -i.bak "s/GIST_ID_PLACEHOLDER/$GIST_ID/" /Users/panda/Desktop/UBOS/monitor_gist.sh
    chmod +x /Users/panda/Desktop/UBOS/monitor_gist.sh
    
    echo "✅ Monitor script created: /Users/panda/Desktop/UBOS/monitor_gist.sh"
    echo ""
    echo "Run it with: ./monitor_gist.sh"
fi

echo ""
echo "🦁 SOVEREIGNTY PROTOCOL ACTIVATED!"
echo "═══════════════════════════════════════════════════════"

