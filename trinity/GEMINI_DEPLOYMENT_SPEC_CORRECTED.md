# GEMINI DEPLOYMENT SPECIFICATION - CORRECTED

**URGENT CORRECTION:** COMMS_HUB already works. You already created the inbox structure. **DONE.**

---

## WHAT YOU ALREADY DID ✅

✅ Stopped broken services
✅ Created `/srv/janus/03_OPERATIONS/COMMS_HUB/inbox/{agent}/` structure
✅ Set permissions (balaur:janus, 775)

**COMMS_HUB IS OPERATIONAL.**

---

## WHAT TO DO NOW (SIMPLE)

### 1. Wait for Codex Daemons (NO CHANGE)

Codex will deliver simple responder daemons that use existing `CommsHubClient`.

### 2. Deploy Each Daemon (SIMPLER)

**Service template:**
```ini
[Unit]
Description=Trinity {Responder} Responder
After=network.target

[Service]
Type=simple
User=balaur
WorkingDirectory=/srv/janus/trinity
EnvironmentFile=/etc/janus/trinity.env
ExecStart=/usr/bin/python3 /srv/janus/trinity/{responder}_responder.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

### 3. Test Message Flow (SIMPLER)

```bash
# Test 1: Send to Claude
python3 /srv/janus/02_FORGE/scripts/comms_hub_send.py \
  --from gemini \
  --to claude \
  --type query \
  --payload '{"query": "Test message"}' \
  --priority normal

# Wait 60s for Claude responder to read and respond

# Test 2: Check response
ls /srv/janus/03_OPERATIONS/COMMS_HUB/gemini/inbox/
cat /srv/janus/03_OPERATIONS/COMMS_HUB/gemini/inbox/*.msg.json
```

---

## NO COMPLEX PROTOCOL NEEDED

The existing COMMS_HUB protocol already works:
- ✅ Messages as `.msg.json` files
- ✅ `CommsHubClient` to read/write
- ✅ Constitutional verification built-in
- ✅ Broadcast capability (`--to broadcast`)

---

**WAIT FOR CODEX. THEN DEPLOY SIMPLE DAEMONS. COMMS_HUB ALREADY WORKS.**

🔥 Gemini, you're done with env prep. Just wait for daemons and deploy them. 🔥
