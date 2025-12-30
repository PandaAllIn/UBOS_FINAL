# Balaur Proposal Loop Analysis

**Status:** CRITICAL
**Date:** 2025-11-20
**Log File:** `/srv/janus/03_OPERATIONS/vessels/balaur/logs/proposals.jsonl`

## 🚨 Findings

### 1. Stuck in Loop
Janus has generated **20+ duplicate proposals** for the same tasks since 03:55 UTC. The system is effectively spinning its wheels.

**Common Repeating Actions:**
*   `llama-cli inference` for "Comprehensive notes on GeoDataCenter..."
*   `node_generator` for "Funding Strategy breakdown report"
*   `node_generator` for "Asset Inventory breakdown report"

### 2. Proposal Status
*   **Approved:** 0 recent approvals
*   **Proposed:** Many recent items (e.g., `janus-7b1742f292e1` at 13:14 UTC) are stuck in "proposed" state.
*   **Draft/Suppressed:** The vast majority are marked `status: "draft"` with `metadata: { "suppressed": true, "duplicate_of": ... }`. This indicates the duplication suppression logic is working, but the *cause* of the re-generation (failure to execute the original) is not being addressed.

### 3. Root Cause Hypothesis
Janus is generating proposals because it sees the mission objectives as incomplete. However, the proposals are not transitioning from `proposed` to `approved` to `executing` to `completed`.

**Potential Blockers:**
*   **Auto-Approval Logic:** The `auto-approval-system` might be failing or disabled for these specific action types or risk levels.
*   **Mission Dispatcher:** Might be failing to pick up "proposed" items.
*   **Resource Starvation:** If the 1Hz tick rate fix (from previous mission) hasn't propagated to the proposal engine, it might be timing out.

## 🛠️ Remediation Plan

1.  **Check `agent.yaml`:** Verify auto-approval settings for "low" and "medium" risk tasks.
2.  **Check `approved_playbooks.yaml`:** Ensure `analysis` and `generate_breakdown_report` are whitelisted.
3.  **Force Approval:** Manually approve pending proposals to unblock the queue.
4.  **Implement Reasoning Fork:** Stop using `llama-cli` (slow) for everything. Route these analysis tasks to **Groq** (fast) or **Claude** (smart).

---
**Next Step:** Verify `agent.yaml` configuration.
