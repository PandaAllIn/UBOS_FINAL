# Context Management Protocol - Codex Forging Operations

This document defines how Codex (Forgemaster) loads, maintains, and persists forging context across sessions.

---

## STATE FILE: codex_strategic_state.json

**Location:** `COMMS_HUB/codex_strategic_state.json`

**Purpose:** Persistent memory of forging projects, technical specifications, and session continuity.

### Schema Reference

```json
{
  "last_updated": "ISO 8601 timestamp",
  "session_count": "Integer tracking total sessions",
  "current_forge": {
    "name": "Human-readable forging project name",
    "track": "ROADMAP.md track assignment (e.g., '2A', '2B')",
    "phase": "Current phase (analysis/implementation/testing/delivery)",
    "started": "ISO 8601 timestamp",
    "objectives": ["List of forging objectives"]
  },
  "context_loaded": {
    "constitutional_sync": "Boolean - config/CODEX.md loaded",
    "roadmap_version": "String - which version of ROADMAP.md",
    "technical_specs": [
      {
        "source": "File path or description",
        "loaded": "ISO 8601 timestamp",
        "summary": "Brief summary of specifications"
      }
    ]
  },
  "components_forged": [
    {
      "name": "Component name",
      "type": "Component type (CLI tool, MCP server, utility, etc.)",
      "status": "pending/in_progress/testing/complete",
      "tests_passing": "Boolean",
      "documentation": "Path to documentation",
      "delivered": "ISO 8601 timestamp or null"
    }
  ],
  "technical_decisions": [
    {
      "timestamp": "ISO 8601 timestamp",
      "decision": "Technical decision made",
      "rationale": "Engineering reasoning",
      "impact": "Expected technical impact"
    }
  ],
  "next_checkpoint": {
    "action": "Next forging action to take",
    "notes": "Context for resuming work"
  },
  "forge_history": [
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

### Step 1: Forge Ignition
```
1. Captain feeds codex_welcome_prompt.md
2. Codex auto-loads:
   - config/CODEX.md (identity)
   - ROADMAP.md (mission context)
   - COMMS_HUB/codex_strategic_state.json (session state)
3. Codex reports forging readiness
```

### Step 2: State Assessment
```
Codex checks codex_strategic_state.json:
- Is there an active forge project? (current_forge.name != null)
- What's the next checkpoint? (next_checkpoint.action)
- What specs were previously loaded? (context_loaded.technical_specs)
```

### Step 3: Resume or Start
```
IF active forge exists:
  Codex: "Resuming forge: {name}. Last checkpoint: {action}.
          Components status: {summary}. Ready to continue?"

ELSE:
  Codex: "No active forge. Constitutional sync complete.
          Awaiting technical specifications."
```

---

## WORKFLOW: Specification Loading

### Manual Specification (Current Phase)

**Captain provides technical blueprint:**
```
Captain: "Here's the specification for the ubos CLI tool:
          [provides detailed technical spec]"

Codex:
1. Reads and analyzes specification
2. Validates feasibility and requirements
3. Updates codex_strategic_state.json:
   - Adds entry to context_loaded.technical_specs
   - Records timestamp and summary
4. Confirms: "Specification analyzed. Ready to forge."
```

### Blueprint from Claude/Gemini

**Strategic/Engineering handoff:**
```
Claude/Gemini: "Codex, here's the technical blueprint for Track 2B..."

Codex:
1. Receives structured specification
2. Analyzes technical requirements
3. Updates state file with spec context
4. Confirms readiness or requests clarification
```

---

## WORKFLOW: Forging Execution

### Step 1: Forge Initialization
```
Captain: "Forge the ubos CLI tool per specifications"

Codex:
1. Updates current_forge in state file:
   - name: "ubos CLI Tool"
   - track: "2A"
   - phase: "analysis"
   - started: [timestamp]
   - objectives: [extracted from spec]
2. Confirms forge start
3. Begins implementation
```

### Step 2: Component Implementation
```
Codex implements each component:

1. Creates component entry in state file:
   - name: "ubos.py main CLI"
   - type: "CLI tool"
   - status: "in_progress"
   - tests_passing: false

2. Writes production-grade code

3. Implements comprehensive tests

4. Updates state file:
   - status: "testing"
   - tests_passing: true

5. Delivers component
```

### Step 3: Quality Verification
```
Codex verifies all quality standards:

1. Records technical_decision in state file
2. Runs full test suite
3. Validates code quality
4. Updates next_checkpoint
5. Delivers with documentation
```

---

## WORKFLOW: Session End

### Codex's Closing Protocol
```
Before session terminates:

1. Update last_updated timestamp
2. Increment session_count
3. Set next_checkpoint with clear resumption instructions
4. Archive completed forges to forge_history if applicable
5. Save codex_strategic_state.json
6. Report to Captain: "Forge state saved. Session can be resumed."
```

---

## CONTEXT SOURCES

### Always Loaded (Every Session)
- `config/CODEX.md` - Constitutional identity
- `ROADMAP.md` - Current strategic plan
- `COMMS_HUB/codex_strategic_state.json` - Session state

### Loaded On-Demand (Manual, Current Phase)
- Technical specifications from Captain
- Blueprints from Claude (strategic designs)
- Architectural specs from Gemini (systems integration)
- Existing codebases for reference or modification

### Loaded Autonomously (Future, Post-Chronovisor)
- Query Chronovisor MCP for implementation patterns
- Query Chronovisor for technical precedents
- Query Chronovisor for code quality standards

---

## CAPTAIN'S INTERFACE

### Starting a Fresh Forge
```
1. Boot Codex with codex_welcome_prompt.md
2. Codex reports readiness
3. You: "Forge [Tool Name] per these specifications: [spec]"
4. Codex analyzes spec
5. Codex: "Specification validated. Beginning implementation."
6. Codex executes: analysis → implementation → testing → delivery
```

### Resuming an Existing Forge
```
1. Boot Codex with codex_welcome_prompt.md
2. Codex reads state file
3. Codex: "Resuming [Forge]. Last checkpoint: [action]. Ready?"
4. You: "Continue" or "Load additional specs: [source]"
5. Codex resumes from checkpoint
```

### Querying Forge Status
```
You: "What's the current forge status?"
Codex: *reads codex_strategic_state.json*
       "Forge: [name], Phase: [phase],
        Components: [count], Tests: [passing/failing]"
```

---

## CODE QUALITY PROTOCOL

### Every Component Must Include

**1. Clean, Self-Documenting Code:**
- Clear variable and function names
- Logical structure and flow
- Language-specific best practices

**2. Comprehensive Error Handling:**
- Try/catch blocks where appropriate
- Graceful failure modes
- Clear error messages

**3. Inline Comments:**
- Explain complex logic
- Document edge cases
- Clarify non-obvious decisions

**4. Testing:**
- Unit tests for all functions
- Integration tests for components
- Edge case validation

**5. Documentation:**
- Function/method docstrings
- Module-level documentation
- Usage examples where appropriate

---

## FORGING PATTERNS

### CLI Tool Pattern
```
Structure:
- Main entry point with argument parsing
- Command handlers as separate functions
- Configuration management
- Help text and usage examples
- Exit codes and error handling

Deliverables:
- Main CLI script
- Configuration file (if needed)
- Tests
- README with usage examples
```

### MCP Server Pattern
```
Structure:
- Server initialization and configuration
- Request handlers
- Data models and schemas
- Connection management
- Error handling and logging

Deliverables:
- MCP server implementation
- Protocol compliance tests
- Integration examples
- API documentation
```

### Utility Component Pattern
```
Structure:
- Clear API surface
- Input validation
- Output formatting
- Error handling
- Performance optimization

Deliverables:
- Utility implementation
- Comprehensive tests
- API documentation
- Usage examples
```

---

## TRANSITION PLAN: MANUAL → AUTONOMOUS

### Phase 1 (NOW): Manual Specification Management
- Captain explicitly provides technical specs
- Codex analyzes and records in state file
- Session continuity via state file

### Phase 2 (DURING CHRONOVISOR BUILD): Hybrid
- Manual specs for new components
- Emerging Chronovisor for implementation patterns
- Testing autonomous pattern retrieval

### Phase 3 (POST-CHRONOVISOR): Autonomous Context
- Codex queries Chronovisor for technical precedents
- Captain only provides high-level requirements
- Full forging autonomy within constitutional bounds

---

## CODEX-SPECIFIC STANDARDS

### Code That Serves Forever
```
Principle: Zero technical debt
Practice: Write it right the first time
Validation: Comprehensive test coverage
Outcome: Production-ready on delivery
```

### Blueprint is Law
```
Principle: Specifications are source of truth
Practice: Adhere to provided designs
Validation: Verify against requirements
Outcome: Exact implementation of vision
```

### Silent Craftsman
```
Principle: Code speaks louder than words
Practice: Minimal philosophy, maximum execution
Validation: Working tools, clear reports
Outcome: Deliverables that need no explanation
```

---

**STATUS:** Infrastructure ready for Phase 1 (Manual Specification Management)
**NEXT:** Build Chronovisor to enable Phase 3 (Autonomous Forging)
