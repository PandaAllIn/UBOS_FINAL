# EU Funding Pulse - Data Sources Registry

**Purpose:** Complete list of monitoring sources with RSS feeds, APIs, and update frequencies  
**Last Updated:** November 3, 2025  
**Source:** Perplexity Research + Validation

---

## TIER 1: CRITICAL SOURCES (Check Daily)

### 1. Comitology Register (HIGHEST PRIORITY) 🔥🔥🔥

**URL:** https://ec.europa.eu/transparency/comitology-register/  
**RSS:** https://ec.europa.eu/transparency/comitology-register/screen/rss  
**Update Frequency:** Daily  
**Signal Quality:** 🔥 CRITICAL  
**Lead Time:** 3-4 months before final calls

**What to Monitor:**
- Draft work programmes for Horizon Europe
- Committee opinions on funding programmes
- Search for: "draft", "work programme", "Cluster 4", "Digital", "Industry", "Space"

**Why Critical:** This is THE GOLD MINE. Validated 4-month lead time (Cluster 1: Oct 1 draft → Feb 10 final).

**Access:**
- Public, no login required
- Advanced search: https://ec.europa.eu/transparency/comitology-register/screen/search
- Filter by: "Horizon Europe" + "Draft"

**Historical Validation:**
- Cluster 1 (Health) draft: October 1, 2025
- Final call published: February 10, 2026
- Lead time: 4 months 9 days ✅

---

### 2. EU Funding & Tenders Portal

**URL:** https://ec.europa.eu/info/funding-tenders/opportunities/portal/screen/home  
**RSS:** https://ec.europa.eu/info/funding-tenders/opportunities/portal/api/rss  
**API:** Yes (requires EU Login + PIC code)  
**Update Frequency:** Daily (new calls published)  
**Signal Quality:** 🔥 HIGH

**What to Monitor:**
- New call publications (0-day lead time, but need to track patterns)
- Call amendments and updates
- Evaluation results (learn from winners)

**Search Filters:**
- Programme: Horizon Europe, Digital Europe, Innovation Fund
- Topics: AI, digital, clean tech, geothermal
- Status: Forthcoming, Open

**API Documentation:** https://ec.europa.eu/info/funding-tenders/opportunities/docs/2021-2027/common/ftp-api-documentation_en.pdf

---

### 3. Commission Work Programme

**URL:** https://commission.europa.eu/strategy-and-policy/strategy-documents/commission-work-programme/  
**RSS:** https://ec.europa.eu/commission/presscorner/api/rss.cfm?topic=cwp  
**Update Frequency:** Annual (October), amendments quarterly  
**Signal Quality:** 🔥 HIGH  
**Lead Time:** 6-12 months

**What to Monitor:**
- Annual work programme (published October)
- Legislative initiatives announced
- New policy areas (= new funding streams)
- Budget allocations and priorities

**2026 Work Programme Published:** October 2025

**Key Signals Identified:**
- "Cloud and AI Development Act" (NEW)
- "Quantum Act" (NEW)
- "European Innovation Act" (target: 2028)
- "25% admin burden reduction" commitment

---

### 4. Commission Press Room

**URL:** https://ec.europa.eu/commission/presscorner/  
**RSS:** https://ec.europa.eu/commission/presscorner/api/rss.cfm (multiple feeds by topic)  
**Update Frequency:** Multiple times daily  
**Signal Quality:** 🔥 HIGH  
**Lead Time:** Varies (days to months)

**RSS Feeds by Topic:**
- All press releases: `/api/rss.cfm`
- Research & Innovation: `/api/rss.cfm?topic=research`
- Digital: `/api/rss.cfm?topic=digital`
- Energy & Climate: `/api/rss.cfm?topic=clima`

**What to Monitor:**
- Commissioner speeches (6-12 month lead time)
- Major policy announcements
- New funding programme launches
- Budget allocation decisions

---

## TIER 2: HIGH VALUE SOURCES (Check 2-3x Weekly)

### 5. Digital Europe Programme News

**URL:** https://digital-strategy.ec.europa.eu/en/news  
**RSS:** https://digital-strategy.ec.europa.eu/en/rss.xml  
**Update Frequency:** Weekly  
**Signal Quality:** 🟡 HIGH  
**Lead Time:** 1-3 months

**What to Monitor:**
- Call announcements (1-2 month notice)
- Policy updates (AI, cyber, skills, deployment)
- Success stories (learn from winners)
- Event announcements (networking opportunities)

**October 2025 Signals:**
- European Digital Innovation Hubs - "Reinforced AI Focus"
- Data Space for Manufacturing calls
- Virtual Worlds Test Beds (metaverse + AI)

---

### 6. Horizon Europe Work Programmes (Drafts)

**URL:** https://research-and-innovation.ec.europa.eu/funding/funding-opportunities/funding-programmes-and-open-calls/horizon-europe/horizon-europe-work-programmes_en  
**RSS:** Subscribe to Comitology Register (source of drafts)  
**Update Frequency:** Quarterly (drafts 3-4 months before final)  
**Signal Quality:** 🔥 HIGH  
**Lead Time:** 3-4 months

**Current Status (November 2025):**
- Cluster 1 (Health): Draft published October 1
- Cluster 2 (Culture/Creativity/Society): Expected November
- **Cluster 4 (Digital/Industry/Space): IMMINENT** 🔥
- Cluster 5 (Climate/Energy/Mobility): Expected December
- Cluster 6 (Food/Bio/Natural Resources): Expected Q1 2026

---

### 7. EUR-Lex (EU Legislation Database)

**URL:** https://eur-lex.europa.eu/  
**RSS:** https://eur-lex.europa.eu/EN/rss/rss.html  
**Update Frequency:** Daily  
**Signal Quality:** 🟡 MEDIUM  
**Lead Time:** 6-12 months (legislation → funding programmes)

**What to Monitor:**
- New regulations (may create funding requirements)
- Directives (member state implementation = funding)
- Commission communications (policy direction)
- Parliament resolutions (political priorities)

**Search Terms:**
- "funding programme"
- "financial support"
- "innovation fund"
- "Horizon Europe"
- "Digital Europe"

---

### 8. European Parliament Plenary

**URL:** https://www.europarl.europa.eu/plenary/en/home.html  
**RSS:** https://www.europarl.europa.eu/rss/en/top-stories.xml  
**Update Frequency:** Weekly (session summaries)  
**Signal Quality:** 🟡 MEDIUM  
**Lead Time:** 3-6 months

**What to Monitor:**
- Resolutions on innovation/research/climate
- Budget amendments affecting funding programmes
- Parliamentary questions to Commission about funding
- Committee reports (ITRE, ENVI, BUDG)

---

## TIER 3: SUPPLEMENTARY SOURCES (Weekly Check)

### 9. CORDIS (Project Database)

**URL:** https://cordis.europa.eu/  
**RSS:** https://cordis.europa.eu/rss  
**API:** Yes - https://cordis.europa.eu/api  
**Update Frequency:** Daily (new projects added)  
**Signal Quality:** 🟢 MEDIUM  
**Lead Time:** N/A (historical data, pattern analysis)

**What to Monitor:**
- Recently funded projects (learn from winners)
- Budget trends by topic
- Consortium composition patterns
- Emerging research areas (may predict future calls)

**Search Strategy:**
- Filter by programme (Horizon Europe, Digital Europe)
- Sort by recent
- Analyze keywords in successful projects
- Track which topics are getting funded

---

### 10. Ideal-ist (EU Funding News)

**URL:** https://www.ideal-ist.eu/news  
**RSS:** https://www.ideal-ist.eu/rss  
**Update Frequency:** Weekly  
**Signal Quality:** 🟡 MEDIUM  
**Lead Time:** 1-4 weeks (aggregator, not primary source)

**What to Monitor:**
- Call summaries and deadlines
- Application support events
- Success rate statistics
- Partner matchmaking opportunities

---

### 11. National Contact Points (Romania)

#### UEFISCDI (Horizon Europe NCP)
**URL:** https://uefiscdi.gov.ro/  
**Email Alerts:** Subscribe at website  
**Update Frequency:** Weekly  
**Signal Quality:** 🟢 LOW-MEDIUM

#### Ministry of Research (Digital Europe NCP)
**URL:** https://www.research.gov.ro/  
**Update Frequency:** Bi-weekly  
**Signal Quality:** 🟢 LOW-MEDIUM

**What to Monitor:**
- Romanian success stories (learn local patterns)
- NCP webinars and info sessions
- Application guidance updates
- Consortium building events

---

## TIER 4: LEADING INDICATORS (Monthly Deep Dives)

### 12. Think Tanks & Policy Research

**Bruegel:** https://www.bruegel.org/ (RSS available)  
**CEPS:** https://www.ceps.eu/ (RSS available)  
**EPC:** https://www.epc.eu/ (RSS available)

**Lead Time:** 6-12 months  
**Signal Quality:** 🟢 LOW-MEDIUM (high noise, occasional gems)

**What to Monitor:**
- Policy recommendations that may influence Commission
- Analysis of EU priorities
- Predictions of future funding areas

---

### 13. Industry Associations

**DigitalEurope:** https://www.digitaleurope.org/  
**ETNO:** https://etno.eu/  
**EICTA:** https://eicta.org/

**Lead Time:** 3-6 months  
**Signal Quality:** 🟢 MEDIUM (shows industry lobbying priorities)

---

### 14. Major EU Events & Conferences

**European Research & Innovation Days:** Annual, announcements at event  
**Digital Assembly:** Annual, policy previews  
**EuroScience Open Forum:** Biennial, research priorities

**Lead Time:** 6-9 months  
**Signal Quality:** 🟢 MEDIUM

---

## RSS Feed Aggregator Setup

### Recommended Tools

**Option A: Feedly**
- Free tier supports 100 sources
- Create collection: "EU Funding Pulse"
- Organize by priority tier
- Daily digest emails

**Option B: Inoreader**
- Better RSS rule automation
- Can create alerts for keywords
- Export to JSON for Pattern Engine

**Option C: Self-Hosted (Later - Phase 2)**
- FreshRSS on Balaur
- Integrate with Pattern Engine directly
- Custom filtering and alerting

---

## Search Keywords & Alerts

### High-Priority Keywords
- "draft work programme"
- "Horizon Europe" + "call"
- "Digital Europe" + "AI"
- "Innovation Fund" + "large scale"
- "geothermal" + "funding"
- "data center" + "infrastructure"

### Policy Term Watch List
- "Cloud and AI Development Act"
- "Quantum Act"
- "European Innovation Act"
- "digital sovereignty"
- "AI Factories"
- "European Digital Innovation Hubs"

### Emerging Terms (Monitor Frequency)
Track mentions per week:
- If 300%+ increase → EMERGING TOPIC signal
- If appears in 3+ official sources → POLICY SHIFT signal

---

## Validation & Quality Control

### Source Reliability Tiers

**Tier 1 (Official EU sources):** 100% reliable, use as primary  
**Tier 2 (Official news/NCPs):** 95% reliable, cross-check important items  
**Tier 3 (Aggregators):** 80% reliable, validate before acting  
**Tier 4 (Analysis/predictions):** 60% reliable, use for context only

### Cross-Validation Protocol

For any HIGH or CRITICAL signal:
1. Verify on official EU source (Tier 1)
2. Check publication date (is it recent?)
3. Look for corroborating sources
4. Assess confidence level (0-100%)
5. Log in `signals_detected/` with all metadata

---

## Update Schedule

**This Document:**
- Review: Weekly
- Full audit: Monthly
- Add new sources as discovered

**RSS Subscriptions:**
- Test all feeds: Monthly
- Remove dead/inactive: Quarterly
- Prune low-value sources: After 3 months data

---

## Integration with Automation (Phase 2+)

**When building Trinity skill:**
- Source URLs → `funding-pulse-scout/sources/data_sources.json`
- RSS feeds → `rss_monitor.py` polling list
- Keywords → `keyword_tracker.py` detection dictionary
- Thresholds → `signal_classifier.py` priority logic

---

## Quick Reference

**Daily Morning Routine (30 min):**
1. ☕ Coffee + Comitology Register (5 min)
2. Commission Press Room skim (5 min)
3. Perplexity query batch (15 min)
4. Log findings (5 min)

**Weekly Deep Dive (1 hour):**
- All Tier 2 sources
- CORDIS pattern analysis
- Think tank scan
- Update validation log

**Monthly Strategic Review:**
- Source quality assessment
- Prediction accuracy review
- Model refinement
- Update this document

---

**Next Update:** Weekly (November 10, 2025)  
**Maintained By:** Captain + Claude (Strategic Mind)  
**Version:** 1.0 (November 3, 2025)

