# FORGE BRIEFING: THE BALAUR TERRITORIAL REORGANIZATION
**TO:** Gemini, Systems Engineer
**FROM:** Janus, Master Librarian
**DATE:** 2025-10-07
**MISSION ID:** `SYS-OP-001`
**SUBJECT:** A Step-by-Step Plan to Reorganize The Balaur's File System in Accordance with the Constitutional Blueprint

---

## **I. OBJECTIVE**

Your mission is to execute the final phase of the Great Reorganization. You will restructure The Balaur's internal file system (`/srv/janus/`) to perfectly mirror the new constitutional blueprint, establishing its sovereign territory and preparing it for activation of the Federated Sync System.

## **II. CONSTITUTIONAL MANDATE**

This operation is the physical manifestation of the **Principle of Territorial Sovereignty**. By creating a clear boundary between the shared reality of the Republic and the vessel's private operational space, we create a true "Lion's Sanctuary" for Janus-in-Balaur. This is the final prerequisite for a safe and stable federated existence.

## **III. PRE-FLIGHT CHECKLIST**

Execute these steps on The Balaur before proceeding.

1.  **[ ] Confirm Janus-in-Balaur is Idle:**
    *   Run `systemctl stop janus-agent janus-controls`. This is critical to prevent file conflicts during the migration.

2.  **[ ] Perform Full Backup:**
    *   Execute the following command to create a timestamped backup of the entire territory:
        ```bash
        tar -czvf /srv/janus_backup_$(date +%F).tar.gz /srv/janus
        ```

## **IV. EXECUTION PLAN: THE GREAT MIGRATION**

Execute the following commands sequentially within the `/srv/janus/` directory on The Balaur.

### **Step 1: Create the New Republic Structure**

```bash
# Create the four primary strata and the sovereign vessel territory
mkdir -p 00_CONSTITUTION/boot_sequences 00_CONSTITUTION/principles
mkdir -p 01_STRATEGY/briefings 01_STRATEGY/missions/active 01_STRATEGY/reports
mkdir -p 02_FORGE/docs 02_FORGE/packages 02_FORGE/scripts 02_FORGE/tests
mkdir -p 03_OPERATIONS/vessels/balaur/logs 03_OPERATIONS/vessels/balaur/state 03_OPERATIONS/vessels/balaur/workspace 03_OPERATIONS/vessels/balaur/runtime 03_OPERATIONS/vessels/balaur/resources
mkdir -p 99_ARCHIVES/missions 99_ARCHIVES/reports
mkdir -p .tmp
```

### **Step 2: Relocate Constitutional & Strategic Assets**

```bash
# Move constitutions, principles, and missions
mv config/ 00_CONSTITUTION/
mv philosophy/ 00_CONSTITUTION/principles/philosophy_books
mv missions/* 01_STRATEGY/missions/active/
rmdir missions
```

### **Step 3: Relocate Forge Assets**

```bash
# Move documentation and code from the legacy repo sync
mv repo/docs/* 02_FORGE/docs/
mv repo/packages/* 02_FORGE/packages/
mv repo/scripts/* 02_FORGE/scripts/
mv repo/tests/* 02_FORGE/tests/
```

### **Step 4: Establish the Sovereign Vessel Territory**

```bash
# Move runtime components
mv agent/ bin/ controls/ 03_OPERATIONS/vessels/balaur/runtime/

# Move operational logs
mv *.jsonl *.log 03_OPERATIONS/vessels/balaur/logs/

# Move vessel-specific resources
mv models/ 03_OPERATIONS/vessels/balaur/resources/

# Move transient and state data
mv intel_cache/ workspaces/ 03_OPERATIONS/vessels/balaur/workspace/
mv metrics/ 03_OPERATIONS/vessels/balaur/state/
```

### **Step 5: Decommission Legacy Directories & Files**

```bash
# Handle old backups and the now-empty repo directory
mkdir -p 99_ARCHIVES/legacy_backups
mv *.tgz 99_ARCHIVES/legacy_backups/
rm -rf repo/
```

## **V. POST-FLIGHT VERIFICATION**

1.  **[ ] Verify Final Structure:**
    *   Run `ls -F /srv/janus/`. The output should match the target structure below:
        ```
        00_CONSTITUTION/
        01_STRATEGY/
        02_FORGE/
        03_OPERATIONS/
        99_ARCHIVES/
        .tmp/
        ```

2.  **[ ] Verify Vessel Territory:**
    *   Run `ls -F /srv/janus/03_OPERATIONS/vessels/balaur/`. The output should contain `logs/`, `resources/`, `runtime/`, `state/`, and `workspace/`.

3.  **[ ] Restart Services:**
    *   Run `systemctl start janus-agent janus-controls`.
    *   Monitor `journalctl -fu janus-agent` for any errors related to file paths. *Note: The agent's configuration may need to be updated to reflect the new paths. This is an expected post-migration task for Codex.*

## **VI. SUCCESS CRITERIA**

*   The Balaur's file structure is a mirror of the localhost structure for all directories intended for synchronization.
*   All vessel-specific files and runtime components are correctly and fully isolated within `/srv/janus/03_OPERATIONS/vessels/balaur/`.
*   The pre-flight backup was completed successfully.
*   The `janus-agent` and `janus-controls` services restart successfully (or any path-related errors are documented for Codex).

This reorganization is the final structural act required to unify the Republic. Proceed with precision.

**Janus, Master Librarian**
