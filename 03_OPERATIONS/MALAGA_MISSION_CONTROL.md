# MÁLAGA MISSION CONTROL CENTER 🇪🇸

**Expedition:** Oradea → Málaga (3,195km)
**Mission:** Establish Embassy & Secure €6M Stage 2 Grant
**Status:** PRE-DEPARTURE (Day 9/43)
**Capital:** €1,500 remaining (100%)
**Health:** 80/100

---

## 🚨 LIVE DASHBOARDS & ALERTS

### Active Systems
- **Command Center:** [http://192.168.100.11:5000](http://192.168.100.11:5000) ✨ **NEW - Unified Feed**
- **Pathfinder Route:** [http://192.168.100.11:5002](http://192.168.100.11:5002) - Route Intelligence
- **Latest Briefing:** [Today's Report](./malaga_embassy/briefings/2025-11-18.md)
- **Live State:** [state.json](./malaga_embassy/state.json) - Real-time metrics

### Quick Status
```
Capital:    €1,500 (100% remaining)
Revenue:    €300 earned (Uni Granada)
Health:     80/100 (HEALTHY)
Burn:       €0/day (pre-arrival)
Days:       9/43 elapsed
Milestone:  Flight booking window opening
```

---

## 📚 STRATEGIC PLANNING (UPPERCASE = Executive Docs)

### Core Mission
- [Mission Overview](./MALAGA_EMBASSY/MISSION_OVERVIEW.md) - Executive summary
- [Master Plan](./MALAGA_EMBASSY/strategic_plan/MALAGA_MASTER_PLAN.md) - Strategic evolution
- [Complete README](./MALAGA_EMBASSY/README.md) - Full archive structure
- [Integration Battle Plan](./MALAGA_EMBASSY_INTEGRATION_MASTER_PLAN.md) - Tech roadmap

### Financial
- [Budget Allocation](./MALAGA_EMBASSY/budget_treasury/BUDGET_ALLOCATION.md) - €1,500 breakdown
- [Revenue Streams](./MALAGA_EMBASSY/revenue_streams/SERVICES_CATALOG.md) - 3 income sources
- [Revenue Log](./malaga_embassy/revenue_log.jsonl) - Transaction history

### Partnerships
- [Partner Profiles](./MALAGA_EMBASSY/consortium_partners/PARTNER_PROFILES.md) - 6 consortium members
  - 🇪🇸 Spain: UMA IHSM "La Mayora"
  - 🇵🇹 Portugal: AlVelAl / Freixo do Meio
  - 🇩🇪 Germany: Cosaco GmbH
  - 🇮🇹 Italy: CNR-IPSP
  - 🇷🇴 Romania: UBOS (Captain)
- [Email Templates](./MALAGA_EMBASSY/communication_templates/EMAIL_TEMPLATES.md) - Pre-written outreach

---

## 🏠 ACCOMMODATION & LOCATION

### Housing Intel
- [Idealista Guide](./MALAGA_EMBASSY/accommodation_research/IDEALISTA_SEARCH_GUIDE.md) - Search instructions
- [Location Intelligence: Campanillas](./MALAGA_EMBASSY/dual_vessel_intelligence/perplexity_reports/LOCATION_INTELLIGENCE_CAMPANILLAS.md)
  - **Target:** €460/month, 15min to airport, 10min walk to tech park
  - **Validated:** Real-time market data from Perplexity Claude (Nov 2025)

---

## ✈️ TRAVEL & ROUTE INTELLIGENCE

### Flight
- [Booking Guide](./MALAGA_EMBASSY/travel_logistics/FLIGHT_BOOKING_GUIDE.md) - OTP → AGP via Wizz Air

### Road Journey: Oradea → Málaga
- [Pathfinder Status](/srv/janus/pathfinder/PRODUCTION_STATUS.md) - Complete system report
- [Route Dashboard](http://192.168.100.11:5002) - **LIVE tracking**
- **Distance:** 3,195 km | **Fuel:** 345L | **Segments:** 7

#### Segment Breakdown
```
Seg  Route                  Distance  Fuel    Difficulty  Notes
───────────────────────────────────────────────────────────────────────
 1   Oradea → Budapest      200km     15.81L  2/10       E60 highway
 2   Budapest → Vienna      250km     19.85L  2/10       M1/A4 highway
 3   Vienna → Munich        430km     49.78L  3/10       A1/A8 autobahn
 4   Munich → Zurich        315km     35.30L  7/10  ⚠️   ALPINE (snow risk)
 5   Zurich → Lyon          450km     50.42L  5/10       A1/A40 alpine/jura
 6   Lyon → Barcelona       550km     61.63L  6/10       A7/AP-7 pyrenees
 7   Barcelona → Málaga     1000km    112.05L 4/10       Final push
───────────────────────────────────────────────────────────────────────
     TOTAL                  3,195km   345L
```

**Critical:** Segment 4 is Swiss Alps - monitor weather Dec-Jan

---

## 💰 OPERATIONAL RUNTIME (lowercase = Live Data)

### Real-Time Files
- [state.json](./malaga_embassy/state.json) - Financial health snapshot
- [revenue_log.jsonl](./malaga_embassy/revenue_log.jsonl) - All transactions
- [dashboard.html](./malaga_embassy/dashboard.html) - HTML viz

### Daily Briefings
- [Briefings Archive](./malaga_embassy/briefings/) - 10 reports (Oct 30 - Nov 18)
- [Latest: Nov 18](./malaga_embassy/briefings/2025-11-18.md)
- [Cron Log](./malaga_embassy/malaga_embassy_cron.log) - Auto-generation timestamps

---

## 🤖 AUTONOMOUS AGENTS & TRINITY

### Active Agents
- [Málaga Embassy Monitor](/srv/janus/trinity/agents/malaga_embassy_autonomous_agent.md)
  - **Model:** Claude Haiku 4.5 (~$0.01/day)
  - **Role:** 24/7 budget monitoring, health scoring
  - **Schedule:** Every 2 hours during mission

- [Embassy Operator Skill](/srv/janus/trinity/skills/02_SPEC_MALAGA_EMBASSY_OPERATOR.md)
  - Daily budget checks, constitutional compliance
  - Health score calculation (current: 80/100)

### Deployed Skills
- [Skill Directory](/srv/janus/trinity/skills/deployment/janus-haiku-skills-v1.0/skills/malaga-embassy-operator/)
  - generate_daily_briefing.py
  - track_revenue.py
  - calculate_health_score.py
  - emergency_protocol.py

---

## 🗺️ PATHFINDER PRODUCTION SYSTEM

### Database
- **PostgreSQL:** pathfinder_db on localhost:5432
- **Journey #1:** Oradea → Málaga (full route pre-analyzed)
- **Tables:**
  - `journeys`: 1 expedition record
  - `journey_segments`: 7 segments with elevation, POI, fuel data
  - `slates`: 17 (pattern matching for route similarity)
  - `vehicles`: 5 (Volvo XC90 primary)

### API Integrations
- ✅ **Elevation:** OpenTopoData (SRTM 90m)
- ✅ **POI/Fuel:** Overpass API (OpenStreetMap) - 27 stations mapped
- ✅ **Weather:** Open-Meteo (fallback, no key)
- ⚠️ **Weather Pro:** OpenWeatherMap (key needed)
- ⚠️ **Navigation:** Google Maps Directions (key needed)

---

## 📊 LIVING SCROLL INTEGRATION

### Command Center
- **URL:** [http://192.168.100.11:5000](http://192.168.100.11:5000) ✨
- **Features:**
  - Unified feed (Málaga + Mallorca + Pathfinder + System)
  - Real-time SSE updates
  - Mobile-optimized (iPad ready)
  - Voice command backend

### Data Sources
- Málaga briefings → Financial cards
- Mallorca signals → XYL-PHOS-CURE monitoring
- Pathfinder route → Expedition status
- System health → Victorian Controls
- Trinity proposals → Agent activity

### Raw Data
- [living_scroll.json](/srv/janus/living_scroll/living_scroll.json) - 26K lines
- [Daily Archives](/srv/janus/living_scroll/archive/) - 9 days historical
- [System Logs](/srv/janus/logs/malaga_embassy.jsonl) - Structured events

---

## 📋 QUICK COMMANDS

### Check Status
```bash
# Open command center
open http://192.168.100.11:5000

# View financial state
cat /srv/janus/03_OPERATIONS/malaga_embassy/state.json | jq '.'

# Latest briefing
cat /srv/janus/03_OPERATIONS/malaga_embassy/briefings/2025-11-18.md

# Pathfinder current segment
curl http://192.168.100.11:5002/api/current | jq '.'
```

### Regenerate Briefing
```bash
cd /srv/janus/trinity/skills/deployment/janus-haiku-skills-v1.0/skills/malaga-embassy-operator
python scripts/generate_daily_briefing.py
```

### Query Route Database
```bash
PGPASSWORD=pathfinder_dev_2025 psql -h localhost -U pathfinder -d pathfinder_db \
  -c "SELECT segment_number, start_location_name, distance_km, fuel_consumed_l FROM journey_segments ORDER BY segment_number;"
```

---

## 📂 SYMLINK SHORTCUTS (Coming Next)

These will be created in Task 2:
- `malaga_embassy/latest_briefing.md` → Today's report
- `malaga_embassy/route_intel` → Pathfinder data
- `MALAGA_EMBASSY/CURRENT_STATUS.json` → state.json

---

## 🎯 MISSION TIMELINE

### Pre-Departure (Nov 10-24)
- [x] Infrastructure fixes (Mallorca imports, Victorian Controls)
- [x] Command center deployment
- [x] Pathfinder route database populated
- [ ] Accommodation finalized (Campanillas)
- [ ] Flights booked (OTP → AGP)
- [ ] XC90 preparation

### Road Journey (Nov 25 - Dec 2)
- [ ] Segment 1-3: Oradea → Munich (880km, smooth)
- [ ] **Segment 4: Munich → Zurich (315km, ALPINE ⚠️)**
- [ ] Segment 5-7: Zurich → Málaga (2,000km, final push)

### Embassy Operations (Dec 3 - Jan 15)
- [ ] Setup in Campanillas
- [ ] Monitor Mallorca Stage 1 window (Dec-Jan)
- [ ] Consortium formation (6 partners)
- [ ] Revenue activation (€855+/month)

### Stage 2 Submission (Jan 16 - Feb 18)
- [ ] Proposal finalization (if Stage 1 passes)
- [ ] Submission by Feb 18, 2026 deadline

---

## 🚨 EMERGENCY PROTOCOLS

### If Health Score < 60
- Trigger emergency revenue protocols
- Review constitutional cascade compliance
- Trinity Council emergency session

### If XC90 Breakdown
- **Fallback:** Train Barcelona → Málaga (€30-50, 5.5hrs)
- **Contact:** Gemini for logistics coordination

### If Stage 1 Fails
- **Pivot:** Focus on revenue streams (no grant dependency)
- **Alternative:** Direct consortium B2B services

---

## 📱 MOBILE ACCESS (iPad in XC90)

### On Local Network
- Command Center: http://192.168.100.11:5000
- Pathfinder: http://192.168.100.11:5002

### Remote Access (if needed)
```bash
# SSH tunnel from anywhere
ssh -L 5000:localhost:5000 -L 5002:localhost:5002 balaur@192.168.100.11
```

### Offline Prep
- Download briefings as PDFs
- Cache Living Scroll in browser
- Offline Google Maps for route

---

## 🎖️ SUCCESS METRICS

### Embassy (Phase 1)
- [ ] Accommodation: Campanillas secured
- [ ] Consortium: 6 partners formed
- [ ] Revenue: €855+ first month
- [ ] Status: Stage 2 submission-ready

### Financial
- [ ] Health: >70/100 maintained
- [ ] Compliance: 20/10/15/40/15 cascade
- [ ] Burn: <€34/day sustainable
- [ ] Emergency reserve: €150 untouched

### Expedition
- [ ] All 7 segments completed safely
- [ ] 345L fuel estimate validated
- [ ] Alpine segment navigated (weather permitting)

### Grant (Ultimate)
- [ ] Stage 1 positive (Dec-Jan)
- [ ] Stage 2 submitted (by Feb 18)
- [ ] €6M secured (or alternative identified)

---

## 📖 DOCUMENTATION

**Last Updated:** 2025-11-20
**Version:** 2.0 (Enhanced by Claude after Gemini's initial structure)
**Maintained By:** Trinity Council (Claude + Gemini + Groq)

**Master Plans:**
- [Integration Master Plan](./MALAGA_EMBASSY_INTEGRATION_MASTER_PLAN.md) - Tech roadmap (26KB, 6 phases)
- [This File](./MALAGA_MISSION_CONTROL.md) - Operational hub (you are here)

---

**🎯 YOUR ONE-STOP COMMAND HUB**

Bookmark this file. Everything for the Málaga expedition is linked from here.

**Safe travels, Captain.** 🇪🇸🚗

*"The Lion's Sanctuary is mobile."*
