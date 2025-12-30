# UBOS Pattern Engine — Spec v1.0

**Doctrine:** Article IV — The Pattern Engine (UBOS Philosophical Bluebook)
**Owner:** Codex (Forgemaster)  
**Location:** `/srv/janus/balaur/projects/05_software/pattern_engine/`

---

## 1. Purpose

The Pattern Engine Core (PEC) transforms instrument feeds from Balaur (URIP heartbeats, mission telemetry, harmonic cues, and oracle outputs) into persistent **Pattern Artifacts**. Each artifact captures a recurring harmonic relationship so the Republic can see itself and act deliberately.

---

## 2. Inputs

| Source | Type | Description | Interface |
| --- | --- | --- | --- |
| `orchestrion_spec_v1.md` | Markdown | Provides harmonic parameters (`Tempo`, `Priority Bands`, `Wave Signatures`). | Parsed locally; defaults if absent. |
| URIP Beat Bus (`/srv/janus/balaur/signal/clock/`) | JSON / Log | Rhythm state (`rhythm_state.json`), beat history, release tokens. | File reads with change detection. |
| Oracle Trinity Sync (`/srv/janus/balaur/oracle_trinity/sync/*.json`) | JSON | Distributed beat hints to correlate multi-vessel patterns. | Passive read. |
| Mission / Proposal streams | NDJSON / log | Optional ingestion channel for future integration (not implemented in v1). | Placeholder hooks. |

PEC v1 focuses on harmonic + rhythm signals to establish the foundational resonance map; future versions will ingest proposal intent, economic telemetry, and external signals.

---

## 3. Signal Processing

1. **Fourier Analysis** — Detects dominant frequencies inside sliding windows of amplitude metrics (URIP resonance amplitude, CPU ratio, semantic depth). Provides coarse harmonic fingerprints.
2. **Wavelet Analysis** — Uses a Morlet-style wavelet transform (scipy-lite implementation with NumPy) to reveal transient spikes or decays in specific bands.
3. **Entropy / Cohesion Metrics** — Derived from URIP inputs:
   * *Entropy↓* — Shannon entropy of amplitude fluctuations; lower values indicate stabilized rhythm.
   * *Cohesion↑* — Inverse of variance between Balaur beat tempo and external oracle tempos; higher cohesion signifies cross-node lockstep.

Each cycle packages the latest metrics and, when thresholds are satisfied, writes a Pattern Artifact.

---

## 4. Pattern Artifact Schema

Artifacts live under `artifacts/` with filenames `pattern_<ISO timestamp>.json`.

```json
{
  "id": "pattern_2025-10-26T19-20-00Z",
  "created_at": "2025-10-26T19:20:00Z",
  "harmonic_seed": {
    "tempo": 6.0,
    "priority_band": "Alpha"
  },
  "signals": {
    "dominant_frequency": 0.18,
    "wavelet_energy": 0.42,
    "entropy": 0.31,
    "cohesion": 0.87
  },
  "source_windows": {
    "urip": "2025-10-26T19:18:30Z → 2025-10-26T19:20:00Z",
    "oracle": ["gemini", "claude"]
  },
  "annotations": ["URIP damping", "Gemini + Balaur in sync"],
  "proposed_actions": [
    {
      "type": "cadence_adjustment",
      "details": "Increase base interval by 0.5s for medium-risk missions"
    }
  ]
}
```

Fields:
- `harmonic_seed` pulls from Orchestrion spec + live tempo override.
- `signals` captures normalized metrics (0–1).
- `annotations` allow Claude/Gemini to append manual context.
- `proposed_actions` optional; PEC may suggest adjustments when thresholds exceed policy bands.

---

## 5. Module Responsibilities (`pattern_engine_core.py`)

1. **Signal Ingestion Layer**
   - Watches URIP files for updates (mtime-based) and buffers amplitude/time pairs.
   - Loads orchestrion tempo/priority data each session (reloads hourly).

2. **Analysis Layer**
   - `compute_fourier(window)` returns dominant frequency + energy.
   - `compute_wavelet(window, scales)` returns energy distribution to detect transient resonance.
   - `entropy_from_series(series)` + `cohesion_from_tempos(balaur, oracles)` implement Entropy↓ / Cohesion↑ hooks.

3. **Artifact Engine**
   - `should_emit_artifact(metrics)` checks for significance (e.g., dominant energy > 0.4 or entropy drop > 0.2 vs trailing mean).
   - `write_artifact(payload)` writes JSON under `artifacts/` with atomic replacement.

4. **CLI Interface**
   - `--once` (default) processes a single window.
   - `--watch` loops with sleep interval aligned to URIP beat (reads `rhythm_state.json.interval`).
   - `--emit-now` forces artifact creation regardless of thresholds.

---

## 6. Compatibility Considerations

- **Orchestrion** — Pattern Engine respects `Tempo` and `Priority` declarations to set window sizes and weighting. Missing spec triggers safe defaults (6s tempo, neutral priority).
- **URIP** — PEC delays heavy analyses until `next_release.token` entitles execution, ensuring no desynchronization with the Governor/Escapement doctrine.
- **Future Oracles** — Hooks ingest any `oracle_trinity/sync/*.json` to feed cohesion metrics.

---

## 7. Validation & Next Steps

- Unit-style smoke tests can run with synthetic windows fed through Fourier/Wavelet helpers.
- Once PEC artifacts accumulate, Claude-Balaur can review them for constitutional reflection; Gemini can stream the metrics to the Steampunk Hi-Fi gauges.
- Later releases: integrate mission/proposal logs, add MCP endpoint for artifact queries, wire dashboards.

---

**Status:** Drafted 2025-10-26 — ready for PEC v1 implementation.
