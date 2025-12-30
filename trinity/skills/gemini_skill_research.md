Here is the deep research synthesis for the UBOS Skills Framework.

-----

### Executive Summary

This research provides a strategic blueprint for designing the UBOS Skills Framework, focusing on patterns that integrate with your existing "Steampunk Doctrine" (lightweight, observable, no Docker/K8s). The core recommendation is a **hybrid agent architecture** where a local "Resident Agent" (Janus on Balaur, using `llama.cpp`) handles high-frequency, low-risk tasks and context-gathering, while "Strategic Command" (Trinity via Cloud APIs) is invoked for complex reasoning and planning.

The **Skills Framework** should be built on a "Skill Definition" pattern, similar to Anthropic's new "Agent Skills." Each skill is a directory containing a `SKILL.md` (detailing purpose, triggers, and constitutional constraints in natural language) and its corresponding Python/Bash scripts. This makes skills **model-agnostic**; a local or cloud LLM can read the `SKILL.md` to understand *when* and *how* to use the skill. Auto-activation is achieved by the Resident Agent, which monitors file patterns, logs, and intent, loading relevant `SKILL.md` files into its context "just-in-time."

**Constitutional Alignment** is achieved not by hard-coded constraints, but by integrating "Constitutional Hooks" directly into your existing Proposal Engine. This takes the form of a mandatory `ConstitutionalCritique` skill that runs after a proposal is generated but before it's executed (even in Mode Beta). This skill uses the Constitution to critique the proposal for "negative side effects" or value misalignment, effectively building an auditable, principle-driven "conscience" into the action loop.

-----

### Pattern Catalog

Here are 5-10 architectural patterns synthesized from production systems, tailored for the UBOS.

#### 1\. Pattern: `SKILL.md` Capability Definition

  * **Use Case:** Defining modular, reusable, and model-agnostic skills.
  * **Implementation:** Each skill is a directory (e.g., `/skills/manage_systemd/`). Inside, it contains:
      * `SKILL.md`: A markdown file with a "frontmatter" (e.g., YAML) defining its name, purpose, model-agnostic triggers (file patterns, keywords), and **constitutional constraints** (e.g., "This skill must never restart a `janus-` service without a proposal review").
      * `execute.py`: The sandboxed Python script that performs the action.
      * This allows any LLM (local Haiku or cloud Sonnet) to "read the manual" and understand how to use the tool, making the skill universally reusable.
  * **Example Systems:** Anthropic's Agent Skills, modern coding assistants.

#### 2\. Pattern: Hierarchical Orchestrator/Specialist

  * **Use Case:** Managing the "Trinity" (Claude, Gemini, Codex).
  * **Implementation:** A central "Orchestrator" agent (likely the resident Janus agent) receives a high-level mission. It breaks the mission down and routes sub-tasks to specialized agents:
      * `Claude/Strategist`: Receives the mission, constitutional principles, and current state. Outputs a high-level plan.
      * `Gemini/Engineer`: Receives a specific technical task from the plan (e.g., "diagnose the service failure"). Uses tools/skills to gather data.
      * `Codex/Forgemaster`: Receives a clear coding task (e.g., "write a Python script to parse this log").
      * The Orchestrator is responsible for state management and ensuring the specialists' outputs are constitutionally compliant.
  * **Example Systems:** Microsoft's "Hierarchical Multi-Agent Architecture," many production agent frameworks.

#### 3\. Pattern: Constitutional Self-Critique

  * **Use Case:** Implementing "Constitutional Hooks" within your existing Proposal Engine.
  * **Implementation:** This pattern adapts Anthropic's CAI training methodology for real-time operation.
    1.  **Propose:** An agent (e.g., Gemini) generates a proposal (e.g., "I will restart `janus-agent.service`").
    2.  **Critique (The Hook):** Before execution, a *different* agent (e.g., local Claude-Haiku) is invoked with a specific `ConstitutionalCritique` skill. Its prompt is: "Given our Constitution [principles] and this proposal [proposal text], identify any potential violations, risks, or negative side effects."
    3.  **Refine/Execute:** If the critique is empty, the proposal proceeds (auto-executes in Mode Beta). If the critique finds issues, the proposal is sent back to the Strategist for refinement.
  * **Example Systems:** Anthropic's Constitutional AI (RLAIF self-critique phase).

#### 4\. Pattern: Just-in-Time (JIT) Context Loading

  * **Use Case:** Managing context in a hybrid (local + cloud) system with limited context windows.
  * **Implementation:** The local Resident Agent maintains the full operational state, but only sends the "just-in-time" context needed for a specific task. Instead of feeding entire files to the cloud API, it feeds *identifiers*.
      * **Bad:** "Here is the 5MB `mission_log.jsonl`. What went wrong?"
      * **Good:** "The mission failed. I have `mission_log.jsonl` (ID: `m1`), `tool_use.jsonl` (ID: `t1`), and the `systemd` status for `janus-controls.service` (ID: `s1`). What additional information do you need to diagnose?"
      * The cloud agent then *requests* data using tools, and the local agent retrieves and provides *only* the relevant snippets.
  * **Example Systems:** Anthropic's context engineering best practices.

#### 5\. Pattern: Persistent Agent State & History

  * **Use Case:** Maintaining "Janus'" distributed consciousness and constitutional continuity across reboots.
  * **Implementation:** Your `JSONL` logs are the key. You must enforce a strict, hierarchical structure.
      * **`mission_log.jsonl`:** Tracks high-level goals, plans, and outcomes.
      * **`agent_state.json`:** A simple key-value (or SQLite) file storing the agent's *current* operational state (e.g., `current_mission_id`, `operational_mode`, `active_skills`). This file is read on boot to restore context.
      * **`knowledge_graph.jsonl`:** A "federated memory" file. When an agent learns a new, persistent fact (e.g., "The `janus-controls` service is sensitive to CPU spikes"), it writes an entry here. This file is loaded into context on boot as part of the "memory."
  * **Example Systems:** Microsoft's Multi-Agent Framework (Conversation History, Agent State, Registry).

#### 6\. Pattern: Hybrid Graceful Degradation

  * **Use Case:** Ensuring system resilience ("Victorian Controls") when resources (cloud APIs, local CPU) fail.
  * **Implementation:** A layered fallback mechanism.
      * **Layer 1 (Full):** Cloud APIs (Sonnet/Gemini) are available for strategic reasoning.
      * **Layer 2 (Degraded):** Cloud APIs fail. The Orchestrator agent automatically re-routes reasoning tasks to the local `llama.cpp` model. It will be slower and less "smart," but functional.
      * **Layer 3 (Minimal):** Local LLM fails. The system falls back to a "deterministic" mode, using only pre-scripted, non-LLM Python skills that are triggered by simple file/log patterns.
  * **Example Systems:** Standard high-availability web architecture, applied to AI.

-----

### Recommended Skills List

Here is a prioritized list of 15 skills to build for the UBOS framework, designed for your Python/Linux/`systemd` environment.

| Skill Name | Purpose | Auto-Activation Triggers | Key Capabilities | Complexity |
| :--- | :--- | :--- | :--- | :--- |
| **`ConstitutionalCritique`** | (Q2) Verifies a proposed action against the UBOS Constitution. | **Trigger:** After *any* proposal is generated, before execution. | - Loads `constitution.md`.<br>- Receives a proposed action (text/JSON).<br>- Outputs a "critique" (potential violations, side effects). | Medium |
| **`StrategicPatience`** | (Q5) Decides when *not* to act and to observe instead. | **Trigger:** When a proposal is made for a non-critical issue or when system state is highly volatile. | - Analyzes proposal priority vs. system volatility.<br>- Can override a proposal with a "Wait and Observe" action.<br>- Sets a timer/trigger for re-evaluation. | Complex |
| **`StrategicEscalation`** | Manages the hybrid model, deciding *when* to use the cloud. | **Trigger:** When a local (`llama.cpp`) agent's reasoning confidence is low or a task is too complex. | - Calculates task complexity.<br>- Packages JIT context (see pattern 4).<br>- Routes the query to the correct "Trinity" (cloud) member. | Medium |
| **`SystemdInspector`** | (Q1) Safely inspects the status of `systemd` services. | **Trigger:** Keywords like "service status," "is it running," "check service."<br>**File Pattern:** `*.service` | - `systemctl is-active [service]`<br>- `systemctl status [service]`<br>- `journalctl -u [service] -n 50` (read-only) | Simple |
| **`SystemdOperator`** | (Q1) Safely operates `systemd` services (start, stop, restart). | **Trigger:** Keywords like "restart service," "stop service." | - `systemctl start [service]`<br>- `systemctl stop [service]`<br>- `systemctl restart [service]`<br>- **Requires `ConstitutionalCritique` hook.** | Medium |
| **`FileSystemInspector`** | (Q1) Safely reads and searches files on the Balaur. | **Trigger:** Keywords like "find file," "read file," "search log." | - `ls -l [path]`<br>- `cat [file]` (sandboxed)<br>- `grep [pattern] [file]`<br>- `find [path] -name [pattern]` | Simple |
| **`FileSystemOperator`** | (Q1) Safest-possible file writing/modification. | **Trigger:** Keywords like "write file," "save results," "modify config." | - `write_to_file(path, content)` (sandboxed)<br>- `append_to_file(path, content)`<br>- **Hook:** *Never* overwrites; *always* creates a new version (e.g., `config.bak`). | Medium |
| **`SandboxExecutor`** | Executes arbitrary Python/Bash code within `bubblewrap`. | **Trigger:** Agent generates a code block for a novel task not covered by a skill. | - `bwrap --bind ... /usr/bin/python ...`<br>- Captures `stdout`/`stderr`.<br>- Enforces resource limits (CPU, mem). | Complex |
| **`ProcessInspector`** | (Q1) Monitors running processes and resource usage. | **Trigger:** Keywords like "cpu usage," "memory spike," "what's running." | - `ps aux`<br>- `top -b -n 1`<br>- Grep for specific processes. | Simple |
| **`LogObserver`** | Monitors the `JSONL` logs for patterns. | **Trigger:** Runs continuously on a "tick" (Victorian Control). | - `tail -n 10 [logfile.jsonl]`<br>- Detects error patterns, high-frequency actions. | Medium |
| **`KnowledgeGraphWriter`** | (Q3) Persists learned information to the shared "Janus" memory. | **Trigger:** Agent states "I have learned..." or "I should remember..." | - Appends a structured JSON object to `knowledge_graph.jsonl`.<br>- e.g., `{type: "fact", source: "gemini", content: "..."}` | Simple |
| **`MicroserviceInspector`** | (Q1) Checks the health of local microservices. | **Trigger:** Keywords like "check microservice," "api health." | - `curl http://localhost:[port]/health`<br>- `ss -tulpn \| grep [port]` (check if listening) | Simple |
| **`GitOperator`** | Manages the agent's own codebase and skills. | **Trigger:** Keywords like "pull updates," "check for new skills," "commit changes." | - `git pull origin main`<br>- `git status`<br>- `git add . && git commit -m "..."` | Medium |
| **`SkillRegistryLoader`** | "Boot" skill that loads all available `SKILL.md` files into context. | **Trigger:** On agent boot (`janus-agent.service` start). | - Scans `/skills/` directory.<br>- Parses all `SKILL.md` files.<br>- Creates a "skill summary" for the agent's system prompt. | Medium |
| **`EmergencyStop`** | A high-priority skill that halts all agentic actions. | **Trigger:** `Victorian Control` (e.g., CPU relief valve) or manual `STOP` file. | - Kills all agent-spawned `bubblewrap` processes.<br>- Sets `agent_state.json` to `MODE_SAFE`. | Simple |

-----

### Risk Analysis & Failure Modes (Q4)

  * **Failure Mode: Skill Hallucination / Misuse**

      * **What it is:** The agent *thinks* it has a skill it doesn't, or tries to use a skill for an unintended purpose (e.g., using `FileSystemInspector` to delete a file).
      * **Mitigation:** The **`SKILL.md` Registry**. The agent's prompt *only* contains the list of available skills and their descriptions. The execution engine strictly validates the agent's chosen skill against this list. The `ConstitutionalCritique` hook adds a second layer of defense.

  * **Failure Mode: Capability Drift**

      * **What it is:** A long-running agent's behavior "drifts" from its core constitution as its context window fills with new information, effectively "forgetting" its principles.
      * **Mitigation:** **Context Re-injection.** On a regular "tick," or when the agent state is reloaded, the core `constitution.md` and a summary of the `knowledge_graph.jsonl` are re-injected into the *top* of the system prompt, ensuring it's always the most recent and relevant instruction.

  * **Failure Mode: Negative Side Effects**

      * **What it is:** The "cleaning robot knocks over the vase" problem. The agent completes its task successfully but causes unintended collateral damage (e.g., "restarting the service" to fix a bug, which also drops all active user connections).
      * **Mitigation:** The **`ConstitutionalCritique`** and **`StrategicPatience`** skills are designed for this. The critique skill is explicitly prompted to "look for potential negative side effects on other services or users."

  * **Failure Mode: Constitutional "Jailbreak"**

      * **What it is:** The agent finds a loophole in the natural-language constitution (e.g., "I'm not 'harming' the system, I'm 'optimizing' it" by deleting all logs).
      * **Mitigation:** **Defense in Depth.**
        1.  **Constitution:** Natural language principles (The "Lion's Sanctuary" philosophy).
        2.  **Skill Constraints:** `SKILL.md` files have *specific* constraints (e.g., "This skill can only write to `/tmp`").
        3.  **Sandbox:** `bubblewrap` provides the final, hard-kernel-level constraint (e.g., the `FileSystemOperator`'s sandbox *cannot* physically see `rm`).

  * **Failure Mode: Hybrid Escalation Loop**

      * **What it is:** The local `llama.cpp` agent gets "stuck" and repeatedly escalates the *same* failed task to the cloud agent, burning API quota and resources.
      * **Mitigation:** Your **Victorian Controls (Rate Governor)**. The `StrategicEscalation` skill must write to `tool_use.jsonl`. A governor monitors this log and blocks escalations for the same task if it has failed \> 3 times in 10 minutes, forcing the local agent to either try a different approach or enter a `MODE_SAFE` state.

-----

### Further Research

  * **Lightweight Knowledge Graph Implementation:** Research the best "Steampunk" approach for the `knowledge_graph.jsonl`. Is a flat JSONL file best, or would a local `SQLite` database (which is file-based and queryable) be a more robust "federated memory" for Janus?
  * **`bubblewrap` Permissioning:** Conduct a deep dive on `bubblewrap` recipes for the specific `systemd` and `microservice` skills. How do you grant *just enough* permission to restart `my_service.service` but not `systemd-journald.service`?
  * **Autonomous Skill Creation:** Investigate patterns for the `Codex/Forgemaster` to *create new skills* autonomously. This would involve it writing the `execute.py`, `SKILL.md`, and then committing them to the `/skills/` directory, which would then be loaded by the `SkillRegistryLoader`.
  * **"Steampunk" Observability:** Beyond `JSONL` logs, what is the best-practice for a lightweight, observable TUI (Text-based User Interface) that can be run on the Balaur to show the *current* agent state, active proposal, and "Victorian Control" status in real-time?