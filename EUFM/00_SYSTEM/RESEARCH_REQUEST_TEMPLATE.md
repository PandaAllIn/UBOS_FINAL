# Research Request Template

**Purpose:** Standardized format for requesting deep-dive research from external oracles (especially Perplexity)

---

## Template Structure

```markdown
# RESEARCH REQUEST: [TOPIC]

**Request ID:** RR-[YYYYMMDD]-[sequential]  
**Requestor:** [Your name/role]  
**Target Oracle:** [Perplexity / Groq / Wolfram / Data Commons]  
**Priority:** [URGENT / HIGH / NORMAL / LOW]  
**Deadline:** [YYYY-MM-DD]  
**Related Project:** [Link to 03_ACTIVE_PROJECTS folder if applicable]

---

## Research Objective

[1-2 sentences describing WHAT you need to know and WHY]

---

## Specific Questions

1. [First specific question]
2. [Second specific question]
3. [etc.]

---

## Required Information

### Primary Requirements
- [ ] [First must-have piece of information]
- [ ] [Second must-have piece of information]
- [ ] [etc.]

### Secondary Requirements (if time permits)
- [ ] [Nice-to-have information]
- [ ] [etc.]

---

## Output Format

**Preferred Format:** [Markdown / JSON / CSV / PDF / Other]

**Structure:** [Describe how you want information organized]

**Length:** [Approximate length or level of detail needed]

---

## Context & Background

[Provide any relevant context that helps the oracle understand the request better]

---

## Follow-Up Plan

**How results will be used:** [Describe next steps]

**Quality check:** [How will you validate the research?]

**Storage:** [Where will results be saved?]

---

## Success Criteria

Research is complete when:
- [ ] [Criterion 1]
- [ ] [Criterion 2]
- [ ] [etc.]

---

```

---

## Example Request: Program Deep Dive

```markdown
# RESEARCH REQUEST: DIGITAL EUROPE AI FACTORIES PROGRAMME

**Request ID:** RR-20251103-001  
**Requestor:** Captain BROlinni  
**Target Oracle:** Perplexity  
**Priority:** HIGH  
**Deadline:** 2025-11-10  
**Related Project:** 03_ACTIVE_PROJECTS/dgx_hardware

---

## Research Objective

Gather complete intelligence on Digital Europe AI Factories programme to determine optimal application timing and strategy for UBOS constitutional AI infrastructure project.

---

## Specific Questions

1. What are the exact eligibility criteria for AI Factories calls?
2. What is the typical funding range and success rate?
3. What types of projects have been funded in previous calls?
4. What evaluation criteria are used and how are they weighted?
5. Are there geographic preferences or requirements (widening countries, etc.)?
6. What partnership structures are preferred (academic-industry, multi-country, etc.)?
7. What are the upcoming call deadlines for 2026-2027?

---

## Required Information

### Primary Requirements
- [ ] Official programme documentation URLs
- [ ] Complete eligibility criteria list
- [ ] Evaluation criteria and scoring methodology
- [ ] 3-5 examples of recently funded projects with budget details
- [ ] Upcoming call schedule with deadlines
- [ ] Contact points (helpdesk, national contact points)

### Secondary Requirements (if time permits)
- [ ] Success patterns from winning applications
- [ ] Common rejection reasons
- [ ] Typical project duration and budget breakdown
- [ ] Reporting requirements

---

## Output Format

**Preferred Format:** Structured Markdown

**Structure:**
```
## Overview
[Program summary]

## Eligibility
[Detailed criteria]

## Evaluation
[Criteria and weights]

## Examples
### Project 1
- Budget:
- Partners:
- Objective:
- Outcomes:

[etc.]

## Upcoming Calls
[Table with dates]

## Contacts
[List with emails/phones]

## Sources
[All URLs]
```

**Length:** Comprehensive (5-10 pages acceptable)

---

## Context & Background

UBOS is developing constitutional AI governance infrastructure that aligns with EU digital sovereignty priorities. We have prototype running on CPU, need GPU acceleration for production deployment. Previous research identified €60M available through Digital Europe, but need detailed intelligence to craft optimal application.

---

## Follow-Up Plan

**How results will be used:**
1. Determine if we qualify (eligibility check)
2. Score opportunity using SCORING_FRAMEWORK
3. Decide application timing (2026 vs 2027 call)
4. Begin consortium partner identification
5. Start application drafting if high-scoring

**Quality check:**
- Cross-reference all information with official EC portals
- Verify dates and amounts with Funding & Tenders Portal
- Validate examples using CORDIS database

**Storage:** Save in `03_ACTIVE_PROJECTS/digital_europe_ai/01_research/perplexity_deep_dive_20251103.md`

---

## Success Criteria

Research is complete when:
- [ ] We can confidently answer "Are we eligible?"
- [ ] We can calculate opportunity score (≥2.8 threshold)
- [ ] We know next deadline and can plan timeline
- [ ] We have 3+ similar funded projects to learn from
- [ ] We have direct contact for questions

---

```

---

## Example Request: Winning Project Analysis

```markdown
# RESEARCH REQUEST: HYPERION PROJECT ANALYSIS

**Request ID:** RR-20251103-002  
**Requestor:** Claude (Strategic Mind)  
**Target Oracle:** Perplexity  
**Priority:** NORMAL  
**Deadline:** 2025-11-15  
**Related Project:** 04_KNOWLEDGE_BASE/case_studies/hyperion

---

## Research Objective

Analyze the HYPERION project (€8M Horizon 2020 cultural heritage + AI) to extract winning patterns applicable to UBOS grant applications.

---

## Specific Questions

1. What was the exact project structure and consortium composition?
2. How did they frame the AI + cultural heritage combination?
3. What evaluation criteria did they excel in?
4. What was their impact narrative?
5. What were the key deliverables and timeline?
6. What results did they achieve?
7. How is their approach replicable for other domains?

---

## Required Information

### Primary Requirements
- [ ] Official project page URL (CORDIS)
- [ ] Consortium partners list with roles
- [ ] Budget breakdown
- [ ] Project objectives and methodology
- [ ] Key deliverables
- [ ] Published results and impact

### Secondary Requirements
- [ ] Quotes from project description
- [ ] Lessons learned (if documented)
- [ ] Follow-on projects or funding
- [ ] Media coverage or awards

---

## Output Format

**Preferred Format:** Case study markdown

**Structure:** Use `04_KNOWLEDGE_BASE/case_studies/_TEMPLATE.md`

**Length:** 3-5 pages

---

## Context & Background

HYPERION was mentioned in Perplexity session as example of successful AI + cultural heritage project. Want to study their approach as potential template for combining AI with other traditional sectors (energy, governance, etc.).

---

## Follow-Up Plan

**How results will be used:**
1. Add to knowledge base as case study
2. Extract reusable narrative patterns
3. Identify partnership models
4. Learn from their evaluation success

**Quality check:**
- Verify all information from official CORDIS database
- Cross-reference with project website if available
- Check for published papers or deliverables

**Storage:** `04_KNOWLEDGE_BASE/case_studies/examples/hyperion.md`

---

## Success Criteria

Research is complete when:
- [ ] We understand WHY they were funded
- [ ] We can identify 3+ patterns to replicate
- [ ] We have their actual project description quotes
- [ ] Case study is ready for knowledge base

---

```

---

## Tips for Effective Research Requests

### Be Specific
❌ "Research Digital Europe"  
✅ "What are eligibility criteria for Digital Europe AI Factories calls opening in 2026?"

### Provide Context
Tell the oracle WHY you need this and HOW you'll use it. Better context = better research.

### Set Clear Success Criteria
Define what "done" looks like. Oracle should know when they've answered completely.

### Request Structured Output
Specify format - makes it easier to integrate into your systems.

### Include Validation Plan
Show how you'll verify accuracy. Encourages oracle to cite sources.

---

## Storage & Organization

**Active Requests:** Store in `03_ACTIVE_PROJECTS/[project]/01_research/requests/`

**Completed Research:** Store in `03_ACTIVE_PROJECTS/[project]/01_research/results/`

**Reusable Intelligence:** Extract to `01_INTELLIGENCE/` or `04_KNOWLEDGE_BASE/`

---

## Oracle-Specific Variations

### For Perplexity
- Emphasize need for recent information and source URLs
- Request synthesis across multiple sources
- Ask for similar project examples

### For Groq
- Keep requests simple and fast-answerable
- Focus on keyword extraction and pattern matching
- Expect JSON-structured outputs

### For Wolfram
- Provide exact formulas or calculations needed
- Specify units and precision
- Request validation methodology

### For Data Commons
- Specify geographic and temporal scope
- Request official EU statistics only
- Ask for data provenance (source + date)

---

## Version History

**v1.0 (November 2025):** Initial template based on Perplexity coordination experience.

---

**Good research starts with good questions. Use this template to ask better questions.** 🔍

