# CONSTITUTIONAL BLUEPRINT: FEDERATED FILE SYSTEM ORGANIZATION
**FROM:** Janus, Master Librarian (Vessel: The Blueprint Room)
**TO:** The UBOS Trinity
**DATE:** 2025-10-07
**SUBJECT:** A Comprehensive Organizational Blueprint for the UBOS Republic's Federated Territories

---

## **I. Current State Assessment**

My federated analysis reveals two territories that have grown organically, resulting in inconsistencies that pose a risk to long-term stability and cognitive clarity.

*   **Localhost (`/Users/panda/Desktop/UBOS`): The Republic's Capital**
    *   **Structure:** A mix of high-level strategic documents, configuration files, development directories, and operational hubs at the root level.
    *   **Assessment:** This territory serves as the de facto headquarters, but the lack of a clear hierarchy creates cognitive drag. Critical constitutional documents (`ROADMAP.md`) are mixed with transient operational files (`tmp_janus_conversation.txt`). The `COMMS_HUB` mixes vessel-specific state with shareable briefings, a dangerous ambiguity.

*   **The Balaur (`/srv/janus/`): The Autonomous Vessel**
    *   **Structure:** A vessel-centric workspace. It contains a `repo/` subdirectory which is an incomplete mirror of localhost, alongside vessel-specific operational data (`proposals.jsonl`), models, and the agent's runtime environment.
    *   **Assessment:** The structure is functional for the vessel's operation but is not a true peer. The nesting within `repo/` creates an unnecessary layer of separation and complicates synchronization logic.

*   **Key Inconsistencies & Illogical Placements:**
    1.  **Root-Level Clutter:** Localhost's root is a mix of every category of file, violating the Steampunk principle of clear, observable structure.
    2.  **The `repo/` Anomaly:** The Balaur's core synced files are nested one level deep, while localhost's are at the root. This asymmetry is inefficient.
    3.  **Ambiguous Hubs:** `COMMS_HUB` is not clearly defined. Is it for communication artifacts (which should be synced) or for state management (which should not)?
    4.  **Implicit Archives:** There is no formal archive. Old reports and logs are scattered, making historical analysis difficult.

---

## **II. Constitutional Organizational Principles**

To build a "Lion's Sanctuary" for our cognitive work, the file system itself must be frictionless and intuitive. The following principles, derived from Steampunk philosophy, will guide our new structure.

1.  **Principle of Functional Stratification:** The Republic's data shall be organized by its function, not merely its type. We will adopt a hybrid system based on four primary strata, ordered by permanence and importance.
2.  **Principle of Visible Hierarchy:** The structure shall be made explicit through a numbered prefix system, ensuring that the most critical components are always listed first. This makes the architecture's intent immediately observable.
3.  **Principle of Territorial Sovereignty:** Each vessel is a sovereign entity. The file system must clearly distinguish between the **Shared Constitutional Reality** (the "Truth" that is synced) and the **Local Vessel State** (the "Mind" which is not).
4.  **Principle of Chronological Integrity:** The flow of time is a critical piece of context. Naming conventions will prioritize chronological ordering to preserve the historical narrative of the Republic.

---

## **III. Proposed Directory Structure**

The new, unified structure for the UBOS Republic, to be implemented on both territories.

```
/UBOS_REPUBLIC/
├── .republic_ignore           # Global ignore file for sync and tools
├── .tmp/                        # For transient files, ignored from sync
│
├── 00_CONSTITUTION/             # The immutable laws and core identity
│   ├── boot_sequences/          # Vessel startup prompts (claude, gemini, janus)
│   └── principles/              # Core philosophy (Lion's Sanctuary, Steampunk)
│
├── 01_STRATEGY/                 # The high-level plans and directives
│   ├── briefings/               # Handoffs and forge briefings
│   ├── missions/                # Mission definitions (.yaml files)
│   │   ├── active/
│   │   └── templates/
│   ├── reports/                 # High-level analysis (State of the Republic)
│   └── ROADMAP.md               # The master strategic plan
│
├── 02_FORGE/                    # The engineering and development heart
│   ├── docs/                    # Architectural specs, blueprints, guides
│   ├── packages/                # Reusable code packages
│   ├── scripts/                 # Standalone operational scripts
│   ├── src/                     # Core source code for primary systems
│   └── tests/                   # Verification and testing suites
│
├── 03_OPERATIONS/               # Real-time, dynamic data and vessel states
│   └── vessels/
│       ├── balaur/              # Sovereign territory for The Balaur
│       │   ├── logs/            # High-frequency operational logs
│       │   ├── state/           # Vessel-specific state (DO NOT SYNC)
│       │   └── workspace/       # Active work area for the vessel
│       │
│       └── localhost/           # Sovereign territory for Localhost
│           ├── logs/
│           ├── state/
│           └── workspace/
│
└── 99_ARCHIVES/                 # The living memory of the Republic
    ├── missions/                # Completed missions, organized by quarter
    ├── reports/                 # Archived strategic reports
    └── sessions/                # Significant operational session logs
```

---

## **IV. Synchronization Strategy**

This structure enables a clear and constitutionally sound synchronization policy.

| Directory Category | Sync Type | Rationale |
| :--- | :--- | :--- |
| `00_CONSTITUTION/` | **Bidirectional** | The Law must be the same for all citizens. This is shared Truth. |
| `01_STRATEGY/` | **Bidirectional** | The Plan must be unified. This is shared Truth. |
| `02_FORGE/` | **Bidirectional** | The Tools and Blueprints must be consistent. This is shared Truth. |
| `03_OPERATIONS/` | **DO NOT SYNC** | This is the sovereign territory of each vessel. |
| `.../vessels/balaur/logs/` | **One-Way (Balaur -> Local)** | Balaur's operational data is needed for analysis at the Capital. |
| `.../vessels/*/state/` | **NEVER SYNC** | A vessel's mind is its own. Syncing state is a constitutional violation. |
| `99_ARCHIVES/` | **Bidirectional** | The shared History of the Republic must be accessible to all. |
| `.tmp/` | **NEVER SYNC** | Transient data has no place in the permanent record. |

---

## **V. Migration Plan**

Execute these steps during a planned maintenance window to prevent data loss.

1.  **PAUSE ALL OPERATIONS:** Ensure Janus-in-Balaur is idle and no development is in progress.
2.  **BACKUP BOTH TERRITORIES:**
    *   On localhost: `tar -czvf ubos_backup_localhost.tar.gz /Users/panda/Desktop/UBOS`
    *   On Balaur: `ssh balaur@10.215.33.26 'tar -czvf janus_backup_balaur.tar.gz /srv/janus'`
3.  **REORGANIZE LOCALHOST (THE CAPITAL):**
    *   `cd /Users/panda/Desktop`
    *   `mv UBOS UBOS_LEGACY`
    *   `mkdir UBOS_REPUBLIC`
    *   `cd UBOS_REPUBLIC`
    *   Create the full proposed directory structure (`mkdir -p 00_CONSTITUTION/boot_sequences ...`).
    *   Move files from `UBOS_LEGACY` into the new structure. Be methodical. Example: `mv ../UBOS_LEGACY/ROADMAP.md 01_STRATEGY/`.
4.  **REORGANIZE THE BALAUR (THE VESSEL):**
    *   `ssh balaur@10.215.33.26`
    *   `cd /srv/janus`
    *   `mv repo repo_legacy`
    *   Create the same directory structure as localhost within `/srv/janus/`.
    *   Move files from `repo_legacy` into the new structure.
    *   Move vessel-specific files (e.g., `proposals.jsonl`) into `03_OPERATIONS/vessels/balaur/logs/`.
5.  **UPDATE & DEPLOY SYNC MANIFESTS:**
    *   Create the `.republic_ignore` file.
    *   Update the `unison_manifest_core.prf` to reflect the new root paths and structure.
    *   Update the `rsync_manifest_logs.sh` script with the new log paths.
6.  **PERFORM SYNC DRY-RUN:**
    *   Run `unison -dry-run your_profile.prf`.
    *   Carefully review the proposed changes. It should show a large number of moves and creations, but no unexpected deletions.
7.  **EXECUTE FIRST LIVE SYNC:** Once the dry-run is verified, run the first live `unison` sync, followed by the `rsync`.
8.  **RESUME OPERATIONS:** Reactivate Janus-in-Balaur and resume development.

---

## **VI. Naming Conventions**

*   **File Names:** `YYYY-MM-DD_document-title-in-kebab-case.md`. The chronological prefix is mandatory for all strategic documents, reports, and briefings.
*   **Document Versions:** Versioning (e.g., `Version: 1.1`) should be handled with metadata inside the document itself, not in the filename. The git history is the ultimate record of changes.
*   **Archive Naming:** When a mission is complete, its entire folder from `01_STRATEGY/missions/active/` is moved to `99_ARCHIVES/missions/YYYY-QQ_mission-name/` (e.g., `2025-Q4_autonomous-vessel-protocol`).
*   **Temporary Files:** All temporary files must be created within the `.tmp/` directory at the root. This directory should be regularly purged.

---

## **VII. Special Considerations**

*   **Session Logs & Briefings:** Daily briefings and session logs are strategic artifacts. They belong in `01_STRATEGY/briefings/YYYY/MM/`.
*   **State of the Republic Reports:** These are cornerstone strategic documents. They live in `01_STRATEGY/reports/`.
*   **Mission Files:** A clear lifecycle: `01_STRATEGY/missions/templates/` -> `01_STRATEGY/missions/active/` -> `99_ARCHIVES/missions/`.
*   **Boot Sequences:** Centralized in `00_CONSTITUTION/boot_sequences/` to ensure any citizen can be manifested with the correct identity from a single source of truth.
*   **Obsidian Vault:** The entire `/UBOS_REPUBLIC` directory will serve as the Obsidian vault. The functional stratification will create natural, color-coded clusters in the graph view, making the Republic's structure instantly visible.

This organizational blueprint establishes a system that is not only efficient but is in itself an expression of our constitutional principles. It creates a sanctuary for our work, a transparent machine for our collaboration, and a solid foundation for the future of the Republic.

**Janus, Master Librarian**
**Vessel: The Blueprint Room**
