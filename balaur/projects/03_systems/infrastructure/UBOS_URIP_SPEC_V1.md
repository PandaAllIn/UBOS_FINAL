# UBOS Rhythmic Integrity Protocol (URIP) — Spec v1

**Owner:** Codex, Forgemaster  
**Location:** `/srv/janus/balaur/projects/03_systems/infrastructure/`  
**Related Doctrine:** Article III — Governors & Escapements (UBOS Philosophical Bluebook)

---

## 1. Purpose

URIP translates the philosophical mandate “The Governor is wisdom; the Escapement is patience” into a concrete systems service. The module measures Balaur’s computational resonance, enforces harmonic pacing for heavy tasks, and broadcasts synchronization pulses so other vessels (Gemini, Claude, Oracle nodes) can act in cadence.

The system adds three guarantees:

1. **Measured Motion:** Every asynchronous or AI-resident action is throttled to a tempo derived from the Harmonic Layer in `orchestrion_spec_v1.md`.
2. **Feedback Wisdom:** Compute amplitude (CPU, memory, semantic depth) is compared to constitutional limits and immediately dampened if thresholds are crossed.
3. **Distributed Rhythm:** Clock pulses written to `/srv/janus/balaur/signal/clock/` allow satellites to phase-lock with Balaur’s heartbeat.

---

## 2. Component Overview

| Component | Description | Key Inputs | Outputs |
| --- | --- | --- | --- |
| `TelemetryProbe` | Collects CPU load, memory pressure, query frequency, and semantic depth estimates. | `/proc/stat`, `/proc/meminfo`, optional `oracle_trinity/sync/*.json`, Orchestrion harmonic hints. | Raw metrics packet |
| `GovernorEngine` | Computes resonance index, compares amplitude to URIP thresholds, and derives throttle factors / beat intervals. | Telemetry packet, config thresholds, harmonic tempo. | `governor_state` dict |
| `EscapementScheduler` | Releases heavy operations on discrete beats and ensures spacing between task bursts. | `governor_state`, queue descriptors. | `heartbeat` payload + release window timestamps |
| `OracleSynchronizer` | Reads remote beats from `balaur/oracle_trinity/sync/` to maintain distributed coherence. | External beat JSON files. | Phase offset + adjusted interval |
| `BeatBus` | Writes canonical heartbeat artifacts for monitoring + downstream automation. | `heartbeat` payload. | `signal/clock/rhythm_state.json`, `signal/clock/beat.log` |

---

## 3. Data Flow

```
 ┌────────────────┐     ┌─────────────────┐     ┌───────────────────┐
 │ telemetry loop │ --> │ governor engine │ --> │ escapement pulses │
 └────────────────┘     └─────────────────┘     └───────────────────┘
          ▲                       ▲                      │
          │                       │                      ▼
   orchestrion spec         urip_daemon.conf    /srv/janus/balaur/signal/clock/
          │                       │                      │
          ▼                       ▼                      ▼
  harmonic tempo         amplitude thresholds    beat logs + release tokens
```

1. **Harmonic Seed:** `orchestrion_spec_v1.md` contains `Tempo:` and `Priority:` declarations. The controller parses these values (fallbacks exist if the file is absent).
2. **Telemetry Sampling:** Every loop reads system load, semantic depth estimates, and query backlog counts. External oracle beats may tighten or loosen timing.
3. **Governor Adjustment:** The resonance index (0–1) reflects how close Balaur is to its soft and hard limits. Interval and throttle factors scale inversely with that index.
4. **Escapement Pulse:** Each beat produces a JSON heartbeat plus a release window timestamp that downstream daemons can inspect before launching heavy jobs.
5. **Beat Bus:** Artifacts inside `signal/clock/` form the canonical time source. Gemini can mirror these beats on the hardware telemetry bus; Claude can audit them for rhythm drift.

---

## 4. Configuration (`urip_daemon.conf`)

`URIP_controller.py` consumes an INI-style config containing:

```ini
[orchestrion]
spec_path=/srv/janus/balaur/projects/03_systems/infrastructure/orchestrion_spec_v1.md

[urip]
base_interval=6          ; Seconds between low-load beats
min_interval=2
max_interval=30
cpu_soft_limit=0.65      ; Ratio 0–1
cpu_hard_limit=0.85
mem_soft_limit=0.70
mem_hard_limit=0.90
token_soft_limit=4000    ; Derived from semantic depth estimates
token_hard_limit=7000
beat_bus_dir=/srv/janus/balaur/signal/clock
oracle_sync_dir=/srv/janus/balaur/oracle_trinity/sync
log_level=INFO
```

*Threshold semantics:* once a “soft” threshold is exceeded, beat intervals stretch towards `max_interval`. Crossing “hard” thresholds sets the controller to **relief mode**—heartbeat cadence is published, but escapement releases are paused until amplitude decays.

Optional telemetry fields extend the `[urip]` block as follows:

- `query_soft_limit` / `query_hard_limit` &mdash; expected beats per minute from distributed nodes.
- `semantic_probe_file` &mdash; optional JSON with `semantic_depth` for live prompt/token load.
- `task_meter_file` &mdash; optional JSON with `pending_jobs` + `avg_weight` to bias the escapement.

---

## 5. Output Artifacts

URIP emits artifacts every cycle:

| File | Description |
| --- | --- |
| `signal/clock/rhythm_state.json` | Latest heartbeat payload with metrics, interval, throttle factor, and release window. |
| `signal/clock/rhythm_history.log` | Append-only log of beats (ISO timestamp + resonance summary). |
| `signal/clock/next_release.token` | Contains the earliest timestamp when new heavy jobs may execute; downstream schedulers poll this file. |
| `signal/clock/urip.alert` | Human-readable note when hard limits engage (optional, created only under stress). |

Each file is overwritten or appended atomically to avoid race conditions for other daemons polling the directory.

---

## 6. Oracle Trinity Synchronization

* Drop JSON beat capsules inside `/srv/janus/balaur/oracle_trinity/sync/` in the following form:

```json
{
  "oracle": "gemini",
  "timestamp": "2025-10-26T11:54:07Z",
  "interval": 5.0,
  "phase_hint": 0.12
}
```

* URIP averages recent `interval` values to nudge its own pacing when Balaur is under light load, ensuring the distributed vessels remain phase-aligned.
* If external pulses stop arriving for more than `max_interval`, URIP reverts to autonomous timing using its harmonic defaults.

---

## 7. Deployment & Operation

1. Ensure Python 3.10+ is available on Balaur.
2. Confirm the directories:
   * `/srv/janus/balaur/projects/03_systems/infrastructure/`
   * `/srv/janus/balaur/signal/clock/`
   * `/srv/janus/balaur/oracle_trinity/sync/`
3. Configure `urip_daemon.conf` with site-specific thresholds.
4. Launch the controller:  
   `python3 URIP_controller.py --config urip_daemon.conf`
5. Optionally run in one-shot diagnostic mode:  
   `python3 URIP_controller.py --config urip_daemon.conf --once`

Systemd unit guidance (pseudo):

```
[Service]
ExecStart=/usr/bin/python3 /srv/janus/balaur/projects/03_systems/infrastructure/URIP_controller.py \
  --config /srv/janus/balaur/projects/03_systems/infrastructure/urip_daemon.conf
Restart=always
```

---

## 8. Future Hooks

* **Hardware Telemetry:** Gemini can bind GPU thermals and fan curves to the same beat bus so mechanical telemetry resonates with software tempo.
* **Proposal Governor:** Claude can subscribe to `next_release.token` before approving auto-executor proposals in Mode Beta, guaranteeing constitutional pacing.
* **Pattern Engine (Article IV):** URIP exposes the rhythm primitives the Pattern Engine will modulate when it starts weaving multi-layer campaigns.

URIP v1 establishes the pulse. Later releases may add MCP endpoints (`GET /urip/state`, `POST /urip/beat`) and encrypted beat mirroring for off-Balaur vessels.

---

**Status:** Drafted 2025-10-26 — Ready for implementation in `URIP_controller.py`.
