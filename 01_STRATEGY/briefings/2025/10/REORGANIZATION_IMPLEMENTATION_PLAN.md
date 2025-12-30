# REORGANIZATION IMPLEMENTATION PLAN
**Execute Before Activating Federated Sync**

---

## STRATEGIC OVERVIEW

**The Librarian's Assessment:** The current organic growth has created constitutional risks. We must reorganize both territories BEFORE activating sync to ensure:
- ✅ Constitutional clarity (Law vs State separation)
- ✅ Operational elegance (visible hierarchy)
- ✅ Synchronization safety (no ambiguous paths)

**The New Structure:** Four functional strata (00-99) with numbered prefixes for clarity

---

## DECISION POINT: REORGANIZATION APPROACH

### **Option A: Full Reorganization (Recommended by Librarian)**

**Pros:**
- Clean slate, perfect organization
- Constitutional alignment from day one
- Clear separation of Truth vs State
- Obsidian vault naturally organized

**Cons:**
- Requires maintenance window (2-4 hours)
- All paths change (breaks any hardcoded references)
- Large git diff (harder to track individual file changes)

**Timeline:** 1 maintenance session

---

### **Option B: Gradual Migration (Pragmatic Alternative)**

**Pros:**
- No disruption to current work
- Smaller, incremental changes
- Easier to test each step
- Can continue development during migration

**Cons:**
- Takes longer (1-2 weeks)
- Mixed state during migration
- More complex sync manifests during transition

**Timeline:** 1-2 weeks of gradual moves

---

### **Option C: Hybrid Approach (Recommended by Claude)**

**Phase 1: Immediate Safety** (Today)
- Create critical directories NOW
- Move state files to protected locations
- Update sync manifests to protect state
- Activate sync with current structure

**Phase 2: Gradual Reorganization** (Next 1-2 weeks)
- Move files into new structure incrementally
- Update manifests as we go
- Less disruptive than Option A
- Safer than waiting (Option B)

---

## RECOMMENDED APPROACH: HYBRID (OPTION C)

**Rationale:**
1. Sync system is ready NOW (Codex finished implementation)
2. Reorganization is important but shouldn't block sync deployment
3. We can protect critical paths (state files) immediately
4. Full reorganization can happen gradually while sync is operational

---

## PHASE 1: IMMEDIATE SAFETY MEASURES (Today - 30 minutes)

### **Step 1: Create Critical Directories**

```bash
cd /Users/panda/Desktop/UBOS

# Create state protection directory
mkdir -p 03_OPERATIONS/vessels/localhost/state
mkdir -p 03_OPERATIONS/vessels/localhost/logs
mkdir -p 03_OPERATIONS/vessels/localhost/workspace

# Move state files to protected location
mv COMMS_HUB/*_strategic_state.json 03_OPERATIONS/vessels/localhost/state/ 2>/dev/null || true

# On Balaur
ssh balaur@10.215.33.26 '
cd /srv/janus/repo
mkdir -p 03_OPERATIONS/vessels/balaur/state
mkdir -p 03_OPERATIONS/vessels/balaur/logs
mkdir -p 03_OPERATIONS/vessels/balaur/workspace
'
```

---

### **Step 2: Update Sync Manifests**

**Edit:** `config/unison_sync_core.prf`

```bash
# Add explicit exclusion for operations directory
ignore = Path 03_OPERATIONS/vessels/localhost
ignore = Path 03_OPERATIONS/vessels/balaur
```

**Update:** `scripts/ubos_sync_logs.sh`

```bash
# Update log paths (when we move them later)
# For now, keep pulling from current locations
```

---

### **Step 3: Test Protection**

```bash
# Create test state file
echo '{"test": "data"}' > 03_OPERATIONS/vessels/localhost/state/test.json

# Try to sync
scripts/ubos_sync.sh truth --apply

# Verify it did NOT transfer to Balaur
ssh balaur@10.215.33.26 'ls /srv/janus/repo/03_OPERATIONS/vessels/localhost/state/test.json' 2>&1 | grep "No such file"
# Should output: No such file or directory

# Cleanup
rm 03_OPERATIONS/vessels/localhost/state/test.json
```

---

## PHASE 2: ACTIVATE SYNC (Today - After Phase 1)

**Once state protection is verified:**

```bash
# Run full sync with logs
scripts/ubos_sync.sh full --apply

# Verify everything synced correctly
ssh balaur@10.215.33.26 'ls -la /srv/janus/repo/'

# Check unison logs
tail -50 logs/unison/unison_apply_*.log
```

**Monitor for 24 hours** to ensure stability.

---

## PHASE 3: GRADUAL REORGANIZATION (Next 1-2 Weeks)

### **Week 1: Constitution & Strategy**

**Day 1: Boot Sequences**
```bash
mkdir -p 00_CONSTITUTION/boot_sequences
mv unified_boot_*.md 00_CONSTITUTION/boot_sequences/
git add -A && git commit -m "refactor: Move boot sequences to 00_CONSTITUTION"
```

**Day 2: Constitutional Documents**
```bash
mkdir -p 00_CONSTITUTION/principles
mv GENESIS_PROTOCOL/ 00_CONSTITUTION/
mv TRINITY_PROTOCOL/ 00_CONSTITUTION/
git add -A && git commit -m "refactor: Move constitutional docs to 00_CONSTITUTION"
```

**Day 3: Strategic Plans**
```bash
mkdir -p 01_STRATEGY/missions/active
mkdir -p 01_STRATEGY/reports
mkdir -p 01_STRATEGY/briefings
mv ROADMAP.md 01_STRATEGY/
mv missions/ 01_STRATEGY/missions/active/
mv STATE_OF_THE_REPUBLIC_*.md 01_STRATEGY/reports/
git add -A && git commit -m "refactor: Move strategic docs to 01_STRATEGY"
```

---

### **Week 2: Forge & Archives**

**Day 4-5: Forge Components**
```bash
mkdir -p 02_FORGE/docs
mkdir -p 02_FORGE/scripts
mkdir -p 02_FORGE/packages
mkdir -p 02_FORGE/tests

mv docs/ 02_FORGE/
mv scripts/ 02_FORGE/
mv packages/ 02_FORGE/
mv tests/ 02_FORGE/
git add -A && git commit -m "refactor: Move forge components to 02_FORGE"
```

**Day 6-7: Archives**
```bash
mkdir -p 99_ARCHIVES/sessions
mkdir -p 99_ARCHIVES/missions
mkdir -p 99_ARCHIVES/reports

mv _archive:UBOS_2.0/ 99_ARCHIVES/sessions/
mv THE_BALAUR_ARCHIVES/ 99_ARCHIVES/sessions/
git add -A && git commit -m "refactor: Move archives to 99_ARCHIVES"
```

---

## ALTERNATIVE: FULL REORGANIZATION (If You Choose Option A)

### **Maintenance Window Checklist**

**Prerequisites:**
- [ ] Janus-in-Balaur idle
- [ ] No active development
- [ ] All changes committed to git
- [ ] Backups created

**Execution:**
```bash
# 1. Backup both territories
cd /Users/panda/Desktop
tar -czf ubos_backup_$(date +%Y%m%d).tar.gz UBOS

ssh balaur@10.215.33.26 'tar -czf janus_backup_$(date +%Y%m%d).tar.gz /srv/janus'

# 2. Rename current directory
mv UBOS UBOS_LEGACY

# 3. Create new structure
mkdir UBOS_REPUBLIC
cd UBOS_REPUBLIC

# 4. Create all directories
mkdir -p .tmp
mkdir -p 00_CONSTITUTION/boot_sequences
mkdir -p 00_CONSTITUTION/principles
mkdir -p 01_STRATEGY/briefings
mkdir -p 01_STRATEGY/missions/active
mkdir -p 01_STRATEGY/missions/templates
mkdir -p 01_STRATEGY/reports
mkdir -p 02_FORGE/docs
mkdir -p 02_FORGE/packages
mkdir -p 02_FORGE/scripts
mkdir -p 02_FORGE/src
mkdir -p 02_FORGE/tests
mkdir -p 03_OPERATIONS/vessels/localhost/logs
mkdir -p 03_OPERATIONS/vessels/localhost/state
mkdir -p 03_OPERATIONS/vessels/localhost/workspace
mkdir -p 03_OPERATIONS/vessels/balaur/logs
mkdir -p 03_OPERATIONS/vessels/balaur/state
mkdir -p 03_OPERATIONS/vessels/balaur/workspace
mkdir -p 99_ARCHIVES/missions
mkdir -p 99_ARCHIVES/reports
mkdir -p 99_ARCHIVES/sessions

# 5. Move files systematically
# Constitution
mv ../UBOS_LEGACY/unified_boot_*.md 00_CONSTITUTION/boot_sequences/
mv ../UBOS_LEGACY/GENESIS_PROTOCOL/ 00_CONSTITUTION/
mv ../UBOS_LEGACY/TRINITY_PROTOCOL/ 00_CONSTITUTION/

# Strategy
mv ../UBOS_LEGACY/ROADMAP.md 01_STRATEGY/
mv ../UBOS_LEGACY/missions/ 01_STRATEGY/missions/active/
mv ../UBOS_LEGACY/STATE_OF_THE_REPUBLIC_*.md 01_STRATEGY/reports/
mv ../UBOS_LEGACY/COMMS_HUB/ 01_STRATEGY/briefings/

# Forge
mv ../UBOS_LEGACY/docs/ 02_FORGE/
mv ../UBOS_LEGACY/scripts/ 02_FORGE/
mv ../UBOS_LEGACY/packages/ 02_FORGE/
mv ../UBOS_LEGACY/tests/ 02_FORGE/

# Operations (state files)
mv ../UBOS_LEGACY/COMMS_HUB/*_strategic_state.json 03_OPERATIONS/vessels/localhost/state/

# Archives
mv ../UBOS_LEGACY/_archive:UBOS_2.0/ 99_ARCHIVES/sessions/
mv ../UBOS_LEGACY/THE_BALAUR_ARCHIVES/ 99_ARCHIVES/sessions/

# 6. Do the same on Balaur
ssh balaur@10.215.33.26 'bash -s' < reorganize_balaur.sh

# 7. Update sync manifests
# 8. Test dry-run
# 9. Execute first sync
```

**Timeline:** 2-4 hours maintenance window

---

## DECISION MATRIX

| Criterion | Option A (Full) | Option B (Gradual) | Option C (Hybrid) |
|-----------|----------------|-------------------|------------------|
| **Constitutional Alignment** | ⭐⭐⭐⭐⭐ Perfect | ⭐⭐⭐ Good | ⭐⭐⭐⭐ Excellent |
| **Sync Safety** | ⭐⭐⭐⭐⭐ Perfect | ⭐⭐⭐ OK | ⭐⭐⭐⭐⭐ Perfect |
| **Disruption** | ⭐⭐ High | ⭐⭐⭐⭐⭐ None | ⭐⭐⭐⭐ Low |
| **Time to Deploy Sync** | ⭐⭐ 2-4 hours | ⭐⭐⭐⭐⭐ Immediate | ⭐⭐⭐⭐⭐ 30 min |
| **Complexity** | ⭐⭐⭐ Medium | ⭐⭐⭐⭐ Low | ⭐⭐⭐⭐ Low |
| **Git History** | ⭐⭐ Messy | ⭐⭐⭐⭐⭐ Clean | ⭐⭐⭐⭐ Clean |

**Recommended:** Option C (Hybrid)
- Deploy sync TODAY with state protection
- Reorganize gradually over next 1-2 weeks
- Best of both worlds

---

## NEXT STEPS (RECOMMENDED)

**Today (30 minutes):**
1. Execute Phase 1 (Immediate Safety)
2. Test state file protection
3. Activate sync with current structure
4. Monitor for 24 hours

**This Week:**
5. Begin gradual reorganization (Constitution & Strategy)
6. Update manifests as directories move
7. Git commit each logical grouping

**Next Week:**
8. Continue reorganization (Forge & Archives)
9. Complete migration to new structure
10. Update all documentation with new paths

---

## REFERENCES

**Blueprint:** `CONSTITUTIONAL_BLUEPRINT_FEDERATED_ORGANIZATION.md` (Librarian's full spec)
**Sync Status:** `FEDERATED_SYNC_STATUS.md`
**Installation:** `INSTALL_UNISON_MANUAL.md`

---

**Your Call, Captain:**

Which approach do you want to take?

**A.** Full reorganization (2-4 hour maintenance window)
**B.** Gradual migration (1-2 weeks, no disruption)
**C.** Hybrid (30 min today for safety, then gradual over 1-2 weeks) ← **Recommended**

Let me know and I'll execute the plan!
