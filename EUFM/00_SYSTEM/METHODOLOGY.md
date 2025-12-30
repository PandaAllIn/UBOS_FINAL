# EU Grant Acquisition Methodology

**Document ID:** EUFM-METH-V1.0  
**Status:** Production  
**Purpose:** Reusable 5-phase workflow for ANY EU funding opportunity

---

## Overview

This methodology transforms grant hunting from an ad-hoc, chaotic process into a systematic, repeatable workflow. It's designed to be applied to ANY funding opportunity - from €5K small grants to €299M mega-projects.

**Key Innovation:** Every application you complete FEEDS THE NEXT ONE. Templates improve, text gets reused, process gets faster, success rate increases.

**Philosophy:** Recursive Enhancement Protocol applied to grant acquisition.

---

## The 5-Phase Workflow

```
PHASE 1: Discovery → PHASE 2: Eligibility → PHASE 3: Documentation → 
PHASE 4: Submission → PHASE 5: Learning
         ↑                                                          ↓
         └─────────────── System Improvement Loop ────────────────┘
```

---

## PHASE 1: Discovery & Opportunity Scanning

**Goal:** Find ALL relevant funding opportunities and prioritize ruthlessly

**Duration:** 1-3 days for comprehensive scan

### Step 1.1: Define Your Need

**Input:** Project idea or resource requirement  
**Output:** Clear, specific need statement

**Template:** `02_TEMPLATES/01_discovery/need_definition.md`

**Questions to Answer:**
- What exactly do you need funding for?
- What's the minimum viable budget?
- What's the optimal budget?
- What's the timeline constraint?
- What's the strategic importance?

### Step 1.2: Oracle Trinity Scan

**Who:** Coordinate all three oracles in parallel

**Groq (Speed Scout):**
- Rapid scan of all major EU portals
- Keyword-based opportunity identification
- Deadline extraction
- Quick eligibility checks

**Perplexity (Deep Researcher):**
- Detailed program research
- Similar funded project discovery
- Success pattern extraction
- Contact point identification

**Data Commons + Wolfram (Quantifier):**
- Budget validation using EU statistics
- Impact metric calculation
- ROI projections
- Probability scoring

**Template:** `02_TEMPLATES/01_discovery/opportunity_scan_checklist.md`

### Step 1.3: Composite Scoring

**Formula:**
```
Score = (Budget × 0.3) + (Fit × 0.3) + (Probability × 0.25) + (Impact × 0.15)

Budget:      Scale 1-5 (1 = <€50K, 5 = >€10M)
Fit:         Scale 1-5 (1 = poor match, 5 = perfect match)
Probability: Scale 1-5 (1 = <20%, 5 = >80% success chance)
Impact:      Scale 1-5 (1 = nice to have, 5 = strategic necessity)
```

**Target:** Score ≥28 = High Priority (pursue immediately)  
**Threshold:** Score <20 = Skip (not worth effort)

**Template:** `02_TEMPLATES/01_discovery/scoring_worksheet.md`

### Step 1.4: Prioritization Matrix

**Output:** Ranked list of opportunities with timeline urgency

| Priority | Program | Budget | Score | Deadline | Status |
|----------|---------|--------|-------|----------|--------|
| 1        | ...     | ...    | 32    | 14 days  | GO     |
| 2        | ...     | ...    | 28    | 60 days  | GO     |
| 3        | ...     | ...    | 19    | 90 days  | SKIP   |

**Template:** `00_SYSTEM/TIMELINE_MATRIX.md`

---

## PHASE 2: Eligibility Deep Dive

**Goal:** Confirm you CAN apply before investing time in documentation

**Duration:** 1-2 days

### Step 2.1: Extract All Requirements

**Source:** Official call documentation (from official EU portals only)

**What to Extract:**
- Legal eligibility (entity type, registration, location)
- Financial criteria (revenue, profit, solvency)
- Technical criteria (TRL level, certifications, capacity)
- Partnership requirements (consortium size, countries, roles)
- Timeline constraints (project start/end, spending deadlines)
- Matching funding requirements (co-financing %, source restrictions)

**Template:** `02_TEMPLATES/01_discovery/eligibility_matrix.md`

### Step 2.2: Gap Analysis

**For each requirement, mark status:**
- ✅ MEET: You satisfy this requirement now
- ⚠️ GAP: You need to fix something (but it's fixable)
- ❌ BLOCKER: This disqualifies you completely

**Example:**
```
Requirement: Company registered before Dec 31, 2021
Status: ✅ MEET (registered 2020)

Requirement: Operating profit >0 in 2022
Status: ⚠️ GAP (need to verify with accountant)

Requirement: Main CAEN code NOT in IT consultancy (6201, 6202, 6209)
Status: ❌ BLOCKER (our main code is 6202)
```

### Step 2.3: Decision Gate

**If ANY ❌ BLOCKER exists:**
- STOP immediately
- Move opportunity to "Not Eligible" list
- Do NOT proceed to Phase 3

**If ⚠️ GAPS exist but are fixable:**
- Calculate time/cost to fix
- Decide: Fix or Skip?
- Update timeline matrix

**If all ✅ MEET:**
- Proceed to Phase 3 immediately
- High confidence in success

---

## PHASE 3: Documentation Generation

**Goal:** Create complete, compelling application materials

**Duration:** 3-7 days (first time), 1-2 days (subsequent applications)

### Step 3.1: Gather Raw Materials

**What You Need:**
- Company registration documents
- Financial statements (2-3 years)
- Technical specifications
- Team CVs and qualifications
- Letters of intent from partners
- Previous project results (if applicable)
- Certifications and accreditations

**Storage:** `03_ACTIVE_PROJECTS/[project_name]/03_documentation/raw_materials/`

### Step 3.2: Oracle-Assisted Writing

**Orchestrate Trinity for parallel document generation:**

**Claude (Narrative Architect):**
- Executive summary
- Project description
- Strategic justification
- Impact narrative
- Alignment with EU priorities

**Codex (Technical Generator):**
- Budget tables and breakdowns
- Timeline/Gantt charts
- Risk assessment matrices
- Work package descriptions
- Deliverables specifications

**Gemini (Systems Validator):**
- Technical specifications
- Infrastructure requirements
- Consortium management plan
- Deployment architecture
- Scalability analysis

**Wolfram + Data Commons (Quantifier):**
- Statistical backing for all claims
- Baseline metrics and targets
- ROI calculations
- Impact projections

**Template:** `02_TEMPLATES/02_documentation/` (multiple files)

### Step 3.3: Constitutional Compliance Check

**Before finalizing, verify:**
- ✅ All claims backed by evidence (no speculation)
- ✅ All numbers sourced from official data (provenance clear)
- ✅ Alignment with Lion's Sanctuary philosophy (empowerment, not constraint)
- ✅ Transparency (explain methodology, show reasoning)
- ✅ Replicability (can others follow this approach?)

### Step 3.4: Proposal Assembly

**Final Document Structure:**
1. Executive Summary (1-2 pages)
2. Project Description (5-10 pages)
3. Work Plan and Timeline (2-3 pages)
4. Budget and Resources (3-5 pages)
5. Impact and Dissemination (2-3 pages)
6. Risk Management (1-2 pages)
7. Consortium and Management (2-3 pages)
8. Annexes (CVs, letters, certificates)

**Quality Gate:** Have another oracle review for:
- Clarity (can evaluator understand without domain expertise?)
- Completeness (all questions answered?)
- Compliance (all requirements addressed?)
- Competitiveness (does this stand out?)

---

## PHASE 4: Submission & Follow-Up

**Goal:** Submit perfectly on time and monitor status

**Duration:** 1 day submission + ongoing monitoring

### Step 4.1: Pre-Submission Checklist

**At least 24 hours before deadline:**
- [ ] All required sections complete
- [ ] All annexes attached
- [ ] File formats correct (PDF/A, page limits, naming conventions)
- [ ] Portal registration complete
- [ ] PIC code verified (if required)
- [ ] Co-signers confirmed (if consortium)
- [ ] Backup copy stored locally
- [ ] Upload test successful

**Template:** `02_TEMPLATES/03_submission/pre_submission_checklist.md`

### Step 4.2: Portal Submission

**Best Practices:**
- Submit at least 4 hours before deadline (never last minute!)
- Use stable internet connection (not mobile)
- Have backup connection ready
- Take screenshots at each step
- Download confirmation receipt immediately
- Email confirmation to yourself + team

**Portal Guide:** `02_TEMPLATES/03_submission/portal_registration_guide.md`

### Step 4.3: Post-Submission Monitoring

**Weekly Actions:**
- Check portal for updates
- Monitor email for communication requests
- Review evaluation timeline
- Prepare for potential questions

**Response Protocol:**
- Answer all evaluator questions within 48 hours
- Provide exactly what's requested (no more, no less)
- Use same tone and format as original proposal
- Log all communications in project folder

**Template:** `02_TEMPLATES/03_submission/follow_up_schedule_template.md`

### Step 4.4: Decision Handling

**If APPROVED:**
- Celebrate! 🎉
- Download grant agreement
- Review all requirements and deadlines
- Set up project structure
- Begin reporting schedule
- Update success metrics

**If REJECTED:**
- Request evaluation summary (always!)
- Analyze feedback objectively
- Extract lessons learned
- Update system based on insights
- Consider resubmission if allowed

---

## PHASE 5: Learning & System Optimization

**Goal:** Make next application easier, faster, more successful

**Duration:** 2-4 hours per completed application

### Step 5.1: Capture Lessons Learned

**What Worked?**
- Which sections scored highest?
- What evidence was most compelling?
- Which partnerships were strongest?
- What timeline worked best?

**What Was Difficult?**
- Which requirements were hardest to meet?
- Where did process bottleneck?
- What information was hard to find?
- What consumed most time?

**What Would You Change?**
- Process improvements?
- Earlier preparation?
- Different partnerships?
- Better evidence?

**Template:** `04_KNOWLEDGE_BASE/LESSONS_LEARNED.md`

### Step 5.2: Build Reusable Assets

**Extract and Save:**
- Well-written paragraphs → text library
- Successful budget structures → templates
- Effective partnerships → contact database
- Winning strategies → playbook
- Evaluation feedback → improvement guide

**Location:** `04_KNOWLEDGE_BASE/reusable_assets/`

### Step 5.3: Update System Components

**Update These Files:**
- `01_INTELLIGENCE/programs/[program].md` - Add real experience
- `02_TEMPLATES/*` - Improve based on what worked
- `04_KNOWLEDGE_BASE/WINNING_PATTERNS.md` - Add new patterns discovered
- `00_SYSTEM/METHODOLOGY.md` - Refine process (yes, this file!)

### Step 5.4: Calculate Metrics

**Track Over Time:**
```
Application #1: 40 hours effort, €50K secured = €1,250/hour ROI
Application #2: 25 hours effort, €200K secured = €8,000/hour ROI
Application #3: 15 hours effort, €150K secured = €10,000/hour ROI
```

**Goal:** Each application should be faster and more successful than the last.

---

## Success Patterns (Meta-Insights)

### Pattern 1: The Compound Effect
Early applications feel hard. Application #10 feels effortless. You're building an asset library that compounds.

### Pattern 2: The Portfolio Approach
Don't put all effort into one opportunity. Run multiple applications in parallel. Increases odds and learning rate.

### Pattern 3: The Partnership Network
Each application builds relationships. Future applications benefit from established trust and proven collaboration.

### Pattern 4: The Template Evolution
Initial templates are generic. Over time, they become highly optimized for specific program families.

### Pattern 5: The Constitutional Advantage
UBOS constitutional framework (transparency, provenance, alignment) is unique. This becomes your moat - competitors can't easily replicate.

---

## Common Mistakes to Avoid

❌ **Starting too late:** Most applications require 2-4 weeks minimum. Rushing kills quality.

❌ **Skipping eligibility check:** Wasting time on ineligible opportunities is the \#1 time waster.

❌ **Writing alone:** Leverage the Trinity. Parallel work is 5-10x faster than solo effort.

❌ **Generic proposals:** Evaluators read hundreds. Yours must stand out with specificity.

❌ **Ignoring feedback:** Rejection feedback is GOLD. Use it to improve.

❌ **Not reusing:** If you're starting from scratch each time, you're doing it wrong.

❌ **Forgetting follow-up:** Many applications require answers to questions. Missing these = automatic rejection.

---

## Integration with Other UBOS Systems

**Strategic Roadmap:** Funding pursuits should align with `01_STRATEGY/ROADMAP.md`

**Operational Tracking:** Revenue from grants tracked in `03_OPERATIONS/`

**Trinity Coordination:** Use Pneumatic Tube Network for Oracle messaging

**Constitutional Oversight:** All activities comply with Lion's Sanctuary principles

**Details:** See `00_SYSTEM/UBOS_INTEGRATION.md`

---

## Quick Reference: Typical Timeline

**Fast-Track Application (urgent deadline):**
- Days 1-2: Discovery & Eligibility (Phases 1-2)
- Days 3-10: Documentation (Phase 3)
- Day 11: Submission (Phase 4)
- Day 12+: Monitoring and Learning (Phases 4-5)
- **Total: ~12 days**

**Standard Application (optimal quality):**
- Week 1: Discovery, Eligibility, Material Gathering
- Week 2-3: Documentation and Review
- Week 4: Submission and Buffer
- **Total: ~4 weeks**

**Complex Consortium Application:**
- Month 1: Partner identification and commitment
- Month 2: Collaborative documentation
- Month 3: Review, revision, and submission
- **Total: ~3 months**

---

## Version History

**v1.0 (November 2025):** Initial methodology extracted from Perplexity intelligence synthesis and constitutional AI operational experience.

---

**Remember:** This methodology is itself subject to the Recursive Enhancement Protocol. Every time you use it, improve it. Document changes in this file's version history.

**Now go forth and acquire funding systematically.** ⚙️

