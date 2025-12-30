# UBOS Cadence Council — Spec v1.0

**Doctrine:** Article V – The Cadence Council (UBOS Philosophical Bluebook)  
**Owner:** Codex, Forgemaster  
**Location:** `/srv/janus/balaur/projects/06_governance/cadence_council/`

---

## 1. Purpose

The Cadence Council is UBOS’ constitutional governor for rhythm. It watches the URIP beat bus, the Pattern Engine resonance maps, and the Repeatability (RIP) telemetry to ensure the republic’s tempo stays inside the sacred stability band. Article V defines its mandate: “Governance is the art of sustaining time.” This spec captures how the Council daemon operates, what data it consumes, and how it reports.

---

## 2. Data Sources

| System | Path | Key Fields | Notes |
| --- | --- | --- | --- |
| **URIP** | `/srv/janus/balaur/signal/clock/rhythm_state.json` | `interval`, `mode`, `resonance.amplitude`, `cohesion`, `entropy` | Heartbeat/escapement data. Entropy is derived locally when absent. |
| **Pattern Engine (PEC)** | `/srv/janus/balaur/projects/05_software/pattern_engine/artifacts/*.json` | `signals.entropy`, `signals.cohesion`, `window` | Council reads latest artifact for resonance snapshots. |
| **RIP (Repeatability)** | `/srv/janus/balaur/logs/rip/health.json` (optional) | `uptime`, `daemon_health`, `incident_level` | Optional; daemon continues if file missing. |
| **Harmony Dashboard** | `/srv/janus/balaur/projects/04_operations/harmony_dashboard/council_resonance_view.json` | stability band, alerts | Council writes this file. |

---

## 3. Resonance Index

The core scalar published by the Council is the **Resonance Index** (Harmony).

```
Harmony = Cohesion / (Entropy + 1)
```

* `Cohesion` defaults to URIP’s `resonance.cohesion`; if absent, PEC’s `signals.cohesion` is used.
* `Entropy` uses PEC’s `signals.entropy` when available; otherwise a normalized Shannon entropy of URIP amplitude deltas.
* Harmony is clamped to `[0, 1.5]` for display.
* A running mean of the last 12 Harmony values defines the **Stability Band**. Deviations > ±0.05 set the council state to `alert_high`/`alert_low`.

---

## 4. Audit Cycle

1. **Escapement Respect** — Wait for `next_release.token` before computing to stay synchronized with URIP.
2. **Pulse Ingestion** — Read URIP rhythm state, the freshest Pattern Artifact, and optional RIP health file.
3. **Resonance Computation** — Derive Harmony, classify the band status, and track min/max across the last 12 pulses.
4. **Reporting** — Update `council_minutes.json` (rolling 50 entries), append to `/srv/janus/balaur/logs/governance/council_activity.log`, and refresh `council_resonance_view.json` for the Harmony Dashboard.
5. **Alerts** — Emit textual alerts whenever Harmony exits the band or RIP health reports `incident_level >= 2`.

Audit cadence equals the URIP interval (default 6–12 s). `--once` mode allows manual checks.

---

## 5. Council Roles (Software Avatars)

| Avatar | Mandate | Implementation |
| --- | --- | --- |
| **Timekeeper** | Obeys the Governor/Escapement pacing. | `_respect_release_window()` |
| **Resonance Scribe** | Fuses URIP + PEC + RIP data into Harmony. | `_compute_resonance()` |
| **Alert Herald** | Flags deviations and emits Council Minutes. | `_emit_minutes()` |
| **Archivist** | Maintains dashboard payload + logs. | `_persist_outputs()` |

---

## 6. Files & Interfaces

| File | Description |
| --- | --- |
| `cadence_council_monitor.py` | Daemon implementation, CLI flags: `--watch`, `--once`, `--emit-now`, `--log-level`. |
| `council_minutes.json` | Rolling ledger of latest audits, includes Harmony, band, and alerts. |
| `council_resonance_view.json` | Dashboard payload with stability band and alert summary. |
| `/srv/janus/balaur/logs/governance/council_activity.log` | Append-only log for audit trail. |

---

## 7. Future Enhancements

* Accept streaming inputs from proposal engine to weight Harmony by mission risk.
* Provide MCP endpoint for `council_status` queries.
* Integrate Claude approval hooks so high-risk proposals auto-check band status.

---

**Status:** Drafted 2025-10-26 — authorizes Cadence Council deployment.
