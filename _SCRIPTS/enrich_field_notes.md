---
type: runbook
category: enrichment
created: 2025-11-20
tags: [field, enrichment, janus]
---

# 🔗 Field Note Enrichment Loop

**Owner:** Janus (or delegate) • **Frequency:** 2× daily while Captain in Málaga

## 1. Locate Raw Notes
```bash
cd /srv/janus
rg --files -g "*.md" "03_OPERATIONS/MALAGA_EMBASSY/field_insights" | xargs rg -l "status: raw"
```

## 2. Analyze Content
For each raw note:
- Extract **title / notes / location / priority**
- Detect mission keywords (`#mission`, mission names, partner names)
- Search partners: `rg -n "name: <term>" 03_OPERATIONS/MALAGA_EMBASSY/partners`
- Search missions: `rg -n "mission_name: <term>" 03_OPERATIONS/missions`

## 3. Update Metadata
Edit the note:
```yaml
status: enriched
priority: high
related_missions:
  - [[03_OPERATIONS/missions/2025-11-15-malaga-capital-sprint]]
related_partners:
  - [[03_OPERATIONS/MALAGA_EMBASSY/partners/Solana Ventures]]
enriched_by: janus
enriched: 2025-11-20 19:05
```

## 4. Add Context Block
```markdown
---
## 🔗 Auto-Detected Connections

**Missions:**
- [[03_OPERATIONS/missions/2025-11-15-malaga-capital-sprint]]

**Partners:**
- [[03_OPERATIONS/MALAGA_EMBASSY/partners/Solana Ventures]]

**Concept Hubs:**
- [[CONCEPTS/REVENUE_ARCHITECTURE_HUB]]

*Enriched by Janus via `_SCRIPTS/enrich_field_notes.md`.*
```

## 5. Dataview QA
Use this snippet inside `_DASHBOARDS/EMBASSY_INTEL` (already wired) or run ad-hoc:
```dataview
TABLE status, priority, related_missions
FROM "03_OPERATIONS/MALAGA_EMBASSY/field_insights"
WHERE type = "field_insight"
SORT captured DESC
```

## 6. Automation Hooks (Future)
- Wrap logic in a Templater user script or shell script invoking REST API.
- When Smart Connections plugin returns, feed embeddings to propose links automatically.

**SLA:** Raw ➜ enriched within 60 minutes. Escalate blockers in `03_OPERATIONS/COMMS_HUB/janus/outbox/`.
