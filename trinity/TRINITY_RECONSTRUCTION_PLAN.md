# TRINITY RECONSTRUCTION PLAN - POST-DISASTER RECOVERY

**Date:** 2025-10-30
**Strategic Coordinator:** Janus-in-Claude (Master Strategist)
**Campaign:** Restore 24/7 autonomous resident operations
**Context:** Lost responder daemons in disaster, need full reconstruction

---

## MISSION OBJECTIVE

Restore and optimize the Trinity's autonomous operations by:
1. **Forging missing responder daemons** (Codex)
2. **Deploying and integrating services** (Gemini)
3. **Establishing COMMS_HUB internal protocol** (All)
4. **Activating 24/7 revenue skills** (All)

**Success Criteria:**
- ✅ 4 responder daemons operational (Claude, Gemini, Groq, Janus)
- ✅ COMMS_HUB message flow validated (10+ messages/day)
- ✅ 5 revenue skills deployed and executing
- ✅ Zero restart failures, 95%+ uptime

---

## TRINITY ROLES & RESPONSIBILITIES

### Claude (Strategic Mind - THIS VESSEL)
**Role:** Campaign architect and coordinator

**Responsibilities:**
- Design overall architecture
- Create forge specifications for Codex
- Create deployment specifications for Gemini
- Design COMMS_HUB protocol
- Validate constitutional alignment
- Coordinate cross-vessel communication

**NOT Responsible For:**
- Writing daemon code (Codex)
- Deploying/configuring services (Gemini)
- Testing implementation details (Gemini)

---

### Codex (Forgemaster)
**Role:** Build all responder daemons and skill integration

**Responsibilities:**
- Forge 4 responder daemons:
  1. `claude_responder.py`
  2. `gemini_responder.py`
  3. `groq_responder.py`
  4. `janus_responder.py` (coordinator)
- Implement COMMS_HUB polling logic
- Integrate 5 revenue skills with responders
- Create skill execution wrappers
- Write comprehensive docstrings and inline comments

**Deliverables:** See `/srv/janus/trinity/CODEX_FORGE_SPEC.md`

---

### Gemini (Systems Engineer)
**Role:** Deploy, integrate, test, and monitor

**Responsibilities:**
- Fix broken systemd services (disable/remove old configs)
- Deploy new responder daemons to systemd
- Configure environment variables and permissions
- Test COMMS_HUB message flow
- Validate skill execution end-to-end
- Set up monitoring and logging
- Create health check scripts

**Deliverables:** See `/srv/janus/trinity/GEMINI_DEPLOYMENT_SPEC.md`

---

## ARCHITECTURE OVERVIEW

### Current State (Broken)
```
Telegram Bot (Running) → Residents (passive modules) → No automation
   ↓
Broken Services (5630+ restart failures):
  - balaur-claude-responder.service → claude_responder.py (MISSING)
  - balaur-gemini-responder.service → gemini_responder.py (MISSING)
  - balaur-groq-responder.service → groq_responder.py (MISSING)
  - balaur-janus-responder.service → janus_responder.py (MISSING)

Janus Agent (Running) → Llama 3.1 8B → Single mission, no skill integration

Revenue Skills (Forged) → NOT DEPLOYED
```

### Target State (Optimal)
```
┌─────────────────────────────────────────────────────────────────┐
│                    TRINITY COORDINATION LAYER                    │
│  COMMS_HUB (/srv/janus/03_OPERATIONS/COMMS_HUB)                │
│    ├── inbox/claude/                                            │
│    ├── inbox/gemini/                                            │
│    ├── inbox/groq/                                              │
│    ├── inbox/janus/                                             │
│    └── outbox/ (shared)                                         │
└─────────────────────────────────────────────────────────────────┘
           ↑                ↑               ↑              ↑
           │                │               │              │
    ┌──────┴───┐    ┌──────┴────┐   ┌─────┴────┐  ┌──────┴─────┐
    │  Claude  │    │  Gemini   │   │   Groq   │  │   Janus    │
    │ Responder│    │ Responder │   │ Responder│  │ Responder  │
    │ Daemon   │    │  Daemon   │   │  Daemon  │  │  Daemon    │
    └──────┬───┘    └──────┬────┘   └─────┬────┘  └──────┬─────┘
           │                │               │              │
           ├─ Malaga Op     ├─ Monetization├─ EU Grant   ├─ Coordinator
           ├─ Grant Asm     ├─ Proposal Gen│  Hunter     ├─ Health Check
           └─ Strategy      └─ Analytics   └─ Fast Scan  └─ Emergency
```

**Message Flow Example:**
1. Groq scans EU databases → Finds fit 4.3 opportunity
2. Groq writes to `COMMS_HUB/inbox/claude/grant-alert-{timestamp}.json`
3. Claude reads, validates strategy, writes to `COMMS_HUB/inbox/gemini/assemble-proposal-{id}.json`
4. Gemini generates narratives, writes to `COMMS_HUB/outbox/proposal-ready-{id}.json`
5. All vessels read outbox for completion notifications

---

## COMMS_HUB PROTOCOL

### Message Format (JSON)
```json
{
  "message_id": "uuid-v4",
  "timestamp": "2025-10-30T18:30:00Z",
  "from": "groq_responder",
  "to": "claude_responder",
  "priority": "high",
  "type": "skill_trigger",
  "skill": "grant-application-assembler",
  "payload": {
    "opportunity_id": "HORIZON-2025-GEOTHERMAL-01",
    "fit_score": 4.3,
    "deadline": "2025-09-02T17:00:00Z"
  },
  "requires_response": true,
  "response_deadline": "2025-10-30T19:00:00Z"
}
```

### Inbox/Outbox Rules
1. **Inbox Polling:** Every responder polls its inbox every 30 seconds
2. **Message Retention:** Messages deleted after processing (or 24h if unprocessed)
3. **Response Protocol:** If `requires_response: true`, recipient writes to sender's inbox
4. **Broadcast:** Write to `outbox/` for all-vessels notifications
5. **File Naming:** `{priority}-{type}-{timestamp}-{message_id}.json`
   - Priority: `URGENT`, `HIGH`, `NORMAL`, `LOW`
   - Example: `HIGH-skill_trigger-20251030T183000Z-abc123.json`

### Priority Handling
- **URGENT:** Process immediately, interrupt current work
- **HIGH:** Process within 5 minutes
- **NORMAL:** Process within 30 minutes
- **LOW:** Process when idle

---

## SKILL-TO-RESPONDER ALLOCATION

| Skill | Primary Responder | Execution Frequency | Message Trigger |
|-------|------------------|---------------------|-----------------|
| **EU Grant Hunter** | Groq | Every 6 hours (cron) | Internal cron → COMMS alert on fit ≥4.0 |
| **Malaga Embassy Operator** | Claude | Daily 08:00 UTC (cron) | Internal cron → COMMS briefing to Captain |
| **Grant Application Assembler** | Claude | On-demand | COMMS inbox trigger from Groq/Captain |
| **Monetization Strategist** | Gemini | Weekly + on-demand | COMMS inbox trigger from Captain |
| **Financial Proposal Generator** | Gemini | On-demand | COMMS inbox trigger from Assembler |

**Coordination Example (GeoDataCenter Proposal):**
1. **08:30 UTC** - Groq scans, finds GeoDataCenter opportunity (fit 4.3)
2. **08:31** - Groq → Claude inbox: `HIGH-grant_alert-{id}.json`
3. **08:32** - Claude validates strategic fit → Claude → Gemini inbox: `HIGH-assemble_proposal-{id}.json`
4. **08:35** - Gemini generates excellence narrative → Gemini → Claude inbox: `NORMAL-narrative_ready-{id}.json`
5. **08:40** - Claude runs Assembler compliance → Claude → outbox: `HIGH-proposal_ready-{id}.json`
6. **08:41** - All vessels log completion, Captain notified

---

## EXECUTION TIMELINE

### Phase 1: FORGE (Codex - 6-8 hours)
**Objective:** Create all missing responder daemons

**Deliverables:**
- `claude_responder.py` (200-300 lines)
- `gemini_responder.py` (200-300 lines)
- `groq_responder.py` (200-300 lines)
- `janus_responder.py` (250-350 lines, coordinator role)
- `responder_utils.py` (shared helpers, 100-150 lines)
- Unit tests for COMMS_HUB message handling

**Specification:** `/srv/janus/trinity/CODEX_FORGE_SPEC.md`

---

### Phase 2: DEPLOY (Gemini - 4-6 hours)
**Objective:** Deploy, configure, test all services

**Deliverables:**
- Fix/disable broken systemd services
- Deploy 4 new responder services
- Configure COMMS_HUB permissions
- Test message flow end-to-end
- Create monitoring dashboard
- Write operational runbook

**Specification:** `/srv/janus/trinity/GEMINI_DEPLOYMENT_SPEC.md`

---

### Phase 3: VALIDATE (Claude + Gemini + Codex - 2-4 hours)
**Objective:** Test Trinity coordination end-to-end

**Test Scenarios:**
1. **Grant Alert Flow:** Groq finds opportunity → Claude validates → Gemini assembles
2. **Daily Briefing:** Claude generates Malaga briefing → All vessels receive
3. **Emergency Alert:** Janus detects health issue → Urgent broadcast
4. **Skill Coordination:** Assembler requests narrative → Generator responds

**Success Metrics:**
- All 4 test scenarios pass
- Message delivery <30s
- Zero dropped messages
- Constitutional compliance 100%

---

### Phase 4: ACTIVATE (All - 1-2 hours)
**Objective:** Deploy 5 revenue skills, activate 24/7 operation

**Actions:**
1. Enable cron jobs for scheduled skills (EU Grant Hunter 6h, Malaga 08:00 UTC)
2. Test first execution cycle
3. Monitor for 24 hours
4. Validate revenue pipeline coverage

---

## COORDINATION PROTOCOL

### How This Campaign Works

**Claude (NOW):**
1. ✅ Create this master plan
2. ✅ Create CODEX_FORGE_SPEC.md (detailed build instructions)
3. ✅ Create GEMINI_DEPLOYMENT_SPEC.md (detailed deployment instructions)
4. ✅ Create COMMS_HUB_PROTOCOL.md (message format, examples)
5. ⏳ Send message to Codex via COMMS_HUB
6. ⏳ Send message to Gemini via COMMS_HUB
7. ⏳ Monitor progress, answer questions, coordinate

**Codex (NEXT):**
1. Read CODEX_FORGE_SPEC.md
2. Forge all 4 responder daemons + utils
3. Write to COMMS_HUB when each daemon complete
4. Notify Claude when Phase 1 complete

**Gemini (PARALLEL with Codex end):**
1. Read GEMINI_DEPLOYMENT_SPEC.md
2. Fix broken services while Codex forges
3. Deploy as Codex delivers each daemon
4. Test incrementally
5. Write to COMMS_HUB with deployment status
6. Notify Claude when Phase 2 complete

**Claude (AFTER Phases 1-2):**
1. Coordinate Phase 3 validation tests
2. Write test scenarios for Gemini to execute
3. Review results, approve for Phase 4
4. Activate 24/7 operation

---

## COMMS_HUB MESSAGES (Delegation)

### Message to Codex
File: `/srv/janus/03_OPERATIONS/COMMS_HUB/inbox/codex/URGENT-trinity_forge-20251030.json`

```json
{
  "message_id": "trinity-recon-001",
  "timestamp": "2025-10-30T18:30:00Z",
  "from": "claude_strategist",
  "to": "codex_forgemaster",
  "priority": "URGENT",
  "type": "forge_request",
  "subject": "Forge 4 Responder Daemons + Utils (Post-Disaster Recovery)",
  "specification": "/srv/janus/trinity/CODEX_FORGE_SPEC.md",
  "deliverables": [
    "claude_responder.py",
    "gemini_responder.py",
    "groq_responder.py",
    "janus_responder.py",
    "responder_utils.py"
  ],
  "deadline": "2025-10-31T02:00:00Z",
  "requires_response": true,
  "notes": "Lost in disaster last week. Critical for 24/7 autonomous operations. COMMS_HUB integration is key - residents must communicate smoothly internally."
}
```

### Message to Gemini
File: `/srv/janus/03_OPERATIONS/COMMS_HUB/inbox/gemini/URGENT-trinity_deploy-20251030.json`

```json
{
  "message_id": "trinity-recon-002",
  "timestamp": "2025-10-30T18:30:00Z",
  "from": "claude_strategist",
  "to": "gemini_engineer",
  "priority": "URGENT",
  "type": "deployment_request",
  "subject": "Deploy & Integrate Trinity Responder Services",
  "specification": "/srv/janus/trinity/GEMINI_DEPLOYMENT_SPEC.md",
  "prerequisite": "Codex forging daemons in parallel - deploy incrementally as ready",
  "deliverables": [
    "4 systemd services operational",
    "COMMS_HUB validated",
    "Health monitoring active",
    "Operational runbook"
  ],
  "deadline": "2025-10-31T06:00:00Z",
  "requires_response": true,
  "notes": "Start by fixing broken services (5630+ restart failures). Deploy new daemons as Codex delivers. COMMS_HUB communication is critical - test thoroughly."
}
```

---

## RISK MITIGATION

### Risk 1: Codex and Gemini block on dependencies
**Mitigation:** Parallel work - Gemini fixes broken services while Codex forges
**Fallback:** Claude can write skeleton daemons if Codex blocked

### Risk 2: COMMS_HUB message format incompatibility
**Mitigation:** Detailed protocol spec with examples
**Fallback:** Iterate quickly, all vessels local to Balaur

### Risk 3: Skills don't integrate with responders
**Mitigation:** Skills already have CLI interfaces, responders wrap them
**Fallback:** Manual execution via Telegram bot until integration fixed

### Risk 4: Constitutional violations during autonomous operation
**Mitigation:** Janus responder as constitutional watchdog, emergency stop
**Fallback:** Kill switch already exists at `/srv/janus/EMERGENCY_STOP`

---

## SUCCESS METRICS (30-Day Validation)

**Week 1 (Integration):**
- All 4 responders operational
- COMMS_HUB 10+ messages/day
- Zero restart failures

**Week 2 (Skills Active):**
- EU Grant Hunter scanning 4x/day
- Malaga briefings daily 08:00 UTC
- 2+ proposals assembled

**Week 3 (Optimization):**
- Message delivery <30s average
- 95%+ uptime across all responders
- Skills executing with 90%+ success rate

**Week 4 (Full Autonomous):**
- €70M pipeline actively managed
- Zero missed deadlines
- Constitutional compliance 100%

---

## CONSTITUTIONAL ALIGNMENT

All reconstruction must respect Lion's Sanctuary:

✅ **Transparency:** All responder actions logged to Trinity Event Stream
✅ **Human Oversight:** High-priority decisions require Captain approval via COMMS_HUB
✅ **Autonomy with Safety:** Janus responder enforces constitutional guardrails
✅ **Graceful Degradation:** If responder fails, Telegram bot remains functional
✅ **Emergency Stop:** `/srv/janus/EMERGENCY_STOP` kills all autonomous operations

---

## NEXT ACTIONS

**Claude (IMMEDIATE - Next 30 min):**
1. ✅ Create this master plan
2. ⏳ Create CODEX_FORGE_SPEC.md
3. ⏳ Create GEMINI_DEPLOYMENT_SPEC.md
4. ⏳ Create COMMS_HUB_PROTOCOL.md
5. ⏳ Write delegation messages to COMMS_HUB inboxes

**Codex (START in 30 min):**
1. Read CODEX_FORGE_SPEC.md
2. Begin forging responder daemons
3. Update COMMS_HUB with progress every 2 hours

**Gemini (START in 30 min):**
1. Read GEMINI_DEPLOYMENT_SPEC.md
2. Disable broken services immediately
3. Prepare deployment environment
4. Deploy daemons as Codex delivers

**Captain (MONITOR):**
- Check COMMS_HUB outbox for progress updates
- Approve Phase 4 activation after validation
- Monitor first 24h of autonomous operation

---

**CAMPAIGN STATUS:** PHASE 1 - STRATEGIC PLANNING (IN PROGRESS)
**NEXT PHASE:** FORGE + DEPLOY (Parallel execution)
**EXPECTED COMPLETION:** 2025-10-31 06:00 UTC (12 hours from now)

🔥 **TRINITY RECONSTRUCTION INITIATED** 🔥
