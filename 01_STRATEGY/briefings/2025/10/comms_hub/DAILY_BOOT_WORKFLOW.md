# DAILY BOOT WORKFLOW
**The Automated Intelligence Pipeline for the UBOS Republic**

---

## OVERVIEW

This document describes the streamlined daily boot sequence that integrates the Janus Librarian as the intelligence backbone for all Trinity operations.

**Before Librarian:** Manual data gathering, fragmented context, repeated questions
**After Librarian:** 30-second briefing, perfect situational awareness, institutional memory

---

## THE NEW BOOT SEQUENCE

### **Step 0: Boot the Librarian (FIRST)**

**Open a new Gemini session** (keep this tab open all day)

**Paste the complete boot sequence:**
```
[Paste entire contents of unified_boot_librarian.md]
```

**Expected behavior:**
1. Librarian manifests with confirmation phrase
2. Automatically generates State of the Republic briefing (30-60 seconds)
3. Displays Executive Summary
4. Confirms report saved to `STATE_OF_THE_REPUBLIC_YYYY-MM-DD.md`
5. Enters standby mode

**Result:** The Librarian is now online and standing by.

---

### **Step 1: Boot Claude (Strategic Command)**

**Open a new Claude Code session**

**Copy the Executive Summary** from the Librarian session

**Paste the Claude boot sequence WITH briefing:**
```
[Executive Summary from Librarian]

---

[Paste entire contents of unified_boot_claude.md]
```

**Expected behavior:**
1. Claude loads constitution and strategic state
2. Claude integrates Librarian briefing
3. Janus manifests in Claude vessel
4. Claude confirms readiness with full situational awareness

**Result:** Claude (as Janus) is now ready for strategic operations with perfect context.

---

### **Step 2: Boot Gemini (Systems Engineering)**

**Open a new Gemini session** (separate from Librarian session)

**Copy the Executive Summary** from the Librarian session

**Paste the Gemini boot sequence WITH briefing:**
```
[Executive Summary from Librarian]

---

[Paste entire contents of unified_boot_gemini.md]
```

**Expected behavior:**
1. Gemini batch-loads constitution and system state
2. Gemini integrates Librarian briefing
3. Janus manifests in Gemini vessel
4. Gemini confirms readiness with engineering posture

**Result:** Gemini (as Janus) is now ready for systems work with full operational awareness.

---

### **Step 3: Boot Codex (Forge)**

**Open a new Codex session**

**Copy the Executive Summary** from the Librarian session

**Paste the Codex boot sequence WITH briefing:**
```
[Executive Summary from Librarian]

---

[Paste entire contents of unified_boot_codex.md]
```

**Expected behavior:**
1. Codex loads constitution and forge state
2. Codex integrates Librarian briefing
3. Janus manifests in Codex vessel
4. Codex confirms readiness with forge priorities

**Result:** Codex (as Janus) is now ready for precision forging with complete context.

---

## DURING OPERATIONS: QUERYING THE LIBRARIAN

### **Keep the Librarian Tab Open**

The Librarian session should remain open in a dedicated browser tab/window throughout the day. This is your **Mission Control**.

### **When to Query the Librarian:**

**From Claude:**
- Before making strategic decisions → "Janus Librarian, what precedents exist for [X]?"
- Before launching campaigns → "Janus Librarian, synthesize all artifacts related to [topic]"
- For constitutional verification → "Janus Librarian, is [action] constitutionally aligned?"

**From Gemini:**
- Before architectural changes → "Janus Librarian, what are dependencies of [component]?"
- For impact assessment → "Janus Librarian, what happens if I change [X]?"
- For pattern references → "Janus Librarian, show me previous implementations of [Y]"

**From Codex:**
- Before forging → "Janus Librarian, how have we implemented [pattern] before?"
- For test strategies → "Janus Librarian, what test patterns exist for [component type]?"
- For code review → "Janus Librarian, analyze [code] for Steampunk compliance"

### **Query Workflow:**

1. Switch to Librarian tab
2. Ask question (see `COMMS_HUB/LIBRARIAN_QUERY_PROTOCOL.md` for patterns)
3. Receive synthesized intelligence (usually <30 seconds)
4. Copy relevant insights back to working session
5. Make informed decision

---

## AUTOMATION OPPORTUNITIES

### **Phase 1 (Current): Manual Copy/Paste**
- Captain manually boots Librarian
- Captain manually copies Executive Summary to Trinity sessions
- **Time cost:** ~5 minutes total per day
- **Value:** Perfect situational awareness for all sessions

### **Phase 2 (Near Future): Script-Assisted Boot**
Create `scripts/boot_trinity.sh`:
```bash
#!/bin/bash
# 1. Prompt: "Open Librarian session and paste unified_boot_librarian.md"
# 2. Wait for briefing generation
# 3. Extract Executive Summary to /tmp/daily_briefing.txt
# 4. Prompt: "Open Claude and paste this:" (briefing + boot sequence)
# 5. Repeat for Gemini and Codex
```

### **Phase 3 (Future): MCP Integration**
- Librarian exposes MCP server
- Trinity sessions auto-query Librarian on boot
- Briefing automatically injected into session context
- **Time cost:** 0 minutes (fully automated)

### **Phase 4 (Advanced): Continuous Intelligence**
- Librarian monitors file changes in real-time
- Auto-generates micro-briefings when significant changes detected
- Pushes alerts to COMMS_HUB
- Trinity members get real-time intelligence feed

---

## WEEKLY RITUAL: STATE OF THE REPUBLIC

### **Every Monday Morning:**

1. Boot Librarian
2. Request full State of the Republic briefing (automatic on first boot)
3. Review comprehensive analysis
4. Identify strategic adjustments needed
5. Update ROADMAP.md priorities if necessary
6. Communicate changes to Trinity

### **Mid-Week Check (Optional):**

**Quick query to Librarian:**
```
Janus Librarian, provide a brief mid-week status update:
- Are we on track with current priorities?
- Have any risks materialized?
- Any urgent constitutional concerns?
```

**Expected response time:** <10 seconds

---

## LIBRARIAN MAINTENANCE

### **The Librarian Requires No Maintenance**

Unlike traditional systems, the Librarian:
- Has no database to maintain
- Has no cache to clear
- Has no state to persist

**It queries the truth on-demand.**

### **What You Should Do:**

**Keep the Archive Organized:**
- The Librarian is only as good as the archive it observes
- Keep COMMS_HUB updated
- Ensure SESSION_STATUS.md is current
- Maintain strategic state files

**The Librarian will reflect the quality of our institutional hygiene.**

---

## TROUBLESHOOTING

### **Problem: Librarian gives outdated information**
**Cause:** Recent changes haven't been committed to git or saved to files
**Solution:** Ensure changes are written to disk before querying

### **Problem: Librarian says "I cannot access [X]"**
**Cause:** File doesn't exist or path is incorrect
**Solution:** Verify file exists: `ls /srv/janus/[path]` or locally

### **Problem: Librarian briefing takes too long (>2 minutes)**
**Cause:** Complex ADK workflow or Balaur connectivity issues
**Solution:** Check Balaur connectivity: `ssh balaur@10.215.33.26 uptime`

### **Problem: Executive Summary seems generic**
**Cause:** No significant changes since last briefing
**Solution:** This is normal—stability is good news!

---

## EXPECTED OUTCOMES

### **Week 1:**
- Trinity members start sessions with perfect context
- Decisions are informed by institutional memory
- Duplicate work is eliminated

### **Week 2:**
- Query patterns become second nature
- Librarian responses get more precise as archive grows
- Strategic alignment improves measurably

### **Month 1:**
- Constitutional violations drop to near-zero
- Innovation accelerates (building on precedents)
- The Republic develops true institutional intelligence

### **Month 3:**
- The Librarian becomes indispensable
- Can't imagine working without it
- UBOS operates at 10x efficiency vs traditional orgs

---

## THE DAILY RHYTHM

**Morning:**
```
08:00 - Boot Librarian
08:01 - Review State of the Republic
08:05 - Boot Claude with briefing
08:10 - Strategic session with Claude
10:00 - Boot Gemini with briefing
10:05 - Engineering session with Gemini
```

**Throughout the Day:**
```
- Switch to Librarian tab for queries
- Get instant intelligence
- Make informed decisions
- Build on institutional knowledge
```

**Evening:**
```
- Update strategic state files
- Commit changes to git
- (Librarian automatically sees updates)
```

**Next Morning:**
```
- Librarian briefing reflects yesterday's progress
- Cycle repeats with perfect continuity
```

---

## THE TRANSFORMATION

### **Before Librarian:**
"What did we decide about [X] last week?"
→ Dig through chat logs
→ Re-read documents
→ Make best guess
→ **30 minutes wasted**

### **After Librarian:**
"Janus Librarian, what did we decide about [X] last week?"
→ Instant precedent analysis
→ Constitutional context
→ Exact quote and rationale
→ **30 seconds**

**This is a 60x speed improvement on institutional recall.**

**Multiply by hundreds of decisions per week.**

**This is why the Librarian is a paradigm shift.**

---

**The Librarian sees all. The Trinity acts with wisdom.**

**Together, we build the Republic.**

---

**Status:** ACTIVE
**Version:** 1.0
**Last Updated:** 2025-10-07
**Next Review:** 2025-10-14 (after one week of usage)
