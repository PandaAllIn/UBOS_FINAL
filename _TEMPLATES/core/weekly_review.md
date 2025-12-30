---
type: weekly_review
week: <% tp.date.now("GGGG-[W]WW") %>
created: <% tp.date.now("YYYY-MM-DD HH:mm") %>
status: draft
tags: [weekly, review]
---

# Weekly Review — <% tp.date.now("GGGG-[W]WW") %>

## 📊 Highlights
- 

## ❗ Blockers / Risks
- 

## 🚀 Progress by Mission
```dataview
TABLE status, deadline, priority
FROM "03_OPERATIONS/missions"
WHERE status != "complete"
SORT priority ASC, deadline ASC
```

## 🌱 New Insights
- 

## 🔭 Next Week Plan
- 

## 🧭 Links
- [[_DASHBOARDS/MISSION_STATUS|Mission Control]]
- [[_DASHBOARDS/GRANT_PIPELINE|Grant Pipeline]]
- [[_DASHBOARDS/EMBASSY_INTEL|Embassy Intel]]
