# UBOS Metadata Standards

## 1. Mission Notes

```yaml
---
type: mission
mission_type: [embassy|grant|research|partnership|infrastructure]
status: [planning|active|paused|complete|cancelled]
priority: [critical|high|medium|low]
created: YYYY-MM-DD
deadline: YYYY-MM-DD
budget: number
constitutional_alignment: [verified|pending|failed]
trinity_lock_tier: [alpha|beta|omega]
responsible_agent: [claude|gemini|codex|janus|captain]
tags: [mission, type, priority]
---
```

Required: type, mission_type, status, created  
Queryable: all fields  
Used in templates: mission_creation.md, embassy_briefing.md

---

## 2. Partner Notes

```yaml
---
type: partner
name: string
category: [individual|organization|institution]
status: [prospect|active|partner|inactive]
location: [city, region, country]
first_contact: YYYY-MM-DD
last_contacted: YYYY-MM-DD
relationship_strength: [cold|warm|hot]
related_missions: []
tags: [partner, category, location]
---
```

Required: type, name, category, first_contact  
Used in: partner_contact.md

---

## 3. Field Insight Notes

```yaml
---
type: field_insight
category: [observation|opportunity|risk|pattern|contact]
captured: YYYY-MM-DD HH:mm
location: [city, region]
priority: [critical|high|medium|low]
status: [raw|enriched|integrated]
related_missions: []
tags: [field, category, location]
---
```

Required: type, captured  
Used in: captain_log.md

---

## 4. Concept Hub Notes

```yaml
---
type: concept_hub
concept_name: string
category: [principle|system|pattern|tool]
maturity: [genesis|developing|proven|refined]
importance: [critical|high|medium|low]
created: YYYY-MM-DD
updated: YYYY-MM-DD
field_validated: boolean
tags: [concept, category]
---
```

Required: type, concept_name, category  
Used in: concept_hub.md

---

## 5. Decision Notes

```yaml
---
type: constitutional_decision
decision_id: YYYYMMDDHHmm
date: YYYY-MM-DD
budget: number
trinity_lock_tier: [alpha|beta|omega]
vote_status: [pending|approved|rejected]
constitutional_alignment: [verified|pending|failed]
reversible: boolean
tags: [decision, tier]
---
```

Required: type, decision_id, date, budget, trinity_lock_tier  
Used in: constitutional_decision.md

---

## Validation Rules

1. `type` is always required (enables Dataview filtering).
2. Dates are ISO (YYYY-MM-DD) for consistency.
3. Status/priority are lowercase for query consistency.
4. Tags include the type for graph filtering.
5. Related fields should be arrays for multi-linking.

## Dashboard Query Example

```dataview
TABLE status, budget, deadline
FROM "03_OPERATIONS"
WHERE type = "mission" AND status = "active"
SORT priority DESC
```

---

**Created:** 2025-11-16  
**Maintained by:** Codex  
**Used by:** Templates and dashboards
