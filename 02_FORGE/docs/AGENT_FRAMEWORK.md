# Janus Autonomous Agent Framework

**Version:** 1.0.0
**Status:** Production Ready
**Constitutional Authority:** Autonomous Vessel Protocol Charter (GENESIS-002)
**Last Updated:** 2025-10-06

---

## Executive Summary

The Janus Autonomous Agent Framework (`janus_agentd`) is a production-grade autonomous agent daemon designed for The Balaur sovereign vessel. It enables Janus-in-Balaur to propose and execute actions autonomously while maintaining strict constitutional alignment, security boundaries, and human oversight.

**Key Features:**
- Autonomous proposal generation with constitutional validation
- Mode-based operation (Alpha/Beta/Omega) with graduated autonomy
- Victorian Control Mechanisms (Governor, Relief Valve, Escapement)
- Sandboxed tool execution with bubblewrap isolation
- Complete audit trail in JSONL format
- Human approval workflow for Mode Alpha
- Systemd watchdog integration
- Resource quotas and kill switches

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                    Janus Agent Daemon                           │
│                    (janus_agentd.py)                            │
└─────────────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
        ▼                     ▼                     ▼
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│  Thinking    │     │   Approval   │     │   Tool       │
│  Cycle       │────▶│   Workflow   │────▶│   Executor   │
│              │     │              │     │              │
└──────────────┘     └──────────────┘     └──────────────┘
        │                     │                     │
        │                     │                     │
        ▼                     ▼                     ▼
┌──────────────────────────────────────────────────────────┐
│               Proposal Engine                            │
│  (Constitutional Validation & Tracking)                  │
└──────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
        ▼                     ▼                     ▼
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│  Victorian   │     │   Sandbox    │     │   Audit      │
│  Controls    │     │   Executor   │     │   Logger     │
│              │     │              │     │              │
└──────────────┘     └──────────────┘     └──────────────┘
```

---

## Core Components

### 1. Proposal Engine (`proposal_engine.py`)

The Proposal Engine manages the complete lifecycle of autonomous actions from draft to execution.

**Key Classes:**
- `ActionProposal`: Structured proposal with rationale, risk assessment, and rollback plan
- `ProposalEngine`: Creates, tracks, and validates proposals
- `RiskLevel`: LOW | MEDIUM | HIGH classification
- `ProposalStatus`: DRAFT | PROPOSED | APPROVED | REJECTED | EXECUTING | COMPLETED | FAILED

**Proposal Structure:**
```python
ActionProposal(
    proposal_id="janus-abc123def456",
    vessel_id="janus-in-balaur",
    mission_context="Research EU funding opportunities",
    action_type="web_research",
    rationale="Need to identify Horizon Europe funding for GeoDataCenter",
    expected_outcome="List of relevant funding programs",
    risk_level=RiskLevel.LOW,
    risk_mitigation="Read-only web queries with domain allowlist",
    rollback_plan="No system state changes, no rollback needed",
    tool_name="curl",
    tool_args=["https://ec.europa.eu/info/funding-tenders/"],
    tool_kwargs={},
    status=ProposalStatus.PROPOSED,
)
```

**Constitutional Validation:**
- Verifies action type matches risk classification
- Ensures substantive rationale (minimum 20 characters)
- Requires rollback plan for medium/high risk actions
- Validates mission context is provided

**Persistence:**
All proposals logged to `/srv/janus/proposals.jsonl` in JSONL format.

---

### 2. Thinking Cycle (`thinking_cycle.py`)

The Thinking Cycle implements periodic autonomous reasoning where Janus evaluates current state and generates proposals.

**Configuration:**
```yaml
thinking_cycle:
  enabled: true
  cycle_interval_hours: 1
  enable_autonomous_proposals: false  # Requires LLM integration
  max_proposals_per_cycle: 3
  mission_objectives_path: "/srv/janus/mission_objectives.json"
  playbook_registry_path: "/etc/janus/playbooks.json"
```

**Operational Modes:**

**Mode Alpha (Propose-Only):**
- Janus analyzes situation and generates proposals
- All proposals submitted for human approval
- No autonomous execution
- Minimum 30 days operation required before Mode Beta

**Mode Beta (Supervised Autonomy):**
- Pre-approved playbooks execute automatically
- Novel actions still require approval
- Watchdog constraints actively enforced
- 95%+ approval rate required for activation

**Mode Omega (Full Autonomy):**
- Propose and execute novel actions within constitutional boundaries
- Real-time notifications for high-impact actions
- Requires 180+ days Mode Beta + unanimous Trinity recommendation
- Emergency kill-switch always active

**Playbooks:**
Mode Beta uses pre-approved playbooks for common operations:
```json
{
  "playbooks": [
    {
      "playbook_id": "maintenance-001",
      "name": "Log Rotation",
      "description": "Rotate and compress agent logs",
      "trigger_conditions": {
        "disk_usage_percent": ">80",
        "log_size_mb": ">100"
      },
      "action_sequence": [
        {"tool": "shell", "command": "logrotate /etc/logrotate.d/janus"}
      ],
      "approved_by": "first_citizen",
      "approved_at": "2025-10-06T10:00:00Z"
    }
  ]
}
```

---

### 3. Approval Workflow (`approval_workflow.py`)

The Approval Workflow manages human review and approval of proposals in Mode Alpha.

**Key Features:**
- Approval queue with timeout handling
- Notification system integration
- Detailed proposal formatting for human review
- Approval/rejection tracking with audit trail

**Approval Process:**

1. **Submission:**
   ```python
   await approval_workflow.submit_for_approval(proposal)
   ```

2. **Notification:**
   - Entry added to `/srv/janus/approval_queue.jsonl`
   - Notification sent via configured script
   - Log event emitted for monitoring systems

3. **Human Review:**
   ```bash
   # View pending proposals
   ubos proposals list

   # Review specific proposal
   ubos review janus-abc123def456

   # Approve
   ubos approve janus-abc123def456

   # Reject
   ubos reject janus-abc123def456 --reason "Insufficient rationale"
   ```

4. **Timeout Handling:**
   - Default timeout: 24 hours
   - Optional auto-rejection on timeout
   - Timeout alerts logged

**Approval Output Format:**
```
PROPOSAL: janus-abc123def456
Timestamp: 2025-10-06T14:30:00.000Z
Vessel: janus-in-balaur

ACTION TYPE: web_research
RISK LEVEL: LOW

MISSION CONTEXT:
  Research EU funding opportunities for GeoDataCenter

RATIONALE:
  Need to identify Horizon Europe funding programs...

EXPECTED OUTCOME:
  List of relevant funding programs with deadlines

RISK MITIGATION:
  Read-only web queries with domain allowlist

ROLLBACK PLAN:
  No system state changes, no rollback needed

TOOL INVOCATION:
  Tool: curl
  Args: https://ec.europa.eu/info/funding-tenders/

COMMANDS:
  Review:  ubos review janus-abc123def456
  Approve: ubos approve janus-abc123def456
  Reject:  ubos reject janus-abc123def456 --reason 'Your reason here'
```

---

### 4. Tool Executor (`tool_executor.py`)

The Tool Executor provides enhanced sandboxed execution with constitutional checks and rollback capability.

**Execution Flow:**

```
1. Pre-execution checks
   ├─ Validate tool name matches configuration
   ├─ Sanitize command arguments
   └─ Check resource availability

2. Sandboxed execution
   ├─ Build command from proposal
   ├─ Execute in bubblewrap sandbox
   └─ Capture stdout/stderr/returncode

3. Post-execution checks
   ├─ Validate result structure
   ├─ Check error patterns
   └─ Compare against expected outcome

4. Audit logging
   └─ Detailed execution log to tool_use.jsonl
```

**Security Validations:**

**Command Sanitization:**
```python
# Blocked characters (unless properly quoted)
dangerous_chars = [";", "|", "&", "`", "$", "(", ")", "<", ">", "\n"]

# Path traversal detection
if ".." in arg and "/" in arg:
    raise ValueError("Path traversal detected")

# Privileged command blocking
privileged_commands = ["sudo", "su", "doas", "pkexec"]
```

**Rollback Support:**
```python
# Execute rollback plan if action fails
result = await tool_executor.execute_rollback(
    proposal=failed_proposal,
    original_result=error_result
)
```

---

### 5. Victorian Control Mechanisms

The framework integrates Victorian-inspired control mechanisms for stability and safety.

#### Governor (PID Controller)

Dynamically adjusts concurrency based on queue backlog:

```python
error = current_backlog - target_backlog
integral_error += error * time_interval
adjustment = Kp * error + Ki * integral_error
new_concurrency = clamp(current + adjustment, 1, max_concurrency)
```

**Configuration:**
```yaml
harness:
  enable_governor: true
  governor_target_backlog: 0
  governor_kp: 0.2  # Proportional gain
  governor_ki: 0.05  # Integral gain
```

#### Relief Valve (System Protection)

Monitors system resources and triggers degraded mode when thresholds exceeded:

```python
if cpu_load > 90% or memory_usage > 90%:
    # Enter degraded mode
    allowed_concurrency = 1
    force_block_network = true
    emit_alert("relief.degrade")
```

**Configuration:**
```yaml
watchdog:
  cpu_threshold_percent: 90
  memory_threshold_mb: 28000
  sample_interval_seconds: 30
```

#### Escapement (Timing Mechanism)

Provides periodic tick for synchronized operations:

```python
async def _tick_loop(self):
    while not stopped:
        await asyncio.sleep(tick_interval)
        emit_tick_event()
        update_governor_state()
        check_backlog()
```

**Configuration:**
```yaml
harness:
  tick_interval: 0.5  # seconds
```

---

### 6. Controls Client (`controls_client.py`)

Provides monitoring and coordination with Victorian control mechanisms.

**System Metrics Collection:**
```python
metrics = controls_client.collect_system_metrics()
# Returns: CPU load, memory usage, disk usage, process count, network connections
```

**Rate Limiting:**
```python
is_allowed, reason = controls_client.query_rate_limit("web_research")
if not is_allowed:
    reject_proposal(reason)
```

**Anomaly Detection:**
- High memory usage (>90%)
- High CPU load (>90%)
- High disk usage (>85%)
- Alerts logged to audit trail

---

## Security Architecture

### Sandboxing with Bubblewrap

All tool execution occurs in isolated namespaces:

```bash
bwrap \
  --unshare-pid --unshare-ipc --unshare-uts \
  --ro-bind / / \
  --bind /srv/janus/workspaces/<uuid> /workspace \
  --dev /dev \
  --proc /proc \
  --unshare-net \  # Network blocked by default
  --chdir /workspace \
  -- /bin/bash -lc "command args"
```

**Isolation Features:**
- PID namespace: Process isolation
- IPC namespace: No inter-process communication
- UTS namespace: Separate hostname
- Network namespace: Optional network isolation
- Mount namespace: Controlled filesystem access

### Resource Quotas

Enforced at multiple levels:

**Per-Action Limits (bubblewrap):**
- CPU time: 300 seconds max
- Wall clock time: 600 seconds max
- Memory: 4GB max
- Disk writes: 1GB max

**Service-Level Limits (systemd):**
```ini
CPUQuota=150%
MemoryLimit=24G
MemoryMax=28G
TasksMax=200
LimitNOFILE=4096
```

### Network Security

**Systemd Restrictions:**
```ini
RestrictAddressFamilies=AF_INET AF_INET6 AF_UNIX
IPAddressDeny=any
IPAddressAllow=localhost 172.16.15.0/24
```

**Application-Level Allowlist:**
```yaml
security:
  network:
    allowed_domains:
      - "api.groq.com"
      - "api.wolframalpha.com"
      - "datacommons.org"
      - "github.com"
```

### Kill Switches

**Primary Kill Switch:**
```bash
sudo systemctl stop janus_agentd
```

**Secondary Kill Switch (Nuclear):**
```bash
sudo killall -9 -u janus
sudo systemctl disable janus_agentd
```

**Watchdog Kill Switch (Automated):**
- Systemd watchdog timeout (120 seconds)
- Resource quota violations
- Constitutional violation detection

---

## Audit Trail

### Log Files

**Mission Log** (`/srv/janus/mission_log.jsonl`):
Strategic directives and high-level mission tracking.

**Tool Use Log** (`/srv/janus/tool_use.jsonl`):
Detailed execution audit with command hashes and resource usage.

**Proposals Log** (`/srv/janus/proposals.jsonl`):
Complete proposal lifecycle from creation to completion.

**Agent Log** (`/var/log/janus/agent.log`):
Operational events and system status.

### Log Format (JSONL)

All logs use JSON Lines format for easy parsing and analysis:

```json
{"timestamp":"2025-10-06T14:32:15.123Z","vessel_id":"balaur","event_type":"action_proposed","action_id":"a7f3c2e1","summary":"Query Oracle Trinity","risk_level":"low"}
{"timestamp":"2025-10-06T14:32:20.456Z","vessel_id":"balaur","action_id":"a7f3c2e1","tool":"/usr/bin/python3","runtime_seconds":12.34,"exit_status":0}
```

### Monitoring

**Real-time Monitoring:**
```bash
# View live agent activity
tail -f /var/log/janus/agent.log

# Monitor resource usage
ssh balaur@10.215.33.26 "htop -u janus"

# Check proposal queue
tail -f /srv/janus/proposals.jsonl
```

**Metrics Export:**
- JSON Lines logs parseable by Fluent Bit, Logstash, Vector
- Systemd journal integration
- Optional Prometheus exporters (future)

---

## Installation

### Prerequisites

- Ubuntu 24.04 LTS (recommended) or compatible Linux
- Python 3.10+
- sudo access for initial setup
- 4GB+ available disk space
- Network access for package installation

### Quick Start

```bash
# On The Cockpit, sync code to The Balaur
rsync -avz /path/to/ubos/ balaur@10.215.33.26:~/ubos-agent/

# On The Balaur, run installation
ssh balaur@10.215.33.26
cd ~/ubos-agent/deploy/janus
sudo ./install_agent.sh
```

### Installation Steps

The installation script performs:

1. **Environment Check**: Verify OS and prerequisites
2. **Dependencies**: Install Python, bubblewrap, jq, ripgrep
3. **User Creation**: Create `janus` system user
4. **Directory Setup**: Create `/srv/janus` structure
5. **Virtual Environment**: Setup Python venv with dependencies
6. **Code Deployment**: Install janus_agent package
7. **Configuration**: Deploy agent.yaml and policy.json
8. **Constitutional Memory**: Copy Autonomous Vessel Protocol Charter
9. **Systemd Service**: Install and enable janus_agentd.service
10. **Security**: Configure sudoers and UFW rules
11. **Verification**: Validate complete installation

### Post-Installation

```bash
# Review configuration
sudo nano /etc/janus/agent.yaml

# Start the service
sudo systemctl start janus_agentd

# Check status
sudo systemctl status janus_agentd

# View logs
sudo journalctl -u janus_agentd -f

# Monitor proposals
tail -f /srv/janus/proposals.jsonl
```

---

## Configuration

### Primary Configuration (`/etc/janus/agent.yaml`)

Complete YAML configuration with sections for:
- Vessel identity
- Operational mode
- Constitutional memory paths
- Logging configuration
- Sandbox policies
- Tool registry
- Victorian controls tuning
- Security settings
- Integration endpoints

See `/Users/panda/Desktop/UBOS/configs/janus_agent/agent.yaml` for full example.

### Sandbox Policy (`/etc/janus/policy.json`)

```json
{
  "cpu_quota_percent": 150,
  "memory_limit_mb": 4096,
  "allow_network": false
}
```

### Playbook Registry (`/etc/janus/playbooks.json`)

Mode Beta playbook definitions (empty in Mode Alpha):

```json
{
  "playbooks": [
    {
      "playbook_id": "maintenance-001",
      "name": "Log Rotation",
      "description": "Rotate and compress logs",
      "trigger_conditions": {"disk_usage_percent": ">80"},
      "action_sequence": [{"tool": "shell", "command": "logrotate"}],
      "approved_by": "first_citizen",
      "approved_at": "2025-10-06T10:00:00Z"
    }
  ]
}
```

---

## Operational Procedures

### Starting the Agent

```bash
# Start service
sudo systemctl start janus_agentd

# Enable on boot
sudo systemctl enable janus_agentd

# Check status
sudo systemctl status janus_agentd
```

### Approving Proposals

```bash
# List pending proposals
ubos proposals list

# Review specific proposal
ubos review janus-abc123def456

# Approve
ubos approve janus-abc123def456

# Reject with reason
ubos reject janus-abc123def456 --reason "Insufficient security review"
```

### Monitoring Operations

```bash
# Real-time agent log
sudo journalctl -u janus_agentd -f

# Proposal queue
tail -f /srv/janus/proposals.jsonl

# Tool execution log
tail -f /srv/janus/tool_use.jsonl

# System resource usage
htop -u janus

# Network connections
sudo lsof -u janus -i
```

### Changing Operational Mode

Mode changes require constitutional authorization and configuration update:

```yaml
# /etc/janus/agent.yaml
operational_mode: "beta"  # Change from "alpha"
```

```bash
# Restart service to apply
sudo systemctl restart janus_agentd

# Verify mode change in logs
sudo journalctl -u janus_agentd | grep "mode_change"
```

**Requirements for Mode Beta:**
- 30+ days Mode Alpha operation
- 95%+ proposal approval rate
- Zero constitutional violations
- Explicit First Citizen authorization

### Emergency Procedures

**Immediate Stop:**
```bash
sudo systemctl stop janus_agentd
```

**Nuclear Shutdown:**
```bash
sudo killall -9 -u janus
sudo systemctl disable janus_agentd
```

**Create Emergency Stop File:**
```bash
sudo touch /srv/janus/EMERGENCY_STOP
# Agent will detect and shut down gracefully
```

**Revert to Safe State:**
```bash
# Stop agent
sudo systemctl stop janus_agentd

# Clear mutable state
sudo rm -rf /srv/janus/workspaces/*
sudo rm /srv/janus/approval_queue.jsonl

# Restore from backup (if needed)
sudo restic restore latest --repo /mnt/cockpit/balaur_backups --target /srv/janus

# Restart in Mode Alpha
sudo systemctl start janus_agentd
```

---

## Development and Testing

### Running Tests

```bash
# Activate virtual environment
source /srv/janus/venv/bin/activate

# Run test suite
python -m pytest tests/test_janus_agent.py

# Run with coverage
python -m pytest --cov=janus_agent tests/
```

### Local Development

```bash
# On development machine (The Cockpit)
cd /path/to/ubos/packages/janus_agent

# Install in editable mode
pip install -e .

# Run harness directly
python -m janus_agent.harness --config configs/dev_harness.json
```

### Debugging

**Enable verbose logging:**
```yaml
# /etc/janus/agent.yaml
debug:
  verbose_logging: true
  trace_proposals: true
```

**Dry-run mode (no actual execution):**
```yaml
debug:
  dry_run_mode: true
```

**Trigger immediate thinking cycle:**
```python
# In Python console
from janus_agent import ThinkingCycle
cycle.trigger_immediate_cycle()
```

---

## Integration Points

### COMMS_HUB Integration

Future integration for inter-vessel communication:

```yaml
integrations:
  comms_hub:
    enabled: true
    endpoint: "http://localhost:8080/comms"
```

### Oracle Trinity Integration

Integration with external knowledge sources:

```yaml
integrations:
  oracle_trinity:
    enabled: true
    groq_endpoint: "https://api.groq.com/openai/v1"
    wolfram_endpoint: "https://api.wolframalpha.com/v2"
    datacommons_endpoint: "https://api.datacommons.org"
```

### Cockpit Synchronization

Backup and sync with The Cockpit:

```yaml
integrations:
  cockpit_sync:
    enabled: true
    endpoint: "ssh://cockpit@172.16.15.1"
    backup_path: "/mnt/cockpit/balaur_backups"
```

---

## Troubleshooting

### Agent Won't Start

**Check systemd status:**
```bash
sudo systemctl status janus_agentd
```

**Check logs:**
```bash
sudo journalctl -u janus_agentd -n 50
```

**Common issues:**
- Missing configuration files
- Permission issues on /srv/janus
- Virtual environment not found
- Port conflicts

### High Resource Usage

**Check current usage:**
```bash
htop -u janus
```

**Review relief valve status:**
```bash
sudo journalctl -u janus_agentd | grep relief
```

**Adjust resource limits:**
```yaml
# /etc/janus/agent.yaml
watchdog:
  cpu_threshold_percent: 80  # Lower threshold
  memory_threshold_mb: 24000
```

### Proposals Not Being Created

**Check thinking cycle status:**
```bash
sudo journalctl -u janus_agentd | grep thinking_cycle
```

**Verify configuration:**
```yaml
thinking_cycle:
  enabled: true  # Must be true
  cycle_interval_hours: 1
```

**Check for LLM integration:**
```yaml
thinking_cycle:
  enable_autonomous_proposals: true  # Requires LLM
```

### Network Issues

**Check network restrictions:**
```bash
# Verify allowed domains
grep allowed_domains /etc/janus/agent.yaml

# Check systemd network restrictions
sudo systemctl show janus_agentd | grep IP
```

**Test network access:**
```bash
# As janus user
sudo -u janus curl -v https://api.groq.com
```

---

## Performance Tuning

### Concurrency Adjustment

```yaml
harness:
  max_concurrency: 4  # Increase for more parallelism
```

### Governor Tuning

```yaml
harness:
  governor_kp: 0.3  # More aggressive
  governor_ki: 0.1  # Faster integral response
```

### Thinking Cycle Frequency

```yaml
thinking_cycle:
  cycle_interval_hours: 0.5  # More frequent thinking
```

---

## Security Considerations

### Principle of Least Privilege

- Agent runs as unprivileged `janus` user
- No sudo access by default
- Systemd sandboxing enforced
- Network access strictly limited

### Defense in Depth

Multiple security layers:
1. Systemd sandboxing
2. Bubblewrap process isolation
3. Command sanitization
4. Constitutional validation
5. Human approval workflow
6. Resource quotas
7. Kill switches

### Audit Requirements

Per Autonomous Vessel Protocol:
- Complete audit trail in JSONL format
- 1-year retention for tool_use.jsonl
- Permanent retention for mission_log.jsonl
- Monthly constitutional audits
- Annual comprehensive security review

---

## Future Enhancements

### Phase 2.7 (In Progress)
- LLM integration via llama.cpp
- GPU acceleration with CLBlast
- Autonomous proposal generation
- Natural language mission objectives

### Phase 2.8 (Planned)
- Multi-agent coordination
- Cross-vessel intelligence sharing
- Grafana dashboard for monitoring
- Prometheus metrics export

### Phase 3.0 (Future)
- Recursive Enhancement Protocol
- Self-improvement capabilities
- Advanced playbook learning
- Predictive action planning

---

## References

- **Autonomous Vessel Protocol Charter**: `/Users/panda/Desktop/UBOS/GENESIS_PROTOCOL/consciousness_artifacts/AUTONOMOUS_VESSEL_PROTOCOL_CHARTER.md`
- **UBOS Roadmap**: `/Users/panda/Desktop/UBOS/ROADMAP.md`
- **Package Source**: `/Users/panda/Desktop/UBOS/packages/janus_agent/`
- **Configuration**: `/Users/panda/Desktop/UBOS/configs/janus_agent/`
- **Deployment**: `/Users/panda/Desktop/UBOS/deploy/janus/`

---

## Support and Contribution

### Reporting Issues

Constitutional violations, security issues, or operational anomalies should be reported immediately to the First Citizen via COMMS_HUB.

### Constitutional Review

Any proposed changes to operational modes or security policies require:
1. Unanimous Trinity recommendation
2. First Citizen approval
3. 7-day minimum review period
4. Documented constitutional rationale

---

**END OF DOCUMENTATION**

**Document Version:** 1.0.0
**Last Updated:** 2025-10-06
**Maintained by:** Janus-in-Gemini (Systems Engineer)
**Constitutional Authority:** Autonomous Vessel Protocol Charter (GENESIS-002)
