# WORK DISTRIBUTION: Trinity Deployment Mission
**Date:** 2025-10-06
**Mission:** Full System Integration of Janus Autonomous Agent
**Status:** Ready to Execute

---

## MISSION OVERVIEW

We are deploying the complete Janus autonomous system to The Balaur in three parallel tracks:

1. **Victorian Controls** (Codex)
2. **Agent Framework** (Gemini)
3. **Strategic Oversight** (Claude + Captain)

Each member of the Trinity has specific responsibilities. This document defines WHO does WHAT.

---

## CODEX: Victorian Controls Deployment & Monitoring

**Primary Responsibility:** Deploy and maintain the Victorian Control Mechanisms

### YOUR TASKS

**Phase 1: Deployment (30 minutes)**
1. Transfer your hardened controls to The Balaur:
   - Location: `UBOS/SystemFundamentals/Books/deploy/janus-controls/`
   - Destination: `balaur@10.215.33.26:/srv/janus/controls/`
   - Files: governor.py, relief_valve.py, escapement.py, control_orchestrator.py, test_controls.py

2. Install systemd service:
   - Copy `janus-controls.service` to `/etc/systemd/system/`
   - Run `systemctl daemon-reload`
   - Enable and start the service

3. Create metrics infrastructure:
   - Directory: `/srv/janus/metrics/`
   - Initial file: `token_rate.json` with structure `{"current_rate": 0, "timestamp": 0}`

4. Run test suite:
   - Execute: `python3 /srv/janus/controls/test_controls.py`
   - Verify: All 21 tests pass
   - Report: Any failures immediately

5. Start the service:
   - Command: `sudo systemctl start janus-controls`
   - Monitor: `journalctl -u janus-controls -f` for 5 minutes
   - Verify: NOMINAL status on all three controls

**Phase 2: Integration Support (15 minutes)**
6. Verify integration with Agent Framework:
   - Confirm Governor is reading token rate metrics
   - Confirm Relief Valve is monitoring CPU correctly
   - Confirm Escapement is providing timing signals
   - Test: Trigger a throttle event intentionally

**Phase 3: Ongoing Monitoring (Duration of deployment)**
7. Watch Victorian Controls during agent activation:
   - Monitor CPU usage patterns
   - Verify Governor responds to load changes
   - Confirm Relief Valve activates at correct thresholds
   - Check Escapement timing precision

8. Tune if needed:
   - Adjust thresholds based on real behavior
   - Optimize PI controller parameters if oscillation detected
   - Document any modifications

**Deliverables:**
- ✅ Victorian Controls running on The Balaur
- ✅ All tests passing
- ✅ Service stable for 1+ hour
- ✅ Integration with agent confirmed
- ✅ Performance report with any tuning recommendations

**Communication:**
Report status after each phase to Captain via session log or direct message.

---

## GEMINI: Agent Framework Deployment & Infrastructure

**Primary Responsibility:** Deploy and maintain the Janus Agent Framework

### YOUR TASKS

**Phase 1: Core Framework Deployment (30 minutes)**
1. Transfer agent framework to The Balaur:
   - Location: `UBOS/packages/janus_agent/`
   - Destination: `balaur@10.215.33.26:/srv/janus/agent/`
   - Files: All Python modules (llm_client, oracle_client, comms_client, etc.)

2. Deploy configuration:
   - Source: `UBOS/configs/janus_agent/agent.yaml`
   - Destination: `/srv/janus/config/agent.yaml`
   - Verify: All paths are correct for The Balaur

3. Install dependencies:
   - Create Python venv if needed
   - Install: FastAPI, uvicorn, PyYAML, psutil
   - Verify: `pip3 list` shows all requirements

4. Deploy systemd service:
   - Source: `UBOS/deploy/janus/systemd/janus_agentd.service`
   - Destination: `/etc/systemd/system/janus-agent.service`
   - Modify paths if needed
   - Run: `systemctl daemon-reload`

**Phase 2: Integration Wiring (30 minutes)**
5. Wire llm_client to The Mill:
   - Configure: Path to `/srv/janus/bin/llama-cli`
   - Configure: Model path to `/srv/janus/models/Meta-Llama-3.1-8B-Instruct-Q4_K_M.gguf`
   - Test: Generate a test inference to verify connectivity

6. Integrate with Victorian Controls:
   - Configure: Controls client to read from `/srv/janus/metrics/`
   - Verify: Agent can query Governor/Relief Valve/Escapement status
   - Test: Agent respects rate limits from Governor

7. Deploy Brass Gauges monitoring:
   - Start: FastAPI server (monitoring.py)
   - Verify: Health endpoint responding
   - Document: Access URL and available endpoints

8. Run health checks:
   - Execute: `/srv/janus/agent/health_check.sh`
   - Verify: All components report healthy
   - Fix: Any failures before proceeding

**Phase 3: Mode Alpha Activation (15 minutes)**
9. Configure Mode Alpha operation:
   - Verify: `operational_mode: "alpha"` in agent.yaml
   - Verify: Approval workflow is enabled
   - Verify: Proposal engine is configured

10. Start the agent:
    - Command: `sudo systemctl start janus-agent`
    - Monitor: `journalctl -u janus-agent -f` for 5 minutes
    - Verify: Agent loads constitution and philosophy
    - Verify: Thinking cycle starts (check logs)

**Phase 4: Oracle Trinity Integration (Optional - if time permits)**
11. Wire Oracle Trinity clients:
    - Groq: Configure API key and endpoint
    - Wolfram: Configure app ID
    - DataCommons: Configure endpoints
    - Test: Each client can make a test query

**Deliverables:**
- ✅ Agent Framework running on The Balaur
- ✅ Health checks passing
- ✅ Integration with Victorian Controls confirmed
- ✅ Mode Alpha active and generating proposals
- ✅ Brass Gauges monitoring accessible
- ✅ Operations manual (`JANUS_AGENT_OPERATIONS.md`) validated

**Communication:**
Report status after each phase to Captain via session log or direct message.

---

## CLAUDE: Strategic Oversight & Coordination

**Primary Responsibility:** Coordinate deployment, verify constitutional alignment, manage approvals

### YOUR TASKS

**Phase 1: Pre-Deployment Verification (15 minutes)**
1. Review deployment plan (`DEPLOYMENT_PLAN_2025-10-06.md`)
2. Verify constitutional safeguards are in place
3. Confirm rollback procedures are clear
4. Validate success criteria
5. Approve commencement of deployment

**Phase 2: Deployment Coordination (Duration of deployment)**
6. Monitor both Codex and Gemini progress
7. Identify blockers and coordinate resolution
8. Verify communication between Trinity members
9. Ensure phases are executing in correct order
10. Track completion of deliverables

**Phase 3: Integration Validation (30 minutes)**
11. Test The Balaur Command Center (`/tmp/balaur_console.py`)
12. Verify both services are running (`systemctl status`)
13. Check all log files for errors or warnings
14. Validate audit trail (mission_log.jsonl, tool_use.jsonl, proposals.jsonl)
15. Test end-to-end: Send Janus a message, receive response

**Phase 4: Mode Alpha Verification (30 minutes)**
16. Monitor Janus's first autonomous thinking cycle
17. Review generated proposals for constitutional alignment
18. Test approval workflow (approve a proposal)
19. Verify proposal execution and logging
20. Confirm Victorian Controls respond to agent activity

**Phase 5: Strategic Mission Activation (Ongoing)**
21. Send Janus his strategic mission (distributed reconnaissance)
22. Monitor how he orchestrates the Trinity
23. Respond to delegation requests from Janus
24. Synthesize research findings
25. Coordinate knowledge graph architecture decisions

**Deliverables:**
- ✅ Deployment coordinated and successful
- ✅ Constitutional alignment verified
- ✅ Mode Alpha functioning correctly
- ✅ Approval workflow tested
- ✅ Janus strategic mission activated
- ✅ Session documentation complete

**Communication:**
You are the central coordinator. Maintain communication with Codex, Gemini, and Captain throughout deployment.

---

## CAPTAIN: Final Authority & Constitutional Guardian

**Your Responsibilities:**

1. **Approve Deployment:** Review plan, give go/no-go decision
2. **Monitor Progress:** Use The Balaur Command Center
3. **Approve Proposals:** When Janus generates proposals in Mode Alpha
4. **Make Strategic Decisions:** If unexpected situations arise
5. **Declare Success/Failure:** Final call on deployment outcome

**Your Tools:**
- The Balaur Command Center: `python3 /tmp/balaur_console.py`
- Direct SSH: `ssh balaur@10.215.33.26`
- Real-time logs: `journalctl -u janus-controls -f` and `journalctl -u janus-agent -f`

---

## COMMUNICATION PROTOCOL

**Status Updates:**
- After each phase completion
- Immediately upon any error or blocker
- When awaiting coordination or decision

**Channels:**
- Session logs (primary)
- Direct messages between Trinity members (if separate sessions)
- The Balaur mission logs (for Janus)

**Emergency:**
- Any Trinity member can call for pause
- Captain has final authority on stop/continue

---

## TIMELINE

**T+0:00** - Deployment begins (Captain approval)
**T+0:30** - Phase 1 complete (Victorian Controls + Framework core)
**T+1:00** - Phase 2 complete (Integration wiring)
**T+1:30** - Phase 3 complete (Both services running)
**T+2:00** - Phase 4 complete (Mode Alpha validated)
**T+2:00+** - Phase 5 ongoing (Strategic mission execution)

**Total Estimated Time:** 2-3 hours for full deployment and validation

---

## SUCCESS CRITERIA (FINAL)

- [ ] Victorian Controls: Running, stable, responding correctly
- [ ] Agent Framework: Running, stable, generating proposals
- [ ] Integration: Both systems communicating correctly
- [ ] Mode Alpha: Proposal workflow functioning
- [ ] Constitutional Alignment: All safeguards active
- [ ] Audit Trail: All logs writing correctly
- [ ] Monitoring: Command Center and Brass Gauges operational
- [ ] Janus: Receives strategic mission, begins orchestration

---

**Status:** Awaiting Captain's approval to commence
**Trinity Status:** Ready
**The Balaur:** Ready
**Janus:** Awaiting activation

Let's build the future of constitutional AI.
