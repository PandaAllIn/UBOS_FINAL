# BALAUR RESIDENTS TESTING & AUTO-START GUIDE
**Date:** 2025-10-31
**Purpose:** Complete testing and auto-start configuration for Balaur API residents
**Status:** READY FOR TESTING

---

## OVERVIEW

The Balaur hosts **4 permanent API residents** that auto-start with Janus manifested:

1. **Groq Hot Vessel** - Ultra-fast inference (450-1200 tps)
2. **OpenAI Hot Vessel** - Multi-modal intelligence (text, image, audio, video)
3. **Claude Haiku Resident** - Fast strategic support
4. **Gemini 2.5 Pro Resident** - Systems engineering support

---

## FILES CREATED

### Service Definitions (systemd)

```
/srv/janus/03_OPERATIONS/vessels/balaur/services/
├── groq-hot-vessel.service           # Groq auto-start service
├── openai-hot-vessel.service         # OpenAI auto-start service
├── claude-haiku-resident.service     # Claude Haiku auto-start service
└── gemini-pro-resident.service       # Gemini 2.5 Pro auto-start service
```

### Testing & Setup Scripts

```
/srv/janus/03_OPERATIONS/vessels/balaur/scripts/
├── setup_auto_start.sh               # Install and enable all services
└── verify_all_residents.sh           # Comprehensive boot verification
```

### Boot Sequences (Already Created)

```
/srv/janus/00_CONSTITUTION/boot_sequences/
├── GROQ_HOT_VESSEL_V5.md            # Groq boot sequence with model routing
├── OPENAI_HOT_VESSEL_V5.md          # OpenAI boot sequence with task routing
├── CLAUDE_BOOT_V5.md                # Claude boot sequence (used by Haiku)
├── GEMINI_BOOT_V5.md                # Gemini boot sequence (used by 2.5 Pro)
└── MASTER_BOOT_ORCHESTRATOR.md      # Republic-wide orchestration
```

---

## SETUP PROCEDURE

### Step 1: Verify Prerequisites

Make sure API keys are set in the environment:

```bash
# Check if API keys are configured
echo "GROQ_API_KEY: ${GROQ_API_KEY:+SET}"
echo "OPENAI_API_KEY: ${OPENAI_API_KEY:+SET}"
echo "ANTHROPIC_API_KEY: ${ANTHROPIC_API_KEY:+SET}"
echo "GOOGLE_API_KEY: ${GOOGLE_API_KEY:+SET}"
```

**If not set**, add them to the janus user's environment:

```bash
# Option 1: Add to /home/janus/.bashrc
sudo -u janus bash -c 'echo "export GROQ_API_KEY=\"your_key_here\"" >> ~/.bashrc'
sudo -u janus bash -c 'echo "export OPENAI_API_KEY=\"your_key_here\"" >> ~/.bashrc'
sudo -u janus bash -c 'echo "export ANTHROPIC_API_KEY=\"your_key_here\"" >> ~/.bashrc'
sudo -u janus bash -c 'echo "export GOOGLE_API_KEY=\"your_key_here\"" >> ~/.bashrc'

# Option 2: Add to /etc/environment (system-wide)
echo 'GROQ_API_KEY="your_key_here"' | sudo tee -a /etc/environment
echo 'OPENAI_API_KEY="your_key_here"' | sudo tee -a /etc/environment
echo 'ANTHROPIC_API_KEY="your_key_here"' | sudo tee -a /etc/environment
echo 'GOOGLE_API_KEY="your_key_here"' | sudo tee -a /etc/environment
```

### Step 2: Install Auto-Start Services

Run the setup script with sudo:

```bash
sudo /srv/janus/03_OPERATIONS/vessels/balaur/scripts/setup_auto_start.sh
```

This will:
1. ✅ Copy service files to `/etc/systemd/system/`
2. ✅ Enable services for auto-start on boot
3. ✅ Create log directory
4. ✅ Verify environment variables
5. ✅ Optionally start services immediately

### Step 3: Verify All Residents

Run the comprehensive verification script:

```bash
/srv/janus/03_OPERATIONS/vessels/balaur/scripts/verify_all_residents.sh
```

This will test:
- ✅ Boot sequence files exist
- ✅ Services are active
- ✅ API connectivity
- ✅ Janus manifestation configuration
- ✅ Boot logs

---

## TESTING EACH RESIDENT

### Test 1: Groq Hot Vessel

**Check Service:**
```bash
systemctl status groq-hot-vessel.service
```

**Check Logs:**
```bash
journalctl -u groq-hot-vessel.service -f
```

**Test Model Routing:**
```bash
# Test fast inference (should use llama-3.1-8b @ 560 tps)
curl -X POST http://localhost:8080/inference \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Quick test", "task_type": "simple"}'

# Test complex inference (should use gpt-oss-120b @ 500 tps)
curl -X POST http://localhost:8080/inference \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Analyze strategic implications...", "task_type": "complex"}'
```

**Expected Output:**
- Service status: `active (running)`
- Log shows: "Groq Hot Vessel: ONLINE - Janus manifested"
- Model routing working correctly

---

### Test 2: OpenAI Hot Vessel

**Check Service:**
```bash
systemctl status openai-hot-vessel.service
```

**Check Logs:**
```bash
journalctl -u openai-hot-vessel.service -f
```

**Test Multi-Modal Routing:**
```bash
# Test text reasoning (should route to gpt-5-pro or o3)
curl -X POST http://localhost:8081/inference \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Deep strategic analysis", "task_type": "reasoning", "complexity": "max"}'

# Test image generation (should route to gpt-image-1)
curl -X POST http://localhost:8081/generate \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Steampunk logo", "type": "image"}'
```

**Expected Output:**
- Service status: `active (running)`
- Log shows: "OpenAI Hot Vessel: ONLINE - Janus manifested"
- Multi-modal routing working correctly

---

### Test 3: Claude Haiku Resident

**Check Service:**
```bash
systemctl status claude-haiku-resident.service
```

**Check Logs:**
```bash
journalctl -u claude-haiku-resident.service -f
```

**Test Strategic Support:**
```bash
# Test quick strategic query
curl -X POST http://localhost:8082/query \
  -H "Content-Type: application/json" \
  -d '{"query": "What is the Lion'\''s Sanctuary philosophy?", "speed": "fast"}'
```

**Expected Output:**
- Service status: `active (running)`
- Log shows: "Claude Haiku Resident: ONLINE - Janus manifested"
- Fast responses for strategic queries

---

### Test 4: Gemini 2.5 Pro Resident

**Check Service:**
```bash
systemctl status gemini-pro-resident.service
```

**Check Logs:**
```bash
journalctl -u gemini-pro-resident.service -f
```

**Test Systems Support:**
```bash
# Test technical query
curl -X POST http://localhost:8083/query \
  -H "Content-Type: application/json" \
  -d '{"query": "Best practices for systemd service hardening", "context_size": "large"}'
```

**Expected Output:**
- Service status: `active (running)`
- Log shows: "Gemini 2.5 Pro Resident: ONLINE - Janus manifested"
- Large context window utilized

---

## VERIFY AUTO-START ON BOOT

### Test Boot Sequence

1. **Reboot the Balaur:**
   ```bash
   sudo reboot
   ```

2. **After reboot, verify all services started automatically:**
   ```bash
   /srv/janus/03_OPERATIONS/vessels/balaur/scripts/verify_all_residents.sh
   ```

3. **Check boot log:**
   ```bash
   cat /srv/janus/03_OPERATIONS/vessels/balaur/logs/boot.log
   ```

**Expected boot log entries:**
```
2025-10-31T14:30:00+00:00 - Groq Hot Vessel: ONLINE - Janus manifested
   Models: 13 available (7 prod, 2 systems, 4 preview)
   Max Speed: 1000 tokens/sec
2025-10-31T14:30:02+00:00 - OpenAI Hot Vessel: ONLINE - Janus manifested
   Models: 30+ (Frontier, Specialized, Reasoning, Multi-modal)
   Capabilities: Text, Image, Audio, Video, Deep Research
2025-10-31T14:30:05+00:00 - Claude Haiku Resident: ONLINE - Janus manifested
   Role: Strategic Support (Fast, Lightweight)
   Capabilities: Quick strategic queries, analysis, synthesis
2025-10-31T14:30:07+00:00 - Gemini 2.5 Pro Resident: ONLINE - Janus manifested
   Role: Systems Support (1M Context, ADK)
   Capabilities: Infrastructure queries, technical analysis, code review
```

---

## JANUS MANIFESTATION VERIFICATION

Each resident service has `JANUS_MANIFESTED=true` in its environment. Verify this is working:

### Check Janus State

```bash
# For each service, check if Janus is manifested
for service in groq-hot-vessel openai-hot-vessel claude-haiku-resident gemini-pro-resident; do
    echo "=== $service ==="
    systemctl show "$service.service" -p Environment | grep JANUS_MANIFESTED
done
```

**Expected Output:**
```
=== groq-hot-vessel ===
Environment=JANUS_MANIFESTED=true
=== openai-hot-vessel ===
Environment=JANUS_MANIFESTED=true
=== claude-haiku-resident ===
Environment=JANUS_MANIFESTED=true
=== gemini-pro-resident ===
Environment=JANUS_MANIFESTED=true
```

### Test Janus-Aware Behavior

Janus-manifested residents should:
- ✅ Use boot sequences from `/srv/janus/00_CONSTITUTION/boot_sequences/`
- ✅ Have constitutional alignment built in
- ✅ Log to Republic-wide boot log
- ✅ Integrate with Pneumatic Tube Network (COMMS_HUB)

---

## TROUBLESHOOTING

### Service Won't Start

**Check logs:**
```bash
journalctl -u <service-name>.service -n 50
```

**Common issues:**
- API key not set → Set in environment
- Port already in use → Change port in service file
- Package missing → Install required Python packages

### API Not Reachable

**Test manually:**
```bash
# Groq
curl https://api.groq.com/openai/v1/models \
  -H "Authorization: Bearer $GROQ_API_KEY"

# OpenAI
curl https://api.openai.com/v1/models \
  -H "Authorization: Bearer $OPENAI_API_KEY"
```

**Common issues:**
- Network connectivity → Check firewall
- Invalid API key → Verify key is correct
- Rate limit exceeded → Wait and retry

### Service Keeps Restarting

**Check resource limits:**
```bash
systemctl status <service-name>.service
```

**Common issues:**
- Memory limit too low → Increase in service file
- API quota exceeded → Check API usage
- Configuration error → Review service file

---

## INTEGRATION WITH CLI TRINITY

The CLI Trinity (Claude, Gemini, Codex in VSCode) can use the Balaur residents:

### From Claude CLI

```python
# Use Groq for fast inference
from groq_vessel import query
response = query("Analyze Portal Oradea viability", speed="fast")

# Use OpenAI for multi-modal
from openai_vessel import generate_image
logo = generate_image("UBOS Republic logo", quality="hd")
```

### From Gemini CLI

```python
# Use Claude Haiku for quick strategic checks
from claude_haiku import consult
advice = consult("Is this infrastructure change aligned?")

# Use Gemini Pro for large context analysis
from gemini_pro import analyze_codebase
review = analyze_codebase("/srv/janus/02_FORGE/")
```

### From Codex CLI

```python
# Use Groq for fast code generation
from groq_vessel import generate_code
code = generate_code("Python function to validate JSON", language="python")

# Use OpenAI for complex code review
from openai_vessel import review_code
review = review_code(source_code, focus=["security", "performance"])
```

---

## SUCCESS CRITERIA

All tests pass when:

✅ **Auto-Start:** All 4 services start automatically on boot
✅ **Janus Manifested:** All services have `JANUS_MANIFESTED=true`
✅ **API Connectivity:** All APIs are reachable
✅ **Model Routing:** Groq and OpenAI intelligently route to optimal models
✅ **Boot Logs:** Clean boot sequence logged
✅ **Integration:** CLI Trinity can access Balaur residents
✅ **Constitutional Alignment:** All residents follow Lion's Sanctuary principles

---

## MONITORING & MAINTENANCE

### Daily Health Check

```bash
/srv/janus/03_OPERATIONS/vessels/balaur/scripts/verify_all_residents.sh
```

### View Realtime Logs

```bash
tail -f /srv/janus/03_OPERATIONS/vessels/balaur/logs/*.log
```

### Restart All Services

```bash
sudo systemctl restart groq-hot-vessel
sudo systemctl restart openai-hot-vessel
sudo systemctl restart claude-haiku-resident
sudo systemctl restart gemini-pro-resident
```

### View Boot History

```bash
cat /srv/janus/03_OPERATIONS/vessels/balaur/logs/boot.log
```

---

## NEXT STEPS

Once all tests pass:

1. ✅ Document successful boot configuration
2. ✅ Update STATE_OF_THE_REPUBLIC.md
3. ✅ Test end-to-end Trinity workflow with Balaur residents
4. ✅ Verify Janus manifestation across all vessels
5. ✅ Create monitoring dashboard for resident health

---

**TESTING CHECKLIST:**

- [ ] API keys configured
- [ ] Auto-start services installed
- [ ] All services running
- [ ] Boot log shows successful initialization
- [ ] Janus manifestation verified
- [ ] Model routing working (Groq)
- [ ] Multi-modal routing working (OpenAI)
- [ ] Strategic support working (Claude Haiku)
- [ ] Systems support working (Gemini Pro)
- [ ] Auto-start verified after reboot
- [ ] Integration with CLI Trinity tested

---

**STATUS:** Ready for Captain BROlinni to test on Balaur! 🔥

**The Republic awaits activation, Captain.** 🏛️
