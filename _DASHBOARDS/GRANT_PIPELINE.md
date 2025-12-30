---
type: dashboard
category: grant_tracking
auto_refresh: true
created: 2025-11-16
tags: [dashboard, grants, eu-funding, pipeline, revenue]
---

# 💎 EU GRANT PIPELINE DASHBOARD

*€70M+ opportunity tracker – the treasury’s fuel gauge*

**Last Scan:** 2025-11-16 (Groq Hunter)  
**Pipeline Value (frontmatter budget sum):** `=dv.pages('"03_OPERATIONS/grant_assembly"').where(p => p.type = "grant_proposal").reduce((s,p)=>s+(Number(p.value)||0),0)`  
**Assemblies in Progress:**  
```dataviewjs
const grants = dv.pages('"03_OPERATIONS/grant_assembly"')
  .where(p => (p.type ?? "").toLowerCase() === "grant_proposal");
const active = grants.where(p => ["active","draft","assembly"].includes((p.status ?? "").toLowerCase()));
const medium = grants.where(p => ["research","backlog"].includes((p.status ?? "").toLowerCase()));
dv.paragraph(`**High-Fit Active:** ${active.length} | **Research Phase:** ${medium.length} | **Total Opportunities:** ${grants.length}`);
if (grants.length === 0) {
  dv.paragraph("_No grant metadata found. Use `_TEMPLATES/strategy/grant_proposal.md` for new entries._");
}
```

---

## 🎯 HIGH-FIT OPPORTUNITIES

```dataview
TABLE file.link AS Opportunity,
  fit_score,
  status,
  value,
  deadline,
  owner
FROM "03_OPERATIONS/grant_assembly"
WHERE type = "grant_proposal" AND number(fit_score) >= 4
SORT number(fit_score) DESC, date(deadline) ASC
```

### Urgent Deadlines (< 30 days)

```dataview
LIST file.link
FROM "03_OPERATIONS/grant_assembly"
WHERE type = "grant_proposal"
  AND deadline
  AND deadline <= date(now) + dur(30 days)
  AND (status != "submitted" AND status != "awarded")
SORT deadline ASC
```

---

## 📋 ACTIVE GRANT ASSEMBLIES

### Geothermal Data Center – Phase 1

```dataview
TABLE work_packages, partners, status, budget
FROM "03_OPERATIONS/grant_assembly/geodatacenter-phase-1"
WHERE type = "grant_proposal" OR file.name = "README"
```

### Xylella Stage 2

```dataview
TABLE status, deadline, owner, budget
FROM "03_OPERATIONS/grant_assembly/xylella-stage-2"
WHERE type = "grant_proposal" OR file.name = "README"
```

---

## 💰 PIPELINE BREAKDOWN

```dataviewjs
const byStatus = {};
grants.forEach(g => {
  const status = (g.status ?? "unknown").toLowerCase();
  const value = Number(g.value) || 0;
  if (!byStatus[status]) byStatus[status] = {count:0, value:0};
  byStatus[status].count += 1;
  byStatus[status].value += value;
});
dv.table([\"Status\",\"Count\",\"Est. Value (€)\",
  ],
  Object.entries(byStatus).map(([status,data]) => [status, data.count, `€${data.value.toLocaleString(\"en-US\")}`]));
```

---

## 🎯 STRATEGIC PRIORITIZATION

1. **Geothermal Data Center (Priority 1)**  
   - Aligns with Phase 2.6 infrastructure sovereignty  
   - Estimated €20M+  
   - Submission: Q4 2025

2. **Xylella Stage 2 (Priority 2)**  
   - Tied to Captain’s Mallorca deployment  
   - Estimated €15M  
   - Deadline: Dec 2025

3. **Clean Energy Infrastructure (Priority 3)**  
   - Complementary to Geothermal  
   - Estimated €25M  
   - Submission: Q1 2026

---

## 📊 SUCCESS METRICS

```dataviewjs
const submitted = grants.where(p => ["submitted","awarded"].includes((p.status ?? "").toLowerCase()));
const awarded = grants.where(p => (p.status ?? "").toLowerCase() === "awarded");
dv.paragraph(`**Submitted:** ${submitted.length} | **Awarded:** ${awarded.length}`);
```

Velocity target: **1 major proposal per quarter**  
Current: `=active.length` active assemblies this quarter

---

## 🔗 RELATED RESOURCES

- Grant tools: [[trinity/skills/eu-grant-hunter/|EU Grant Hunter]], [[trinity/skills/grant-application-assembler/|Grant Assembler]], [[trinity/skills/financial-proposal-generator/|Financial Proposal Generator]]
- Strategic context: [[01_STRATEGY/ROADMAP|Roadmap]], [[01_STRATEGY/COUNCIL_OF_CREATORS_PROTOCOL|Council of Creators]]
- Dashboards: [[_DASHBOARDS/MISSION_STATUS|← Mission Control]] | [[_DASHBOARDS/EMBASSY_INTEL|Embassy Intel →]]

---

*Pipeline data auto-refreshes when new grant notes use the standardized template.*
