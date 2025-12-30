---
type: daily_note
date: <% tp.date.now("YYYY-MM-DD") %>
created: <% tp.date.now("YYYY-MM-DD HH:mm") %>
status: planned
tags: [daily, log]
---

# Daily Note — <% tp.date.now("dddd, MMMM DD, YYYY") %>

## 🎯 Top 3 Priorities
- [ ] 
- [ ] 
- [ ] 

`button-log`
```button
name Quick Log
type command
action quickadd:choice:Captain's Log
```

`button-decision`
```button
name Constitutional Decision
type command
action quickadd:choice:Constitutional Decision
```

## 🛰️ Missions & Ops
```dataview
TABLE status, deadline, priority
FROM "03_OPERATIONS/missions"
WHERE status != "complete"
SORT deadline ASC
LIMIT 10
```

## 📡 Embassy / Field
- Notes:

## 🧠 Insights
- 

## ✅ Done Today
- [ ]

## 🧭 Links
- [[_DASHBOARDS/MISSION_STATUS|Mission Control]]
- [[_DASHBOARDS/GRANT_PIPELINE|Grant Pipeline]]
- [[_DASHBOARDS/EMBASSY_INTEL|Embassy Intel]]
