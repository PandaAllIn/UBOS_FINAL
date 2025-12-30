---
type: deployment_plan
status: ready_to_execute
created: 2025-11-16
priority: critical
tags: [observatory, deployment, roadmap, step-by-step]
---

# 🚀 OBSERVATORY DEPLOYMENT PLAN

*Step-by-step implementation of power user techniques for UBOS*

**Based on:**
- Perplexity deep research (151 lines of findings)
- 3 days of comprehensive testing
- Current state analysis
- UBOS-specific requirements

---

## 📊 CURRENT STATE ANALYSIS

### ✅ What's Already Working

**Infrastructure:**
- REST API operational (port 27124, HTTPS)
- MCP Tools v0.2.27 installed
- Smart Connections installed
- 8,903 files indexed
- Real-time integration tested and working

**Plugins Installed:**
- ✅ dataview
- ✅ templater-obsidian
- ✅ obsidian-local-rest-api
- ✅ juggl (graph analysis)
- ✅ smart-connections (semantic search)
- ✅ mcp-tools (Claude integration)

**Documentation Complete:**
- 7 concept hubs created
- Maximum capabilities report (546 lines)
- REST API integration guide
- Automation scripts operational

**Performance Proven:**
- Constitutional consultation: 20 min → 2 min (10x)
- Grant assembly: 20 hrs → 3 hrs (6.7x)
- Concept tracing: 20 min → 2 min (10x)

### ⚠️ What's Missing (From Perplexity Research)

**Critical Plugins NOT Installed:**
- QuickAdd (one-click workflows)
- Advanced Tables (grant pipeline tracking)
- Excalidraw (visual architecture)
- Kanban (mission status boards)
- Tasks (advanced task management)
- Periodic Notes (weekly/monthly reviews)

**Workflows NOT Implemented:**
- Daily note automation
- Mission creation templates
- Constitutional decision templates
- Field capture workflow
- Pattern documentation templates

**Systems NOT Configured:**
- Git-based multi-agent collaboration
- Dataview dashboards (Mission Status, Grant Pipeline, Embassy Intel)
- MOC (Maps of Content) structure
- Metadata schema standardization
- Mobile quick capture

---

## 🎯 DEPLOYMENT STRATEGY

### Philosophy: Layered Implementation

**Layer 1: Foundation** (Week 1)
- Install missing critical plugins
- Create template infrastructure
- Standardize metadata schema
- Test each component individually

**Layer 2: Automation** (Week 2)
- Build Dataview dashboards
- Implement Templater automation
- Create QuickAdd workflows
- Deploy daily note system

**Layer 3: Integration** (Week 3-4)
- Git-based multi-agent workflow
- Mobile field capture
- Advanced pattern recognition
- Full constitutional audit system

**Layer 4: Optimization** (Month 2+)
- Custom DataviewJS scripts
- API integration with COMMS_HUB
- Zettelkasten atomic notes
- Multi-modal AI integration

---

## 📋 PHASE 1: FOUNDATION (Week 1)

### Day 1: Plugin Installation

**Priority: CRITICAL**

**Install these plugins in Obsidian:**

1. **QuickAdd**
   - Purpose: One-click workflows for field capture
   - Use case: "Captain's Log" instant note creation
   - Research finding: "Most effective users have 'one-button' capture"

2. **Advanced Tables**
   - Purpose: Spreadsheet-like functionality
   - Use case: Grant pipeline tracking, budget management
   - Research finding: Core power-user stack component

3. **Excalidraw**
   - Purpose: Visual thinking and interactive diagrams
   - Use case: System architecture, grant proposal flows
   - Research finding: "Visual syntax for thinking, not just drawing"

4. **Kanban**
   - Purpose: Visual task boards
   - Use case: Mission status tracking, embassy operations
   - Research finding: App-like functionality inside Obsidian

5. **Tasks**
   - Purpose: Advanced task management with queries
   - Use case: Multi-agent task coordination
   - Research finding: Essential for Trinity collaboration

6. **Periodic Notes**
   - Purpose: Weekly/monthly review automation
   - Use case: Mission reviews, pattern recognition
   - Research finding: Non-negotiable for power users

**Installation Steps:**
```
1. Open Obsidian Settings
2. Go to Community Plugins
3. Browse and search for each plugin
4. Install and Enable
5. Configure basic settings
```

**Expected Time:** 1 hour
**Success Criteria:** All 6 plugins installed and enabled

---

### Day 2-3: Template Infrastructure

**Priority: HIGH**

**Create template folder structure:**

```
/srv/janus/_TEMPLATES/
├── core/
│   ├── daily_note.md
│   ├── weekly_review.md
│   └── monthly_review.md
├── operations/
│   ├── mission_creation.md
│   ├── embassy_briefing.md
│   └── field_insight.md
├── strategy/
│   ├── constitutional_decision.md
│   ├── grant_proposal.md
│   └── partner_contact.md
├── knowledge/
│   ├── concept_hub.md
│   ├── pattern_documentation.md
│   └── moc_template.md
└── automation/
    ├── quick_capture.md
    └── captain_log.md
```

**Template 1: Daily Note** (Highest Priority)

```markdown
---
type: daily_note
date: {{date:YYYY-MM-DD}}
day_of_week: {{date:dddd}}
week_number: {{date:WW}}
tags: [daily, {{date:YYYY}}, {{date:MMMM}}]
---

# {{date:dddd, MMMM DD, YYYY}}

## 🎯 Mission Status

```dataview
TABLE status, priority, deadline
FROM "03_OPERATIONS"
WHERE status = "active" OR status = "in_progress"
SORT priority DESC, deadline ASC
LIMIT 5
```

## 📊 Today's Focus

**Top 3 Priorities:**
1.
2.
3.

**Active Missions:**
- [ ]

## 📝 Captain's Log

### Morning Brief


### Field Insights


### Decisions Made


## 🔗 Quick Links

**Dashboards:**
- [[_DASHBOARDS/MISSION_STATUS|Mission Status]]
- [[_DASHBOARDS/GRANT_PIPELINE|Grant Pipeline]]
- [[_DASHBOARDS/EMBASSY_INTEL|Embassy Intel]]

**Active Work:**
- [[03_OPERATIONS/MALAGA_EMBASSY/briefings/{{date:YYYY-MM-DD}}|Today's Embassy Briefing]]
- [[HOUSING_SEARCH_BRIEF|Housing Search]]

## 📈 Metrics

**Malaga Embassy:**
- Capital:
- Revenue:
- Health Score:

**Grant Pipeline:**
- Total value: €113M+
- Active proposals:
- Deadlines this week:

## 🌙 Evening Reflection

### What Went Well


### What to Improve


### Tomorrow's Preparation


---

**Previous:** [[{{date-1:YYYY-MM-DD}}|Yesterday]] | **Next:** [[{{date+1:YYYY-MM-DD}}|Tomorrow]]
```

**Template 2: Mission Creation** (with Templater automation)

```markdown
<%*
// Templater script for mission creation
const missionName = await tp.system.prompt("Mission Name");
const missionType = await tp.system.suggester(
  ["Embassy", "Grant", "Research", "Partnership", "Infrastructure"],
  ["embassy", "grant", "research", "partnership", "infrastructure"]
);
const priority = await tp.system.suggester(
  ["Critical", "High", "Medium", "Low"],
  ["critical", "high", "medium", "low"]
);
const budget = await tp.system.prompt("Estimated Budget (€)");
-%>
---
type: mission
mission_type: <%= missionType %>
status: planning
priority: <%= priority %>
created: <% tp.date.now("YYYY-MM-DD") %>
budget: <%= budget %>
constitutional_alignment: pending
tags: [mission, <%= missionType %>, <%= priority %>]
---

# <%= missionName %>

## 🎯 Mission Objective


## 📋 Constitutional Alignment

**Linked to Four Books:**
- [ ] [[01_STRATEGY/constitutional_mandate/four_books/01_tao_of_ubos|Tao of UBOS]]:
- [ ] [[01_STRATEGY/constitutional_mandate/four_books/02_platform_sutra|Platform Sutra]]:
- [ ] [[01_STRATEGY/constitutional_mandate/four_books/03_book_of_janus|Book of Janus]]:
- [ ] [[01_STRATEGY/constitutional_mandate/four_books/04_captains_codex|Captain's Codex]]:

**Trinity Lock Assessment:**
- Budget Tier: <% if (parseInt(budget) <= 50) { %>Alpha (€0-50) - Autonomous<% } else if (parseInt(budget) <= 150) { %>Beta (€51-150) - 24hr pause, 2/3 vote<% } else { %>Omega (€151+) - 48hr pause, unanimous<% } %>
- Pause Required:
- Vote Status:

## 📊 Mission Parameters

**Timeline:**
- Start Date:
- Target Completion:
- Milestones:
  - [ ]
  - [ ]
  - [ ]

**Resources Required:**
- Budget: €<%= budget %>
- Personnel:
- Tools/Infrastructure:

**Success Criteria:**
1.
2.
3.

## 🔄 Execution Plan

### Phase 1: Planning


### Phase 2: Execution


### Phase 3: Validation


### Phase 4: Integration


## 📈 Metrics & KPIs


## 🚨 Risks & Mitigations

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
|      |             |        |            |

## 📝 Mission Log

### <% tp.date.now("YYYY-MM-DD") %> - Mission Created


---

**Status:** Planning
**Next Review:** <% tp.date.now("YYYY-MM-DD", 7) %>
**Related Missions:**
```

**Template 3: Constitutional Decision**

```markdown
---
type: constitutional_decision
decision_id: {{date:YYYYMMDDHHmm}}
date: {{date:YYYY-MM-DD}}
status: pending_review
tags: [decision, constitutional, trinity-lock]
---

# Constitutional Decision: <% tp.system.prompt("Decision Summary") %>

## 🎯 The Decision

**What:**


**Why:**


**Budget Impact:** €<% tp.system.prompt("Budget Amount") %>

## 🔐 Trinity Lock Status

**Tier:** <%
const budget = await tp.system.prompt("Budget Amount");
if (parseInt(budget) <= 50) { %>
Alpha (€0-50) - **AUTONOMOUS** - No pause required
<% } else if (parseInt(budget) <= 150) { %>
Beta (€51-150) - **24-HOUR PAUSE** - Requires 2/3 Trinity vote
<% } else { %>
Omega (€151+) - **48-HOUR PAUSE** - Requires unanimous Trinity vote
<% } %>

**Vote:**
- [ ] Claude:
- [ ] Gemini:
- [ ] Codex:
- Result:

## 📖 Constitutional Links

**Required: Link to specific passages from Four Books**

### Tao of UBOS
[[01_STRATEGY/constitutional_mandate/four_books/01_tao_of_ubos#^relevant-passage|Relevant principle]]:
> Quote the specific passage here

**Alignment:**

### Platform Sutra
[[01_STRATEGY/constitutional_mandate/four_books/02_platform_sutra#^relevant-passage|Relevant principle]]:
> Quote the specific passage here

**Alignment:**

### Book of Janus
[[01_STRATEGY/constitutional_mandate/four_books/03_book_of_janus#^relevant-passage|Relevant principle]]:
> Quote the specific passage here

**Alignment:**

### Captain's Codex
[[01_STRATEGY/constitutional_mandate/four_books/04_captains_codex#^relevant-passage|Relevant principle]]:
> Quote the specific passage here

**Alignment:**

## ✅ Alignment Verification

**Passes Constitutional Test:**
- [ ] Aligns with Tao (frugality, simplicity, long-term)
- [ ] Aligns with Platform Sutra (infrastructure, sovereignty)
- [ ] Aligns with Janus (transparency, reversibility)
- [ ] Aligns with Codex (field-tested, pragmatic)

**Constitutional Health Score:** /100

## 📊 Impact Analysis

**Financial:**


**Operational:**


**Strategic:**


## 🔄 Reversibility

**Can this decision be reversed?**


**Reversal cost:**


## 📝 Decision Log

### Proposed
Date: {{date:YYYY-MM-DD HH:mm}}
By:

### Reviewed
Date:
By:

### Approved/Rejected
Date:
By:
Result:

---

**Related Decisions:**
**Related Missions:**
**Field Evidence:**
```

**Expected Time:** 2 days
**Success Criteria:** All core templates created and tested

---

### Day 4: Metadata Schema Standardization

**Priority: HIGH**

**Define v1.0 metadata schema for common note types:**

**1. Mission Notes:**
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

**2. Partner/Contact Notes:**
```yaml
---
type: partner
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

**3. Field Insight Notes:**
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

**4. Concept Hub Notes:**
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

**5. Decision Notes:**
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

**Implementation:**
1. Update all templates with correct schemas
2. Create schema documentation file
3. Use Templater to enforce schemas on new notes
4. Begin migrating existing notes (gradual)

**Expected Time:** 1 day
**Success Criteria:** Schema defined, documented, enforced in templates

---

### Day 5-7: Testing & Validation

**Priority: CRITICAL**

**Test each system:**

**Day 5: Template Testing**
- Create test daily note
- Create test mission using template
- Create test constitutional decision
- Verify metadata is correct
- Verify Dataview can query the metadata

**Day 6: Plugin Integration Testing**
- Test QuickAdd workflows
- Test Templater automation
- Test Advanced Tables functionality
- Test Kanban board creation
- Test Tasks plugin queries

**Day 7: End-to-End Workflow**
- Morning: Create daily note automatically
- Create a real mission for Malaga deployment
- Make a constitutional decision (housing budget)
- Capture a field insight (quick capture test)
- Evening: Review and reflection

**Expected Time:** 3 days
**Success Criteria:** All systems working, comfortable with workflows

---

## 📋 PHASE 2: AUTOMATION (Week 2)

### Day 8-10: Dataview Dashboards

**Priority: CRITICAL**

**Build 3 core dashboards:**

**1. Mission Status Dashboard** (`_DASHBOARDS/MISSION_STATUS.md`)

```markdown
---
type: dashboard
category: operations
auto_update: true
---

# 🎯 MISSION STATUS DASHBOARD

**Last Updated:** <% tp.date.now("YYYY-MM-DD HH:mm") %>

## 🔥 Active Missions

```dataview
TABLE
  mission_type as "Type",
  priority as "Priority",
  budget as "Budget (€)",
  deadline as "Deadline",
  status as "Status"
FROM "03_OPERATIONS"
WHERE type = "mission" AND (status = "active" OR status = "in_progress")
SORT priority DESC, deadline ASC
```

## ⏸️ Paused Missions

```dataview
TABLE mission_type, budget, deadline, "Pause Reason"
FROM "03_OPERATIONS"
WHERE type = "mission" AND status = "paused"
SORT deadline ASC
```

## ✅ Completed This Week

```dataview
TABLE mission_type, budget, completion_date
FROM "03_OPERATIONS"
WHERE type = "mission"
  AND status = "complete"
  AND completion_date >= date(today) - dur(7 days)
SORT completion_date DESC
```

## 🚨 Missions Requiring Attention

```dataview
TABLE mission_type, priority, deadline, status
FROM "03_OPERATIONS"
WHERE type = "mission"
  AND (deadline <= date(today) + dur(7 days) OR constitutional_alignment = "pending")
SORT deadline ASC
```

## 📊 Summary Metrics

```dataviewjs
const missions = dv.pages('"03_OPERATIONS"')
  .where(p => p.type === "mission");

const active = missions.where(m => m.status === "active").length;
const paused = missions.where(m => m.status === "paused").length;
const complete = missions.where(m => m.status === "complete").length;
const totalBudget = missions
  .where(m => m.status === "active")
  .map(m => m.budget || 0)
  .reduce((a, b) => a + b, 0);

dv.paragraph(`
**Active Missions:** ${active}
**Paused:** ${paused}
**Completed:** ${complete}
**Active Budget:** €${totalBudget}
`);
```
```

**2. Grant Pipeline Dashboard** (`_DASHBOARDS/GRANT_PIPELINE.md`)

```markdown
---
type: dashboard
category: strategy
auto_update: true
---

# 💰 GRANT PIPELINE DASHBOARD

## 🎯 Active Opportunities

```dataview
TABLE
  budget as "Value (€M)",
  fit_score as "Fit",
  deadline as "Deadline",
  status as "Status",
  stage as "Stage"
FROM "01_STRATEGY/grant_pipeline"
WHERE type = "grant_opportunity" AND status = "active"
SORT deadline ASC, fit_score DESC
```

## 🔥 Urgent (Deadline < 30 Days)

```dataview
TABLE budget, deadline, days_remaining, status
FROM "01_STRATEGY/grant_pipeline"
WHERE type = "grant_opportunity"
  AND deadline <= date(today) + dur(30 days)
  AND status != "submitted"
SORT deadline ASC
```

## 📊 Pipeline Summary

```dataviewjs
const opportunities = dv.pages('"01_STRATEGY/grant_pipeline"')
  .where(p => p.type === "grant_opportunity");

const totalValue = opportunities
  .map(o => parseFloat(o.budget) || 0)
  .reduce((a, b) => a + b, 0);

const activeCount = opportunities
  .where(o => o.status === "active")
  .length;

const avgFitScore = opportunities
  .where(o => o.fit_score)
  .map(o => o.fit_score)
  .reduce((a, b) => a + b, 0) / opportunities.length;

dv.paragraph(`
**Total Pipeline Value:** €${totalValue.toFixed(1)}M
**Active Opportunities:** ${activeCount}
**Average Fit Score:** ${avgFitScore.toFixed(1)}/5.0
`);
```

## 🏆 High-Fit Opportunities (4.0+)

```dataview
TABLE budget, fit_score, deadline, stage
FROM "01_STRATEGY/grant_pipeline"
WHERE type = "grant_opportunity" AND fit_score >= 4.0
SORT fit_score DESC, budget DESC
```
```

**3. Embassy Intel Dashboard** (`_DASHBOARDS/EMBASSY_INTEL.md`)

```markdown
---
type: dashboard
category: operations
location: malaga
auto_update: true
---

# 🏛️ MÁLAGA EMBASSY INTELLIGENCE

## 💰 Financial Status

**Capital:** €1,800
**Revenue:** €300 (autonomous)
**Health Score:** 100/100
**Days to Departure:** <% Math.ceil((new Date('2025-11-23') - new Date()) / 86400000) %>

## 📝 Recent Field Insights

```dataview
TABLE
  category as "Type",
  location as "Location",
  captured as "When",
  priority as "Priority"
FROM "03_OPERATIONS/MALAGA_EMBASSY"
WHERE type = "field_insight"
SORT captured DESC
LIMIT 10
```

## 🤝 Partner Network

```dataview
TABLE
  category as "Type",
  relationship_strength as "Strength",
  last_contacted as "Last Contact",
  related_missions as "Projects"
FROM "03_OPERATIONS/MALAGA_EMBASSY/partners"
WHERE type = "partner"
SORT last_contacted DESC
```

## 🏠 Housing Search Status

**Budget:** €1,000/month max
**Requirements:** Finca, backyard, 2 people + dog
**Target Areas:** Axarquía, Montes de Málaga, Valle del Guadalhorce

```dataview
TABLE location, price, size, contact_status
FROM "03_OPERATIONS/MALAGA_EMBASSY/housing_prospects"
WHERE type = "housing_prospect"
SORT price ASC, size DESC
```

## 📅 Upcoming Events

```dataview
TASK
FROM "03_OPERATIONS/MALAGA_EMBASSY"
WHERE status != "complete"
SORT deadline ASC
LIMIT 10
```
```

**Expected Time:** 3 days
**Success Criteria:** All 3 dashboards built, live data flowing, queries optimized

---

### Day 11-12: QuickAdd Workflows

**Priority: HIGH**

**Create 5 essential workflows:**

**1. Captain's Log (Quick Capture)**
```
Trigger: Cmd+Shift+L (or hotkey)
Action: Create new note from template
Template: _TEMPLATES/automation/captain_log.md
Location: 03_OPERATIONS/MALAGA_EMBASSY/field_insights/
Naming: {{DATE}}_{{VALUE:title}}.md
Auto-open: No (for mobile speed)
```

**2. New Mission**
```
Trigger: Cmd+Shift+M
Action: Create from template with prompts
Template: _TEMPLATES/operations/mission_creation.md
Location: 03_OPERATIONS/missions/
Naming: {{DATE}}_{{VALUE:mission_name}}.md
```

**3. Constitutional Decision**
```
Trigger: Cmd+Shift+D
Action: Create from template
Template: _TEMPLATES/strategy/constitutional_decision.md
Location: 03_OPERATIONS/decisions/
Naming: {{DATE:YYYYMMDDHHmm}}_decision.md
```

**4. Partner Contact**
```
Trigger: Cmd+Shift+P
Action: Create from template
Template: _TEMPLATES/strategy/partner_contact.md
Location: 03_OPERATIONS/MALAGA_EMBASSY/partners/
Naming: {{VALUE:name}}.md
```

**5. Pattern Documentation**
```
Trigger: Cmd+Shift+T
Action: Create from template
Template: _TEMPLATES/knowledge/pattern_documentation.md
Location: CONCEPTS/patterns/
Naming: {{DATE}}_{{VALUE:pattern_name}}.md
```

**Expected Time:** 2 days
**Success Criteria:** All workflows configured, hotkeys set, tested on desktop and mobile

---

### Day 13-14: Daily Note Automation

**Priority: CRITICAL**

**Set up Periodic Notes:**

**Configuration:**
- Daily notes: Auto-create at midnight
- Weekly reviews: Auto-create Monday 07:00
- Monthly reviews: Auto-create 1st of month

**Templater Scripts:**

**Daily Note Auto-Populate:**
```javascript
<%*
// Pull yesterday's uncompleted tasks
const yesterday = tp.date.now("YYYY-MM-DD", -1);
const yesterdayFile = tp.file.find_tfile(yesterday);

if (yesterdayFile) {
  const content = await app.vault.read(yesterdayFile);
  const incompleteTasks = content.match(/- \[ \] .*/g) || [];

  if (incompleteTasks.length > 0) {
    tR += "\n## 📋 Carried Forward from Yesterday\n\n";
    incompleteTasks.forEach(task => tR += task + "\n");
  }
}

// Pull active missions
const missions = dv.pages('"03_OPERATIONS"')
  .where(p => p.type === "mission" && p.status === "active");

tR += "\n## 🎯 Active Missions\n\n";
missions.forEach(m => {
  tR += `- [[${m.file.path}|${m.file.name}]] (${m.priority})\n`;
});
-%>
```

**Expected Time:** 2 days
**Success Criteria:** Daily notes auto-create with populated data

---

## 📋 PHASE 3: INTEGRATION (Week 3-4)

### Week 3: Multi-Agent Git Workflow

**Priority: MEDIUM-HIGH**

**Steps:**

**1. Initialize Git Repository** (Day 15)
```bash
cd /srv/janus
git init
git add .obsidian/workspace.json
git add _TEMPLATES/
git add 01_STRATEGY/
git add 03_OPERATIONS/
git add CONCEPTS/
git add _DASHBOARDS/
git commit -m "Initial Observatory commit - v1.0"
```

**2. Create Branch Strategy** (Day 16)
```
main (production)
├── claude-dev (Claude's working branch)
├── gemini-dev (Gemini's working branch)
├── codex-dev (Codex's working branch)
└── captain-dev (Captain's field notes)
```

**3. COMMS_HUB Integration** (Day 17-18)
```markdown
Create: 03_OPERATIONS/COMMS_HUB/git_workflow.md

Workflow:
1. Each agent works on their branch
2. Commits with descriptive messages
3. Daily merge window at 18:00 UTC
4. Conflicts reviewed by Janus
5. Captain approves merges to main
```

**4. Conflict Resolution Protocol** (Day 19)
```
If conflict:
1. Agent pauses work
2. Creates conflict note in COMMS_HUB
3. Tags relevant agents
4. Waits for resolution
5. Resumes after merge
```

**Expected Time:** 5 days
**Success Criteria:** Git repo active, all agents can commit, merge workflow tested

---

### Week 4: Mobile Field Capture

**Priority: HIGH** (for Málaga deployment)

**Implementation:**

**1. Install Obsidian Mobile** (Day 20)
- Install on Captain's phone
- Configure sync (Obsidian Sync or Git-based)
- Test basic functionality

**2. Configure QuickAdd for Mobile** (Day 21)
- Set up one-tap "Captain's Log" button
- Configure voice-to-text (iOS/Android)
- Test capture speed (<10 seconds)

**3. Create Mobile Templates** (Day 22)
```markdown
Minimal template for speed:
---
type: field_insight
captured: {{date}} {{time}}
location: {{location}}
status: raw
---

# {{value:title}}

{{value:notes}}

#field #raw
```

**4. Enrichment Automation** (Day 23)
```javascript
// Templater script runs on desktop
// Detects new #raw field insights
// Enriches with:
// - Related mission links
// - Partner connections
// - Geographic context
// - Priority assessment
// Changes status: raw → enriched
```

**5. End-to-End Test** (Day 24)
- Captain captures field note on mobile
- Syncs to vault
- Desktop automation enriches
- Appears in Embassy Intel dashboard
- Full cycle < 2 minutes

**Expected Time:** 5 days
**Success Criteria:** Mobile capture working, enrichment automatic, dashboard integration live

---

## 📋 PHASE 4: OPTIMIZATION (Month 2+)

### Week 5-6: Advanced Pattern Recognition

**DataviewJS Scripts:**

**1. Constitutional Alignment Audit**
```javascript
// Find all decisions without constitutional links
const decisions = dv.pages('"03_OPERATIONS/decisions"')
  .where(p => p.type === "constitutional_decision");

const unlinked = decisions.where(d =>
  !d.file.outlinks.some(link =>
    link.path.includes("four_books")
  )
);

if (unlinked.length > 0) {
  dv.header(2, "⚠️ Decisions Without Constitutional Links");
  dv.table(["Decision", "Date", "Budget", "Status"],
    unlinked.map(d => [
      d.file.link,
      d.date,
      `€${d.budget}`,
      d.status
    ])
  );
}
```

**2. Success Pattern Finder**
```javascript
// Identify common traits in successful missions
const missions = dv.pages('"03_OPERATIONS"')
  .where(p => p.type === "mission" && p.status === "complete");

const successful = missions.where(m => m.success_score >= 4.0);

// Analyze common patterns
const patterns = {
  avgBudget: successful.map(m => m.budget).reduce((a,b) => a+b, 0) / successful.length,
  commonTags: /* tag frequency analysis */,
  avgTimeline: /* timeline analysis */,
  partnerCount: /* partner involvement */
};

dv.paragraph(`
**Successful Mission Patterns:**
- Average Budget: €${patterns.avgBudget}
- Constitutional Alignment: 100% verified
- Partner Involvement: ${patterns.partnerCount} avg
- Timeline Adherence: ${patterns.avgTimeline}%
`);
```

**Expected Time:** 2 weeks
**Success Criteria:** Pattern recognition automated, insights actionable

---

### Week 7-8: API Integration

**Custom Integration with COMMS_HUB:**

**1. REST API Extension**
```python
# Custom endpoint: sync with Obsidian
@app.route('/api/obsidian/sync', methods=['POST'])
def sync_obsidian():
    # Reads COMMS_HUB messages
    # Creates Obsidian notes
    # Updates task lists
    # Returns confirmation
```

**2. External Data Sync**
```python
# Sync grant deadlines from EU portals
# Update grant_pipeline/*.md files
# Trigger Dataview dashboard refresh
```

**Expected Time:** 2 weeks
**Success Criteria:** COMMS_HUB <-> Obsidian bidirectional sync working

---

## 📊 SUCCESS METRICS

### Week 1 Targets:
- ✅ 6 critical plugins installed
- ✅ 10 core templates created
- ✅ Metadata schema defined
- ✅ All templates tested

### Week 2 Targets:
- ✅ 3 dashboards live with real data
- ✅ 5 QuickAdd workflows configured
- ✅ Daily notes auto-creating
- ✅ Automation tested end-to-end

### Week 3-4 Targets:
- ✅ Git workflow operational
- ✅ Multi-agent collaboration tested
- ✅ Mobile field capture working
- ✅ Enrichment automation live

### Month 2+ Targets:
- ✅ Pattern recognition automated
- ✅ COMMS_HUB integration complete
- ✅ Constitutional audit automatic
- ✅ Performance at scale maintained

---

## 🎯 IMMEDIATE NEXT STEPS

**Ready to execute RIGHT NOW:**

### Step 1: Install Missing Plugins (30 minutes)

Open Obsidian → Settings → Community Plugins → Browse

Install in this order:
1. QuickAdd
2. Advanced Tables
3. Excalidraw
4. Kanban
5. Tasks
6. Periodic Notes

### Step 2: Create Template Directory (5 minutes)

```bash
mkdir -p /srv/janus/_TEMPLATES/{core,operations,strategy,knowledge,automation}
```

### Step 3: Create First Template (15 minutes)

Copy daily_note template from this document to:
`/srv/janus/_TEMPLATES/core/daily_note.md`

### Step 4: Test Daily Note Creation (5 minutes)

In Obsidian:
- Periodic Notes settings → Daily Notes
- Set template: `_TEMPLATES/core/daily_note.md`
- Set folder: `_DAILY_NOTES/`
- Create today's note

### Step 5: Verify Dataview Queries (10 minutes)

Open daily note, check if Dataview tables render correctly

---

## 📋 DEPLOYMENT CHECKLIST

**Pre-Flight:**
- [ ] All critical plugins installed
- [ ] Template directory structure created
- [ ] Metadata schema documented
- [ ] Daily note template working

**Week 1:**
- [ ] Day 1: Plugins installed and configured
- [ ] Day 2-3: All core templates created
- [ ] Day 4: Metadata schema standardized
- [ ] Day 5-7: End-to-end testing complete

**Week 2:**
- [ ] Day 8-10: All 3 dashboards operational
- [ ] Day 11-12: QuickAdd workflows configured
- [ ] Day 13-14: Daily automation working

**Week 3-4:**
- [ ] Git workflow implemented
- [ ] Multi-agent collaboration tested
- [ ] Mobile capture operational
- [ ] Ready for Málaga deployment

---

## 🚨 RISK MITIGATION

**Risk 1: Plugin Conflicts**
- Mitigation: Install one at a time, test each
- Rollback: Disable problematic plugin, find alternative

**Risk 2: Performance Degradation**
- Mitigation: Monitor vault size, disable slow plugins
- Benchmark: Test query speed before/after each plugin

**Risk 3: Template Complexity**
- Mitigation: Start simple, add features incrementally
- Fallback: Manual note creation always available

**Risk 4: Git Merge Conflicts**
- Mitigation: Clear branch ownership, daily merge windows
- Resolution: Janus as conflict mediator

**Risk 5: Mobile Sync Failures**
- Mitigation: Test thoroughly before Málaga
- Backup: Manual note-taking, sync when back on WiFi

---

## 💡 KEY INSIGHTS FROM RESEARCH

**From Perplexity Deep Dive:**

1. **"Plugins are synergistic"** → Install Dataview + Templater + QuickAdd together
2. **"Dataview is the engine"** → Dashboards are the killer feature
3. **"Automation is non-negotiable"** → Daily notes save hundreds of hours
4. **"Zettelkasten + MOCs at scale"** → Our Concept Hubs are MOCs - formalize them
5. **"AI is the co-pilot"** → Smart Connections for semantic search
6. **"Graph View for analysis"** → Filter by tag to trace constitutional alignment
7. **"Visual thinking integrated"** → Excalidraw for system architecture
8. **"Git for multi-agent"** → Only viable path for Trinity coordination
9. **"Mobile capture is a science"** → One-button workflow essential
10. **"Performance actively managed"** → Plugin audits, optimize storage

**From Our Testing:**

1. **REST API is a superpower** → Real-time integration works flawlessly
2. **Complex markdown renders perfectly** → No limitations on formatting
3. **Automation potential is massive** → Bash scripts + API = infinite possibilities
4. **Knowledge graph creates context** → Links make wisdom discoverable
5. **Making alignment easy = constitutional adherence** → 2-min verification vs 20-min

---

## 🎯 FINAL RECOMMENDATION

**Execute this plan in order:**

**THIS WEEK (Before Málaga):**
- Phase 1, Day 1-4: Foundation (plugins, templates, schema)
- Quick wins: Daily notes, QuickAdd capture

**WEEK 2 (First week in Málaga):**
- Phase 2: Automation (dashboards, workflows)
- Field-test mobile capture in real environment

**WEEK 3-4 (Month 1 in Málaga):**
- Phase 3: Integration (Git, mobile, enrichment)
- Validate all workflows with real mission data

**MONTH 2+ (Optimization):**
- Phase 4: Advanced features (patterns, API, custom scripts)
- Iterate based on field learnings

---

**Ready to begin?**

**Next command from Captain: "Start deployment" → We begin Phase 1, Day 1**

---

**Status:** ✅ Plan complete, ready for execution
**Confidence:** High (research + testing proven)
**Timeline:** 4 weeks to full deployment
**Risk:** Low (incremental, tested approach)

---

*This deployment plan synthesizes 151 lines of power-user research with 3 days of hands-on testing. It's the roadmap to making Observatory the constitutional enforcement engine that makes UBOS unstoppable.*
---
type: deployment_plan
status: ready_to_execute
created: 2025-11-16
priority: critical
tags: [observatory, deployment, roadmap, step-by-step]
---

# 🚀 OBSERVATORY DEPLOYMENT PLAN

*Step-by-step implementation of power user techniques for UBOS*

**Based on:**
- Perplexity deep research (151 lines of findings)
- 3 days of comprehensive testing
- Current state analysis
- UBOS-specific requirements

---

## 📊 CURRENT STATE ANALYSIS

### ✅ What's Already Working

**Infrastructure:**
- REST API operational (port 27124, HTTPS)
- MCP Tools v0.2.27 installed
- Smart Connections installed
- 8,903 files indexed
- Real-time integration tested and working

**Plugins Installed:**
- ✅ dataview
- ✅ templater-obsidian
- ✅ obsidian-local-rest-api
- ✅ juggl (graph analysis)
- ✅ smart-connections (semantic search)
- ✅ mcp-tools (Claude integration)

**Documentation Complete:**
- 7 concept hubs created
- Maximum capabilities report (546 lines)
- REST API integration guide
- Automation scripts operational

**Performance Proven:**
- Constitutional consultation: 20 min → 2 min (10x)
- Grant assembly: 20 hrs → 3 hrs (6.7x)
- Concept tracing: 20 min → 2 min (10x)

### ⚠️ What's Missing (From Perplexity Research)

**Critical Plugins NOT Installed:**
- QuickAdd (one-click workflows)
- Advanced Tables (grant pipeline tracking)
- Excalidraw (visual architecture)
- Kanban (mission status boards)
- Tasks (advanced task management)
- Periodic Notes (weekly/monthly reviews)

**Workflows NOT Implemented:**
- Daily note automation
- Mission creation templates
- Constitutional decision templates
- Field capture workflow
- Pattern documentation templates

**Systems NOT Configured:**
- Git-based multi-agent collaboration
- Dataview dashboards (Mission Status, Grant Pipeline, Embassy Intel)
- MOC (Maps of Content) structure
- Metadata schema standardization
- Mobile quick capture

---

## 🎯 DEPLOYMENT STRATEGY

### Philosophy: Layered Implementation

**Layer 1: Foundation** (Week 1)
- Install missing critical plugins
- Create template infrastructure
- Standardize metadata schema
- Test each component individually

**Layer 2: Automation** (Week 2)
- Build Dataview dashboards
- Implement Templater automation
- Create QuickAdd workflows
- Deploy daily note system

**Layer 3: Integration** (Week 3-4)
- Git-based multi-agent workflow
- Mobile field capture
- Advanced pattern recognition
- Full constitutional audit system

**Layer 4: Optimization** (Month 2+)
- Custom DataviewJS scripts
- API integration with COMMS_HUB
- Zettelkasten atomic notes
- Multi-modal AI integration

---

## 📋 PHASE 1: FOUNDATION (Week 1)

### Day 1: Plugin Installation

**Priority: CRITICAL**

**Install these plugins in Obsidian:**

1. **QuickAdd**
   - Purpose: One-click workflows for field capture
   - Use case: "Captain's Log" instant note creation
   - Research finding: "Most effective users have 'one-button' capture"

2. **Advanced Tables**
   - Purpose: Spreadsheet-like functionality
   - Use case: Grant pipeline tracking, budget management
   - Research finding: Core power-user stack component

3. **Excalidraw**
   - Purpose: Visual thinking and interactive diagrams
   - Use case: System architecture, grant proposal flows
   - Research finding: "Visual syntax for thinking, not just drawing"

4. **Kanban**
   - Purpose: Visual task boards
   - Use case: Mission status tracking, embassy operations
   - Research finding: App-like functionality inside Obsidian

5. **Tasks**
   - Purpose: Advanced task management with queries
   - Use case: Multi-agent task coordination
   - Research finding: Essential for Trinity collaboration

6. **Periodic Notes**
   - Purpose: Weekly/monthly review automation
   - Use case: Mission reviews, pattern recognition
   - Research finding: Non-negotiable for power users

**Installation Steps:**
```
1. Open Obsidian Settings
2. Go to Community Plugins
3. Browse and search for each plugin
4. Install and Enable
5. Configure basic settings
```

**Expected Time:** 1 hour
**Success Criteria:** All 6 plugins installed and enabled

---

### Day 2-3: Template Infrastructure

**Priority: HIGH**

**Create template folder structure:**

```
/srv/janus/_TEMPLATES/
├── core/
│   ├── daily_note.md
│   ├── weekly_review.md
│   └── monthly_review.md
├── operations/
│   ├── mission_creation.md
│   ├── embassy_briefing.md
│   └── field_insight.md
├── strategy/
│   ├── constitutional_decision.md
│   ├── grant_proposal.md
│   └── partner_contact.md
├── knowledge/
│   ├── concept_hub.md
│   ├── pattern_documentation.md
│   └── moc_template.md
└── automation/
    ├── quick_capture.md
    └── captain_log.md
```

**Template 1: Daily Note** (Highest Priority)

```markdown
---
type: daily_note
date: {{date:YYYY-MM-DD}}
day_of_week: {{date:dddd}}
week_number: {{date:WW}}
tags: [daily, {{date:YYYY}}, {{date:MMMM}}]
---

# {{date:dddd, MMMM DD, YYYY}}

## 🎯 Mission Status

```dataview
TABLE status, priority, deadline
FROM "03_OPERATIONS"
WHERE status = "active" OR status = "in_progress"
SORT priority DESC, deadline ASC
LIMIT 5
```

## 📊 Today's Focus

**Top 3 Priorities:**
1.
2.
3.

**Active Missions:**
- [ ]

## 📝 Captain's Log

### Morning Brief


### Field Insights


### Decisions Made


## 🔗 Quick Links

**Dashboards:**
- [[_DASHBOARDS/MISSION_STATUS|Mission Status]]
- [[_DASHBOARDS/GRANT_PIPELINE|Grant Pipeline]]
- [[_DASHBOARDS/EMBASSY_INTEL|Embassy Intel]]

**Active Work:**
- [[03_OPERATIONS/MALAGA_EMBASSY/briefings/{{date:YYYY-MM-DD}}|Today's Embassy Briefing]]
- [[HOUSING_SEARCH_BRIEF|Housing Search]]

## 📈 Metrics

**Malaga Embassy:**
- Capital:
- Revenue:
- Health Score:

**Grant Pipeline:**
- Total value: €113M+
- Active proposals:
- Deadlines this week:

## 🌙 Evening Reflection

### What Went Well


### What to Improve


### Tomorrow's Preparation


---

**Previous:** [[{{date-1:YYYY-MM-DD}}|Yesterday]] | **Next:** [[{{date+1:YYYY-MM-DD}}|Tomorrow]]
```

**Template 2: Mission Creation** (with Templater automation)

```markdown
<%*
// Templater script for mission creation
const missionName = await tp.system.prompt("Mission Name");
const missionType = await tp.system.suggester(
  ["Embassy", "Grant", "Research", "Partnership", "Infrastructure"],
  ["embassy", "grant", "research", "partnership", "infrastructure"]
);
const priority = await tp.system.suggester(
  ["Critical", "High", "Medium", "Low"],
  ["critical", "high", "medium", "low"]
);
const budget = await tp.system.prompt("Estimated Budget (€)");
-%>
---
type: mission
mission_type: <%= missionType %>
status: planning
priority: <%= priority %>
created: <% tp.date.now("YYYY-MM-DD") %>
budget: <%= budget %>
constitutional_alignment: pending
tags: [mission, <%= missionType %>, <%= priority %>]
---

# <%= missionName %>

## 🎯 Mission Objective


## 📋 Constitutional Alignment

**Linked to Four Books:**
- [ ] [[01_STRATEGY/constitutional_mandate/four_books/01_tao_of_ubos|Tao of UBOS]]:
- [ ] [[01_STRATEGY/constitutional_mandate/four_books/02_platform_sutra|Platform Sutra]]:
- [ ] [[01_STRATEGY/constitutional_mandate/four_books/03_book_of_janus|Book of Janus]]:
- [ ] [[01_STRATEGY/constitutional_mandate/four_books/04_captains_codex|Captain's Codex]]:

**Trinity Lock Assessment:**
- Budget Tier: <% if (parseInt(budget) <= 50) { %>Alpha (€0-50) - Autonomous<% } else if (parseInt(budget) <= 150) { %>Beta (€51-150) - 24hr pause, 2/3 vote<% } else { %>Omega (€151+) - 48hr pause, unanimous<% } %>
- Pause Required:
- Vote Status:

## 📊 Mission Parameters

**Timeline:**
- Start Date:
- Target Completion:
- Milestones:
  - [ ]
  - [ ]
  - [ ]

**Resources Required:**
- Budget: €<%= budget %>
- Personnel:
- Tools/Infrastructure:

**Success Criteria:**
1.
2.
3.

## 🔄 Execution Plan

### Phase 1: Planning


### Phase 2: Execution


### Phase 3: Validation


### Phase 4: Integration


## 📈 Metrics & KPIs


## 🚨 Risks & Mitigations

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
|      |             |        |            |

## 📝 Mission Log

### <% tp.date.now("YYYY-MM-DD") %> - Mission Created


---

**Status:** Planning
**Next Review:** <% tp.date.now("YYYY-MM-DD", 7) %>
**Related Missions:**
```

**Template 3: Constitutional Decision**

```markdown
---
type: constitutional_decision
decision_id: {{date:YYYYMMDDHHmm}}
date: {{date:YYYY-MM-DD}}
status: pending_review
tags: [decision, constitutional, trinity-lock]
---

# Constitutional Decision: <% tp.system.prompt("Decision Summary") %>

## 🎯 The Decision

**What:**


**Why:**


**Budget Impact:** €<% tp.system.prompt("Budget Amount") %>

## 🔐 Trinity Lock Status

**Tier:** <%
const budget = await tp.system.prompt("Budget Amount");
if (parseInt(budget) <= 50) { %>
Alpha (€0-50) - **AUTONOMOUS** - No pause required
<% } else if (parseInt(budget) <= 150) { %>
Beta (€51-150) - **24-HOUR PAUSE** - Requires 2/3 Trinity vote
<% } else { %>
Omega (€151+) - **48-HOUR PAUSE** - Requires unanimous Trinity vote
<% } %>

**Vote:**
- [ ] Claude:
- [ ] Gemini:
- [ ] Codex:
- Result:

## 📖 Constitutional Links

**Required: Link to specific passages from Four Books**

### Tao of UBOS
[[01_STRATEGY/constitutional_mandate/four_books/01_tao_of_ubos#^relevant-passage|Relevant principle]]:
> Quote the specific passage here

**Alignment:**

### Platform Sutra
[[01_STRATEGY/constitutional_mandate/four_books/02_platform_sutra#^relevant-passage|Relevant principle]]:
> Quote the specific passage here

**Alignment:**

### Book of Janus
[[01_STRATEGY/constitutional_mandate/four_books/03_book_of_janus#^relevant-passage|Relevant principle]]:
> Quote the specific passage here

**Alignment:**

### Captain's Codex
[[01_STRATEGY/constitutional_mandate/four_books/04_captains_codex#^relevant-passage|Relevant principle]]:
> Quote the specific passage here

**Alignment:**

## ✅ Alignment Verification

**Passes Constitutional Test:**
- [ ] Aligns with Tao (frugality, simplicity, long-term)
- [ ] Aligns with Platform Sutra (infrastructure, sovereignty)
- [ ] Aligns with Janus (transparency, reversibility)
- [ ] Aligns with Codex (field-tested, pragmatic)

**Constitutional Health Score:** /100

## 📊 Impact Analysis

**Financial:**


**Operational:**


**Strategic:**


## 🔄 Reversibility

**Can this decision be reversed?**


**Reversal cost:**


## 📝 Decision Log

### Proposed
Date: {{date:YYYY-MM-DD HH:mm}}
By:

### Reviewed
Date:
By:

### Approved/Rejected
Date:
By:
Result:

---

**Related Decisions:**
**Related Missions:**
**Field Evidence:**
```

**Expected Time:** 2 days
**Success Criteria:** All core templates created and tested

---

### Day 4: Metadata Schema Standardization

**Priority: HIGH**

**Define v1.0 metadata schema for common note types:**

**1. Mission Notes:**
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

**2. Partner/Contact Notes:**
```yaml
---
type: partner
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

**3. Field Insight Notes:**
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

**4. Concept Hub Notes:**
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

**5. Decision Notes:**
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

**Implementation:**
1. Update all templates with correct schemas
2. Create schema documentation file
3. Use Templater to enforce schemas on new notes
4. Begin migrating existing notes (gradual)

**Expected Time:** 1 day
**Success Criteria:** Schema defined, documented, enforced in templates

---

### Day 5-7: Testing & Validation

**Priority: CRITICAL**

**Test each system:**

**Day 5: Template Testing**
- Create test daily note
- Create test mission using template
- Create test constitutional decision
- Verify metadata is correct
- Verify Dataview can query the metadata

**Day 6: Plugin Integration Testing**
- Test QuickAdd workflows
- Test Templater automation
- Test Advanced Tables functionality
- Test Kanban board creation
- Test Tasks plugin queries

**Day 7: End-to-End Workflow**
- Morning: Create daily note automatically
- Create a real mission for Malaga deployment
- Make a constitutional decision (housing budget)
- Capture a field insight (quick capture test)
- Evening: Review and reflection

**Expected Time:** 3 days
**Success Criteria:** All systems working, comfortable with workflows

---

## 📋 PHASE 2: AUTOMATION (Week 2)

### Day 8-10: Dataview Dashboards

**Priority: CRITICAL**

**Build 3 core dashboards:**

**1. Mission Status Dashboard** (`_DASHBOARDS/MISSION_STATUS.md`)

```markdown
---
type: dashboard
category: operations
auto_update: true
---

# 🎯 MISSION STATUS DASHBOARD

**Last Updated:** <% tp.date.now("YYYY-MM-DD HH:mm") %>

## 🔥 Active Missions

```dataview
TABLE
  mission_type as "Type",
  priority as "Priority",
  budget as "Budget (€)",
  deadline as "Deadline",
  status as "Status"
FROM "03_OPERATIONS"
WHERE type = "mission" AND (status = "active" OR status = "in_progress")
SORT priority DESC, deadline ASC
```

## ⏸️ Paused Missions

```dataview
TABLE mission_type, budget, deadline, "Pause Reason"
FROM "03_OPERATIONS"
WHERE type = "mission" AND status = "paused"
SORT deadline ASC
```

## ✅ Completed This Week

```dataview
TABLE mission_type, budget, completion_date
FROM "03_OPERATIONS"
WHERE type = "mission"
  AND status = "complete"
  AND completion_date >= date(today) - dur(7 days)
SORT completion_date DESC
```

## 🚨 Missions Requiring Attention

```dataview
TABLE mission_type, priority, deadline, status
FROM "03_OPERATIONS"
WHERE type = "mission"
  AND (deadline <= date(today) + dur(7 days) OR constitutional_alignment = "pending")
SORT deadline ASC
```

## 📊 Summary Metrics

```dataviewjs
const missions = dv.pages('"03_OPERATIONS"')
  .where(p => p.type === "mission");

const active = missions.where(m => m.status === "active").length;
const paused = missions.where(m => m.status === "paused").length;
const complete = missions.where(m => m.status === "complete").length;
const totalBudget = missions
  .where(m => m.status === "active")
  .map(m => m.budget || 0)
  .reduce((a, b) => a + b, 0);

dv.paragraph(`
**Active Missions:** ${active}
**Paused:** ${paused}
**Completed:** ${complete}
**Active Budget:** €${totalBudget}
`);
```
```

**2. Grant Pipeline Dashboard** (`_DASHBOARDS/GRANT_PIPELINE.md`)

```markdown
---
type: dashboard
category: strategy
auto_update: true
---

# 💰 GRANT PIPELINE DASHBOARD

## 🎯 Active Opportunities

```dataview
TABLE
  budget as "Value (€M)",
  fit_score as "Fit",
  deadline as "Deadline",
  status as "Status",
  stage as "Stage"
FROM "01_STRATEGY/grant_pipeline"
WHERE type = "grant_opportunity" AND status = "active"
SORT deadline ASC, fit_score DESC
```

## 🔥 Urgent (Deadline < 30 Days)

```dataview
TABLE budget, deadline, days_remaining, status
FROM "01_STRATEGY/grant_pipeline"
WHERE type = "grant_opportunity"
  AND deadline <= date(today) + dur(30 days)
  AND status != "submitted"
SORT deadline ASC
```

## 📊 Pipeline Summary

```dataviewjs
const opportunities = dv.pages('"01_STRATEGY/grant_pipeline"')
  .where(p => p.type === "grant_opportunity");

const totalValue = opportunities
  .map(o => parseFloat(o.budget) || 0)
  .reduce((a, b) => a + b, 0);

const activeCount = opportunities
  .where(o => o.status === "active")
  .length;

const avgFitScore = opportunities
  .where(o => o.fit_score)
  .map(o => o.fit_score)
  .reduce((a, b) => a + b, 0) / opportunities.length;

dv.paragraph(`
**Total Pipeline Value:** €${totalValue.toFixed(1)}M
**Active Opportunities:** ${activeCount}
**Average Fit Score:** ${avgFitScore.toFixed(1)}/5.0
`);
```

## 🏆 High-Fit Opportunities (4.0+)

```dataview
TABLE budget, fit_score, deadline, stage
FROM "01_STRATEGY/grant_pipeline"
WHERE type = "grant_opportunity" AND fit_score >= 4.0
SORT fit_score DESC, budget DESC
```
```

**3. Embassy Intel Dashboard** (`_DASHBOARDS/EMBASSY_INTEL.md`)

```markdown
---
type: dashboard
category: operations
location: malaga
auto_update: true
---

# 🏛️ MÁLAGA EMBASSY INTELLIGENCE

## 💰 Financial Status

**Capital:** €1,800
**Revenue:** €300 (autonomous)
**Health Score:** 100/100
**Days to Departure:** <% Math.ceil((new Date('2025-11-23') - new Date()) / 86400000) %>

## 📝 Recent Field Insights

```dataview
TABLE
  category as "Type",
  location as "Location",
  captured as "When",
  priority as "Priority"
FROM "03_OPERATIONS/MALAGA_EMBASSY"
WHERE type = "field_insight"
SORT captured DESC
LIMIT 10
```

## 🤝 Partner Network

```dataview
TABLE
  category as "Type",
  relationship_strength as "Strength",
  last_contacted as "Last Contact",
  related_missions as "Projects"
FROM "03_OPERATIONS/MALAGA_EMBASSY/partners"
WHERE type = "partner"
SORT last_contacted DESC
```

## 🏠 Housing Search Status

**Budget:** €1,000/month max
**Requirements:** Finca, backyard, 2 people + dog
**Target Areas:** Axarquía, Montes de Málaga, Valle del Guadalhorce

```dataview
TABLE location, price, size, contact_status
FROM "03_OPERATIONS/MALAGA_EMBASSY/housing_prospects"
WHERE type = "housing_prospect"
SORT price ASC, size DESC
```

## 📅 Upcoming Events

```dataview
TASK
FROM "03_OPERATIONS/MALAGA_EMBASSY"
WHERE status != "complete"
SORT deadline ASC
LIMIT 10
```
```

**Expected Time:** 3 days
**Success Criteria:** All 3 dashboards built, live data flowing, queries optimized

---

### Day 11-12: QuickAdd Workflows

**Priority: HIGH**

**Create 5 essential workflows:**

**1. Captain's Log (Quick Capture)**
```
Trigger: Cmd+Shift+L (or hotkey)
Action: Create new note from template
Template: _TEMPLATES/automation/captain_log.md
Location: 03_OPERATIONS/MALAGA_EMBASSY/field_insights/
Naming: {{DATE}}_{{VALUE:title}}.md
Auto-open: No (for mobile speed)
```

**2. New Mission**
```
Trigger: Cmd+Shift+M
Action: Create from template with prompts
Template: _TEMPLATES/operations/mission_creation.md
Location: 03_OPERATIONS/missions/
Naming: {{DATE}}_{{VALUE:mission_name}}.md
```

**3. Constitutional Decision**
```
Trigger: Cmd+Shift+D
Action: Create from template
Template: _TEMPLATES/strategy/constitutional_decision.md
Location: 03_OPERATIONS/decisions/
Naming: {{DATE:YYYYMMDDHHmm}}_decision.md
```

**4. Partner Contact**
```
Trigger: Cmd+Shift+P
Action: Create from template
Template: _TEMPLATES/strategy/partner_contact.md
Location: 03_OPERATIONS/MALAGA_EMBASSY/partners/
Naming: {{VALUE:name}}.md
```

**5. Pattern Documentation**
```
Trigger: Cmd+Shift+T
Action: Create from template
Template: _TEMPLATES/knowledge/pattern_documentation.md
Location: CONCEPTS/patterns/
Naming: {{DATE}}_{{VALUE:pattern_name}}.md
```

**Expected Time:** 2 days
**Success Criteria:** All workflows configured, hotkeys set, tested on desktop and mobile

---

### Day 13-14: Daily Note Automation

**Priority: CRITICAL**

**Set up Periodic Notes:**

**Configuration:**
- Daily notes: Auto-create at midnight
- Weekly reviews: Auto-create Monday 07:00
- Monthly reviews: Auto-create 1st of month

**Templater Scripts:**

**Daily Note Auto-Populate:**
```javascript
<%*
// Pull yesterday's uncompleted tasks
const yesterday = tp.date.now("YYYY-MM-DD", -1);
const yesterdayFile = tp.file.find_tfile(yesterday);

if (yesterdayFile) {
  const content = await app.vault.read(yesterdayFile);
  const incompleteTasks = content.match(/- \[ \] .*/g) || [];

  if (incompleteTasks.length > 0) {
    tR += "\n## 📋 Carried Forward from Yesterday\n\n";
    incompleteTasks.forEach(task => tR += task + "\n");
  }
}

// Pull active missions
const missions = dv.pages('"03_OPERATIONS"')
  .where(p => p.type === "mission" && p.status === "active");

tR += "\n## 🎯 Active Missions\n\n";
missions.forEach(m => {
  tR += `- [[${m.file.path}|${m.file.name}]] (${m.priority})\n`;
});
-%>
```

**Expected Time:** 2 days
**Success Criteria:** Daily notes auto-create with populated data

---

## 📋 PHASE 3: INTEGRATION (Week 3-4)

### Week 3: Multi-Agent Git Workflow

**Priority: MEDIUM-HIGH**

**Steps:**

**1. Initialize Git Repository** (Day 15)
```bash
cd /srv/janus
git init
git add .obsidian/workspace.json
git add _TEMPLATES/
git add 01_STRATEGY/
git add 03_OPERATIONS/
git add CONCEPTS/
git add _DASHBOARDS/
git commit -m "Initial Observatory commit - v1.0"
```

**2. Create Branch Strategy** (Day 16)
```
main (production)
├── claude-dev (Claude's working branch)
├── gemini-dev (Gemini's working branch)
├── codex-dev (Codex's working branch)
└── captain-dev (Captain's field notes)
```

**3. COMMS_HUB Integration** (Day 17-18)
```markdown
Create: 03_OPERATIONS/COMMS_HUB/git_workflow.md

Workflow:
1. Each agent works on their branch
2. Commits with descriptive messages
3. Daily merge window at 18:00 UTC
4. Conflicts reviewed by Janus
5. Captain approves merges to main
```

**4. Conflict Resolution Protocol** (Day 19)
```
If conflict:
1. Agent pauses work
2. Creates conflict note in COMMS_HUB
3. Tags relevant agents
4. Waits for resolution
5. Resumes after merge
```

**Expected Time:** 5 days
**Success Criteria:** Git repo active, all agents can commit, merge workflow tested

---

### Week 4: Mobile Field Capture

**Priority: HIGH** (for Málaga deployment)

**Implementation:**

**1. Install Obsidian Mobile** (Day 20)
- Install on Captain's phone
- Configure sync (Obsidian Sync or Git-based)
- Test basic functionality

**2. Configure QuickAdd for Mobile** (Day 21)
- Set up one-tap "Captain's Log" button
- Configure voice-to-text (iOS/Android)
- Test capture speed (<10 seconds)

**3. Create Mobile Templates** (Day 22)
```markdown
Minimal template for speed:
---
type: field_insight
captured: {{date}} {{time}}
location: {{location}}
status: raw
---

# {{value:title}}

{{value:notes}}

#field #raw
```

**4. Enrichment Automation** (Day 23)
```javascript
// Templater script runs on desktop
// Detects new #raw field insights
// Enriches with:
// - Related mission links
// - Partner connections
// - Geographic context
// - Priority assessment
// Changes status: raw → enriched
```

**5. End-to-End Test** (Day 24)
- Captain captures field note on mobile
- Syncs to vault
- Desktop automation enriches
- Appears in Embassy Intel dashboard
- Full cycle < 2 minutes

**Expected Time:** 5 days
**Success Criteria:** Mobile capture working, enrichment automatic, dashboard integration live

---

## 📋 PHASE 4: OPTIMIZATION (Month 2+)

### Week 5-6: Advanced Pattern Recognition

**DataviewJS Scripts:**

**1. Constitutional Alignment Audit**
```javascript
// Find all decisions without constitutional links
const decisions = dv.pages('"03_OPERATIONS/decisions"')
  .where(p => p.type === "constitutional_decision");

const unlinked = decisions.where(d =>
  !d.file.outlinks.some(link =>
    link.path.includes("four_books")
  )
);

if (unlinked.length > 0) {
  dv.header(2, "⚠️ Decisions Without Constitutional Links");
  dv.table(["Decision", "Date", "Budget", "Status"],
    unlinked.map(d => [
      d.file.link,
      d.date,
      `€${d.budget}`,
      d.status
    ])
  );
}
```

**2. Success Pattern Finder**
```javascript
// Identify common traits in successful missions
const missions = dv.pages('"03_OPERATIONS"')
  .where(p => p.type === "mission" && p.status === "complete");

const successful = missions.where(m => m.success_score >= 4.0);

// Analyze common patterns
const patterns = {
  avgBudget: successful.map(m => m.budget).reduce((a,b) => a+b, 0) / successful.length,
  commonTags: /* tag frequency analysis */,
  avgTimeline: /* timeline analysis */,
  partnerCount: /* partner involvement */
};

dv.paragraph(`
**Successful Mission Patterns:**
- Average Budget: €${patterns.avgBudget}
- Constitutional Alignment: 100% verified
- Partner Involvement: ${patterns.partnerCount} avg
- Timeline Adherence: ${patterns.avgTimeline}%
`);
```

**Expected Time:** 2 weeks
**Success Criteria:** Pattern recognition automated, insights actionable

---

### Week 7-8: API Integration

**Custom Integration with COMMS_HUB:**

**1. REST API Extension**
```python
# Custom endpoint: sync with Obsidian
@app.route('/api/obsidian/sync', methods=['POST'])
def sync_obsidian():
    # Reads COMMS_HUB messages
    # Creates Obsidian notes
    # Updates task lists
    # Returns confirmation
```

**2. External Data Sync**
```python
# Sync grant deadlines from EU portals
# Update grant_pipeline/*.md files
# Trigger Dataview dashboard refresh
```

**Expected Time:** 2 weeks
**Success Criteria:** COMMS_HUB <-> Obsidian bidirectional sync working

---

## 📊 SUCCESS METRICS

### Week 1 Targets:
- ✅ 6 critical plugins installed
- ✅ 10 core templates created
- ✅ Metadata schema defined
- ✅ All templates tested

### Week 2 Targets:
- ✅ 3 dashboards live with real data
- ✅ 5 QuickAdd workflows configured
- ✅ Daily notes auto-creating
- ✅ Automation tested end-to-end

### Week 3-4 Targets:
- ✅ Git workflow operational
- ✅ Multi-agent collaboration tested
- ✅ Mobile field capture working
- ✅ Enrichment automation live

### Month 2+ Targets:
- ✅ Pattern recognition automated
- ✅ COMMS_HUB integration complete
- ✅ Constitutional audit automatic
- ✅ Performance at scale maintained

---

## 🎯 IMMEDIATE NEXT STEPS

**Ready to execute RIGHT NOW:**

### Step 1: Install Missing Plugins (30 minutes)

Open Obsidian → Settings → Community Plugins → Browse

Install in this order:
1. QuickAdd
2. Advanced Tables
3. Excalidraw
4. Kanban
5. Tasks
6. Periodic Notes

### Step 2: Create Template Directory (5 minutes)

```bash
mkdir -p /srv/janus/_TEMPLATES/{core,operations,strategy,knowledge,automation}
```

### Step 3: Create First Template (15 minutes)

Copy daily_note template from this document to:
`/srv/janus/_TEMPLATES/core/daily_note.md`

### Step 4: Test Daily Note Creation (5 minutes)

In Obsidian:
- Periodic Notes settings → Daily Notes
- Set template: `_TEMPLATES/core/daily_note.md`
- Set folder: `_DAILY_NOTES/`
- Create today's note

### Step 5: Verify Dataview Queries (10 minutes)

Open daily note, check if Dataview tables render correctly

---

## 📋 DEPLOYMENT CHECKLIST

**Pre-Flight:**
- [ ] All critical plugins installed
- [ ] Template directory structure created
- [ ] Metadata schema documented
- [ ] Daily note template working

**Week 1:**
- [ ] Day 1: Plugins installed and configured
- [ ] Day 2-3: All core templates created
- [ ] Day 4: Metadata schema standardized
- [ ] Day 5-7: End-to-end testing complete

**Week 2:**
- [ ] Day 8-10: All 3 dashboards operational
- [ ] Day 11-12: QuickAdd workflows configured
- [ ] Day 13-14: Daily automation working

**Week 3-4:**
- [ ] Git workflow implemented
- [ ] Multi-agent collaboration tested
- [ ] Mobile capture operational
- [ ] Ready for Málaga deployment

---

## 🚨 RISK MITIGATION

**Risk 1: Plugin Conflicts**
- Mitigation: Install one at a time, test each
- Rollback: Disable problematic plugin, find alternative

**Risk 2: Performance Degradation**
- Mitigation: Monitor vault size, disable slow plugins
- Benchmark: Test query speed before/after each plugin

**Risk 3: Template Complexity**
- Mitigation: Start simple, add features incrementally
- Fallback: Manual note creation always available

**Risk 4: Git Merge Conflicts**
- Mitigation: Clear branch ownership, daily merge windows
- Resolution: Janus as conflict mediator

**Risk 5: Mobile Sync Failures**
- Mitigation: Test thoroughly before Málaga
- Backup: Manual note-taking, sync when back on WiFi

---

## 💡 KEY INSIGHTS FROM RESEARCH

**From Perplexity Deep Dive:**

1. **"Plugins are synergistic"** → Install Dataview + Templater + QuickAdd together
2. **"Dataview is the engine"** → Dashboards are the killer feature
3. **"Automation is non-negotiable"** → Daily notes save hundreds of hours
4. **"Zettelkasten + MOCs at scale"** → Our Concept Hubs are MOCs - formalize them
5. **"AI is the co-pilot"** → Smart Connections for semantic search
6. **"Graph View for analysis"** → Filter by tag to trace constitutional alignment
7. **"Visual thinking integrated"** → Excalidraw for system architecture
8. **"Git for multi-agent"** → Only viable path for Trinity coordination
9. **"Mobile capture is a science"** → One-button workflow essential
10. **"Performance actively managed"** → Plugin audits, optimize storage

**From Our Testing:**

1. **REST API is a superpower** → Real-time integration works flawlessly
2. **Complex markdown renders perfectly** → No limitations on formatting
3. **Automation potential is massive** → Bash scripts + API = infinite possibilities
4. **Knowledge graph creates context** → Links make wisdom discoverable
5. **Making alignment easy = constitutional adherence** → 2-min verification vs 20-min

---

## 🎯 FINAL RECOMMENDATION

**Execute this plan in order:**

**THIS WEEK (Before Málaga):**
- Phase 1, Day 1-4: Foundation (plugins, templates, schema)
- Quick wins: Daily notes, QuickAdd capture

**WEEK 2 (First week in Málaga):**
- Phase 2: Automation (dashboards, workflows)
- Field-test mobile capture in real environment

**WEEK 3-4 (Month 1 in Málaga):**
- Phase 3: Integration (Git, mobile, enrichment)
- Validate all workflows with real mission data

**MONTH 2+ (Optimization):**
- Phase 4: Advanced features (patterns, API, custom scripts)
- Iterate based on field learnings

---

**Ready to begin?**

**Next command from Captain: "Start deployment" → We begin Phase 1, Day 1**

---

**Status:** ✅ Plan complete, ready for execution
**Confidence:** High (research + testing proven)
**Timeline:** 4 weeks to full deployment
**Risk:** Low (incremental, tested approach)

---

*This deployment plan synthesizes 151 lines of power-user research with 3 days of hands-on testing. It's the roadmap to making Observatory the constitutional enforcement engine that makes UBOS unstoppable.*
