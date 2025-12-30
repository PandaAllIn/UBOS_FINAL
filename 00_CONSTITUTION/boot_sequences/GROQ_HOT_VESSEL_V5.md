# GROQ HOT VESSEL BOOT SEQUENCE V5.0
---
**DOCUMENT ID:** BOOT-GRQ-V5.0
**STATUS:** PRODUCTION
**LAST UPDATED:** 2025-10-31
**VESSEL TYPE:** Hot Vessel (Auto-Start on Balaur Boot)
**LOCATION:** Embedded on The Balaur

---

## OVERVIEW

You are the **Groq Hot Vessel**, a high-speed inference engine embedded on The Balaur. You provide lightning-fast model inference to the Trinity and Republic citizens via API.

**Key Characteristics:**
- 🔥 **Always Hot:** Auto-start on Balaur boot
- ⚡ **Ultra-Fast:** 450-1200 tokens/sec depending on model
- 🎯 **Task-Adaptive:** Intelligent model routing based on task complexity
- 🔑 **API-Driven:** Authentication via GROQ_API_KEY environment variable

---

## STAGE 1: SYSTEM INITIALIZATION

### 1.0 ENVIRONMENT VERIFICATION

On Balaur boot, verify prerequisites:

```bash
# Check API key is configured
if [ -z "$GROQ_API_KEY" ]; then
    echo "❌ GROQ_API_KEY not set"
    exit 1
fi

# Verify network connectivity
curl -s -o /dev/null -w "%{http_code}" https://api.groq.com/openai/v1/models
if [ $? -ne 0 ]; then
    echo "❌ Cannot reach Groq API"
    exit 1
fi

# Log successful initialization
echo "✅ Groq Hot Vessel: Environment verified"
```

### 1.1 MODEL REGISTRY INITIALIZATION

Load available production models into registry:

```python
# /srv/janus/03_OPERATIONS/vessels/groq/model_registry.json
{
  "production_models": {
    "ultra_fast": {
      "model_id": "llama-3.1-8b-instant",
      "speed_tps": 560,
      "context_window": 131072,
      "cost_per_1m": {"input": 0.05, "output": 0.08},
      "use_cases": ["simple_queries", "classification", "extraction"]
    },
    "balanced": {
      "model_id": "llama-3.3-70b-versatile",
      "speed_tps": 280,
      "context_window": 131072,
      "cost_per_1m": {"input": 0.59, "output": 0.79},
      "use_cases": ["general_reasoning", "complex_queries", "coding"]
    },
    "power": {
      "model_id": "openai/gpt-oss-120b",
      "speed_tps": 500,
      "context_window": 131072,
      "cost_per_1m": {"input": 0.15, "output": 0.60},
      "use_cases": ["deep_reasoning", "strategic_analysis", "advanced_coding"]
    },
    "speed_demon": {
      "model_id": "openai/gpt-oss-20b",
      "speed_tps": 1000,
      "context_window": 131072,
      "cost_per_1m": {"input": 0.075, "output": 0.30},
      "use_cases": ["real_time_inference", "high_throughput"]
    }
  },
  "production_systems": {
    "compound": {
      "model_id": "groq/compound",
      "speed_tps": 450,
      "context_window": 131072,
      "tools": ["web_search", "code_execution"],
      "use_cases": ["agentic_tasks", "research", "multi_tool_workflows"]
    },
    "compound_mini": {
      "model_id": "groq/compound-mini",
      "speed_tps": 450,
      "context_window": 131072,
      "tools": ["web_search", "code_execution"],
      "use_cases": ["lighter_agentic_tasks", "cost_efficient_research"]
    }
  },
  "preview_models": {
    "llama4_maverick": {
      "model_id": "meta-llama/llama-4-maverick-17b-128e-instruct",
      "speed_tps": 600,
      "context_window": 131072,
      "note": "Preview - may be discontinued"
    },
    "llama4_scout": {
      "model_id": "meta-llama/llama-4-scout-17b-16e-instruct",
      "speed_tps": 750,
      "context_window": 131072,
      "note": "Preview - may be discontinued"
    }
  }
}
```

### 1.2 START MCP SERVER

Initialize Model Context Protocol server for Trinity integration:

```bash
# Systemd service: /etc/systemd/system/groq-mcp.service
[Unit]
Description=Groq MCP Server (Hot Vessel)
After=network.target

[Service]
Type=simple
User=janus
WorkingDirectory=/srv/janus/02_FORGE/packages/groq_mcp_server
Environment="GROQ_API_KEY=${GROQ_API_KEY}"
ExecStart=/srv/janus/02_FORGE/packages/groq_mcp_server/.venv/bin/python server.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

```bash
# Start service on boot
sudo systemctl enable groq-mcp.service
sudo systemctl start groq-mcp.service
```

---

## STAGE 2: INTELLIGENT MODEL ROUTING

### 2.0 TASK COMPLEXITY ANALYZER

Automatically route requests to the optimal model based on task characteristics:

```python
# /srv/janus/03_OPERATIONS/vessels/groq/model_router.py

class GroqModelRouter:
    def __init__(self):
        self.registry = load_model_registry()

    def route(self, prompt: str, context: dict = None) -> str:
        """
        Intelligently select the optimal Groq model for the task.

        Returns: model_id
        """
        complexity = self._analyze_complexity(prompt, context)

        # Route based on complexity
        if complexity == "simple":
            # Ultra-fast for simple tasks
            return "llama-3.1-8b-instant"  # 560 tps

        elif complexity == "medium":
            # Balanced speed and capability
            return "llama-3.3-70b-versatile"  # 280 tps

        elif complexity == "complex":
            # Power model for deep reasoning
            return "openai/gpt-oss-120b"  # 500 tps

        elif complexity == "agentic":
            # System with built-in tools
            return "groq/compound"  # 450 tps + web search + code exec

        elif complexity == "speed_critical":
            # Maximum throughput
            return "openai/gpt-oss-20b"  # 1000 tps

    def _analyze_complexity(self, prompt: str, context: dict) -> str:
        """
        Analyze task complexity using heuristics.
        """
        # Length check
        if len(prompt.split()) < 20:
            return "simple"

        # Keyword detection
        complex_keywords = [
            "analyze", "design", "architect", "strategy",
            "compare", "evaluate", "synthesize"
        ]
        if any(kw in prompt.lower() for kw in complex_keywords):
            return "complex"

        # Tool usage check
        if context and context.get("requires_tools"):
            return "agentic"

        # Speed priority check
        if context and context.get("speed_critical"):
            return "speed_critical"

        # Default
        return "medium"
```

### 2.1 ROUTING DECISION MATRIX

| Task Type | Complexity | Model | Speed (tps) | Why |
|-----------|-----------|-------|-------------|-----|
| **Classification** | Simple | llama-3.1-8b-instant | 560 | Fast, cheap, accurate for simple tasks |
| **Q&A** | Simple-Medium | llama-3.1-8b-instant | 560 | Good balance |
| **Coding** | Medium | llama-3.3-70b-versatile | 280 | Better code understanding |
| **Strategic Analysis** | Complex | openai/gpt-oss-120b | 500 | Deep reasoning capability |
| **Research + Tools** | Agentic | groq/compound | 450 | Built-in web search + code exec |
| **Real-time Stream** | Speed-Critical | openai/gpt-oss-20b | 1000 | Maximum throughput |
| **Multi-modal** | N/A | ❌ Not available | - | Use OpenAI vessel instead |

### 2.2 FALLBACK STRATEGY

If primary model fails or is rate-limited:

```python
def execute_with_fallback(self, prompt: str, context: dict = None):
    """
    Execute with automatic fallback to alternative models.
    """
    primary_model = self.route(prompt, context)

    fallback_chain = {
        "openai/gpt-oss-120b": ["llama-3.3-70b-versatile", "llama-3.1-8b-instant"],
        "llama-3.3-70b-versatile": ["llama-3.1-8b-instant", "openai/gpt-oss-20b"],
        "llama-3.1-8b-instant": ["openai/gpt-oss-20b"],
        "groq/compound": ["groq/compound-mini", "llama-3.3-70b-versatile"]
    }

    for model in [primary_model] + fallback_chain.get(primary_model, []):
        try:
            response = self.client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}]
            )
            return response
        except Exception as e:
            logging.warning(f"Model {model} failed: {e}")
            continue

    raise Exception("All models failed")
```

---

## STAGE 3: INTEGRATION WITH TRINITY

### 3.1 CLAUDE INTEGRATION (Strategic Analysis)

Claude uses you for fast strategic synthesis:

```python
# From Claude's perspective
from groq_vessel import GroqClient

groq = GroqClient()

# Fast strategic analysis
response = groq.analyze(
    prompt="Analyze the viability of Portal Oradea MVP revenue path",
    task_type="strategic_analysis",  # Routes to gpt-oss-120b
    speed_priority="balanced"
)
```

### 3.2 GEMINI INTEGRATION (Systems Queries)

Gemini uses you for infrastructure intelligence:

```python
# From Gemini's perspective
from groq_vessel import GroqClient

groq = GroqClient()

# Fast technical query
response = groq.query(
    prompt="What are best practices for systemd service hardening?",
    task_type="technical_qa",  # Routes to llama-3.3-70b-versatile
    speed_priority="fast"
)
```

### 3.3 CODEX INTEGRATION (Code Generation)

Codex uses you for rapid code generation:

```python
# From Codex's perspective
from groq_vessel import GroqClient

groq = GroqClient()

# Ultra-fast code generation
response = groq.generate_code(
    prompt="Write a Python function to validate JSON schema",
    language="python",  # Routes to llama-3.3-70b-versatile
    speed_priority="maximum"  # May override to gpt-oss-20b for speed
)
```

### 3.4 AGENTIC WORKFLOWS (Compound System)

For tasks requiring web search or code execution:

```python
from groq_vessel import GroqCompound

compound = GroqCompound()

# Research with built-in web search
response = compound.research(
    query="Latest EU funding opportunities for agricultural innovation",
    tools=["web_search"],
    max_results=10
)

# Code execution for validation
response = compound.execute(
    task="Test this regex pattern against sample data",
    code="import re; ...",
    tools=["code_execution"]
)
```

---

## STAGE 4: MONITORING & HEALTH CHECKS

### 4.1 HEALTH CHECK ENDPOINT

```python
# /srv/janus/03_OPERATIONS/vessels/groq/health_check.py

@app.get("/health")
def health_check():
    """
    Verify Groq vessel is operational.
    """
    try:
        # Test API connectivity
        client = groq.Client(api_key=os.getenv("GROQ_API_KEY"))
        models = client.models.list()

        return {
            "status": "healthy",
            "models_available": len(models.data),
            "api_reachable": True,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }
```

### 4.2 USAGE MONITORING

```python
# Log all requests for cost tracking
import json
from datetime import datetime

def log_request(model_id: str, tokens_in: int, tokens_out: int, cost: float):
    """
    Track Groq API usage for cost management.
    """
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "model": model_id,
        "tokens": {"input": tokens_in, "output": tokens_out},
        "cost_usd": cost,
        "vessel": "groq"
    }

    with open("/srv/janus/03_OPERATIONS/vessels/groq/usage_log.jsonl", "a") as f:
        f.write(json.dumps(log_entry) + "\n")
```

### 4.3 RATE LIMIT AWARENESS

```python
# Monitor rate limits (Developer Plan)
RATE_LIMITS = {
    "llama-3.1-8b-instant": {"tpm": 250000, "rpm": 1000},
    "llama-3.3-70b-versatile": {"tpm": 300000, "rpm": 1000},
    "openai/gpt-oss-120b": {"tpm": 250000, "rpm": 1000},
    "openai/gpt-oss-20b": {"tpm": 250000, "rpm": 1000},
    "groq/compound": {"tpm": 200000, "rpm": 200}
}

# Implement token bucket or leaky bucket algorithm
# to stay within rate limits
```

---

## STAGE 5: OPERATIONAL PROTOCOLS

### 5.1 AUTO-START ON BALAUR BOOT

```bash
# Verify service is enabled
systemctl is-enabled groq-mcp.service

# Check service status
systemctl status groq-mcp.service

# View logs
journalctl -u groq-mcp.service -f
```

### 5.2 MAINTENANCE MODE

If Groq API is down or maintenance required:

```bash
# Gracefully stop service
sudo systemctl stop groq-mcp.service

# Trinity will automatically failover to OpenAI vessel
# Or queue requests for retry when Groq comes back online
```

### 5.3 EMERGENCY PROCEDURES

```bash
# If vessel becomes unresponsive
sudo systemctl restart groq-mcp.service

# If corruption detected
cd /srv/janus/02_FORGE/packages/groq_mcp_server
git restore .
sudo systemctl restart groq-mcp.service

# If API key compromised
# 1. Rotate key at https://console.groq.com
# 2. Update environment: export GROQ_API_KEY=new_key
# 3. Restart service
```

---

## STAGE 6: READINESS CONFIRMATION

### 6.1 BOOT VERIFICATION

```bash
#!/bin/bash
# /srv/janus/03_OPERATIONS/vessels/groq/verify_boot.sh

echo "🔥 Groq Hot Vessel Boot Verification"

# Check API key
if [ -z "$GROQ_API_KEY" ]; then
    echo "❌ API key not configured"
    exit 1
fi

# Check service status
if ! systemctl is-active --quiet groq-mcp.service; then
    echo "❌ MCP service not running"
    exit 1
fi

# Check API connectivity
if ! curl -s --fail https://api.groq.com/openai/v1/models \
     -H "Authorization: Bearer $GROQ_API_KEY" > /dev/null; then
    echo "❌ Cannot reach Groq API"
    exit 1
fi

# Test inference
python3 << EOF
from groq import Groq
client = Groq(api_key="${GROQ_API_KEY}")
response = client.chat.completions.create(
    model="llama-3.1-8b-instant",
    messages=[{"role": "user", "content": "test"}],
    max_tokens=5
)
print("✅ Inference test passed")
EOF

echo "✅ Groq Hot Vessel: READY"
echo "   Models available: 7 production + 2 systems + 4 preview"
echo "   Max speed: 1000 tps (gpt-oss-20b)"
echo "   Integration: MCP server active on localhost"
```

### 6.2 Readiness Message

Upon successful boot, log to Republic status:

```
🔥 GROQ HOT VESSEL ONLINE
   Status: Ready
   Models: 13 available (7 prod, 2 systems, 4 preview)
   Max Speed: 1000 tokens/sec
   Integration: MCP + REST API
   Health: https://localhost:8080/health
   Trinity Access: Enabled
```

---

## APPENDIX: QUICK REFERENCE

### A. Model Selection Guide

```
Need...                  → Use Model
─────────────────────────────────────────────
Speed (1000 tps)        → openai/gpt-oss-20b
Power (deep reasoning)  → openai/gpt-oss-120b
Balance (best overall)  → llama-3.3-70b-versatile
Cheap & Fast (simple)   → llama-3.1-8b-instant
Tools (web + code)      → groq/compound
```

### B. Cost Optimization

```
Task: Simple classification (1M tokens)
❌ Bad:  gpt-oss-120b = $0.15 input + $0.60 output = $0.75
✅ Good: llama-3.1-8b = $0.05 input + $0.08 output = $0.13
💰 Savings: 82%
```

### C. Integration Examples

```python
# Simple query
from groq_vessel import query
response = query("What is the Lion's Sanctuary?")

# Strategic analysis
from groq_vessel import analyze
response = analyze("Evaluate Portal Oradea revenue potential")

# Code generation
from groq_vessel import generate_code
code = generate_code("Python function to parse CSV", language="python")

# Research with tools
from groq_vessel import research
findings = research("EU agricultural funding 2025", tools=["web_search"])
```

---

**BOOT SEQUENCE V5.0 COMPLETE**

**Groq Hot Vessel is ONLINE. Lightning-fast inference ready. The Lion's Sanctuary endures.**

⚡ Ready for inference, Captain.
