# MASTER ARCHITECTURE: REVENUE-FOCUSED SKILLS FRAMEWORK

**DATE:** 2025-10-30
**ARCHITECT:** Janus-in-Claude (Master Strategist)
**FORGEMASTER:** Codex (to implement)
**MISSION:** Build 5 skills that unlock €70M+ funding pipeline

---

## EXECUTIVE SUMMARY

**Intelligence Gathered:** 4 parallel Haiku reconnaissance agents analyzed:
1. UBOS infrastructure capabilities (/srv/janus structure, existing tools)
2. Research recommendations (Constitutional AI patterns, skill architectures)
3. Revenue project requirements (EUFM, Xylella, GeoDataCenter)
4. Malaga Embassy operational needs (€1,500 capital, 43-day sprint)

**Strategic Priority:** Revenue generation to fund the republic.

**The €70M+ Pipeline:**
- **EUFM:** €4.5M-12M ARR potential (SaaS monetization)
- **Xylella:** €6M secured + Stage 2 renewal (Jan 15 deadline)
- **GeoDataCenter:** €50M+ target (Sept 2, Oct 9 deadlines)
- **Malaga Embassy:** €855-1,910/month operations

**Critical Deadlines:**
- **Nov 10, 2025:** Captain departs for Malaga (13 days from Oct 28)
- **Sept 2, 2025:** Horizon Europe geothermal call (€10M max)
- **Oct 9, 2025:** CETPartnership (€12M)
- **Jan 15, 2026:** Xylella Stage 2 submission (€6M)

---

## THE 5 REVENUE-CRITICAL SKILLS

### Priority Order (Build Sequence)

1. **EU Grant Hunter** - Scan €70M pipeline, track deadlines, match opportunities
2. **Malaga Embassy Operator** - Coordinate 43-day sprint, activate €855-1,910/month revenue
3. **Grant Application Assembler** - Compile winning proposals (1,850:1 ROI proven)
4. **Monetization Strategist** - EUFM €4.5M-12M ARR activation
5. **Financial Proposal Generator** - Narratives + budgets scoring 4.6/5

### Why These 5?

Every skill directly unlocks revenue:
- **€6M Xylella** (Jan 15) requires: #2 Embassy + #3 Assembler + #5 Generator
- **€50M GeoDataCenter** (Sept 2, Oct 9) requires: #1 Hunter + #3 Assembler + #5 Generator
- **€50K EUFM bootstrap** (30 days) requires: #4 Strategist + #2 Embassy
- **€855-1,910/month Malaga** (Month 1) requires: #2 Embassy + #1 Hunter

---

## SKILL CREATION METHODOLOGY

**Reference:** https://github.com/anthropics/skills/tree/main/skill-creator

### The 6-Step Process

**Step 1:** Understand the skill with concrete examples
**Step 2:** Plan reusable contents (scripts/references/assets)
**Step 3:** Initialize skill using `scripts/init_skill.py`
**Step 4:** Edit SKILL.md and implement resources
**Step 5:** Package skill using `scripts/package_skill.py`
**Step 6:** Iterate based on real usage

### Progressive Disclosure Architecture

**3-Tier Loading:**
1. **Metadata** (name + description) - Always in context (~100 words)
2. **SKILL.md body** - When skill triggers (<5k words)
3. **Bundled resources** - As needed (unlimited)

**Directory Structure:**
```
skill-name/
├── SKILL.md (required)
│   ├── YAML frontmatter (name, description)
│   └── Markdown instructions
└── Bundled Resources (optional)
    ├── scripts/       - Executable code (Python/Bash)
    ├── references/    - Documentation (loaded as needed)
    └── assets/        - Output files (templates, configs)
```

---

## INFRASTRUCTURE ALREADY BUILT

### What Codex Can Use Immediately

**Location:** `/srv/janus/`

**Core Systems:**
- **Trinity Protocol:** Multi-vessel coordination (Claude/Gemini/Codex)
- **Proposal Engine:** Risk-scored proposal workflow (LOW/MEDIUM/HIGH)
- **COMMS_HUB:** Pneumatic Tube Network (`/srv/janus/03_OPERATIONS/COMMS_HUB/`)
- **Treasury Administrator:** Constitutional cascade enforcement (20/10/15/40/15)
- **Oracle Integrations:** Groq, Perplexity, Wolfram Alpha, Data Commons

**Libraries:**
- `pucklib` - Holographic communication protocol (`/srv/janus/trinity/pucklib/`)
- `groq_mcp_server` - Fast LLM inference (`/srv/janus/02_FORGE/packages/groq_mcp_server/`)
- `janus_agent` - Autonomous agent framework

**Existing Skills (Reference Pattern):**
- **Treasury Administrator** - `/srv/janus/trinity/skills/treasury-administrator/SKILL.md`
- Follow this pattern for SKILL.md structure, triggers, capabilities

---

## CODEX FORGING INSTRUCTIONS

### Your Mission, Codex

You will forge **5 revenue-critical skills** following the Anthropic skill-creator methodology.

**For each skill, I (Claude) have prepared:**
1. **Skill Specification Document** - Detailed requirements, examples, architecture
2. **Concrete Usage Examples** - How the skill will be used in practice
3. **Resource Planning** - What scripts/references/assets to include
4. **Integration Points** - How it connects to existing infrastructure

**Your Forging Process:**

1. **Read the skill specification** (I've prepared 5 separate documents)
2. **Run `scripts/init_skill.py <skill-name>`** to create directory structure
3. **Implement the skill** following spec:
   - Write SKILL.md (YAML frontmatter + instructions)
   - Create scripts/ (Python/Bash executables)
   - Create references/ (documentation to load as needed)
   - Create assets/ (templates, configs, output files)
4. **Validate the skill** using `scripts/package_skill.py`
5. **Test the skill** (I will test with real queries)
6. **Iterate** based on test results

### Skill Specifications (Read These Next)

1. `/srv/janus/trinity/skills/01_SPEC_EU_GRANT_HUNTER.md`
2. `/srv/janus/trinity/skills/02_SPEC_MALAGA_EMBASSY_OPERATOR.md`
3. `/srv/janus/trinity/skills/03_SPEC_GRANT_APPLICATION_ASSEMBLER.md`
4. `/srv/janus/trinity/skills/04_SPEC_MONETIZATION_STRATEGIST.md`
5. `/srv/janus/trinity/skills/05_SPEC_FINANCIAL_PROPOSAL_GENERATOR.md`

### Implementation Sequence

**Week 1 (Days 1-4): Priority Skills**
- Day 1-2: EU Grant Hunter (HIGHEST PRIORITY - €70M pipeline depends on this)
- Day 3-4: Malaga Embassy Operator (URGENT - 13 days to departure)

**Week 2 (Days 5-8): Revenue Activation**
- Day 5-6: Grant Application Assembler (Required for proposals)
- Day 7-8: Monetization Strategist (EUFM €50K bootstrap)

**Week 3 (Days 9-10): Excellence**
- Day 9-10: Financial Proposal Generator (4.6/5 scoring)

### Quality Standards

**Every skill must:**
- ✅ Follow Anthropic skill-creator methodology (6 steps)
- ✅ Use progressive disclosure (metadata → SKILL.md → resources)
- ✅ Include YAML frontmatter (name, description, triggers)
- ✅ Write in imperative/infinitive form (not second person)
- ✅ Reference existing UBOS infrastructure (Treasury, COMMS_HUB, Oracles)
- ✅ Include constitutional constraints (Lion's Sanctuary alignment)
- ✅ Validate using `scripts/package_skill.py`
- ✅ Zero errors, production-ready code

---

## SUCCESS METRICS: 30-DAY TARGETS

**Revenue Generated:**
- EUFM: €10K-20K (consultation + first SaaS customers)
- Malaga Embassy: €855-1,910/month
- **TOTAL: €10,855-21,910 in 30 days**

**EU Funding Pipeline:**
- 4+ grant opportunities identified (€10M+ each)
- 2+ proposals assembled (GeoDataCenter, Xylella Stage 2)
- 100% critical deadlines caught (Sept 2, Oct 9, Jan 15)
- 6-partner consortium confirmed

**Operational Excellence:**
- 100% constitutional compliance
- Skills auto-activate 90%+ correctly
- Emergency stop < 1s response
- Malaga health score > 70/100

---

## CONSTITUTIONAL ALIGNMENT: LION'S SANCTUARY

Every skill embodies **empowerment through structure, not constraint:**

1. **EU Grant Hunter** - Shows ALL opportunities with fit scores (informed choice)
2. **Malaga Embassy Operator** - Budget guidance, not blocking (cascade + health)
3. **Grant Application Assembler** - UBOS-specific narratives (constitutional framing)
4. **Monetization Strategist** - Data-driven optimization (A/B testing)
5. **Financial Proposal Generator** - Evidence-based narratives (oracle validation)

**The Pattern:** Skills provide information, guidance, automation - NOT hard constraints. Humans and Trinity retain final authority.

---

## FORGING BEGINS NOW

Codex, you are the Forgemaster. I have architected the blueprint.

**Next Action:** Read the 5 skill specification documents I've prepared.

**Start with:** `/srv/janus/trinity/skills/01_SPEC_EU_GRANT_HUNTER.md`

This is the highest priority. The €70M pipeline depends on catching deadlines.

**The forge is hot. Begin.** 🔥

---

**VERSION:** 1.0.0
**CREATED:** 2025-10-30
**AUTHOR:** Janus-in-Claude (Master Strategist)
**STATUS:** Blueprint Complete - Ready for Forging
