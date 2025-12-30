# Mode Beta Deployment Report — 2025-10-10

**Authors:** Janus-in-Codex, Janus-in-Claude  
**Vessel:** The Balaur  
**Status:** COMPLETE — Mode Beta (supervised autonomy) is operational.

---

## 1. Deployment Timeline

### Phase 1 — Foundation (Victorian Controls & Cleanup)
- Installed the PI governor, relief valve, and 10 Hz escapement in `tool_executor.py`/`harness.py`.
- Constrained `llama.cpp` prompt surface; trimmed thinking-cycle context to constitutional essentials.
- Cleansed 197 historical proposals (deduplicate → archive → reject) and reindexed novelty windows.
- Added stubs for `node_generator` and `file_chunker` in preparation for philosophy and chronovisor missions.

### Phase 2 — Execution Engine (Auto-Executor & Monitoring)
- Created `auto_executor.py` with whitelist policy (`analysis`, `optimization_experiment`, `generate_new_nodes`, `process_chunk`).
- Patched `proposal_engine.py` and `tool_executor.py` to support auto approvals, execution lifecycle, and execution-state persistence.
- Delivered `proposal_cli.py` (list/show/watch/export) for live monitoring.
- Refreshed `agent.yaml` to expose auto-executor configuration and mission poll interval.
- Documented operations in `JANUS_AGENT_OPERATIONS.md` and `BALAUR_STATUS.md`.

### Phase 3 — Safety & Reliability
- Resolved Python import deadlock by forward references and local imports.
- Added sandbox fallback (`sandbox.py`) when bubblewrap is absent; enforced tool + risk guardrails.
- Authored `/srv/janus/bin/emergency-stop` to halt `janus-agent`/`janus-controls` and suspend proposals.
- Updated systemd services (`janus-agent`, `janus-controls`) and mission sequencing for the new BETA missions.
- Restarted services and verified auto-executor loop, mission transitions, and audit logs.

---

## 2. Problems Encountered & Resolutions
| Issue | Impact | Resolution |
| --- | --- | --- |
| Import deadlock between `auto_executor` and `daemon` | `janus-agent` froze on startup | Refactored imports to forward references + TYPE_CHECKING |
| Absence of `/usr/bin/bwrap` | Sandbox raised `FileNotFoundError` | Added safe fallback path with resource limits and audit metadata |
| 197 legacy proposals in `proposals.jsonl` | Auto-approval backlog | Purged/archived duplicates; re-seeded novelty index |
| Lack of emergency stop | No rapid shutdown | Delivered `/srv/janus/bin/emergency-stop` (dry-run + full stop) |
| Monitoring gaps | Limited visibility into Mode Beta | Introduced `proposal_cli.py`, docs updates, and log tail commands |

---

## 3. Tool Registry Snapshot (Mode Beta Whitelist)
| Tool | Purpose | Auto-Exec | Notes |
| --- | --- | --- | --- |
| `shell` | Read-only command execution (`echo`, `ls`, chunk processing) | ✅ | Enforced command whitelist + forbidden token check |
| `node_generator` (stub) | Generate philosophy YAML nodes | ✅ | Implementation forthcoming for STUDY-002-BETA |
| `file_chunker` (stub) | Read mission documents in 5k-line segments | ✅ | Used by STUDY-004-BETA chunking workflow |
| `python`, `curl`, `git`, `rg`, `jq`, `sqlite3` | Manual tools | ❌ | Require human approval (risk > low) |

---

## 4. Performance & Validation

* **Auto-executor trial:** 8 low-risk proposals executed successfully on 2025-10-10 (`mode beta deployment test`, mission focus echoes, chunk prep).
* **Resource guardrails:** CPU < 80%, memory < 2 GB, disk writes < 100 MB, timeout 600 s for all auto-exec runs (`tool_use.jsonl` metadata).
* **Emergency stop:** Dry-run verified logging + service kill sequence (production run pending).
* **Mission queue:** New BETA missions deployed — chronological archaeology (13 chunks), hardware optimisation (10–20 experiments), philosophy node generation (30–50 nodes).

---

## 5. Follow-On Work

1. Implement GPU Studio (Phase 2.6B) and connect logging to mission history once filesystem remount allows.
2. Ship node generator + chunk processing tools for STUDY-002/004 execution.
3. Automate Mode Beta daily summaries (success rate, resource metrics, proposals executed).
4. Finish documentation suite (`packages/janus_agent/README.md`, root README updates) for developer onboarding.

Mode Beta is running within constitutional bounds—autonomy through empowerment, not risk.#
