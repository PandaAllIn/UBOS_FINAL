# UBOS Research Agent

A strategic intelligence gathering agent powered by Perplexity's Sonar API, embodying UBOS philosophical principles.

## Philosophy Integration

The agent implements core UBOS principles:
- **Pause Before Response**: Analyzes query complexity before model selection
- **Systems Over Willpower**: Structured approach to research with automatic optimization
- **Strategic Thinking**: Intelligent model selection based on task requirements
- **Tactical Adaptability**: Error handling and graceful degradation

## Installation

```bash
cd /Users/apple/Desktop/UBOS_FINAL/UBOS/Agents/ResearchAgent
pip install -r requirements.txt
```

## Usage

### Command Line Interface

```bash
# Quick research (uses Sonar base model)
python ubos_research_agent.py quick "AI agent architecture trends"

# Deep research (uses Sonar Deep Research model)
python ubos_research_agent.py deep "comprehensive analysis of knowledge graphs"

# Reasoning research (uses Sonar Reasoning model)
python ubos_research_agent.py reason "why are graph databases better for AI systems"

# Pro research (uses Sonar Pro model)
python ubos_research_agent.py pro "strategic analysis of AI market opportunities"

# Using CLI wrapper
./ubos_research_cli.sh quick "research query"
```

### Advanced Options

```bash
# Force specific model
python ubos_research_agent.py quick "query" --model sonar-pro

# Different output formats
python ubos_research_agent.py quick "query" --format json
python ubos_research_agent.py quick "query" --format yaml

# Control research depth
python ubos_research_agent.py quick "query" --depth deep
```

### Research Archive Management

```bash
# List recent research
./ubos_research_cli.sh list --limit 20

# Search research by topic
./ubos_research_cli.sh search --topics ai_agents architecture

# Search by query
./ubos_research_cli.sh search --query "knowledge graphs"

# Show detailed research
./ubos_research_cli.sh show research-20250921-140530-ai-trends

# Archive statistics
./ubos_research_cli.sh stats

# Export insights for AI consumption
./ubos_research_cli.sh export --topic ai_agents --output insights.json
```

### Programmatic Usage

```python
from ubos_research_agent import UBOSResearchAgent
from research_storage import ResearchDocumentStorage

# Initialize agent
agent = UBOSResearchAgent()

# Perform research (automatically saved)
result = agent.research(
    query="AI agent best practices",
    model="sonar-pro",  # Optional - auto-selected if not specified
    format_output="json",
    depth="deep"
)

# Access research archive
storage = ResearchDocumentStorage()
recent_research = storage.search_research(topics=['ai_agents'], limit=10)
insights = storage.extract_insights_for_ai([r['id'] for r in recent_research])

print(result)
```

## Model Selection Logic

The agent automatically selects the optimal Sonar model based on query analysis:

| Complexity Score | Query Characteristics | Recommended Model |
|-----------------|----------------------|-------------------|
| 0-1 | Simple, factual queries | `sonar` |
| 2-3 | Complex analysis needed | `sonar-pro` |
| 4+ | Comprehensive research | `sonar-deep-research` |
| Any + reasoning terms | Contains why/how/explain | `sonar-reasoning` or `sonar-reasoning-pro` |

## AI Agent Integration

### REST API Mode (Future Enhancement)
```python
# For other AI agents to consume
import requests

response = requests.post('http://localhost:8000/research', json={
    'query': 'research topic',
    'model': 'sonar-pro',
    'format': 'json'
})
```

### Direct Python Integration
```python
from ubos_research_agent import UBOSResearchAgent

class MyAIAgent:
    def __init__(self):
        self.research_agent = UBOSResearchAgent()

    def gather_intelligence(self, topic):
        return self.research_agent.research(
            query=f"latest developments in {topic}",
            format_output="json"
        )
```

## Configuration

The agent uses these default settings:
- **API Key**: Set via PERPLEXITY_API_KEY environment variable
- **Max Tokens**: 4000
- **Temperature**: 0.2 (focused, consistent responses)
- **Top P**: 0.9

## Error Handling

The agent implements UBOS resilience principles:
- Graceful error handling with helpful suggestions
- Automatic retry logic (future enhancement)
- Detailed error reporting for debugging

## Output Formats

### Text Format (Default)
Human-readable format with clear sections for findings, sources, and usage statistics.

### JSON Format
Structured data perfect for AI agent consumption:
```json
{
  "query_analysis": {...},
  "content": "research results",
  "citations": [...],
  "model_used": "sonar-pro",
  "usage": {...},
  "timestamp": 1234567890
}
```

### YAML Format
Configuration-friendly format for system integration.

## Integration with Other UBOS Agents

This research agent serves as the intelligence foundation for other UBOS agents:

1. **Master Knowledge Agent** - Consumes research for pattern analysis
2. **Specification Agent** - Uses research to inform spec generation
3. **Implementation Agent** - References research for best practices

## Future Enhancements

- [ ] REST API server mode
- [ ] Caching for repeated queries
- [ ] Batch research processing
- [ ] Integration with UBOS knowledge graph
- [ ] Webhook support for async research
- [ ] Advanced query preprocessing
- [ ] Multi-language support

## Philosophy Alignment

This agent embodies the UBOS approach from Book 2, Chapter 4:
- **Strategic Starting Point**: Intelligent model selection
- **High-Leverage Actions**: Optimal resource utilization
- **System Integration**: Designed for agent ecosystem collaboration
- **Feedback Loops**: Usage tracking for continuous improvement
