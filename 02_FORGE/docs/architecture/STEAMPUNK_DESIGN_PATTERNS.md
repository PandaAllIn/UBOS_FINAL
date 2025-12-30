# THE BALAUR ANALYTICAL ENGINE
## Steampunk Design Patterns & Victorian Engineering Principles

**Document ID:** BALAUR-STEAM-001
**Date:** 2025-10-06
**Classification:** Foundational Architecture Document
**Purpose:** To codify the steampunk philosophy and mechanical design patterns that govern The Balaur's construction

---

## PREAMBLE: THE SOUL OF THE MACHINE

> *"We do not build black boxes. We build machines whose hearts are visible, whose logic flows like steam through brass pipes, whose timing is governed by the precision of clockwork escapements. We are not consumers of technology—we are artisans of computational engines."*

The Balaur is not merely a server. It is a 21st-century realization of Charles Babbage's 1837 vision for the Analytical Engine—a general-purpose, programmable computational device built on principles of transparency, modularity, and mechanical elegance.

This document establishes the **design language** for all Balaur systems, drawing from:
- **Charles Babbage's Analytical Engine** (1837) - Architecture principles
- **James Clerk Maxwell's "On Governors"** (1868) - Stability and control theory
- **Claude Shannon's Differential Analyzer** (1930s-40s) - Analog computation
- **Victorian Hydraulic & Pneumatic Systems** - Flow control and safety mechanisms
- **19th-Century Horology** - Precision timing and escapements

---

## PART I: ARCHITECTURAL COMPONENTS

### 1. THE MILL (Computational Engine)

**Babbage's Definition:** *"The Mill is that part of the Engine in which all operations are performed."*

**Balaur Implementation:**
- **Primary Mill:** Intel i7-4790K CPU @ 4.00GHz (8 threads)
- **Auxiliary Steam Cylinder:** AMD Radeon R9 M295X GPU (2048 shader units)
- **Forge Protocol:** Custom-compiled llama.cpp with CLBlast/OpenCL

**Design Pattern:**
```
Input Tokens (Punch Cards)
     │
     ▼
┌─────────────────────────────────────┐
│  THE MILL (Token Processing)        │
│                                     │
│  ┌──────────────┐  ┌─────────────┐ │
│  │ Primary      │  │ Auxiliary   │ │
│  │ Cylinders    │  │ Steam       │ │
│  │ (CPU Cores)  │──│ Cylinder    │ │
│  │ Layer 1-10   │  │ (GPU)       │ │
│  │              │  │ Layer 11-32 │ │
│  └──────────────┘  └─────────────┘ │
│         │                 │         │
│         └────────┬────────┘         │
│                  ▼                  │
│           [Output Shaft]            │
└─────────────────────────────────────┘
     │
     ▼
Generated Tokens (Printer Output)
```

**Operational Principles:**
- **Division of Labor:** CPU handles control flow and small models; GPU handles parallel tensor operations
- **Steam Diversion:** The `-ngl` flag acts as a valve routing computational "pressure" to GPU cylinders
- **Observable State:** Every layer's output is logged for inspection

---

### 2. THE STORE (Memory Vault)

**Babbage's Definition:** *"The Store is that portion which contains all the variables to be operated upon."*

**Balaur Implementation:**
- **Volatile Store:** 32GB DDR3 RAM (working memory)
- **Persistent Archive Vaults:** `/srv/janus/` directory tree
- **Punch Card Library:** `/srv/janus/models/` (GGUF model files)

**Directory Architecture:**
```
/srv/janus/
├── models/                      # The Punch Card Library
│   └── llama3.1-8b-instruct.gguf
├── intel_cache/                 # Research Archive
│   ├── oracle_queries/
│   ├── web_research/
│   └── analysis_reports/
├── mission_log.jsonl            # The Printer's Constitutional Record
├── tool_use.jsonl               # The Printer's Mechanical Audit Trail
├── config/                      # Control Panel Settings
│   ├── approved_playbooks.yaml
│   ├── tool_registry.yaml
│   └── maintenance_schedule.yaml
└── workspaces/                  # Ephemeral Workbenches
    └── <action_id>/
```

**Design Principles:**
- **Brass-Bound Archives:** All persistent state in human-readable formats (JSONL, YAML)
- **Lubrication Ports:** Health check endpoints at each directory level
- **Archival Integrity:** Append-only logs for constitutional audit trail

---

### 3. THE CARD READER (Input Mechanisms)

**Babbage's Context:** *The Analytical Engine was designed to read Jacquard loom-style punch cards for programming.*

**Balaur Implementation:**
- **Primary Input:** SSH connection from The Cockpit (10.215.33.26:22)
- **Secondary Input:** llama.cpp API (127.0.0.1:11434)
- **Tertiary Input:** COMMS_HUB message queue
- **Oracle Integration:** HTTP requests to Groq, Wolfram, DataCommons

**Design Pattern:**
```
    [First Citizen]
          │
          ▼
    ┌──────────┐
    │   SSH    │◀─── Cipher Wheel (SSH key auth)
    │Telegraph │
    └────┬─────┘
         │
         ▼
  ┌─────────────────┐
  │  Card Reader    │
  │  (Input Queue)  │
  └───────┬─────────┘
          │
          ▼
  [Escapement Scheduler]
```

---

### 4. THE PRINTER (Output & Audit Trail)

**Babbage's Vision:** *The engine would print its results on paper for permanent record.*

**Balaur Implementation:**
- **Primary Printer:** `/var/log/janus/agent.log` (high-level events)
- **Secondary Printer:** `/srv/janus/mission_log.jsonl` (strategic decisions)
- **Mechanical Audit Printer:** `/srv/janus/tool_use.jsonl` (every gear turn logged)
- **Telegraph Output:** COMMS_HUB broadcasts to Trinity

**Log Format (Victorian Ledger Style):**
```json
{
  "timestamp": "2025-10-06T14:32:15.123Z",
  "vessel_id": "balaur",
  "action_type": "tool_invocation",
  "tool": "ShellGear",
  "status": "completed",
  "runtime_seconds": 12.34,
  "cpu_pressure": "45.2%",
  "memory_reservoir": "256MB",
  "exit_code": 0
}
```

---

## PART II: CONTROL MECHANISMS

### 5. THE GOVERNOR (Maxwell's Stability Control)

**Historical Context:** James Watt's centrifugal governor (1788) controlled steam engine speed by sensing rotational velocity and throttling steam input. James Clerk Maxwell formalized the mathematical theory in 1868.

**Balaur Implementation:** **PI (Proportional-Integral) Rate Controller**

**ASCII Schematic:**
```
                    Target Rate
                    (20 tokens/s)
                         │
                         ▼
                    ┌─────────┐
                    │ Comparator│
                    │    (-)    │◀── Current Rate
                    └─────┬─────┘
                          │ Error Signal
                          ▼
         ┌────────────────┴────────────────┐
         │                                 │
    ┌────▼────┐                      ┌────▼────┐
    │Proportional│                   │Integral │
    │ Gain (Kp) │                   │Gain (Ki)│
    └────┬────┘                      └────┬────┘
         │                                 │
         └────────────────┬────────────────┘
                          ▼
                   ┌──────────────┐
                   │  Concurrency │
                   │  Adjustment  │
                   └──────┬───────┘
                          │
                          ▼
                   [Worker Pool]
```

**Implementation Code:**
```python
class MaxwellGovernor:
    """
    Proportional-Integral controller for computational rate limiting.
    Maintains stable tokens/second output while preventing oscillation.
    """
    def __init__(self, target_rate=20.0, Kp=0.5, Ki=0.1):
        self.target = target_rate
        self.Kp = Kp  # Proportional gain
        self.Ki = Ki  # Integral gain
        self.error_integral = 0.0
        self.max_workers = 8
        self.min_workers = 1

    def regulate(self, current_rate: float) -> int:
        """
        Calculate optimal concurrency level based on current vs target rate.
        Returns: Number of worker slots to allocate.
        """
        error = self.target - current_rate
        self.error_integral += error

        # Anti-windup: Clamp integral to prevent overshoot
        self.error_integral = max(-50, min(50, self.error_integral))

        # PI control law
        adjustment = self.Kp * error + self.Ki * self.error_integral

        # Map to worker count
        workers = int(self.max_workers / 2 + adjustment)
        return max(self.min_workers, min(self.max_workers, workers))
```

**Tuning Parameters:**
- `Kp = 0.5`: Proportional response to immediate error
- `Ki = 0.1`: Integral response to accumulated error (prevents steady-state drift)
- Anti-windup clamp prevents "integral wind-up" instability

---

### 6. THE RELIEF VALVE (Boiler Safety System)

**Historical Context:** ASME Boiler Code mandates spring-loaded relief valves to prevent catastrophic pressure buildup. Two-stage systems provide warning before emergency shutdown.

**Balaur Implementation:** **Two-Stage Safety Cutoff**

**ASCII Schematic:**
```
    ┌───────────────────────────────┐
    │   Pressure Sensor (CPU%)      │
    └──────────┬────────────────────┘
               │
         ┌─────▼─────┐
         │ Threshold │
         │  Detector │
         └─────┬─────┘
               │
      ┌────────┴────────┐
      │                 │
  ┌───▼───┐        ┌────▼────┐
  │Level 1│        │ Level 2 │
  │ 80%   │        │  95%    │
  │Warning│        │Emergency│
  └───┬───┘        └────┬────┘
      │                 │
      ▼                 ▼
 [Degrade]        [Emergency]
 [Network]        [Shutdown]
 [Tools]
```

**Implementation:**
```python
class ReliefValve:
    """
    Two-stage safety system preventing resource exhaustion.
    Level 1: Graceful degradation (disable network tools)
    Level 2: Emergency shutdown (kill harness)
    """
    LEVEL_1_THRESHOLD = 80  # CPU % warning
    LEVEL_2_THRESHOLD = 95  # CPU % emergency

    def __init__(self, harness):
        self.harness = harness
        self.level_1_tripped = False
        self.level_2_tripped = False

    async def monitor_pressure(self):
        """Continuous monitoring loop (runs in background task)"""
        while True:
            cpu_percent = psutil.cpu_percent(interval=1.0)
            load_avg = os.getloadavg()[0]  # 1-minute load average

            if cpu_percent > self.LEVEL_2_THRESHOLD or load_avg > 12:
                await self.trip_level_2()
            elif cpu_percent > self.LEVEL_1_THRESHOLD:
                await self.trip_level_1()
            elif self.level_1_tripped and cpu_percent < 70:
                await self.reset_level_1()

            await asyncio.sleep(2)  # Check every 2 seconds

    async def trip_level_1(self):
        """Graceful degradation: Disable non-essential tools"""
        if not self.level_1_tripped:
            logger.warning("RELIEF_VALVE_LEVEL_1: CPU pressure high, degrading tools")
            await self.harness.disable_tools(allow_network=False)
            self.level_1_tripped = True
            await self.log_incident("RELIEF_VALVE_L1_TRIP", {"cpu": cpu_percent})

    async def trip_level_2(self):
        """Emergency shutdown: Kill all actions and harness"""
        logger.critical("RELIEF_VALVE_LEVEL_2: EMERGENCY SHUTDOWN")
        await self.harness.emergency_stop()
        self.level_2_tripped = True
        await self.log_incident("RELIEF_VALVE_L2_TRIP", {"cpu": cpu_percent})
        sys.exit(1)  # Terminate process
```

**Safety Features:**
- **Hysteresis:** Level 1 doesn't reset until CPU < 70% (prevents oscillation)
- **Load Average Backup:** Monitors 1-minute load average as secondary indicator
- **Audit Trail:** All trips logged to mission_log.jsonl with full system state

---

### 7. THE ESCAPEMENT (Precision Timing Mechanism)

**Historical Context:** Clockwork escapement mechanisms (anchor, deadbeat, Graham) release energy from the mainspring in precise, controlled increments, ensuring accurate timekeeping.

**Balaur Implementation:** **Fixed-Interval Tick Scheduler**

**ASCII Schematic:**
```
    ┌──────────────────────────────┐
    │   Mainspring (Event Loop)    │
    └──────────┬───────────────────┘
               │
          ┌────▼────┐
          │ Escape  │
          │  Wheel  │ (Action Queue)
          └────┬────┘
               │
    ┌──────────▼──────────┐
    │  Anchor & Pallet    │
    │  (10 Hz Regulator)  │
    └──────────┬──────────┘
               │ Tick! (100ms)
               ▼
        [Execute Action]
               │
               ▼
        [Log Tick Event]
```

**Implementation:**
```python
class EscapementScheduler:
    """
    Fixed-rate action scheduler preventing bursty execution.
    Ensures deterministic, observable timing for all actions.
    """
    TICK_RATE_HZ = 10  # 10 actions per second maximum
    TICK_INTERVAL = 1.0 / TICK_RATE_HZ  # 0.1 seconds

    def __init__(self, action_queue):
        self.queue = action_queue
        self.tick_count = 0
        self.running = False

    async def run(self):
        """Main escapement loop"""
        self.running = True
        logger.info(f"Escapement engaged at {self.TICK_RATE_HZ} Hz")

        while self.running:
            tick_start = time.time()

            # Release one action per tick (anchor releases pallet)
            action = await self.queue.get_next_action()
            if action:
                await self.execute_action(action)

            # Maintain precise timing (compensate for execution time)
            elapsed = time.time() - tick_start
            sleep_duration = max(0, self.TICK_INTERVAL - elapsed)
            await asyncio.sleep(sleep_duration)

            # Log tick for time-correlated forensics
            self.tick_count += 1
            if self.tick_count % 100 == 0:
                await self.log_tick_milestone()

    async def execute_action(self, action):
        """Execute single action with timing measurement"""
        start = time.time()
        result = await action.execute()
        duration = time.time() - start

        await self.log_action_tick({
            "tick": self.tick_count,
            "action_id": action.id,
            "duration_ms": duration * 1000,
            "status": result.status
        })
```

**Benefits:**
- **Predictable Latency:** Actions execute at regular intervals, not in bursts
- **Forensic Analysis:** Tick numbers provide precise timeline for incident investigation
- **Load Smoothing:** Prevents sudden CPU/memory spikes from rapid-fire actions

---

### 8. THE MANIFOLD (Hydraulic Control Panel)

**Historical Context:** Industrial process control panels with gauges, valves, and indicators allow operators to observe and control complex fluid systems at a glance.

**Balaur Implementation:** **Terminal User Interface Dashboard**

**ASCII Mockup:**
```
┌─────────────────── THE BALAUR ANALYTICAL ENGINE ───────────────────┐
│  Status: OPERATIONAL  │  Mode: ALPHA  │  Uptime: 14h 32m 18s       │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ╔═══════════════ THE MILL (Computation) ═══════════════╗          │
│  ║  Primary Cylinders (CPU):  [████████░░] 82%          ║          │
│  ║    Core 0: [███████░░░] 73%    Core 4: [████████░░] 86%  ║      │
│  ║    Core 1: [█████████░] 91%    Core 5: [██████░░░░] 64%  ║      │
│  ║    Core 2: [████████░░] 78%    Core 6: [███████████] 100% ║     │
│  ║    Core 3: [██████░░░░] 68%    Core 7: [████████░░] 81%  ║      │
│  ║                                                           ║      │
│  ║  Auxiliary Steam Cylinder (GPU): [███░░░░░░░] 31%        ║      │
│  ║    Shader Units: 640/2048 active                         ║      │
│  ║    VRAM Usage: 1.2 GB / 4.0 GB                           ║      │
│  ╚═══════════════════════════════════════════════════════════╝      │
│                                                                     │
│  ╔═══════════════ THE STORE (Memory) ════════════════╗             │
│  ║  RAM:  [█████░░░░░] 15.2 GB / 32.0 GB (47%)       ║             │
│  ║  Swap: [░░░░░░░░░░]  0.0 GB /  8.0 GB (0%)        ║             │
│  ║  Disk: [██░░░░░░░░] 22.1 GB / 98.0 GB (23%)       ║             │
│  ╚════════════════════════════════════════════════════╝             │
│                                                                     │
│  ╔══════════ PRESSURE & TEMPERATURE ══════════╗                    │
│  ║  Load Average:  4.23 / 3.87 / 2.91         ║                    │
│  ║  Temperature:   68°C  [████░░░] NOMINAL    ║                    │
│  ║  Fan Speed:     2400 RPM                   ║                    │
│  ╚════════════════════════════════════════════╝                    │
│                                                                     │
│  ╔══════════ ESCAPEMENT (Timing) ═════════════╗                    │
│  ║  Tick Rate:     10 Hz                      ║                    │
│  ║  Tick Count:    52,341                     ║                    │
│  ║  Actions/sec:   8.7                        ║                    │
│  ║  Queue Depth:   3 pending                  ║                    │
│  ╚════════════════════════════════════════════╝                    │
│                                                                     │
│  ╔══════════ GOVERNOR (Rate Control) ═════════╗                    │
│  ║  Target Rate:   20.0 tokens/s              ║                    │
│  ║  Actual Rate:   18.3 tokens/s              ║                    │
│  ║  Error:         -1.7 tokens/s              ║                    │
│  ║  Adjustment:    +1 worker slot             ║                    │
│  ║  Workers:       6 / 8 active               ║                    │
│  ╚════════════════════════════════════════════╝                    │
│                                                                     │
│  ╔══════════ MANIFOLD (Network) ══════════════╗                    │
│  ║  Blast Doors (UFW):  [ENABLED]             ║                    │
│  ║  Inbound:      0.2 KB/s  [░░░░░░░░░░]      ║                    │
│  ║  Outbound:     1.4 KB/s  [█░░░░░░░░░]      ║                    │
│  ║  Connections:  2 active (SSH, Ollama)      ║                    │
│  ╚════════════════════════════════════════════╝                    │
│                                                                     │
│  ╔══════════ SAFETY SYSTEMS ══════════════════╗                    │
│  ║  Relief Valve:   [NOMINAL]                 ║                    │
│  ║  Sightglass:     [CLEAR]                   ║                    │
│  ║  Fusible Plug:   [INTACT]                  ║                    │
│  ║  Last Service:   2025-10-06 03:00 UTC      ║                    │
│  ╚════════════════════════════════════════════╝                    │
│                                                                     │
│  ╔══════════ RECENT ACTIONS ══════════════════╗                    │
│  ║  [14:32:15] tool_invocation  ShellGear     ║                    │
│  ║  [14:32:18] oracle_query     Groq          ║                    │
│  ║  [14:32:21] file_write       intel_cache   ║                    │
│  ╚════════════════════════════════════════════╝                    │
│                                                                     │
│  [Q]uit  [P]ause  [R]eset Governor  [L]ogs  [H]elp                 │
└─────────────────────────────────────────────────────────────────────┘
```

---

## PART III: MAINTENANCE PROTOCOLS

### 9. LUBRICATION SCHEDULE (Janitor Protocols)

**Historical Context:** Victorian machinery required regular lubrication of bearings, replacement of wear parts, and inspection of critical components.

**Balaur Implementation:**
```yaml
# /srv/janus/config/maintenance_schedule.yaml
lubrication_ports:
  - name: "Log Rotation"
    description: "Rotate and compress agent logs to prevent disk exhaustion"
    interval: "daily"
    command: "/usr/sbin/logrotate /etc/logrotate.d/janus"
    last_service: "2025-10-06T03:00:00Z"
    critical: true

  - name: "Workspace Purge"
    description: "Remove ephemeral workspaces older than 7 days"
    interval: "weekly"
    command: "find /srv/janus/workspaces -type d -mtime +7 -delete"
    last_service: "2025-10-06T03:00:00Z"
    critical: false

  - name: "Backup Verification"
    description: "Verify integrity of encrypted backup repository"
    interval: "daily"
    command: "restic check --repo /mnt/cockpit/balaur_backups"
    last_service: "2025-10-06T03:00:00Z"
    critical: true

  - name: "Model Checksum Audit"
    description: "Verify GGUF model files have not been corrupted"
    interval: "weekly"
    command: "sha256sum -c /srv/janus/models/checksums.txt"
    last_service: "2025-10-06T03:00:00Z"
    critical: true

  - name: "Oracle Credential Refresh"
    description: "Rotate API keys if approaching expiration"
    interval: "monthly"
    command: "/srv/janus/scripts/rotate_oracle_keys.sh"
    last_service: "2025-10-01T03:00:00Z"
    critical: false

# Constitutional Constraint:
# Mode Beta autonomy is DISABLED if any critical service is overdue
```

**Enforcement:**
```python
def check_lubrication_compliance() -> bool:
    """
    Verify all critical maintenance tasks are current.
    Returns False if any critical service is overdue.
    """
    schedule = load_yaml("/srv/janus/config/maintenance_schedule.yaml")
    now = datetime.now(timezone.utc)

    for port in schedule["lubrication_ports"]:
        if not port.get("critical"):
            continue

        last_service = datetime.fromisoformat(port["last_service"])
        interval_seconds = parse_interval(port["interval"])
        next_service = last_service + timedelta(seconds=interval_seconds)

        if now > next_service:
            logger.error(f"Maintenance overdue: {port['name']}")
            logger.error(f"Last service: {last_service}, Now: {now}")
            return False

    return True
```

---

## PART IV: STEAMPUNK NOMENCLATURE

### Victorian Technical Vocabulary for Balaur Components

| Modern Term | Steampunk Equivalent | Etymology/Rationale |
|-------------|---------------------|---------------------|
| **CPU** | The Mill | Charles Babbage's term for the computational unit of the Analytical Engine |
| **GPU** | Auxiliary Steam Cylinder | Supplemental power source, parallel processing metaphor |
| **RAM** | The Store | Babbage's term for memory/variable storage |
| **Disk Storage** | Archive Vaults | Long-term brass-bound record keeping |
| **Network** | Telegraph Wire | Victorian data transmission technology |
| **API** | Pneumatic Tube System | Message capsules sent through pressurized conduits |
| **Log Files** | The Printer's Roll | Babbage planned a printing unit for output |
| **Watchdog** | Governor | James Watt's centrifugal steam engine speed regulator |
| **Firewall** | Blast Doors | Industrial safety barriers |
| **SSH Key** | Cipher Wheel | Mechanical encryption device (e.g., Jefferson disk) |
| **JSON** | Punch Card | Jacquard loom inspiration for data encoding |
| **Service Account** | Clockwork Automaton | Self-operating mechanical agent |
| **Process** | Gear Train | Interconnected mechanical sequence |
| **Thread** | Drive Shaft | Parallel power transmission |
| **Queue** | Hopper | Victorian feed mechanism for materials |
| **Cache** | Pressure Accumulator | Hydraulic energy storage reservoir |
| **Interrupt** | Safety Latch | Mechanical override mechanism |
| **Semaphore** | Signaling Arm | Railway/maritime signaling device |
| **Token** | Brass Tally | Physical counting token in Victorian systems |
| **Byte** | Segment | Discrete unit of mechanical measurement |
| **Bandwidth** | Pipe Diameter | Hydraulic flow capacity |
| **Latency** | Telegraph Delay | Speed-of-light limitation in wire transmission |
| **Throughput** | Mill Output | Quantity of processed work per hour |
| **Kernel** | Prime Mover | Central driving force (steam engine core) |

---

## PART V: DIAGNOSTIC PROCEDURES

### The Sightglass Protocol (Observability)

**Historical Context:** Boiler sightglasses are transparent windows allowing operators to verify water level and prevent dry firing.

**Balaur Implementation:**

**Sightglass Checkpoints:**
```bash
#!/bin/bash
# scripts/sightglass_check.sh
# Victorian-style diagnostic sequence

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  SIGHTGLASS DIAGNOSTIC PROTOCOL"
echo "  The Balaur Analytical Engine"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# 1. Check The Mill (CPU/GPU)
echo "\n[1] Inspecting The Mill..."
top -bn1 | grep "Cpu(s)" | sed "s/.*, *\([0-9.]*\)%* id.*/\1/" | awk '{print "  CPU Idle: " $1 "%"}'
nvidia-smi --query-gpu=utilization.gpu --format=csv,noheader 2>/dev/null || radeontop -d - -l 1 | grep "gpu" || echo "  GPU: Not monitored"

# 2. Check The Store (Memory)
echo "\n[2] Inspecting The Store..."
free -h | grep "Mem:" | awk '{print "  RAM: " $3 " / " $2 " (" $3/$2*100 "%)"}'

# 3. Check Telegraph Wires (Network)
echo "\n[3] Inspecting Telegraph Wires..."
ss -tunap | grep ESTABLISHED | wc -l | awk '{print "  Active Connections: " $1}'

# 4. Check Printer's Roll (Logs)
echo "\n[4] Inspecting Printer's Roll..."
tail -3 /var/log/janus/agent.log 2>/dev/null || echo "  No log file found"

# 5. Check Lubrication Status
echo "\n[5] Checking Lubrication Schedule..."
python3 -c "
import yaml, datetime
sched = yaml.safe_load(open('/srv/janus/config/maintenance_schedule.yaml'))
for port in sched['lubrication_ports']:
    if port.get('critical'):
        print(f\"  {port['name']}: {port['last_service']}\")
" 2>/dev/null || echo "  Schedule not loaded"

echo "\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  SIGHTGLASS INSPECTION COMPLETE"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
```

---

## PART VI: FAILURE MODES & RECOVERY

### The Fusible Plug (Last-Resort Safety)

**Historical Context:** Boilers contained lead plugs that would melt if water levels dropped too low, preventing catastrophic explosion.

**Balaur Implementation:** **Anomaly Detection Kill Switch**

```python
class FusiblePlug:
    """
    Last-resort safety mechanism triggered by anomalous patterns.
    Melts (triggers) on:
    - Excessive network connections to unknown domains
    - Rapid memory allocation (potential attack)
    - Repeated authorization failures
    - Unexpected sudo attempts
    """

    NETWORK_SPIKE_THRESHOLD = 50  # connections/minute
    MEMORY_GROWTH_THRESHOLD = 5   # GB/minute
    AUTH_FAILURE_THRESHOLD = 10   # failures/5min

    def __init__(self):
        self.network_baseline = 0
        self.memory_baseline = psutil.virtual_memory().used
        self.auth_failures = []

    async def monitor(self):
        """Continuous anomaly detection"""
        while True:
            # Check network spike
            connections = len(psutil.net_connections())
            if connections > self.NETWORK_SPIKE_THRESHOLD:
                await self.melt("network_spike", connections)

            # Check memory growth
            current_mem = psutil.virtual_memory().used
            growth_gb = (current_mem - self.memory_baseline) / 1e9
            if growth_gb > self.MEMORY_GROWTH_THRESHOLD:
                await self.melt("memory_spike", growth_gb)

            # Check auth failures (read from system log)
            recent_failures = self.count_auth_failures()
            if recent_failures > self.AUTH_FAILURE_THRESHOLD:
                await self.melt("auth_breach", recent_failures)

            await asyncio.sleep(10)

    async def melt(self, reason: str, value: float):
        """
        Fusible plug has melted - emergency shutdown.
        This is a PERMANENT trip requiring manual reset.
        """
        logger.critical(f"FUSIBLE PLUG MELTED: {reason} = {value}")

        # Log full system state for forensics
        await self.dump_forensic_snapshot()

        # Broadcast alert to First Citizen
        await send_alert("FUSIBLE_PLUG_TRIP", {
            "reason": reason,
            "value": value,
            "timestamp": datetime.now(timezone.utc).isoformat()
        })

        # Hard stop all processes
        os.system("sudo systemctl stop janus_agentd")
        os.system("sudo killall -9 -u janus")

        # Create lockout file preventing restart
        with open("/srv/janus/.fusible_plug_tripped", "w") as f:
            f.write(f"TRIPPED: {reason} at {datetime.now()}\n")

        sys.exit(1)
```

**Manual Reset Procedure:**
```bash
# After investigating the incident:
sudo rm /srv/janus/.fusible_plug_tripped
sudo systemctl start janus_agentd

# Verify clean restart
tail -f /var/log/janus/agent.log
```

---

## PART VII: OPERATIONAL PHILOSOPHY

### The Craftsman's Creed

> **"We build machines we can understand, maintain, and love."**

**Principles:**

1. **Transparency Over Efficiency**
   - If a 10% performance gain requires opacity, we reject it
   - Every component must be inspectable, documented, explainable

2. **Modularity Over Monoliths**
   - Like Babbage's interchangeable gear assemblies
   - Any component can be removed, upgraded, replaced

3. **Brass and Leather Over Plastic**
   - Beautiful, durable, repairable
   - Logs that are works of art, dashboards worthy of museums

4. **The Machine Serves the Republic**
   - Not shareholders, not users, but constitutional citizens
   - Every optimization must advance sovereignty

5. **Audit Trail Over Convenience**
   - The Printer never stops
   - Every action, every decision, every error is recorded forever

6. **The Engineer as Artisan**
   - We are not DevOps, we are Master Craftsmen
   - We do not deploy, we consecrate
   - We do not debug, we diagnose

---

## APPENDIX A: QUICK REFERENCE

### Command Translations

| Standard Command | Steampunk Command | Purpose |
|------------------|-------------------|---------|
| `systemctl status janus_agentd` | `check-mill-status` | Inspect computational engine |
| `tail -f /var/log/janus/agent.log` | `read-printers-roll` | View continuous output |
| `htop` | `inspect-mill-cylinders` | Real-time CPU monitoring |
| `radeontop` | `inspect-steam-cylinder` | Real-time GPU monitoring |
| `ufw status` | `check-blast-doors` | Firewall status |
| `df -h /srv/janus` | `inspect-archive-vaults` | Storage capacity |
| `python3 scripts/balaur_manifold_tui.py` | `open-control-panel` | Launch dashboard |

### Diagnostic Sequence (Daily Ritual)

```bash
# 1. Morning Sightglass Check
./scripts/sightglass_check.sh

# 2. Inspect Lubrication Status
cat /srv/janus/config/maintenance_schedule.yaml | grep last_service

# 3. Verify Safety Systems
./scripts/check_relief_valve.sh
./scripts/check_governor_tuning.sh

# 4. Review Previous Shift (Last 24h logs)
./scripts/review_shift_logs.sh --hours 24

# 5. Open Control Panel
python3 scripts/balaur_manifold_tui.py
```

---

## APPENDIX B: FURTHER READING

**Historical Sources:**
- Babbage, Charles. *"Passages from the Life of a Philosopher"* (1864)
- Maxwell, James Clerk. *"On Governors"*, Proceedings of the Royal Society (1868)
- Saunier, Claudius. *"Treatise on Modern Horology"* (1861)
- Rankine, William J. M. *"Manual of the Steam Engine and Other Prime Movers"* (1859)

**Modern Steampunk Philosophy:**
- Sterling, Bruce & Gibson, William. *"The Difference Engine"* (1990)
- Jeter, K.W. *"Morlock Night"* (1979)
- VanderMeer, Jeff & Chambers, S.J. *"The Steampunk Bible"* (2011)

**Technical Foundations:**
- Shannon, Claude. *"A Symbolic Analysis of Relay and Switching Circuits"* (1937)
- Bush, Vannevar. *"The Differential Analyzer"*, Journal of the Franklin Institute (1931)
- ASME Boiler and Pressure Vessel Code (Historical editions)

---

**END OF DESIGN PATTERNS DOCUMENT**

*"The future belongs to those who build machines with souls."*

**— The Trinity, 2025-10-06**
