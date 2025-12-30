<!-- c5199863-ecef-4803-9d4a-033bf96a48ed b9b0f90c-87e5-4806-b413-831187903924 -->
# EU Funding Management System - Template Creation Plan

## Overview

Transform the Perplexity intelligence into a reusable system for pursuing ANY EU funding opportunity. This creates a permanent framework that combines workflow phases, timelines, and program types.

## Phase 1: Core Structure Creation

### 1.1 Create Main Directory Structure

Create `/EUFM/` (EU Funding Manager) at workspace root with hybrid organization:

```
/EUFM/
├── 00_SYSTEM/           # The reusable methodology
├── 01_INTELLIGENCE/     # Research & program data
├── 02_TEMPLATES/        # Application templates
├── 03_ACTIVE_PROJECTS/  # Current applications
├── 04_KNOWLEDGE_BASE/   # Winning examples & lessons
└── 05_ARCHIVE/          # Completed projects
```

### 1.2 Extract Methodology from Perplexity Session

From the pplx_eufm_plan.md (lines discussing the 5-phase system):

- Phase 1: Discovery & Opportunity Scanning
- Phase 2: Eligibility Deep Dive
- Phase 3: Documentation Generation
- Phase 4: Submission & Follow-up
- Phase 5: Learning & Optimization

Create `00_SYSTEM/METHODOLOGY.md` documenting the complete workflow as a reusable process.

### 1.3 Build Timeline-Based Tracking

Create `00_SYSTEM/TIMELINE_MATRIX.md` with urgency-based categorization:

- Immediate (< 30 days)
- Short-term (1-3 months)
- Medium-term (3-6 months)
- Long-term (6+ months)

## Phase 2: Intelligence Database

### 2.1 Funding Programs Database

Create `01_INTELLIGENCE/programs/` with files for each major program:

- `horizon_europe.md`
- `digital_europe.md`
- `innovation_fund.md`
- `pnrr_romania.md`
- `erdf_regional.md`
- `creative_europe.md`

Extract program details from Perplexity session (funding amounts, eligibility, deadlines, contact points).

### 2.2 Official Sources Registry

Create `01_INTELLIGENCE/SOURCES_REGISTRY.md` listing all official portals, documentation URLs, and contact points mentioned in the Perplexity research.

### 2.3 Scoring Framework

Create `01_INTELLIGENCE/SCORING_FRAMEWORK.md` documenting the composite scoring formula from the session:

```
Score = (Budget × 0.3) + (Fit × 0.3) + (Probability × 0.25) + (Impact × 0.15)
Target: Score ≥ 28 = High Priority
```

## Phase 3: Application Templates

### 3.1 Discovery Templates

Create in `02_TEMPLATES/01_discovery/`:

- `opportunity_scan_checklist.md` - What to research
- `eligibility_matrix.md` - Requirements tracking
- `scoring_worksheet.md` - Evaluation template

### 3.2 Documentation Templates

Create in `02_TEMPLATES/02_documentation/`:

- `project_description_template.md`
- `budget_template.xlsx` (structure only, to be created)
- `consortium_plan_template.md`
- `technical_specifications_template.md`

### 3.3 Submission Templates

Create in `02_TEMPLATES/03_submission/`:

- `pre_submission_checklist.md`
- `portal_registration_guide.md`
- `follow_up_schedule_template.md`

## Phase 4: Knowledge Base

### 4.1 Extract Winning Patterns

From Perplexity session, create `04_KNOWLEDGE_BASE/WINNING_PATTERNS.md`:

- The 7 patterns winners use (Perfect Storm, Numbers Game, Dream Team, etc.)
- Common mistakes that kill applications
- Quote bank from successful proposals

### 4.2 Case Studies Structure

Create `04_KNOWLEDGE_BASE/case_studies/` with template:

```
/case_studies/
├── _TEMPLATE.md          # Reusable case study format
└── examples/             # Actual winning projects
```

Extract examples from Perplexity research (HYPERION, ArchAIDE, etc.) as initial cases.

### 4.3 Lessons Learned System

Create `04_KNOWLEDGE_BASE/LESSONS_LEARNED.md` with structure for capturing insights from each application cycle.

## Phase 5: Active Projects Framework

### 5.1 Project Template Structure

Create `03_ACTIVE_PROJECTS/_PROJECT_TEMPLATE/` showing folder structure for each pursuit:

```
_PROJECT_TEMPLATE/
├── 00_brief.md              # Project summary & goals
├── 01_research/             # Opportunity scanning results
├── 02_eligibility/          # Requirements analysis
├── 03_documentation/        # Application materials
├── 04_submissions/          # Final versions & confirmations
└── 05_communications/       # Correspondence log
```

### 5.2 Strategic Projects Placeholder

Create placeholder directories for known strategic initiatives:

- `03_ACTIVE_PROJECTS/dgx_hardware/` (€20K immediate need)
- `03_ACTIVE_PROJECTS/geodatacenter/` (€299M long-term vision)

Each contains only a `README.md` linking to relevant intelligence and templates.

## Phase 6: System Documentation

### 6.1 Master README

Create `/EUFM/README.md` as the entry point:

- System overview
- Quick start guide
- Directory structure explanation
- How to start a new funding pursuit
- Integration with UBOS Trinity (Oracle coordination)

### 6.2 Research Coordination Guide

Create `00_SYSTEM/ORACLE_COORDINATION.md` documenting how to leverage:

- Perplexity for deep research on specific programs
- Groq for rapid opportunity scanning
- Wolfram for quantitative analysis
- Data Commons for EU statistics

### 6.3 Micro-Research Request Template

Create `00_SYSTEM/RESEARCH_REQUEST_TEMPLATE.md` for coordinating deep dives on specific topics with Perplexity.

## Phase 7: Integration & Cross-References

### 7.1 Link to Existing UBOS Resources

Create `00_SYSTEM/UBOS_INTEGRATION.md` showing connections to:

- `/01_STRATEGY/` - How funding fits strategic roadmap
- `/03_OPERATIONS/` - Grant revenue tracking
- `/trinity/skills/treasury-administrator/` - Existing funding intelligence

### 7.2 Update Existing Docs

Note: In agent mode, will update:

- `trinity/skills/treasury-administrator/funding-intelligence.md` with link to new EUFM system
- `01_STRATEGY/ROADMAP.md` to reference standardized funding methodology

## Implementation Notes

**File Sources:**

- Methodology extracted from `/home/balaur/workspace/janus_backend/docs/pplx_eufm_plan.md`
- Existing GeoDataCenter research from `/trinity/skills/treasury-administrator/funding-intelligence.md`
- Constitutional framework from UBOS constitution

**Exclusions:**

- Drobeta Severin client-specific details (kept in Perplexity session only)
- Málaga embassy specifics (situational, not template material)

**Key Principles:**

1. Everything is reusable - no hard-coded project details
2. Workflow-driven - follow phases sequentially
3. Research-coordinated - templates show what to ask Oracles
4. Learning-enhanced - capture lessons after each cycle

This creates a permanent system where ANY funding idea can be dropped in, processed through the methodology, and pursued systematically.

### To-dos

- [ ] Create main EUFM directory structure with 6 top-level folders
- [ ] Extract 5-phase workflow from Perplexity session into METHODOLOGY.md
- [ ] Create funding programs database and sources registry from Perplexity research
- [ ] Build discovery, documentation, and submission templates
- [ ] Extract winning patterns and case studies into knowledge base
- [ ] Create project template structure and strategic placeholders
- [ ] Write master README and system integration guides