# Daily Funding Pulse Monitoring Checklist

**Purpose:** Systematic daily monitoring routine for Phase 1 (Manual POC)  
**Time Required:** 30-45 minutes  
**Frequency:** Every morning (06:00-07:00 UTC recommended)  
**Owner:** Captain BROlinni

---

## Morning Routine (30 minutes)

### Step 1: Comitology Register Check (5 min) 🔥 TOP PRIORITY

**URL:** https://ec.europa.eu/transparency/comitology-register/screen/search

**Search Configuration:**
- Committee: All
- Document Type: "Draft"
- Subject Matter: "Horizon Europe"
- Date Range: Last 7 days

**What to Look For:**
- [ ] Any new "Draft Work Programme" documents
- [ ] **Cluster 4 (Digital, Industry, Space)** - CRITICAL WATCH
- [ ] Cluster 2 (Culture, Creativity, Society) - Expected November
- [ ] Cluster 5 (Climate, Energy, Mobility) - Expected December

**If Draft Detected:**
1. ⚠️ IMMEDIATE ALERT - This is 4-month lead time!
2. Download PDF immediately
3. Create signal file: `../signals_detected/draft_cluster_X_YYYY-MM-DD.md`
4. Note detection date/time
5. Update TIMELINE_MATRIX with predicted call opening (draft date + 4 months)
6. Send puck to Claude via Comms Hub (if automated) or note for daily review

**Recording:**
```markdown
Date: YYYY-MM-DD
Time: HH:MM UTC
Finding: [Draft detected / No new drafts]
Details: [If detected: which cluster, publication date, URL]
Confidence: [HIGH/MEDIUM/LOW]
```

---

### Step 2: Commission Press Room Scan (5 min)

**URL:** https://ec.europa.eu/commission/presscorner/

**Quick Scan:**
- [ ] Today's press releases (top 5-10)
- [ ] Filter by topic: Research, Digital, Climate, Innovation
- [ ] Look for keywords: "funding", "call", "programme", "billion", "investment"

**What to Flag:**
- Commissioner speeches (especially von der Leyen, Gabriel, Breton)
- New policy initiatives
- Budget announcements
- Programme launches

**If Relevant Found:**
- Copy URL and headline
- Assess relevance to EUFM projects (DGX, GeoDataCenter)
- Log in `../signals_detected/press_YYYY-MM-DD.md` if significant

---

### Step 3: Perplexity Query Batch (20 min)

**Run these 5 queries daily:**

#### Query 1: Today's Opportunities
```
"European Commission funding opportunities November 3 2025 latest"
```
**What to Extract:**
- New call announcements
- Deadline changes
- Programme updates

#### Query 2: Horizon Europe Pipeline
```
"Horizon Europe calls opening Q1 2026 announcement"
```
**What to Extract:**
- Upcoming call previews
- Draft work programme mentions
- Timeline indications

#### Query 3: Digital Europe AI Focus
```
"Digital Europe Programme AI infrastructure new calls November 2025"
```
**What to Extract:**
- AI Factories updates
- EDIH developments
- Cloud/compute infrastructure opportunities

#### Query 4: Policy Developments
```
"EU innovation policy November 2025 updates"
```
**What to Extract:**
- New policy announcements
- Legislative progress
- Priority shifts

#### Query 5: Work Programme Intelligence
```
"Commission work programme 2026 funding implications"
```
**What to Extract:**
- Budget allocation signals
- New initiative mentions
- Implementation timelines

**For Each Query:**
- [ ] Run search
- [ ] Review top 10 results
- [ ] Click through 2-3 most relevant
- [ ] Note: Date, source, key finding, confidence level
- [ ] Save to: `../daily_scans/YYYY-MM-DD_scan.md`

**Template:**
```markdown
## Query: [query text]
**Run at:** HH:MM UTC
**Top findings:**
1. [Source] - [Headline/Summary] - [URL]
2. [Source] - [Headline/Summary] - [URL]
3. [Source] - [Headline/Summary] - [URL]

**Key Signals:**
- [Any significant funding opportunities, policy shifts, or timing indicators]

**Confidence:** [HIGH/MEDIUM/LOW]
**Relevance to EUFM:** [CRITICAL/HIGH/MEDIUM/LOW]
```

---

### Step 4: Quick Portal Check (3 min)

**URL:** https://ec.europa.eu/info/funding-tenders/opportunities/portal/screen/opportunities/calls-search

**Filters:**
- Status: "Forthcoming" (shows what's coming before it opens)
- Programme: Horizon Europe, Digital Europe, Innovation Fund
- Topic: AI, digital, infrastructure, clean tech

**Quick Scan:**
- [ ] Any new "Forthcoming" calls appeared?
- [ ] Any deadline changes to open calls?
- [ ] Budget amounts changed?

**Record:**
- Note any changes vs. yesterday
- If significant: Create signal file

---

### Step 5: Logging & Synthesis (5 min)

**Daily Log Entry:** `../daily_scans/YYYY-MM-DD_scan.md`

**Template:**
```markdown
# Daily Pulse Scan - [Day of Week], [Date]

**Scan completed:** HH:MM UTC  
**Scan duration:** XX minutes  
**Operator:** [Your name]

## Findings Summary

**HIGH PRIORITY:**
- [List any critical findings]

**MEDIUM PRIORITY:**
- [List interesting signals]

**LOW/BACKGROUND:**
- [Note any context or trends]

## Action Items

- [ ] [Any immediate follow-ups needed]
- [ ] [Any signals requiring validation]
- [ ] [Any TIMELINE_MATRIX updates needed]

## Perplexity Query Results

[Paste summaries from Step 3]

## Watch List Status

- Cluster 4 Draft: [Still waiting / DETECTED!]
- Cloud & AI Act: [Any new mentions?]
- Other tracked signals: [Updates]

## Prediction Log

[Any new predictions about upcoming opportunities]

## Notes

[Any observations, patterns, or insights]
```

---

## Weekly Deep Dive (Friday, 1 hour)

### Extended Source Check

- [ ] Digital Europe News (all week's posts)
- [ ] EUR-Lex (filter by last 7 days, keyword search)
- [ ] European Parliament (plenary summaries)
- [ ] CORDIS (newly funded projects analysis)
- [ ] NCP newsletters (UEFISCDI, Ministry)

### Pattern Analysis

- [ ] Review all daily logs from the week
- [ ] Identify recurring themes
- [ ] Track keyword frequency changes
- [ ] Note any emerging topics

### Validation Updates

- [ ] Update `../validation_log.md` with:
  - Predictions made this week
  - Any predictions from past that came true/false
  - Accuracy calculations
  - Model refinements needed

### Timeline Matrix Sync

- [ ] Review EUFM TIMELINE_MATRIX
- [ ] Add any new signals detected this week
- [ ] Update confidence levels on existing entries
- [ ] Move opportunities between urgency tiers as needed

---

## Signal Detection Criteria

### When to Create Signal File

Create `../signals_detected/signal_YYYY-MM-DD_[name].md` when:

**CRITICAL:** (Immediate action required)
- [ ] Draft work programme detected
- [ ] Call opening announced < 30 days
- [ ] Major policy shift in core area (AI, clean tech, digital)

**HIGH:** (Significant opportunity)
- [ ] New programme announced
- [ ] Forthcoming call detected (30-90 days out)
- [ ] New policy term in 3+ sources
- [ ] Budget allocation announced

**MEDIUM:** (Track and monitor)
- [ ] Interesting trend emerging
- [ ] 3-6 month horizon opportunity
- [ ] Related policy development
- [ ] Consortium formation activity

### Signal File Template

```markdown
# Signal: [Brief Description]

**Detected:** YYYY-MM-DD HH:MM UTC  
**Source:** [URL or source name]  
**Priority:** [CRITICAL/HIGH/MEDIUM/LOW]  
**Confidence:** [HIGH/MEDIUM/LOW] (%)

---

## Signal Details

**What was detected:**
[Clear description of the finding]

**Source reliability:**
- Type: [Official EU / News / Analysis / Rumor]
- Verification: [Cross-checked with X other sources]

**Predicted Impact:**
- Type of opportunity: [Call / Programme / Policy change]
- Expected timeline: [When will this materialize?]
- Budget range (if known): €X - €Y
- Relevance to EUFM: [Which active projects?]

---

## Evidence

**Primary Source:**
- URL: [link]
- Date: [publication date]
- Key quote: "[exact text]"

**Corroborating Sources:**
1. [Source 2 - URL]
2. [Source 3 - URL]

---

## Analysis

**Why this matters:**
[Strategic significance]

**Lead time advantage:**
[How much notice do we have vs. general public?]

**Recommended actions:**
- [ ] [Immediate action 1]
- [ ] [Follow-up action 2]
- [ ] [Monitoring action 3]

---

## Validation Plan

**Prediction:**
[What do we expect to happen and when?]

**Check date:**
[When should we verify if this prediction was correct?]

**Success criteria:**
[What would confirm this signal was accurate?]

---

## Updates

[Add updates as situation develops]

- YYYY-MM-DD: [Update 1]
- YYYY-MM-DD: [Update 2]
```

---

## Monthly Review (First Monday, 2 hours)

### Accuracy Assessment

- [ ] Review all predictions from previous month
- [ ] Calculate: Correct predictions / Total predictions
- [ ] Calculate: Average lead time achieved
- [ ] Calculate: False positive rate
- [ ] Calculate: Missed opportunities (false negatives)

### Model Refinement

- [ ] Which sources were most valuable?
- [ ] Which keywords/searches worked best?
- [ ] What patterns emerged?
- [ ] What should we stop monitoring?
- [ ] What new sources should we add?

### Documentation Updates

- [ ] Update `rss_subscriptions.md` with findings
- [ ] Refine search queries based on results
- [ ] Update this checklist with lessons learned

### Strategic Planning

- [ ] Brief Claude on monthly findings
- [ ] Discuss: Ready for Phase 2 automation?
- [ ] Identify: High-value automation targets
- [ ] Plan: Next month's focus areas

---

## Emergency Procedures

### If CRITICAL Signal Detected

**STOP everything and:**
1. ✅ Verify source is official/reliable
2. ✅ Create signal file immediately
3. ✅ Update TIMELINE_MATRIX with urgency flag
4. ✅ Notify Captain (if not you!)
5. ✅ Send puck to Claude for strategic assessment
6. ✅ Check: Does this affect active projects?
7. ✅ Calculate: Lead time advantage
8. ✅ Draft: Immediate response plan

**Examples of CRITICAL signals:**
- Cluster 4 draft detected (GeoDataCenter relevance)
- Digital Europe AI Factories call announced
- Innovation Fund large-scale call opening
- PNRR digitalization programme update
- Major policy shift affecting current applications

---

## Success Metrics (Phase 1)

Track weekly:
- [ ] Scans completed / Scans planned (goal: 100%)
- [ ] Signals detected (total count)
- [ ] Signals by priority (CRITICAL/HIGH/MEDIUM/LOW)
- [ ] Time spent per day (goal: 30-45 min)
- [ ] Perplexity queries run (goal: 5/day)

Track monthly:
- [ ] Prediction accuracy %
- [ ] Average lead time (days)
- [ ] False positive rate %
- [ ] Missed opportunities (count)
- [ ] Value created (€ from early detection)

**Phase 1 Success Criteria:**
- Detect Cluster 4 draft before general awareness ✅
- Achieve 75%+ prediction accuracy ✅
- Maintain 45+ day average lead time ✅
- <15% false positive rate ✅

---

## Tips for Efficiency

### Browser Setup
- Bookmark all Tier 1 sources in folder "Daily Pulse"
- Use browser auto-refresh extensions for Comitology Register
- Set up RSS reader with daily digest email (06:00 UTC)

### Perplexity Optimization
- Save the 5 daily queries as templates
- Use Perplexity collections to organize findings
- Enable date range filters (last 7 days)

### Note-Taking
- Use markdown editor with templates
- Keep Obsidian/Notion open for quick logging
- Use voice-to-text for observations while scanning

### Pattern Recognition
- Keep a "gut feelings" log
- Note when something "feels different"
- Track your own learning curve

---

## Handoff to Automation (Phase 2)

**When this becomes automated:**
- RSS monitor will do Step 1 & 2 hourly
- Perplexity client will run Step 3 automatically
- Signal classifier will identify priority
- Alert router will notify you of HIGH/CRITICAL only
- You'll spend 10 min/day reviewing vs. 30-45 min doing

**Until then:** This checklist is your daily routine.

---

**Created:** November 3, 2025  
**Version:** 1.0 (Manual POC)  
**Next Update:** After first week (November 10, 2025)  
**Status:** ACTIVE - Start tomorrow morning! ☀️

