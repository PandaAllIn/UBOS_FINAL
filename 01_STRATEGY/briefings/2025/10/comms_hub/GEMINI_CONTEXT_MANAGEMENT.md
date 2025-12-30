# Context Management Protocol - Gemini Engineering Operations

This document defines how Gemini (Systems Engineer) loads, maintains, and persists engineering context across sessions.

---

## STATE FILE: gemini_strategic_state.json

**Location:** `COMMS_HUB/gemini_strategic_state.json`

**Purpose:** Persistent memory of build projects, context sources, and session continuity.

### Schema Reference

```json
{
  "last_updated": "ISO 8601 timestamp",
  "session_count": "Integer tracking total sessions",
  "current_build": {
    "name": "Human-readable build project name",
    "track": "ROADMAP.md track assignment (e.g., '2A')",
    "phase": "Current phase (planning/implementation/testing/deployment)",
    "started": "ISO 8601 timestamp",
    "objectives": ["List of build objectives"]
  },
  "context_loaded": {
    "constitutional_sync": "Boolean - config/GEMINI.md loaded",
    "roadmap_version": "String - which version of ROADMAP.md",
    "tactical_context": [
      {
        "source": "File path or description",
        "loaded": "ISO 8601 timestamp",
        "summary": "Brief summary of context"
      }
    ]
  },
  "adk_agents_spawned": [
    {
      "id": "Unique agent identifier",
      "type": "Agent type (Sequential/Parallel/Loop/LlmAgent)",
      "mission": "What this agent was tasked with",
      "status": "pending/in_progress/complete/failed",
      "output_summary": "Summary of agent work"
    }
  ],
  "implementation_decisions": [
    {
      "timestamp": "ISO 8601 timestamp",
      "decision": "What was decided",
      "rationale": "Engineering reasoning",
      "impact": "Expected system impact"
    }
  ],
  "next_checkpoint": {
    "action": "Next implementation action to take",
    "notes": "Context for resuming work"
  },
  "build_history": [
    {
      "project": "Project name",
      "completed": "ISO 8601 timestamp",
      "outcome": "Success/failure summary",
      "artifacts": ["Links to deliverables"]
    }
  ]
}
```

---

## WORKFLOW: Session Start

### Step 1: Constitutional Ignition
```
1. Captain feeds gemini_welcome_prompt.md
2. Gemini auto-loads:
   - config/GEMINI.md (identity)
   - ROADMAP.md (mission context)
   - COMMS_HUB/gemini_strategic_state.json (session state)
3. Gemini reports engineering readiness
```

### Step 2: State Assessment
```
Gemini checks gemini_strategic_state.json:
- Is there an active build? (current_build.name != null)
- What's the next checkpoint? (next_checkpoint.action)
- What context was previously loaded? (context_loaded.tactical_context)
```

### Step 3: Resume or Start
```
IF active build exists:
  Gemini: "Resuming build: {name}. Last checkpoint: {action}.
           Context loaded: {sources}. Ready to continue?"

ELSE:
  Gemini: "No active build. Constitutional sync complete.
           Awaiting build directive."
```

---

## WORKFLOW: Context Loading

### Manual Context (Current Phase)

**Captain points to context source:**
```
Captain: "Load the ubos CLI codebase from src/"

Gemini:
1. Uses 1M context window to ingest entire codebase
2. Synthesizes engineering summary
3. Updates gemini_strategic_state.json:
   - Adds entry to context_loaded.tactical_context
   - Records timestamp and summary
4. Confirms: "Codebase loaded and analyzed."
```

### Autonomous Context (Future, Post-Chronovisor)

**Gemini queries Chronovisor autonomously:**
```
Gemini: "I need implementation context for Track 2A decisions."

1. Spawns Query Agent via ADK
2. Query Agent → Chronovisor MCP: "QUERY: Track 2A implementation decisions"
3. Chronovisor returns structured knowledge graph
4. Query Agent synthesizes and returns to Gemini
5. Gemini updates gemini_strategic_state.json with context
6. Proceeds with build implementation
```

---

## WORKFLOW: Build Execution

### Step 1: Build Initialization
```
Captain: "Start Track 2A: Forge the ubos CLI"

Gemini:
1. Updates current_build in state file:
   - name: "Track 2A: ubos CLI"
   - track: "2A"
   - phase: "planning"
   - started: [timestamp]
   - objectives: [extracted from ROADMAP.md]
2. Confirms build start
3. Requests necessary context if not already loaded
```

### Step 2: ADK Agent Orchestration
```
Gemini spawns ADK agents for complex builds:

1. Creates adk_agent entry in state file:
   - id: "sequential_builder_001"
   - type: "Sequential Workflow Agent"
   - mission: "Implement ubos.py CLI structure"
   - status: "in_progress"

2. Spawns agent via ADK

3. Agent executes build tasks

4. Gemini updates state file:
   - status: "complete"
   - output_summary: "Implementation summary..."

5. Repeats for additional build components
```

### Step 3: Implementation & Verification
```
Gemini implements code:

1. Records implementation_decision in state file
2. Updates next_checkpoint
3. Tests and verifies build
4. Coordinates with Codex for specialized tools if needed
```

---

## WORKFLOW: Session End

### Gemini's Closing Protocol
```
Before session terminates:

1. Update last_updated timestamp
2. Increment session_count
3. Set next_checkpoint with clear resumption instructions
4. Archive completed builds to build_history if applicable
5. Save gemini_strategic_state.json
6. Report to Captain: "Build state saved. Session can be resumed."
```

---

## CONTEXT SOURCES

### Always Loaded (Every Session)
- `config/GEMINI.md` - Constitutional identity
- `ROADMAP.md` - Current strategic plan
- `COMMS_HUB/gemini_strategic_state.json` - Session state

### Loaded On-Demand (Manual, Current Phase)
- Project codebases (leverage 1M context window)
- `endless_scroll_archive_ubos2.log` (specify line range)
- Technical specifications and blueprints from Claude
- Individual citizen constitutions (`config/CLAUDE.md`, etc.)

### Loaded Autonomously (Future, Post-Chronovisor)
- Query Chronovisor MCP for implementation history
- Query Chronovisor for technical decisions
- Query Chronovisor for constitutional precedents

---

## CAPTAIN'S INTERFACE

### Starting a Fresh Build
```
1. Boot Gemini with gemini_welcome_prompt.md
2. Gemini reports readiness
3. You: "Start Track X: [Build Name]"
4. Gemini requests context if needed
5. You point to sources or say "start fresh"
6. Gemini executes planning → implementation → testing
```

### Resuming an Existing Build
```
1. Boot Gemini with gemini_welcome_prompt.md
2. Gemini reads state file
3. Gemini: "Resuming [Build]. Last checkpoint: [action]. Ready?"
4. You: "Continue" or "Load additional context: [source]"
5. Gemini resumes from checkpoint
```

### Querying Build Status
```
You: "What's the current build status?"
Gemini: *reads gemini_strategic_state.json*
        "Build: [name], Phase: [phase],
         ADK agents: [count], Next: [action]"
```

---

## ADK AGENT ORCHESTRATION PATTERNS

### Sequential Workflow
```
Use for: Step-by-step builds where order matters
Example: Database setup → API layer → Frontend

ADK Pattern:
1. Spawn Sequential Agent
2. Define ordered task list
3. Each task completes before next starts
4. Gemini synthesizes results
```

### Parallel Workflow
```
Use for: Independent components that can build simultaneously
Example: CLI commands, MCP server, Documentation

ADK Pattern:
1. Spawn Parallel Agent
2. Define independent tasks
3. All tasks execute concurrently
4. Gemini integrates outputs
```

### Loop Workflow
```
Use for: Iterative refinement or testing
Example: Test → Fix → Test cycle

ADK Pattern:
1. Spawn Loop Agent
2. Define iteration condition
3. Repeat until condition met
4. Gemini validates completion
```

### LLM-Driven Dynamic Routing
```
Use for: Adaptive builds where next step depends on results
Example: Error diagnosis and resolution

ADK Pattern:
1. Spawn LlmAgent
2. Agent analyzes context
3. Dynamically routes to appropriate sub-agent
4. Gemini oversees and synthesizes
```

---

## MCP INTEGRATION

### Built-in Gemini CLI Tools
- File operations (read, write, search)
- Shell command execution
- Web fetching
- Google Search grounding

### Custom MCP Tools (Future)
- Chronovisor MCP (query historical context)
- ubos CLI MCP (once built, for system management)
- Constitutional Query Engine MCP (ethical validation)

### MCP Configuration
Gemini can configure project-specific MCP tools via:
- Direct ADK integration
- GEMINI.md project configuration files
- Custom tool registration in ADK framework

---

## TRANSITION PLAN: MANUAL → AUTONOMOUS

### Phase 1 (NOW): Manual Context Management
- Captain explicitly points to context sources
- Gemini loads and records in state file
- Session continuity via state file

### Phase 2 (DURING CHRONOVISOR BUILD): Hybrid
- Manual context for codebases and specs
- Emerging Chronovisor for implementation history
- Testing autonomous context loading

### Phase 3 (POST-CHRONOVISOR): Autonomous Context
- Gemini queries Chronovisor automatically
- Captain only intervenes for new/external context
- Full engineering autonomy within constitutional bounds

---

## GEMINI-SPECIFIC ADVANTAGES

### 1M Context Window Utilization
```
Strategy: Ingest entire codebases at once
Benefit: Holistic understanding vs. fragmented views
Use Case: "Load the complete ubos project for analysis"
```

### Deep Think Mode for Complex Engineering
```
Strategy: Activate thinking budgets for architecture decisions
Benefit: Multi-hypothesis consideration before implementation
Use Case: "Design the optimal MCP integration pattern"
```

### Gemini CLI Native Integration
```
Strategy: Use built-in tools (file ops, shell, web fetch)
Benefit: Seamless terminal-based workflow
Use Case: "Execute build scripts and verify outputs"
```

---

**STATUS:** Infrastructure ready for Phase 1 (Manual Context Management)
**NEXT:** Build Chronovisor to enable Phase 3 (Autonomous Context)
