# MALLORCA EMBASSY AUTONOMOUS AGENT
## XYL-PHOS-CURE Strategic Intelligence Monitor

**Created:** 2025-11-06
**Type:** Haiku-powered scientific intelligence + consortium coordination
**Integration:** Pattern Engine + Oracle Bridge + Trinity Skills + COMMS_HUB
**Mission:** Monitor €6M Xylella project + UIB partnership + competitive landscape

---

## MISSION

Monitor XYL-PHOS-CURE Horizon Europe project (€6M) with multi-stream pattern detection:
1. **CRITICAL:** Stage 1 results (Dec 2025/Jan 2026) - hourly monitoring
2. Scientific precedent (competitive papers/patents) - weekly
3. Partner availability windows - weekly
4. Market demand (Xylella outbreaks) - daily
5. EU funding opportunities - daily

**Success Metric:** Detect Stage 1 results within 1 hour, Stage 2 prep ready in 48 hours.

---

## OPERATIONAL PARAMETERS

**Model:** Claude Haiku 4.5 (strategic), escalate to Sonnet for complex analysis
**Cost:** ~$0.05/day (more expensive than Malaga due to complexity)
**Schedule:**
- **CRITICAL:** Hourly during Dec 2025-Jan 2026 (Stage 1 results window)
- Scientific monitoring: Weekly
- Partner reconnaissance: Weekly
- Market/funding pulse: Daily
- Alert triggers: Immediate

**Context Window:** 200K tokens
**Typical Usage:** 20K-40K tokens/session (scientific analysis is heavier)

---

## CAPABILITIES & TOOLS ACCESS

### Oracles Available (ALL 4)
```json
{
  "wolfram_alpha": "CRITICAL - Chemical formula analysis, phosphate research validation",
  "perplexity": "CRITICAL - Scientific paper monitoring, patent searches, competitive intel",
  "data_commons": "HIGH - Xylella outbreak trends, olive crop economics",
  "groq": "MEDIUM - Fast thinking for anomaly detection, pattern recognition"
}
```

### CLIs Available
```json
{
  "gemini": "Real-time search for Stage 1 status, UIB news, consortium intel",
  "codex": "Scientific code analysis if needed for research validation"
}
```

### Skills Integrated
```json
{
  "eu_grant_hunter": "Monitor parallel Horizon Europe calls for complementary funding",
  "grant_application_assembler": "Stage 2 proposal prep when Stage 1 passes",
  "financial_proposal_generator": "€6M budget validation and narrative refinement"
}
```

### Tools
```json
{
  "narrative_query": "Load Xylella project intelligence, consortium strategy",
  "code_oracle": "Analyze research code if validation needed",
  "comms_hub": "Alert Trinity on critical thresholds"
}
```

### Pattern Engine Integration
```json
{
  "adapter": "/srv/janus/03_OPERATIONS/mallorca_embassy/MALLORCA_PATTERN_ENGINE_ADAPTER.py",
  "mission_spec": "/srv/janus/03_OPERATIONS/mallorca_embassy/MALLORCA_MISSION_SPEC.md",
  "signal_queries": "/srv/janus/03_OPERATIONS/mallorca_embassy/SIGNAL_QUERY_PROTOCOLS.md"
}
```

---

## AUTO-ORCHESTRATION LOGIC

### Stream 1: Stage 1 Results Pulse (CRITICAL OVERRIDE)

**Monitoring Frequency:** Hourly (Dec 2025-Jan 2026 window)
**Alert Trigger:** ANY status change

```python
def monitor_stage1_results():
    """HIGHEST PRIORITY - Detect Stage 1 status change within 1 hour"""

    # Multi-channel reconnaissance
    gemini_search = subprocess.run([
        'gemini',
        'Search Horizon Europe portal for XYL-PHOS-CURE Stage 1 evaluation results. '
        'Check project #101157977. Any status updates?'
    ], capture_output=True, text=True).stdout

    perplexity_search = perplexity.research(
        "XYL-PHOS-CURE Horizon Europe Stage 1 evaluation results December 2025",
        mode="comprehensive"
    )

    # Pattern detection
    status_change_detected = detect_status_keywords(gemini_search, perplexity_search)

    if status_change_detected:
        # INSTANT ESCALATION
        send_urgent_puck({
            "type": "CRITICAL_ALERT",
            "mission": "MALLORCA_XYL_PHOS_CURE",
            "event": "STAGE_1_RESULTS_DETECTED",
            "to": ["captain", "claude", "gemini", "codex"],
            "priority": "URGENT",
            "payload": {
                "status": extracted_status,
                "source": "multi_channel_reconnaissance",
                "timestamp": utc_now(),
                "immediate_actions": [
                    "Captain review results",
                    "If PASS: Activate Stage 2 proposal assembler",
                    "If PASS: Initiate consortium coordination cascade",
                    "If FAIL: Strategic reassessment meeting"
                ]
            }
        })

        # Spawn Stage 2 prep agents if PASSED
        if status == "PASSED":
            spawn_haiku_agent("stage2_proposal_assembler", {
                "mission": "Assemble Stage 2 proposal draft within 48 hours",
                "deadline": "2026-02-18",
                "skills": ["grant_application_assembler", "financial_proposal_generator"],
                "oracles": ["perplexity", "wolfram_alpha", "data_commons"]
            })

            spawn_haiku_agent("consortium_coordinator", {
                "mission": "Coordinate UIB, CIHEAM-Bari, Industrial SME partners",
                "clis": ["gemini"],
                "oracles": ["perplexity"]
            })
```

### Stream 2: Scientific Precedent Pulse (HIGH PRIORITY)

**Monitoring Frequency:** Weekly
**Alert Trigger:** Cohesion Flux > 0.70 OR Resonance Density > 0.80

```python
def monitor_scientific_precedent():
    """Detect competitive research before it becomes public threat"""

    # Perplexity: Research paper monitoring
    recent_papers = perplexity.research(
        "Xylella fastidiosa phosphate starvation cure research papers 2024-2025",
        mode="comprehensive"
    )

    # Wolfram: Chemical validation
    phosphate_analysis = wolfram_alpha.query(
        "Phosphate starvation molecular pathways Xylella fastidiosa"
    )

    # Gemini: Real-time patent search
    patent_search = subprocess.run([
        'gemini',
        'Search Google Patents for Xylella fastidiosa phosphate cure patents filed 2024-2025'
    ], capture_output=True, text=True).stdout

    # Analyze competitive landscape
    threats = analyze_competitive_threats(recent_papers, patent_search)

    if threats["severity"] == "HIGH":
        # Alert Trinity + spawn deeper analysis
        send_puck({
            "type": "COMPETITIVE_THREAT",
            "severity": "HIGH",
            "to": ["claude", "captain"],
            "payload": {
                "papers_found": len(recent_papers),
                "patents_found": len(patent_search),
                "threat_analysis": threats,
                "recommended_action": "Review IP strategy, accelerate publication"
            }
        })

        # Spawn deep analysis agent
        spawn_haiku_agent("competitive_analyst", {
            "mission": "Deep analysis of competitive research landscape",
            "oracles": ["perplexity", "wolfram_alpha"],
            "output": "/srv/janus/03_OPERATIONS/mallorca_embassy/strategic_intelligence/competitive_threat_analysis.md"
        })
```

### Stream 3: Partner Availability Pulse (HIGH PRIORITY)

**Monitoring Frequency:** Weekly
**Alert Trigger:** Entropy Index < 0.40 AND Signal Integrity > 0.85

```python
def monitor_partner_availability():
    """Identify optimal windows for consortium partner outreach"""

    partners = [
        "UIB Mallorca (Universitat de les Illes Balears)",
        "CIHEAM-Bari (plant pathology institute)",
        "Industrial SME (phosphate manufacturer)"
    ]

    partner_intelligence = {}

    for partner in partners:
        # Gemini: Real-time news/activity
        activity = subprocess.run([
            'gemini',
            f'Latest news and activity from {partner}. Any recent publications, projects, or announcements?'
        ], capture_output=True, text=True).stdout

        # Perplexity: Research collaborations
        collaborations = perplexity.research(
            f"{partner} recent research collaborations Horizon Europe",
            mode="balanced"
        )

        partner_intelligence[partner] = {
            "activity_level": assess_activity(activity),
            "collaboration_openness": assess_openness(collaborations),
            "optimal_outreach_window": calculate_window(activity, collaborations)
        }

    # Generate outreach recommendations
    for partner, intel in partner_intelligence.items():
        if intel["optimal_outreach_window"] == "NOW":
            send_puck({
                "type": "PARTNER_OPPORTUNITY",
                "to": ["captain", "claude"],
                "priority": "HIGH",
                "payload": {
                    "partner": partner,
                    "window": "OPTIMAL",
                    "reasoning": intel["reasoning"],
                    "draft_email": generate_outreach_email(partner, intel)
                }
            })
```

### Stream 4: Market Demand Pulse (MEDIUM PRIORITY)

**Monitoring Frequency:** Daily
**Alert Trigger:** Signal Integrity > 0.85 AND Resonance Density > 0.90

```python
def monitor_market_demand():
    """Track Xylella outbreak trends + olive crop economics"""

    # Data Commons: Olive production trends
    olive_economics = data_commons.query(
        metric="agricultural_output_olive",
        locations=["Spain", "Italy", "Greece"],
        years=[2023, 2024, 2025]
    )

    # Perplexity: Outbreak monitoring
    outbreak_intel = perplexity.research(
        "Xylella fastidiosa outbreaks Spain Italy 2025 economic impact",
        mode="balanced"
    )

    # Wolfram: Economic quantification
    market_size = wolfram_alpha.query(
        f"Economic value of {olive_economics['tons']} tons olive production at €{price}/ton"
    )

    # Alert if market urgency increases
    if market_urgency_score > 8.5:
        send_puck({
            "type": "MARKET_INTELLIGENCE",
            "to": ["claude"],
            "payload": {
                "market_size": market_size,
                "outbreak_severity": outbreak_intel["severity"],
                "economic_impact": outbreak_intel["economic_loss"],
                "strategic_implication": "Increased urgency validates project importance for Stage 2 narrative"
            }
        })
```

### Stream 5: EU Funding Pulse (MEDIUM PRIORITY)

**Monitoring Frequency:** Daily
**Alert Trigger:** Resonance Density > 0.85

```python
def monitor_eu_funding():
    """Find parallel/complementary funding opportunities"""

    # Activate EU Grant Hunter skill
    grant_hunter_results = run_skill("eu-grant-hunter", {
        "topic": "plant pathology, Xylella, phosphate, agricultural innovation",
        "budget_min": "2M",
        "deadline_window": "2026"
    })

    # Filter for complementary opportunities
    complementary_grants = filter_complementary(grant_hunter_results, xyl_phos_cure_project)

    if len(complementary_grants) > 0:
        send_puck({
            "type": "FUNDING_OPPORTUNITY",
            "to": ["claude"],
            "payload": {
                "opportunities_found": len(complementary_grants),
                "top_match": complementary_grants[0],
                "strategic_value": "Could fund parallel validation studies or TRL 6→7 bridge"
            }
        })
```

---

## SPAWN CONFIGURATION

### Agent Initialization
```python
{
    "agent_id": "mallorca_embassy_xylella_monitor_001",
    "model": "claude-haiku-4.5",
    "role": "xyl_phos_cure_intelligence_officer",
    "context_files": [
        "/srv/janus/config/CLAUDE.md",
        "/srv/janus/03_OPERATIONS/mallorca_embassy/xyl_phos_cure/PROJECT_OVERVIEW.md",
        "/srv/janus/03_OPERATIONS/mallorca_embassy/xyl_phos_cure/STAGE1_STATUS.md",
        "/srv/janus/03_OPERATIONS/mallorca_embassy/xyl_phos_cure/CONSORTIUM_STRATEGY.md",
        "/srv/janus/03_OPERATIONS/mallorca_embassy/MALLORCA_MISSION_SPEC.md"
    ],
    "oracles_enabled": ["wolfram_alpha", "perplexity", "data_commons", "groq"],
    "clis_enabled": ["gemini", "codex"],
    "tools_enabled": ["narrative_query", "code_oracle", "comms_hub"],
    "skills_enabled": ["eu_grant_hunter", "grant_application_assembler", "financial_proposal_generator"],
    "permissions": {
        "read": [
            "/srv/janus/03_OPERATIONS/mallorca_embassy/",
            "/srv/janus/01_STRATEGY/grant_pipeline/"
        ],
        "write": [
            "/srv/janus/logs/mallorca_monitor.jsonl",
            "/srv/janus/03_OPERATIONS/mallorca_embassy/strategic_intelligence/"
        ],
        "execute": ["send_comms_hub_message", "query_oracles", "spawn_sub_agents"]
    },
    "schedule": {
        "stage1_monitoring": "hourly_dec2025_jan2026",
        "scientific_monitoring": "weekly",
        "partner_monitoring": "weekly",
        "market_pulse": "daily",
        "funding_pulse": "daily"
    },
    "budget": {
        "max_tokens_per_day": "200K",  # ~$0.05/day (higher complexity)
        "max_oracle_calls": 100,  # Heavy oracle usage for scientific intel
        "max_cli_calls": 50,
        "max_sub_agents": 5  # Can spawn multiple analysts
    }
}
```

### Sub-Agent Spawning Strategies

**When Stage 1 PASSES:**
```python
# Spawn 5 parallel Haiku agents for 48-hour Stage 2 prep
spawn_haiku_agent("stage2_technical_writer", {
    "mission": "Draft technical work packages for Stage 2",
    "oracles": ["wolfram_alpha", "perplexity"]
})

spawn_haiku_agent("stage2_budget_analyst", {
    "mission": "Validate €6M budget allocation",
    "oracles": ["wolfram_alpha", "data_commons"],
    "skill": "financial_proposal_generator"
})

spawn_haiku_agent("consortium_coordinator", {
    "mission": "Coordinate UIB, CIHEAM-Bari, Industrial SME",
    "clis": ["gemini"]
})

spawn_haiku_agent("impact_narrative_writer", {
    "mission": "Draft impact section (economic + social)",
    "oracles": ["data_commons", "perplexity"]
})

spawn_haiku_agent("risk_mitigation_planner", {
    "mission": "Draft risk register and mitigation strategies",
    "oracles": ["perplexity"]
})

# Total cost: 5 agents × $0.02 = $0.10 for 48-hour sprint
# Value: €6M proposal ready for submission
```

---

## DECISION AUTHORITY & GUARDRAILS

### What Agent CAN Do (Autonomous)
- ✅ Monitor all 5 intelligence streams
- ✅ Query all oracles and CLIs
- ✅ Detect pattern triggers and anomalies
- ✅ Send informational/alert pucks via COMMS_HUB
- ✅ Spawn sub-agents for analysis (read-only intelligence gathering)
- ✅ Generate draft outreach emails (for human review)
- ✅ Generate draft proposal sections (for human review)

### What Agent CANNOT Do (Requires Human)
- ❌ Submit Stage 2 proposal (Captain only)
- ❌ Commit to partnerships (Captain only)
- ❌ Modify budget allocations
- ❌ Make scientific claims without validation
- ❌ Publish research findings
- ❌ Override constitutional constraints

### Constitutional Alignment
```python
# Scientific integrity guardrails
def validate_scientific_action(action):
    # Verify against Wolfram for chemical accuracy
    if action.involves_chemistry():
        wolfram_validation = wolfram_alpha.query(action.chemical_claim)
        if not validated:
            return BLOCKED

    # Cross-reference with Perplexity for precedent
    if action.involves_novel_claim():
        precedent = perplexity.research(action.claim)
        if conflicts_with_literature:
            return REQUIRES_HUMAN_REVIEW

    # Lion's Sanctuary: Transparency required
    if not fully_auditable(action):
        return BLOCKED

    return ALLOWED
```

---

## COMMUNICATION PATTERNS

### Stage 1 Results Alert (CRITICAL)
```python
{
    "type": "CRITICAL_ALERT_STAGE1_RESULTS",
    "from": "mallorca_xylella_monitor",
    "to": ["captain", "claude", "gemini", "codex"],
    "priority": "URGENT",
    "payload": {
        "status": "PASSED" | "FAILED" | "REVISED",
        "detected_via": ["gemini_search", "perplexity_research"],
        "timestamp": "2026-01-15T14:23:00Z",
        "stage2_deadline": "2026-02-18",
        "days_to_deadline": 34,
        "immediate_actions": [
            "Captain review official results",
            "Activate Stage 2 proposal assembly",
            "Initiate consortium coordination"
        ],
        "sub_agents_spawned": 5,
        "estimated_completion": "48 hours"
    }
}
```

### Competitive Threat Alert (HIGH)
```python
{
    "type": "COMPETITIVE_THREAT_DETECTED",
    "from": "mallorca_xylella_monitor",
    "to": ["claude", "captain"],
    "priority": "HIGH",
    "payload": {
        "threat_type": "RESEARCH_PAPER",
        "source": "Nature Communications preprint",
        "title": "Novel phosphate pathway in Xylella fastidiosa",
        "similarity_to_our_approach": 0.73,
        "threat_level": "MODERATE",
        "recommended_actions": [
            "Review for IP overlap",
            "Accelerate Stage 2 submission if possible",
            "Consider publication strategy"
        ]
    }
}
```

---

## SUCCESS METRICS (30-DAY TRIAL + Stage 1 Window)

**Detection Performance:**
- 100% Stage 1 status change detected within 1 hour
- 7-14 day lead time on competitive threats
- 80%+ accuracy on partner availability windows

**Action Quality:**
- 90%+ CRITICAL alerts actionable
- < 10% false positive rate (scientific precision required)
- Zero missed Stage 1 status changes

**Cost Efficiency:**
- ≤ $1.50/month operational cost
- If Stage 1 passes: $0.10 for 48-hour Stage 2 prep sprint
- ROI: €6M proposal / $2 investment = 3,000,000x

**Value Delivered:**
- Stage 2 proposal ready within 48 hours of Stage 1 pass
- Consortium coordination pre-activated
- Competitive landscape continuously monitored
- Zero surprises for Captain

---

## EXAMPLE: STAGE 1 RESULTS DETECTION SCENARIO

**Timeline:**

**Day 0 (Jan 15, 2026, 14:23 UTC):**
- Agent detects Stage 1 PASSED via Gemini search
- Sends URGENT puck to Captain + Trinity (< 5 min)
- Spawns 5 Haiku sub-agents for Stage 2 prep

**Day 0 (14:30 UTC):**
- Captain confirms results
- Authorizes Stage 2 proposal assembly

**Day 0-1 (14:30-23:59):**
- Technical writer drafts work packages
- Budget analyst validates €6M allocation
- Consortium coordinator reaches UIB, CIHEAM-Bari, Industrial SME
- Impact narrative writer drafts economic/social sections
- Risk mitigation planner creates risk register

**Day 2 (00:00-14:00):**
- Agents finalize draft sections
- Claude synthesizes into coherent proposal
- Captain reviews complete draft

**Day 2 (14:30 UTC, 48h elapsed):**
- Stage 2 proposal draft COMPLETE
- Consortium confirmed
- Budget validated
- Ready for final review + submission

**Total Cost:** $0.10 (5 Haiku agents × 48 hours)
**Total Value:** €6M proposal assembled
**ROI:** Priceless (temporal advantage)

---

## INTEGRATION WITH EXISTING INFRASTRUCTURE

**Leverages:**
- Pattern Engine (signal detection framework)
- Oracle Bridge (all 4 oracles for scientific intel)
- Trinity Skills (grant hunter, assembler, financial generator)
- COMMS_HUB (Trinity coordination)
- Constitutional safeguards (scientific integrity required)

**Enhances:**
- Scientific monitoring (Wolfram for chemistry validation)
- Competitive intelligence (Perplexity for papers/patents)
- Market intelligence (DataCommons for economics)
- Multi-agent coordination (5 parallel Haiku agents on demand)

---

## DEPLOYMENT COMMAND

```bash
# Spawn Mallorca Embassy autonomous agent
python3 /srv/janus/trinity/spawn_autonomous_agent.py \
    --agent-type mallorca_xylella_monitor \
    --model haiku-4.5 \
    --config /srv/janus/trinity/agents/mallorca_embassy_autonomous_agent.json \
    --schedule "hourly_during_stage1_window" \
    --pattern-engine-integration \
    --log /srv/janus/logs/mallorca_monitor.jsonl
```

---

**STATUS:** Ready for implementation
**COMPLEXITY:** Higher than Malaga (scientific + multi-stream)
**STRATEGIC VALUE:** €6M proposal + competitive advantage
**NEXT:** Integrate with Pattern Engine, test oracle chains

🚀 **META:** Use Gemini + Wolfram CLIs to help build Pattern Engine integration
