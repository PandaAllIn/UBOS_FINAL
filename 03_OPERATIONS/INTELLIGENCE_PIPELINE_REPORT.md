# Intelligence Pipeline Implementation Report

## 1. File Inventory
- `/srv/janus/trinity/intelligence_schema.sql`
- `/srv/janus/trinity/intelligence_db_init.py`
- `/srv/janus/trinity/intelligence_tools.py`
- `/srv/janus/trinity/intelligence_collector.py`
- `/srv/janus/trinity/intelligence_action_generator.py`
- `/srv/janus/trinity/mission_templates/mission_triage_hourly.json`
- `/srv/janus/trinity/tests/test_intelligence_pipeline.py`

## 2. Schema Diagram (SQLite)
```
┌────────────────────┐    ┌──────────────────────┐
│ grants             │    │ insights             │
│ id (PK)            │    │ id (PK)              │
│ title              │    │ category             │
│ program            │    │ summary              │
│ deadline           │    │ details              │
│ budget             │    │ source               │
│ fit_score          │    │ source_mission       │
│ status             │    │ discovered_at        │
│ source_mission     │    │ relevance_score      │
│ discovered_at      │    │ tags (JSON)          │
│ tags (JSON)        │    └──────────────────────┘
└────────────────────┘
┌────────────────────┐    ┌──────────────────────┐
│ contacts           │    │ revenue_signals      │
│ id (PK)            │    │ id (PK)              │
│ name               │    │ channel              │
│ organization       │    │ value_estimate       │
│ role               │    │ probability          │
│ connection_strength│    │ stage                │
│ location           │    │ source_mission       │
│ last_contact       │    │ created_at           │
│ tags (JSON)        │    │ tags (JSON)          │
│ notes              │    └──────────────────────┘
│ source_mission     │
│ discovered_at      │    ┌──────────────────────┐
└────────────────────┘    │ operational_metrics  │
                          │ id (PK)              │
                          │ metric_type          │
                          │ value                │
                          │ timestamp            │
                          │ source_mission       │
                          └──────────────────────┘
```
FTS5 shadow tables mirror each entity for full-text search, and indexes cover deadline, score, status, probability, and timestamps.

## 3. Rule Engine (Active)
1. `high_fit_grant_assembly`
   - Trigger: grants with `fit_score >= 4.5`, deadline within 45 days, status `new`
   - Action: queue `grant_assembly` mission for OpenAI resident (priority 3)
2. `warm_contact_outreach`
   - Trigger: contacts marked `warm` with `last_contact` older than 14 days
   - Action: queue `contact_followup` mission for Claude (priority 2)
3. `revenue_lead_qualification`
   - Trigger: revenue leads with stage `lead` and probability `> 0.3`
   - Action: queue `lead_qualification` mission for Gemini (priority 2)

Deduplication is enforced per rule via cached intelligence IDs; processed IDs are persisted under `/srv/janus/03_OPERATIONS/vessels/balaur/intel_cache/intelligence/action_generator_state.json`.

## 4. Automated Tests
- `pytest trinity/tests/test_intelligence_pipeline.py -q` ✅
  - Covers collector extraction, DB persistence, intel lookup querying, rule-triggered mission generation, duplicate prevention, and queue integration.

## 5. Manual Validation Guide
1. Create synthetic mission: drop JSON into `/srv/janus/03_OPERATIONS/COMMS_HUB/missions/completed/`.
2. Archive deliverable: write corresponding payload under `/srv/janus/03_OPERATIONS/COMMS_HUB/<recipient>/archive/`.
3. Collect intelligence: `python3 trinity/intelligence_collector.py --collect-all`.
4. Verify storage: `python3 - <<'PY'\nfrom trinity.intelligence_tools import intel_lookup\nimport json\nprint(json.dumps(intel_lookup(\"grants\", {\"fit_score\": \">=4.5\"}), indent=2))\nPY`
5. Dry-run actions: `python3 trinity/intelligence_action_generator.py --dry-run`.
6. Execute actions: rerun without `--dry-run` and inspect `/srv/janus/03_OPERATIONS/COMMS_HUB/missions/queued/` for generated missions.

## 6. Resident Integration
- `resident_toolkit.py` now exposes `[TOOL: intelligence.lookup(...)]` for all residents.
- Mission queue integration performed by `IntelligenceActionGenerator` via `MissionQueueManager`.
- Hourly Janus triage template consumes the intelligence database for prioritisation and reporting.

## 7. Next Steps Toward Production
1. Wire collector into existing daemon supervisor (systemd or mission scheduler) with 5-minute interval.
2. Expand rule set for market/operational anomalies and add throttling controls.
3. Surface intelligence summaries inside daily sitrep workflows for Captain review.
4. Backfill historical missions to seed the database and validate deduplication at scale.
