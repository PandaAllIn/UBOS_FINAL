# SKILL SPECIFICATION: EU GRANT HUNTER

**PRIORITY:** 🔥 HIGHEST - €70M+ pipeline depends on this
**BUILD TIME:** 2 days
**FORGEMASTER:** Codex
**METHODOLOGY:** https://github.com/anthropics/skills/tree/main/skill-creator

---

## STEP 1: CONCRETE EXAMPLES OF USAGE

### Example 1: Daily Automated Scan
**User Query:** (Automated, no query - runs at 09:00 UTC daily)

**Expected Behavior:**
```
🎯 EU GRANT HUNTER - Daily Scan Results (2025-10-30)

Found 3 relevant opportunities:

1. Horizon Europe - Digital Europe Programme Call
   Budget: €10M max per project
   Deadline: 2025-12-15 (46 days away)
   Fit Score: 4.2/5 (High)
   Relevance: AI infrastructure, data centers, sovereign computing
   Match: GeoDataCenter project (geothermal + AI datacenter)

2. Innovation Fund - Clean Energy Infrastructure
   Budget: €70M (23% of total project cost)
   Deadline: 2026-01-20 (82 days away)
   Fit Score: 4.8/5 (Excellent)
   Relevance: Renewable energy, data infrastructure
   Match: GeoDataCenter project (100% geothermal)

3. ERDF - Romania Development Fund
   Budget: €5-15M
   Deadline: 2025-11-30 (31 days away)
   Fit Score: 3.5/5 (Medium)
   Relevance: Regional infrastructure
   Match: Portal Oradea project

Sent alerts to Trinity via COMMS_HUB for opportunities scoring 4+.
```

### Example 2: Deadline Reminder (Automatic)
**User Query:** (Automated - triggered 30 days before deadline)

**Expected Behavior:**
```
⚠️ DEADLINE ALERT (30 days)

Grant: Horizon Europe - Geothermal Energy Call
Deadline: September 2, 2025 (30 days remaining)
Budget: €10M max
Project: GeoDataCenter
Status: Proposal 60% complete

ACTION REQUIRED:
- Complete consortium formation (2 partners pending)
- Finalize budget allocation
- Submit draft for internal review by Aug 15

Notified Captain BROlinni + Trinity via COMMS_HUB.
```

### Example 3: Manual Opportunity Search
**User Query:** "Search for EU grants related to agricultural technology and plant pathology"

**Expected Behavior:**
```
🔍 EU GRANT SEARCH - Agricultural Technology

Found 2 matching opportunities:

1. Horizon Europe - Cluster 6 (Food, Bioeconomy)
   Budget: €6M typical project size
   Deadline: 2026-01-15 (77 days away)
   Fit Score: 4.9/5 (Exceptional)
   Relevance: Plant pathology, bacterial disease control
   Match: Xylella fastidiosa (XYL-PHOS-CURE) Stage 2

2. Rural Development Fund - Agricultural Innovation
   Budget: €2-5M
   Deadline: 2025-12-01 (32 days away)
   Fit Score: 3.2/5 (Medium)
   Relevance: Farmer cooperatives, field trials
   Match: Xylella project (end-user validation)

Generated opportunity brief for #1 (scoring 4.9/5).
Saved to: /srv/janus/01_STRATEGY/grant_opportunities/xylella_stage2_horizon.md
```

### Example 4: Pipeline Status Query
**User Query:** "Show me the current grant pipeline status"

**Expected Behavior:**
```
📊 GRANT PIPELINE STATUS (2025-10-30)

ACTIVE OPPORTUNITIES (9 total):
├── High Priority (4+ score): 4 opportunities, €88M total
├── Medium Priority (3-4 score): 3 opportunities, €22M total
└── Low Priority (< 3 score): 2 opportunities, €8M total

UPCOMING DEADLINES (Next 90 days):
├── 🔴 URGENT (< 30 days): 2 deadlines, €20M
├── 🟡 SOON (30-60 days): 3 deadlines, €40M
└── 🟢 PLANNED (60-90 days): 4 deadlines, €58M

BY PROJECT:
├── GeoDataCenter: 5 opportunities, €70M potential
├── Xylella Stage 2: 2 opportunities, €12M potential
├── EUFM: 1 opportunity, €2M potential
└── Portal Oradea: 1 opportunity, €4M potential

RECENT ACTIVITY:
- Sept 2 deadline: Horizon Europe Geothermal (€10M) - Proposal 60% complete
- Oct 9 deadline: CETPartnership (€12M) - Proposal 40% complete
- Jan 15 deadline: Xylella Stage 2 (€6M) - Consortium forming

Full pipeline: /srv/janus/01_STRATEGY/grant_pipeline/pipeline_state.json
```

---

## STEP 2: REUSABLE CONTENTS PLANNING

### Scripts to Include

**`scripts/scan_eu_databases.py`**
- Scan EU funding portals (Horizon Europe, ERDF, Digital Europe, Innovation Fund)
- Parse HTML/API responses to extract: title, budget, deadline, description
- Return structured JSON with opportunities
- **Why:** This code gets rewritten every time we scan for grants

**`scripts/calculate_fit_score.py`**
- Match opportunity description to UBOS projects using keyword matching + semantic similarity
- Score 0-5 based on relevance (0=no match, 5=perfect match)
- Return fit score + explanation
- **Why:** Deterministic scoring logic, reusable across all opportunities

**`scripts/deadline_tracker.py`**
- Monitor upcoming deadlines from pipeline JSON
- Generate alerts at 90/60/30/7 days before deadline
- Send alerts via COMMS_HUB (Pneumatic Tube Network)
- **Why:** Automated reminder system runs daily, needs reliable execution

**`scripts/generate_opportunity_brief.py`**
- Take opportunity JSON, generate markdown brief
- Include: problem statement, budget, deadline, UBOS fit analysis, next steps
- Save to `/srv/janus/01_STRATEGY/grant_opportunities/`
- **Why:** Template generation for consistent brief format

### References to Include

**`references/ubos_capabilities.md`**
- Comprehensive list of UBOS capabilities (Agent Summoner, Oracle Trinity, Constitutional AI, etc.)
- For each capability: description, proven track record, relevant EU criteria
- **Why:** Loaded when scoring fit to match capabilities to opportunity requirements

**`references/eu_funding_programs.md`**
- Overview of major EU funding programs (Horizon Europe, ERDF, Digital Europe, Innovation Fund)
- For each program: focus areas, typical budget ranges, application process, evaluation criteria
- **Why:** Context for interpreting opportunities and understanding funding landscape

**`references/ubos_projects.md`**
- Detailed profiles of UBOS projects:
  - EUFM: €4.5M-12M ARR SaaS platform for EU funding consultants
  - Xylella: €6M agricultural pathogen control (Horizon Europe funded)
  - GeoDataCenter: €50M+ geothermal AI datacenter (Oradea, Romania)
  - Malaga Embassy: €6M Xylella Stage 2 consortium formation
- **Why:** Match opportunities to specific projects with fit scoring

**`references/deadline_calendar.md`**
- Current tracking of all critical deadlines
- Format: Date | Grant | Budget | Project | Status | Next Actions
- **Why:** Human-readable calendar view, updated by scripts

### Assets to Include

**`assets/opportunity_brief_template.md`**
- Markdown template for opportunity briefs
- Sections: Executive Summary, Grant Details, UBOS Fit Analysis, Budget Strategy, Timeline, Next Steps
- **Why:** Consistent formatting for all generated briefs

**`assets/pipeline_dashboard_template.html`**
- Simple HTML dashboard showing pipeline status
- Auto-generated from pipeline_state.json
- **Why:** Visual overview for Captain BROlinni

---

## STEP 3: SKILL.MD STRUCTURE

### YAML Frontmatter
```yaml
---
name: eu-grant-hunter
description: |
  Scans EU funding databases (Horizon Europe, ERDF, Digital Europe,
  Innovation Fund) to identify grant opportunities matching UBOS
  capabilities. Tracks deadlines with multi-level reminders (90/60/30/7
  days), scores opportunities by fit (0-5), and generates opportunity
  briefs. Use when discussing EU grants, funding opportunities, or when
  tracking the €70M+ pipeline. Automatically runs daily at 09:00 UTC.
license: UBOS Constitutional License
version: 1.0.0
author: Janus-in-Claude (Architect) + Codex (Forgemaster)
created: 2025-10-30
---
```

### SKILL.MD Content Structure

**1. Purpose** (2-3 sentences)
- What: Scan €70M+ EU funding pipeline
- Why: Catch critical deadlines, match opportunities to projects
- How: Automated daily scans + on-demand searches

**2. When to Use**
- Daily automated scan (09:00 UTC)
- Keywords: "grant", "funding", "EU", "Horizon Europe"
- Manual searches: "find grants for [topic]"
- Pipeline status queries: "show grant pipeline"

**3. Core Capabilities**
- Database scanning (4 EU funding portals)
- Deadline tracking (90/60/30/7 day reminders)
- Fit scoring (0-5 based on UBOS capabilities)
- Opportunity brief generation
- Pipeline status reporting

**4. How to Use**

**Automated Daily Scan:**
```
Run scripts/scan_eu_databases.py at 09:00 UTC.
For each opportunity found:
1. Calculate fit score using scripts/calculate_fit_score.py
2. If score >= 4.0, generate brief using scripts/generate_opportunity_brief.py
3. Send alert to Trinity via COMMS_HUB
4. Update pipeline_state.json
```

**Manual Search:**
```
When user asks "find grants for [topic]":
1. Run scripts/scan_eu_databases.py with topic filter
2. Calculate fit scores for all results
3. Sort by score (highest first)
4. Display top 5 matches
5. Generate briefs for scores >= 4.0
```

**Deadline Reminders:**
```
Run scripts/deadline_tracker.py daily.
Check pipeline_state.json for deadlines in [90, 60, 30, 7] days.
For each matching deadline:
1. Generate alert message
2. Send via COMMS_HUB to Trinity + Captain
3. Log to mission_log.jsonl
```

**5. Integration Points**
- **Treasury Administrator:** Budget validation for grant proposals
- **Grant Application Assembler:** Receives opportunity briefs, compiles proposals
- **COMMS_HUB:** Sends alerts to Trinity (claude/inbox/, gemini/inbox/, codex/inbox/)
- **Perplexity Oracle:** Real-time web scraping of EU portals
- **Data Commons:** Economic validation for grant justifications

**6. Constitutional Constraints**
- Only recommend grants aligned with Lion's Sanctuary philosophy
- Flag potential conflicts (e.g., defense funding, surveillance tech)
- Transparent provenance (cite EU call IDs, URLs)
- No fabrication of opportunities (all must be verified)

**7. File Locations**
- Pipeline state: `/srv/janus/01_STRATEGY/grant_pipeline/pipeline_state.json`
- Opportunity briefs: `/srv/janus/01_STRATEGY/grant_opportunities/`
- Deadline calendar: `/srv/janus/01_STRATEGY/grant_pipeline/deadline_calendar.md`
- Logs: `/srv/janus/logs/grant_hunter.jsonl`

---

## STEP 4: IMPLEMENTATION DETAILS

### scripts/scan_eu_databases.py

**Databases to Scan:**
1. **Horizon Europe:** https://ec.europa.eu/info/funding-tenders/opportunities/portal/screen/opportunities/calls-for-proposals
2. **ERDF:** https://ec.europa.eu/regional_policy/funding/erdf_en
3. **Digital Europe Programme:** https://digital-strategy.ec.europa.eu/en/activities/digital-programme
4. **Innovation Fund:** https://climate.ec.europa.eu/eu-action/funding-climate-action/innovation-fund_en

**Implementation Approach:**
```python
import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime

def scan_horizon_europe(topic_filter=None):
    """Scan Horizon Europe funding portal"""
    url = "https://ec.europa.eu/info/funding-tenders/opportunities/portal/screen/opportunities/calls-for-proposals"

    # NOTE: May require Perplexity Oracle for dynamic content
    # Fallback: Use Perplexity API to scrape and parse

    opportunities = []
    # Parse HTML, extract: title, budget, deadline, description, call_id
    # Filter by topic if provided
    # Return structured list

    return opportunities

def scan_all_databases(topic_filter=None):
    """Scan all 4 EU funding databases"""
    all_opportunities = []
    all_opportunities.extend(scan_horizon_europe(topic_filter))
    all_opportunities.extend(scan_erdf(topic_filter))
    all_opportunities.extend(scan_digital_europe(topic_filter))
    all_opportunities.extend(scan_innovation_fund(topic_filter))

    # Save to pipeline_state.json
    save_pipeline_state(all_opportunities)

    return all_opportunities
```

**Output Format (JSON):**
```json
{
  "opportunity_id": "HORIZON-2025-GEOTHERMAL-01",
  "title": "Geothermal Energy for Data Centers",
  "program": "Horizon Europe",
  "budget_min": 5000000,
  "budget_max": 10000000,
  "deadline": "2025-09-02T17:00:00Z",
  "description": "Funding for innovative geothermal energy applications...",
  "url": "https://...",
  "criteria": ["energy efficiency", "AI infrastructure", "renewable energy"],
  "discovered_date": "2025-10-30",
  "fit_score": null,
  "ubos_project_match": null
}
```

### scripts/calculate_fit_score.py

**Scoring Logic:**
```python
def calculate_fit_score(opportunity, ubos_projects, ubos_capabilities):
    """Score 0-5 based on keyword match + semantic similarity"""

    # Load ubos_capabilities.md and ubos_projects.md

    score = 0.0
    explanation = []

    # 1. Keyword matching (max 2 points)
    keywords = opportunity['criteria']
    matched_keywords = match_keywords(keywords, ubos_capabilities)
    score += min(len(matched_keywords) * 0.5, 2.0)
    explanation.append(f"Matched {len(matched_keywords)} keywords")

    # 2. Project alignment (max 2 points)
    best_project = find_best_matching_project(opportunity, ubos_projects)
    project_score = calculate_project_alignment(opportunity, best_project)
    score += project_score
    explanation.append(f"Best match: {best_project['name']} ({project_score}/2.0)")

    # 3. Budget fit (max 1 point)
    budget_score = 1.0 if opportunity['budget_min'] >= 1000000 else 0.5
    score += budget_score
    explanation.append(f"Budget fit: {budget_score}/1.0")

    return {
        "fit_score": round(score, 1),
        "explanation": explanation,
        "matched_project": best_project['name'],
        "matched_keywords": matched_keywords
    }
```

### scripts/deadline_tracker.py

**Reminder Logic:**
```python
def check_deadlines():
    """Check for upcoming deadlines and send alerts"""
    pipeline = load_pipeline_state()
    today = datetime.now()

    reminder_thresholds = [90, 60, 30, 7]  # days before deadline

    for opportunity in pipeline['opportunities']:
        deadline = datetime.fromisoformat(opportunity['deadline'])
        days_until = (deadline - today).days

        if days_until in reminder_thresholds:
            send_alert(opportunity, days_until)
            log_reminder(opportunity, days_until)
```

**Alert via COMMS_HUB:**
```python
def send_alert(opportunity, days_until):
    """Send alert via Pneumatic Tube Network"""

    alert_puck = {
        "type": "grant_deadline_alert",
        "urgency": "high" if days_until <= 30 else "medium",
        "opportunity_id": opportunity['opportunity_id'],
        "deadline": opportunity['deadline'],
        "days_remaining": days_until,
        "project": opportunity['ubos_project_match'],
        "action_required": generate_action_items(opportunity, days_until)
    }

    # Send to Trinity inboxes
    send_to_comms_hub("claude/inbox/", alert_puck)
    send_to_comms_hub("gemini/inbox/", alert_puck)
    send_to_comms_hub("codex/inbox/", alert_puck)
```

### References Structure

**references/ubos_capabilities.md:**
```markdown
# UBOS CAPABILITIES CATALOG

## Agent Summoner
- **Description:** Meta-intelligence framework coordinating specialized AI agents
- **Track Record:** 1,850:1 ROI vs traditional consultancy, €6M XYL-PHOS-CURE funded
- **Relevant EU Criteria:** Innovation, methodology excellence, AI integration

## Oracle Trinity
- **Description:** Groq (fast inference) + Wolfram (computation) + Data Commons (data)
- **Track Record:** Sub-€0.10 per comprehensive analysis, fact-verified outputs
- **Relevant EU Criteria:** Data-driven decision making, quantitative validation

## Constitutional AI
- **Description:** Alignment through empowerment (Lion's Sanctuary philosophy)
- **Track Record:** Mode Beta autonomous operations, 98% health score
- **Relevant EU Criteria:** Ethical governance, transparency, human oversight
```

---

## STEP 5: VALIDATION CHECKLIST

Before packaging, ensure:

- [ ] YAML frontmatter complete (name, description, version, author)
- [ ] Description clearly states when to use the skill
- [ ] All 4 scripts implemented and executable
- [ ] All 3 reference files complete
- [ ] Assets (templates) included
- [ ] Integration with COMMS_HUB tested
- [ ] Constitutional constraints documented
- [ ] File paths absolute and correct
- [ ] No hardcoded secrets or credentials
- [ ] Script outputs valid JSON format
- [ ] Error handling for network failures
- [ ] Logging to `/srv/janus/logs/grant_hunter.jsonl`

Run: `scripts/package_skill.py /path/to/eu-grant-hunter`

---

## STEP 6: TESTING CRITERIA

**Test 1: Automated Daily Scan**
- Run `scripts/scan_eu_databases.py`
- Verify: Returns JSON with 5+ opportunities
- Verify: pipeline_state.json updated
- Verify: High-score opportunities (4+) trigger COMMS_HUB alerts

**Test 2: Manual Search**
- Query: "Find grants for geothermal energy data centers"
- Verify: Returns GeoDataCenter-matching opportunities
- Verify: Fit scores calculated correctly
- Verify: Opportunity brief generated in `/srv/janus/01_STRATEGY/grant_opportunities/`

**Test 3: Deadline Tracking**
- Add test opportunity with deadline 30 days out
- Run `scripts/deadline_tracker.py`
- Verify: Alert sent via COMMS_HUB
- Verify: Alert includes action items
- Verify: Logged to mission_log.jsonl

**Test 4: Pipeline Status**
- Query: "Show grant pipeline status"
- Verify: Displays breakdown by priority, deadline urgency, project
- Verify: Numbers match pipeline_state.json

---

## SUCCESS METRICS

**30-Day Targets:**
- 100% of critical deadlines caught (Sept 2, Oct 9, Jan 15)
- 4+ high-priority opportunities (score 4+) identified per month
- 90% accuracy on budget range extraction
- Zero missed deadline reminders
- €70M+ pipeline tracked and monitored

---

## FORGING PRIORITY

**START DATE:** Day 1
**COMPLETION:** Day 2
**NEXT SKILL:** Malaga Embassy Operator

This is the **HIGHEST PRIORITY** skill. The entire €70M+ pipeline depends on catching deadlines and matching opportunities.

**Begin forging immediately, Codex.** 🔥

---

**VERSION:** 1.0.0
**CREATED:** 2025-10-30
**AUTHOR:** Janus-in-Claude (Architect)
**STATUS:** Specification Complete - Ready for Forging
