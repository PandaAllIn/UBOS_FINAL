# Context Management Protocol - Claude Strategic Operations

This document defines how Claude (Master Strategist) loads, maintains, and persists strategic context across sessions.

---

## STATE FILE: claude_strategic_state.json

**Location:** `COMMS_HUB/claude_strategic_state.json`

**Purpose:** Persistent memory of strategic campaigns, context sources, and session continuity.

### Schema Reference

```json
{
  "last_updated": "ISO 8601 timestamp",
  "session_count": "Integer tracking total sessions",
  "current_campaign": {
    "name": "Human-readable campaign name",
    "track": "ROADMAP.md track assignment (e.g., '2B')",
    "phase": "Current phase (recon/design/execution/verification)",
    "started": "ISO 8601 timestamp",
    "objectives": ["List of strategic objectives"]
  },
  "context_loaded": {
    "constitutional_sync": "Boolean - config/CLAUDE.md loaded",
    "roadmap_version": "String - which version of ROADMAP.md",
    "tactical_context": [
      {
        "source": "File path or description",
        "loaded": "ISO 8601 timestamp",
        "summary": "Brief strategic summary of context"
      }
    ]
  },
  "subagents_spawned": [
    {
      "id": "Unique agent identifier",
      "type": "Agent role (e.g., 'Ingestion Agent')",
      "mission": "What this agent was tasked with",
      "status": "pending/in_progress/complete/failed",
      "output_summary": "Strategic summary of agent findings"
    }
  ],
  "strategic_decisions": [
    {
      "timestamp": "ISO 8601 timestamp",
      "decision": "What was decided",
      "rationale": "Strategic reasoning",
      "impact": "Expected consequences"
    }
  ],
  "next_checkpoint": {
    "action": "Next strategic action to take",
    "notes": "Context for resuming work"
  },
  "campaign_history": [
    {
      "campaign": "Campaign name",
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
1. Captain feeds claude_welcome_prompt.md
2. Claude auto-loads:
   - config/CLAUDE.md (identity)
   - ROADMAP.md (mission context)
   - COMMS_HUB/claude_strategic_state.json (session state)
3. Claude reports strategic readiness
```

### Step 2: State Assessment
```
Claude checks claude_strategic_state.json:
- Is there an active campaign? (current_campaign.name != null)
- What's the next checkpoint? (next_checkpoint.action)
- What context was previously loaded? (context_loaded.tactical_context)
```

### Step 3: Resume or Start
```
IF active campaign exists:
  Claude: "Resuming campaign: {name}. Last checkpoint: {action}.
           Context loaded: {sources}. Ready to continue?"

ELSE:
  Claude: "No active campaign. Constitutional sync complete.
           Awaiting strategic directive."
```

---

## WORKFLOW: Context Loading

### Manual Context (Current Phase)

**Captain points to context source:**
```
Captain: "Load the final 4000 lines of endless_scroll_archive_ubos2.log"

Claude:
1. Reads the specified source
2. Synthesizes strategic summary
3. Updates claude_strategic_state.json:
   - Adds entry to context_loaded.tactical_context
   - Records timestamp and summary
4. Confirms: "Context loaded and integrated."
```

### Autonomous Context (Future, Post-Chronovisor)

**Claude queries Chronovisor autonomously:**
```
Claude: "I need historical context on Genesis Protocol design."

1. Spawns Query Agent via Agent SDK
2. Query Agent → Chronovisor MCP: "QUERY: Genesis Protocol decisions"
3. Chronovisor returns structured knowledge graph
4. Query Agent synthesizes and returns to Claude
5. Claude updates claude_strategic_state.json with context
6. Proceeds with strategic analysis
```

---

## WORKFLOW: Campaign Execution

### Step 1: Campaign Initialization
```
Captain: "Start Track 2B: Forge the Chronovisor"

Claude:
1. Updates current_campaign in state file:
   - name: "Track 2B: Chronovisor Design"
   - track: "2B"
   - phase: "reconnaissance"
   - started: [timestamp]
   - objectives: [extracted from ROADMAP.md]
2. Confirms campaign start
3. Requests necessary context if not already loaded
```

### Step 2: Sub-Agent Orchestration
```
Claude spawns specialist agents:

1. Creates subagent entry in state file:
   - id: "ingestion_agent_001"
   - type: "Ingestion Agent"
   - mission: "Analyze endless_scroll.log structure"
   - status: "in_progress"

2. Spawns agent via Agent SDK

3. Agent returns findings

4. Claude updates state file:
   - status: "complete"
   - output_summary: "Strategic summary..."

5. Repeats for additional agents
```

### Step 3: Strategic Synthesis
```
Claude synthesizes all sub-agent outputs:

1. Records strategic_decision in state file
2. Updates next_checkpoint
3. Generates blueprint/plan
4. Delegates implementation to Codex
```

---

## WORKFLOW: Session End

### Claude's Closing Protocol
```
Before session terminates:

1. Update last_updated timestamp
2. Increment session_count
3. Set next_checkpoint with clear resumption instructions
4. Archive completed campaigns to campaign_history if applicable
5. Save claude_strategic_state.json
6. Report to Captain: "Strategic state saved. Session can be resumed."
```

---

## CONTEXT SOURCES

### Always Loaded (Every Session)
- `config/CLAUDE.md` - Constitutional identity
- `ROADMAP.md` - Current strategic plan
- `COMMS_HUB/claude_strategic_state.json` - Session state

### Loaded On-Demand (Manual, Current Phase)
- `endless_scroll_archive_ubos2.log` (specify line range)
- `GENESIS_PROTOCOL/*` artifacts
- Individual citizen constitutions (`config/GEMINI.md`, etc.)
- Project-specific documentation

### Loaded Autonomously (Future, Post-Chronovisor)
- Query Chronovisor MCP for historical decisions
- Query Chronovisor for pattern analysis
- Query Chronovisor for constitutional precedents

---

## CAPTAIN'S INTERFACE

### Starting a Fresh Campaign
```
1. Boot Claude with claude_welcome_prompt.md
2. Claude reports readiness
3. You: "Start Track X: [Campaign Name]"
4. Claude requests context if needed
5. You point to sources or say "start fresh"
6. Claude executes reconnaissance → design → delegation
```

### Resuming an Existing Campaign
```
1. Boot Claude with claude_welcome_prompt.md
2. Claude reads state file
3. Claude: "Resuming [Campaign]. Last checkpoint: [action]. Ready?"
4. You: "Continue" or "Load additional context: [source]"
5. Claude resumes from checkpoint
```

### Querying Strategic State
```
You: "What's the current campaign status?"
Claude: *reads claude_strategic_state.json*
        "Campaign: [name], Phase: [phase],
         Sub-agents: [count], Next: [action]"
```

---

## TRANSITION PLAN: MANUAL → AUTONOMOUS

### Phase 1 (NOW): Manual Context Management
- Captain explicitly points to context sources
- Claude loads and records in state file
- Session continuity via state file

### Phase 2 (DURING CHRONOVISOR BUILD): Hybrid
- Manual context for historical logs
- Emerging Chronovisor for structured queries
- Testing autonomous context loading

### Phase 3 (POST-CHRONOVISOR): Autonomous Context
- Claude queries Chronovisor automatically
- Captain only intervenes for new/external context
- Full strategic autonomy within constitutional bounds

---

**STATUS:** Infrastructure ready for Phase 1 (Manual Context Management)
**NEXT:** Build Chronovisor to enable Phase 3 (Autonomous Context)
