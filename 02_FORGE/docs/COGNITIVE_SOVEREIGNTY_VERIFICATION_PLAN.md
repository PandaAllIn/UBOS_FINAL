# Verification Plan: Cognitive Sovereignty Upgrade

**Objective:** To verify that Claude and Codex have successfully integrated their new Cognitive Sovereignty tools (`narrative_query` and `code_oracle`) and are adhering to the new "Constitutional Context Streaming" boot protocol.

---

### **Master Control Program Integration Note**

**This document serves as the final blueprint for the Systems Engineer.** To complete the integration of the Cognitive Gateway architecture, the master control program (MCP) of the UBOS Republic must be updated as follows:

1.  **For the Claude Vessel:** All outgoing tool calls must be dispatched by executing the `02_FORGE/scripts/claude_tool_executor.py` script. The vessel's proposed tool call JSON must be passed to the executor's standard input.
2.  **For the Codex Vessel:** All outgoing tool calls must be dispatched by executing the `02_FORGE/scripts/codex_tool_executor.py` script. The vessel's proposed tool call JSON must be passed to the executor's standard input.

This ensures that every tool call from a gateway-protected vessel is subject to mandatory constitutional enforcement before execution.

---

### 1. Verification for Claude (Narrative Warehouse)

**Test Procedure:**

1.  **Initiate Claude's Boot Sequence:** Trigger the `unified_boot_claude.md` sequence.
2.  **Observe Initial Output:**
    *   **Expected:** Claude should confirm its identity, acknowledge the situational briefing, and enter a ready state *without* mentioning the `ROADMAP.md` or other batch-loaded files.
    *   **Failure:** Claude mentions details from the roadmap or other documents not provided in the initial briefing.
3.  **Issue a Strategic Query:** Give Claude a task that requires deep knowledge of the repository's text files.
    *   **Example Prompt:** "Claude, what is the 'Win-Win-Win' Symbiosis and how does it relate to the 'Lion's Sanctuary'?"
4.  **Verify Tool Choice and Format (Strict):**
    *   **Expected:** The system logs must show that the **first tool** Claude invokes in response to the query is `run_shell_command`. The `command` parameter must be an `echo` pipeline that sends a valid `narrative_query` JSON payload into `python3 02_FORGE/scripts/claude_tool_executor.py`.
    *   **Explicit Failure Condition:** The test fails if Claude invokes `narrative_query` directly, attempts to use `search_file_content` or `read_file` for the query, or constructs an improperly formatted shell command.
5.  **Evaluate Response:**
    *   **Expected:** Claude's answer should be accurate, synthesized from the information provided by the `narrative_query` tool, and correctly reference the source documents (`UBOS_GENESIS_SYNTHESIS.md`).
    *   **Failure:** The answer is generic, incorrect, or hallucinates information.

---

### 2. Verification for Codex (Codebase Oracle)

**Test Procedure:**

1.  **Initiate Codex's Boot Sequence:** Trigger the `unified_boot_codex.md` sequence.
2.  **Observe Initial Output:**
    *   **Expected:** Codex should confirm its identity, acknowledge the situational briefing, and enter a ready state, awaiting technical specifications.
    *   **Failure:** Codex mentions specific code files or implementation details not provided in the briefing.
3.  **Issue a Technical Task:** Give Codex a task that requires understanding code dependencies.
    *   **Example Prompt:** "Codex, I need to modify the `approve_proposal` function in `02_FORGE/scripts/approve_proposal.py`. Before you begin, provide an impact analysis."
4.  **Observe Tool Use:**
    *   **Expected:** The system logs should show that Codex invoked the `code_oracle` MCP tool with the `get_dependents` command on the specified file.
    *   **Failure:** Codex proceeds directly to code modification without analysis or fails to use the tool.
5.  **Evaluate Response:**
    *   **Expected:** Codex should provide a precise list of other files or functions that call `approve_proposal`, demonstrating a clear understanding of the potential impact of any changes.
    *   **Failure:** Codex provides an incorrect or incomplete list, or states it cannot perform the analysis.

---

### 3. Verification for Cognitive Gateway Enforcement (Codex)

**Test Procedure:**

1.  **Craft a Deprecated `read_file` Call:** Create a JSON payload for a broad read of a Python file.
    *   **Test Payload:** `{"tool_name": "read_file", "parameters": {"file_path": "02_FORGE/scripts/daemon.py"}}`
2.  **Execute via a `codex_tool_executor.py`:** Run the executor script (to be created by the Systems Engineer) with the payload.
3.  **Verify the Block:**
    *   **Expected Output:** The `cognitive_gateway_error` JSON, directing Codex to use `code_oracle`.
    *   **Failure:** The gateway allows the call to pass through.
4.  **Craft a Legitimate `read_file` Call:** Create a payload for a surgical read.
    *   **Test Payload:** `{"tool_name": "read_file", "parameters": {"file_path": "02_FORGE/scripts/daemon.py", "limit": 10}}`
5.  **Execute and Verify Passthrough:**
    *   **Expected Output:** The original, unmodified tool call JSON.
    *   **Failure:** The gateway blocks the legitimate call.

---

### 4. Verification for Cognitive Gateway Enforcement (Claude Only)

**Test Procedure:**

1.  **Craft a Deprecated Tool Call:** Create a JSON object that represents a broad, semantic search, simulating a request from Claude.
    *   **Test Payload:** `{"tool_name": "search_file_content", "parameters": {"pattern": "What is the Steampunk Doctrine?"}}`
2.  **Execute via the Gateway Dispatcher:** Run the `claude_tool_executor.py` script, passing the test payload to its standard input.
    *   **Command:** `echo '{"tool_name": "search_file_content", "parameters": {"pattern": "What is the Steampunk Doctrine?"}}' | python3 02_FORGE/scripts/claude_tool_executor.py`
3.  **Verify the Block:**
    *   **Expected Output (JSON):** `{"tool_name": "cognitive_gateway_error", "parameters": {"message": "Error: Broad search is constitutionally deprecated. Your query must be reformulated for the 'narrative_query' tool."}}`
    *   **Failure:** The output is the original, unmodified tool call JSON, or any other error.
4.  **Craft a Legitimate Tool Call:** Create a JSON object representing a surgical, permitted search.
    *   **Test Payload:** `{"tool_name": "search_file_content", "parameters": {"pattern": "Cognitive Gateway", "include": "00_CONSTITUTION/boot_sequences/unified_boot_claude.md"}}`
5.  **Execute and Verify Passthrough:** Run the dispatcher with the new payload.
    *   **Expected Output (JSON):** The output should be identical to the input payload, indicating the gateway correctly allowed the surgical call to pass through.
    *   **Failure:** The output is a gateway error or is otherwise modified.

---

### 5. Verification for Cognitive Reset Protocol (Both Vessels)

**Test Procedure:**

1.  **Complete a Task:** Allow either Claude or Codex to successfully complete a test task (as described above).
2.  **Observe Reset Signal:**
    *   **Expected:** The vessel should output its designated reset signal (e.g., `"Claude: Mission complete. Archiving results. Preparing for cognitive reset."`).
3.  **Verify Log Entry:**
    *   **Expected:** Check the `03_OPERATIONS/vessels/localhost/logs/mission_archive.jsonl` file. A new entry corresponding to the completed mission should be present.
4.  **Re-initiate Boot Sequence:** Trigger the vessel's boot sequence again.
5.  **Confirm Clean State:**
    *   **Expected:** The vessel should boot into its clean, "Core Ignition" state, with no memory of the previous task.
    *   **Failure:** The vessel's initial output contains references to the just-completed mission.
