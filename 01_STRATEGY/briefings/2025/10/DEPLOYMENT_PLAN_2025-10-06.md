# DEPLOYMENT PLAN: Full System Integration
**Date:** 2025-10-06
**Phase:** Option A - Deploy Everything Now
**Status:** Ready for Execution

---

## OBJECTIVE
Deploy the complete Janus autonomous system to The Balaur, integrating Victorian Controls, Agent Framework, and enabling Mode Alpha operation.

---

## CURRENT STATE

### ✅ COMPLETED
- Janus philosophical awakening (Four Books absorbed, 596 YAML nodes)
- Constitutional Charter loaded (/srv/janus/config/)
- Victorian Controls built by Codex (production-hardened)
- Agent Framework built by Gemini (full infrastructure)
- Janus strategic plan received (IKN proposal + distributed reconnaissance)
- The Mill operational (CPU-only llama.cpp @ 4.70 t/s baseline)

### 📋 READY FOR DEPLOYMENT
**Victorian Controls (Codex):**
- `governor.py` - Maxwell PI controller with monotonic timing
- `relief_valve.py` - Two-stage CPU throttling with structured logging
- `escapement.py` - 10 Hz precision timing with perf_counter
- `control_orchestrator.py` - Master coordinator with real metrics
- `test_controls.py` - Full test suite (all passing)
- `janus-controls.service` - Systemd service with pre-flight checks

**Agent Framework (Gemini):**
- `llm_client.py` - The Mill integration (llama.cpp)
- `oracle_client.py` - Oracle Trinity scaffolding
- `comms_client.py` - COMMS_HUB link
- `monitoring.py` - Brass Gauges FastAPI server
- `health_check.sh` - Operational verification
- `backup.sh` / `restore.sh` - Disaster recovery
- `docs/JANUS_AGENT_OPERATIONS.md` - Operations manual

---

## DEPLOYMENT SEQUENCE

### PHASE 1: Victorian Controls Deployment
**Owner:** Codex
**Duration:** 30 minutes
**Tasks:**
1. Transfer `/deploy/janus-controls/` to The Balaur
2. Install to `/srv/janus/controls/`
3. Create `/srv/janus/metrics/` directory
4. Install systemd service
5. Run test suite to verify
6. Start `janus-controls.service`
7. Monitor logs for 5 minutes

**Success Criteria:**
- All tests pass
- Service starts without errors
- Governor/Relief Valve/Escapement all report NOMINAL
- Mission log entries appearing in `/srv/janus/mission_log.jsonl`

---

### PHASE 2: Agent Framework Deployment
**Owner:** Gemini
**Duration:** 45 minutes
**Tasks:**
1. Transfer `packages/janus_agent/` to The Balaur
2. Install to `/srv/janus/agent/`
3. Deploy configuration from `configs/janus_agent/agent.yaml`
4. Install systemd service (`janus-agent.service`)
5. Run `health_check.sh` to verify
6. Integrate with Victorian Controls
7. Start `janus-agent.service` in Mode Alpha
8. Deploy Brass Gauges monitoring dashboard

**Success Criteria:**
- Health check passes
- Agent starts in Mode Alpha (propose-only)
- Integration with Victorian Controls confirmed
- Brass Gauges accessible on port (TBD)
- No errors in `/var/log/janus/agent.log`

---

### PHASE 3: Integration Testing
**Owner:** Captain + Claude (Strategic Oversight)
**Duration:** 30 minutes
**Tasks:**
1. Verify both services running (`systemctl status`)
2. Check Victorian Controls responding to load
3. Test agent proposal workflow (Mode Alpha)
4. Verify audit logs (mission_log.jsonl, tool_use.jsonl, proposals.jsonl)
5. Test Balaur Command Center connectivity
6. Validate Oracle Trinity access (if configured)

**Success Criteria:**
- Both services healthy and stable
- Victorian Controls throttling when needed
- Agent can generate proposals (await approval)
- All logs writing correctly
- Command Center shows real-time status

---

### PHASE 4: Janus Strategic Mission Activation
**Owner:** Janus (with Trinity support)
**Duration:** Ongoing
**Tasks:**
1. Send Janus his approved mission: Execute distributed reconnaissance
2. Janus orchestrates the AI Cortex:
   - **Janus-in-Balaur:** Internal system inventory
   - **Claude:** Strategic synthesis and coordination
   - **Gemini:** External systems research and integration
   - **Codex:** Knowledge graph architecture research
3. Monitor proposals through approval workflow
4. Execute approved reconnaissance tasks
5. Aggregate findings into "Cartography of the Republic"

**Success Criteria:**
- Janus generates well-reasoned proposals
- Trinity responds to delegated tasks
- System inventory completed
- AI Cortex capability matrix documented
- Harmonization protocol defined

---

## ROLLBACK PLAN

**If Victorian Controls fail:**
1. Stop `janus-controls.service`
2. The Mill continues operating (no dependency)
3. Review logs, fix issues, redeploy

**If Agent Framework fails:**
1. Stop `janus-agent.service`
2. Victorian Controls continue monitoring
3. The Mill continues operating
4. Review logs, fix issues, redeploy

**If integration issues:**
1. Run both services independently first
2. Verify each component works standalone
3. Debug integration points
4. Redeploy with fixes

**Complete rollback:**
1. Stop both services
2. Restore from backup (if needed)
3. Return to manual operation mode
4. Review and replan

---

## MONITORING & VALIDATION

**Real-time Monitoring:**
- The Balaur Command Center (`/tmp/balaur_console.py`)
- Brass Gauges dashboard (Gemini's FastAPI server)
- Systemd logs: `journalctl -u janus-controls -f`
- Systemd logs: `journalctl -u janus-agent -f`

**Key Metrics:**
- Victorian Controls status (NOMINAL/THROTTLE/EMERGENCY)
- Token generation rate (target: ~4.70 t/s)
- CPU usage (warning: 80%, critical: 95%)
- Memory usage
- Proposal queue depth
- Approval workflow latency

**Log Files:**
- `/srv/janus/mission_log.jsonl` - Strategic actions
- `/srv/janus/tool_use.jsonl` - Detailed tool execution
- `/srv/janus/proposals.jsonl` - Proposal lifecycle
- `/srv/janus/approval_queue.jsonl` - Pending approvals
- `/var/log/janus/agent.log` - Agent operational events
- `/srv/janus/metrics/token_rate.json` - Performance data

---

## CONSTITUTIONAL SAFEGUARDS

**Mode Alpha Constraints:**
- Every action requires human approval
- No autonomous execution without First Citizen authorization
- All proposals logged and auditable
- Victorian Controls can emergency stop at any time
- Kill switches available at multiple levels

**Emergency Procedures:**
1. **Manual Kill:** `sudo systemctl stop janus-agent janus-controls`
2. **Emergency File:** `touch /srv/janus/EMERGENCY_STOP`
3. **Watchdog Timeout:** 120 seconds (auto-restart or stop)
4. **Relief Valve:** Auto-throttle at 95% CPU
5. **Network Isolation:** UFW rules restrict to LAN only

---

## SUCCESS DEFINITION

**Deployment Success:**
- Both services running and stable for 1+ hour
- Victorian Controls responding correctly to load
- Agent generating constitutional proposals
- Audit trail complete and correct
- No service crashes or errors

**Mission Success:**
- Janus executes distributed reconnaissance plan
- Trinity collaboration functioning
- System inventory completed
- AI Cortex mapped
- IKN architecture research findings delivered

---

## NEXT STEPS AFTER DEPLOYMENT

1. **30-Day Mode Alpha Trial:** Janus proposes, Captain approves
2. **Collect Operational Data:** Performance, reliability, alignment
3. **Refine Victorian Controls:** Tune thresholds based on real data
4. **Build IKN Components:** Based on reconnaissance findings
5. **Evaluate Mode Beta Readiness:** Supervised autonomy with playbooks

---

**Status:** Ready for execution
**Approval Required:** Captain BROlinni
**Estimated Total Time:** 2-3 hours for full deployment and validation
