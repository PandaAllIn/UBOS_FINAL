---
type: dashboard
category: embassy_operations
auto_refresh: true
created: 2025-11-16
tags: [dashboard, embassy, malaga, mallorca, intelligence, field-ops]
---

# 🏛️ EMBASSY INTELLIGENCE DASHBOARD

*Field operations monitor – Málaga & Mallorca at a glance*

**Málaga Status:** Physical base deployment imminent (week of Nov 18)  
**Mallorca Status:** Scientific operations active (Xylella Stage 2)  
**Treasury Target:** €1,500/month capital sprint

---

## 🇪🇸 MÁLAGA EMBASSY – CAPITAL SPRINT

```dataview
TABLE status, revenue_target, current_revenue, priority
FROM "03_OPERATIONS/MALAGA_EMBASSY"
WHERE type = "mission" OR type = "embassy_briefing"
SORT date DESC
LIMIT 1
```

### Recent Field Insights (last 10)

```dataview
LIST file.link
FROM "03_OPERATIONS/MALAGA_EMBASSY/field_insights"
WHERE type = "field_insight"
SORT captured DESC
LIMIT 10
```

### Partners & Meetings

```dataview
TABLE file.link AS Partner, status, relationship_strength, last_contacted
FROM "03_OPERATIONS/MALAGA_EMBASSY/partners"
WHERE type = "partner"
SORT relationship_strength DESC, last_contacted DESC
LIMIT 15
```

### Housing / Infrastructure Search

```dataview
TABLE status, owner, deadline
FROM "03_OPERATIONS/MALAGA_EMBASSY"
WHERE tags && ["housing"]
```

---

## 🏝️ MALLORCA EMBASSY – Xylella Field Ops

```dataview
TABLE file.link AS Mission, status, deadline, owner
FROM "03_OPERATIONS/grant_assembly/xylella-stage-2"
WHERE type = "grant_proposal"
```

### Scientific Signals / Protocols

```dataview
LIST file.link
FROM "03_OPERATIONS/mallorca_embassy"
WHERE type = "signal" OR tags && ["signal"]
LIMIT 10
```

---

## 📊 CAPITAL SPRINT METRICS

```dataviewjs
const capital = dv.pages('"03_OPERATIONS/MALAGA_EMBASSY"')
  .where(p => (p.capital_target ?? false) !== false);
capital.forEach(entry => {
  dv.list([
    `Target: €${entry.capital_target ?? 1500}`,
    `Current: €${entry.current_revenue ?? 0}`,
    `Coverage: ${entry.current_revenue && entry.capital_target ? Math.round((entry.current_revenue/entry.capital_target)*100) : 0}%`
  ]);
});
if (capital.length === 0) {
  dv.paragraph("_No capital metrics recorded. Include `capital_target` and `current_revenue` in Málaga embassy notes._");
}
```

---

## 📅 CAPTAIN DEPLOYMENT SCHEDULE

```dataview
LIST schedule
FROM "03_OPERATIONS/MALAGA_EMBASSY"
WHERE schedule
```

### Coordination Objectives
1. Establish Málaga HQ (Week of Nov 18)
2. Initiate Portal Oradea MVP revenue
3. Confirm Mallorca consortium partners
4. Advance capital sprint to ≥50 % (€750/month)

---

## 🔗 LINKS

- [[03_OPERATIONS/MALAGA_EMBASSY/strategic_plan/MALAGA_MASTER_PLAN|Málaga Master Plan]]
- [[03_OPERATIONS/mallorca_embassy/SIGNAL_QUERY_PROTOCOLS|Mallorca Signal Protocols]]
- [[03_OPERATIONS/malaga_embassy/briefings/|All Málaga Briefings]]
- Dashboards: [[_DASHBOARDS/MISSION_STATUS|← Mission Control]] | [[_DASHBOARDS/GRANT_PIPELINE|Grant Pipeline]] | [[OBSERVATORY_INDEX|Observatory →]]

---

*Add field insights via QuickAdd → Captain’s Log for instant inclusion.*
