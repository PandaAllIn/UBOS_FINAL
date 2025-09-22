# UBOS Agents

Operational agents implementing UBOS philosophy for strategic intelligence and system automation.

## Available Agents

### 🧠 Master Librarian Agent
Foundational knowledge consultant that ingests every UBOS book, maintains the knowledge graph, analyses patterns, and offers UBOS-aligned guidance.

**Location:** `KnowledgeAgent/MasterLibrarianAgent/`

**Features:**
- Parses the structured book corpus into unified `Concept` records
- Builds/refreshes the UBOS knowledge graph (NetworkX)
- Pattern Engine ranks relevant concepts and flags conflicts
- Consultation Service merges heuristics with Gemini 2.5 Pro (if configured)
- Mermaid visualisation utility for concept diagrams
- Flask API + CLI interface for direct terminal use

**Quick Usage:**
```bash
cd KnowledgeAgent/MasterLibrarianAgent

PYTHONPATH=. python3 -m master_librarian.cli \
  "Design a system for onboarding new remote hires" \
  --objective "Maintain culture" \
  --context "Distributed team" \
  --mermaid

# or run the API
PYTHONPATH=. python3 -m flask --app master_librarian.api.app:create_app run
```

### 🔍 UBOS Research Agent
Strategic intelligence gathering powered by Perplexity Sonar API with comprehensive archive system.

**Location:** `ResearchAgent/`

**Features:**
- Intelligent model selection based on query complexity
- Automatic research archiving in AI-friendly formats (YAML, JSON, Markdown)
- Advanced search and retrieval system
- Multiple output formats and CLI interfaces
- Embodies UBOS pause-before-response principle
- Topic-based organization and indexing

**Quick Usage:**
```bash
cd ResearchAgent/

# Research commands
python ubos_research_agent.py quick "AI trends"
python ubos_research_agent.py deep "comprehensive analysis"

# Archive management
python research_cli.py list
python research_cli.py search --topics ai_agents
python research_cli.py export --topic architecture --output insights.json
```

**Archive Structure:**
```
ResearchAgent/
├── research_archive/
│   ├── by_date/          # Organized by research date
│   ├── by_topic/         # Symlinked by topic
│   └── indices/          # Master indexes and aggregates
├── ubos_research_agent.py
├── research_storage.py
├── research_cli.py
└── README.md
```

See `ResearchAgent/README.md` for complete documentation.

## Agent Architecture

All UBOS agents follow these principles:
- **Independence**: Each agent operates autonomously
- **Interoperability**: Standard interfaces for agent-to-agent communication
- **Philosophy Alignment**: Embody UBOS systems-thinking approach
- **Strategic Operation**: Pause-analyze-respond patterns

## Agent Workflow Blueprint

```
User Task/Query
   ↓
AI Prime Agent (orchestrator – planned next)
   ↓ (always consult)
   ├─ Master Librarian Agent → strategic concepts + diagram request
   └─ Mermaid Agent (MCP) → diagram rendering
   ↓ (conditional)
   ├─ Research Agent (Perplexity Sonar)
   └─ Context7 Agent (MCP tech docs)
   ↓ (if complexity requires)
      Specification Agent (SpecKit)
   ↓
Implementation Agent (Codex CLI)
   ↓
Results fed back to Librarian for knowledge updates
```

## Next Agents to Build

1. **AI Prime Agent** – orchestrator coordinating consultations, research, specs, and implementation handoffs.
2. **Mermaid Agent** – MCP wrapper so Prime can request diagrams without embedding Mermaid logic.
3. **Context7 Agent** – utility layer for technical documentation retrieval via Context7 MCP.
4. **Specification Agent** – SpecKit automation for complex tasks.
5. **Implementation Agent** – standard Codex CLI wrapper (workspace-write sandbox, on-request approvals).
