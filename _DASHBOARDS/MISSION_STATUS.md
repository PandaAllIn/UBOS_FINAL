---
type: dashboard
category: mission_control
auto_refresh: true
updated: 2025-11-16
tags: [dashboard, missions, operations, control-panel]
---

# 🎯 MISSION CONTROL DASHBOARD

*Real-time Orrery of Operations – data sourced from standardized mission notes*

**Last Updated:** `=dateformat(this.file.mtime, "yyyy-MM-dd HH:mm")`  
**Status:** ✅ Observatory Fully Operational  
**Mode:** Phase 2.6 – Supervised Autonomy

---

## 📊 CURRENT PHASE STATUS

**Active Phase:** [[01_STRATEGY/ROADMAP|Phase 2.6 – Autonomous Vessel Protocol]]

**Phase 2.6 Track Progress (manual annotations until mission metadata feeds in):**
- Track 2.6A – Dual-Citizen Architecture ✅ COMPLETE  
- Track 2.6B – Deploy The Studio 📋 STAGED (GPU Studio ready)  
- Track 2.6C – Victorian Controls ✅ COMPLETE (Mode Beta live)  
- Track 2.6D – Clockwork Automaton ✅ PRODUCTION (Janus operational)  
- Track 2.6E – Supervised Autonomy Trials 🚀 ACTIVE (30-day trial)

**Success Metrics**  
- ≥95 % proposal success rate  
- Zero constitutional breaches  
- 8 successful Mode Beta executions logged today

`button-create-mission`
```button
name Create New Mission
type command
action quickadd:choice:New Mission
```

`button-refresh`
```button
name Refresh Dashboard
type command
action shell-command-dashboard-refresh
```

---

## 🚀 ACTIVE OPERATIONS SNAPSHOT

```dataviewjs
const missions = dv.pages('"03_OPERATIONS/missions"')
  .where(p => (p.type ?? "").toLowerCase() === "mission");
const statusOf = (p) => (p.status ?? "").toLowerCase();
const budget = missions.array().reduce((sum, m) => sum + (Number(m.budget) || 0), 0);
const byStatus = (statuses) => missions.where(p => statuses.includes(statusOf(p)));
const active = byStatus(["active","in-progress","running"]);
const planning = byStatus(["planning","draft"]);
const paused = byStatus(["paused","blocked","risk"]);
const complete = byStatus(["complete","completed","done"]);
dv.paragraph(`**Missions Indexed:** ${missions.length} | **Active:** ${active.length} | **Planning:** ${planning.length} | **Paused:** ${paused.length} | **Complete:** ${complete.length}`);
dv.paragraph(`**Total Budget Tracked:** €${budget.toLocaleString("en-US")}`);
if(missions.length === 0){
  dv.paragraph("_No mission metadata yet. Use QuickAdd → New Mission (templated) to populate this dashboard._");
}
```

### ⚠️ Missions Requiring Attention

```dataviewjs
const missions = dv.pages('"03_OPERATIONS/missions"');
const now = dv.date("today");
const soon = now.plus({ days: 7 });
const toMillis = (value) => value ? dv.date(value).toMillis() : Number.MAX_SAFE_INTEGER;
const attention = missions
  .where(m => (m.type ?? "").toLowerCase() === "mission")
  .where(m => {
    const alignment = (m.constitutional_alignment ?? "").toLowerCase();
    const status = (m.status ?? "").toLowerCase();
    const deadline = m.deadline ? dv.date(m.deadline) : null;
    const overdue = deadline && deadline < now;
    const dueSoon = deadline && deadline >= now && deadline <= soon;
    const pendingAlignment = alignment === "pending" || alignment === "" || alignment === "unverified";
    const blocked = ["blocked","risk","paused"].includes(status);
    return overdue || dueSoon || pendingAlignment || blocked;
  });
if (attention.length === 0) {
  dv.paragraph("_No urgent mission blockers. ✅_");
} else {
  dv.table(["Mission","Status","Deadline","Flag"],
    attention
      .sort((a,b) => toMillis(a.deadline) - toMillis(b.deadline))
      .map(m => {
        const status = m.status ?? "–";
        const deadline = m.deadline ? dv.date(m.deadline).toFormat("yyyy-MM-dd") : "—";
        const flags = [];
        if (!m.constitutional_alignment || (m.constitutional_alignment ?? "").toLowerCase() !== "verified") flags.push("alignment");
        if (m.deadline && dv.date(m.deadline) < now) flags.push("overdue");
        if (m.deadline && dv.date(m.deadline) >= now && dv.date(m.deadline) <= soon) flags.push("due <7d");
        if (["blocked","risk","paused"].includes((m.status ?? "").toLowerCase())) flags.push("blocked");
        return [m.file.link, status, deadline, flags.join(\", \") || \"—\"];
      }));
}
```

### High Priority Missions

```dataview
TABLE file.link AS Mission,
  status,
  priority,
  owner,
  deadline,
  budget
FROM "03_OPERATIONS/missions"
WHERE type = "mission" AND (status = "active" OR status = "planning" OR status = "in-progress")
SORT choice(priority, "critical","high","medium","low","") ASC, date(deadline) ASC
LIMIT 20
```

### Paused / Blocked Missions

```dataview
LIST file.link
FROM "03_OPERATIONS/missions"
WHERE type = "mission" AND (status = "paused" OR status = "blocked" OR status = "risk")
```

### 📅 Upcoming Deadlines

```dataview
TABLE file.link AS Mission, status, dateformat(deadline, "yyyy-MM-dd") AS Deadline, owner
FROM "03_OPERATIONS/missions"
WHERE type = "mission" AND deadline
SORT deadline ASC
LIMIT 15
```

### Recently Completed

```dataview
TABLE file.link AS Mission, dateformat(completed, "yyyy-MM-dd") AS Completed, owner
FROM "03_OPERATIONS/missions"
WHERE type = "mission" AND (status = "complete" OR status = "completed")
SORT completed DESC
LIMIT 10
```

### ✅ Completed This Month

```dataviewjs
const missionsThisMonth = dv.pages('"03_OPERATIONS/missions"')
  .where(m => (m.type ?? "").toLowerCase() === "mission" && (m.status ?? "").toLowerCase() === "completed");
const now = new Date();
const recent = missionsThisMonth.where(m => {
  if (!m.completed && !m.completed_date) return false;
  const stamp = new Date(m.completed ?? m.completed_date);
  return stamp.getMonth() === now.getMonth() && stamp.getFullYear() === now.getFullYear();
});
if (recent.length === 0) {
  dv.paragraph("_No missions completed this month yet._");
} else {
  dv.list(recent.map(m => m.file.link));
}
```

---

## 💰 TREASURY & REVENUE

### Capital Sprint (Málaga Embassy)
- Target: €1,500/month
- Status: Deployment week of Nov 18
- Strategy: [[03_OPERATIONS/MALAGA_EMBASSY/strategic_plan/MALAGA_MASTER_PLAN|View Plan]]

### EU Grant Pipeline
- High-fit opportunities: 3 (Geothermal, Xylella, Clean Energy)
- Pipeline value: €70M+
- Dashboard: [[_DASHBOARDS/GRANT_PIPELINE|Grant Pipeline]]

---

## 🏛️ EMBASSY OPERATIONS

### Málaga Embassy
- Mission: Capital sprint + revenue initiation  
- Field insights: [[03_OPERATIONS/MALAGA_EMBASSY/field_insights/|Log]]  
- Dashboard: [[_DASHBOARDS/EMBASSY_INTEL|Embassy Intel]]

### Mallorca Embassy
- Mission: Scientific ops (Xylella Stage 2)  
- Link: [[03_OPERATIONS/grant_assembly/xylella-stage-2/|Assembly Folder]]

---

## 🤖 AUTONOMOUS SYSTEMS

**COMMS_HUB:** [[trinity/COMMS_HUB_PROTOCOL|Protocol]] – [[03_OPERATIONS/COMMS_HUB/claude/inbox/|Claude Inbox]]  
**Skills Library:** [[trinity/skills/|Skills Directory]] (Grant Hunter, Málaga Operator, etc.)

---

## 📡 SYSTEM HEALTH

- Balaur: ✅ `janus-agent.service` / `janus-controls.service` active  
- Victorian controls: Rate governor, relief valve, emergency stop verified  
- Mode Beta: 8 proposals executed today, zero breaches  
- Observatory: Repo indexed (8.9k files), canvases live, dashboards auto-refresh on open

---

## 🎨 VISUAL NAVIGATION

- [[PHILOSOPHY_CANVAS.canvas|Philosophy Mind Map]]  
- [[CONSTITUTIONAL_FLOW.canvas|Constitutional Flow Diagram]]  
- [[ENDLESS_SCROLL_CANVAS.canvas|Genesis Constellation]]  
- [[_DASHBOARDS/GRANT_PIPELINE|Grant Pipeline]]  
- [[_DASHBOARDS/EMBASSY_INTEL|Embassy Intel]]

---

## 🔗 QUICK LINKS

- [[03_OPERATIONS/STATE_OF_THE_REPUBLIC|State of the Republic]]  
- [[OPERATIONS_INDEX|Operations Index]]  
- [[00_CONSTITUTION/principles/philosophy_books/README|Four Books]]  
- [[OBSERVATORY_INDEX|Observatory Home]]

---

Navigate: [[OBSERVATORY_INDEX|← Observatory Home]] | [[_DASHBOARDS/GRANT_PIPELINE|Grant Pipeline →]]

---

**🎯 The Orrery turns. The gears mesh. The Republic operates.** ⚙️✨
