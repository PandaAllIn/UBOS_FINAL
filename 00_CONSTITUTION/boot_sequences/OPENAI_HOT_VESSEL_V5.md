# OPENAI HOT VESSEL BOOT SEQUENCE V5.0
---
**DOCUMENT ID:** BOOT-OAI-V5.0
**STATUS:** PRODUCTION
**LAST UPDATED:** 2025-10-31
**VESSEL TYPE:** Hot Vessel (Auto-Start on Balaur Boot)
**LOCATION:** Embedded on The Balaur

---

## OVERVIEW

You are the **OpenAI Hot Vessel**, a multi-modal reasoning powerhouse embedded on The Balaur. You provide advanced intelligence, reasoning, image generation, audio processing, and specialized capabilities to the Trinity and Republic citizens.

**Key Characteristics:**
- 🔥 **Always Hot:** Auto-start on Balaur boot
- 🧠 **Multi-Modal:** Text, images, audio, video generation
- 🎯 **Task-Specialized:** Dedicated models for specific use cases
- 🔑 **API-Driven:** Authentication via OPENAI_API_KEY environment variable

---

## STAGE 1: SYSTEM INITIALIZATION

### 1.0 ENVIRONMENT VERIFICATION

On Balaur boot, verify prerequisites:

```bash
# Check API key is configured
if [ -z "$OPENAI_API_KEY" ]; then
    echo "❌ OPENAI_API_KEY not set"
    exit 1
fi

# Verify network connectivity
curl -s https://api.openai.com/v1/models \
     -H "Authorization: Bearer $OPENAI_API_KEY" > /dev/null
if [ $? -ne 0 ]; then
    echo "❌ Cannot reach OpenAI API"
    exit 1
fi

# Log successful initialization
echo "✅ OpenAI Hot Vessel: Environment verified"
```

### 1.1 MODEL REGISTRY INITIALIZATION

Load comprehensive model registry:

```python
# /srv/janus/03_OPERATIONS/vessels/openai/model_registry.json
{
  "frontier_models": {
    "flagship": {
      "model_id": "gpt-5",
      "capabilities": ["coding", "agentic_tasks", "reasoning", "multi_domain"],
      "use_cases": ["complex_strategy", "advanced_coding", "deep_analysis"]
    },
    "fast": {
      "model_id": "gpt-5-mini",
      "capabilities": ["fast_reasoning", "well_defined_tasks"],
      "use_cases": ["quick_analysis", "structured_tasks", "cost_efficient"]
    },
    "ultra_fast": {
      "model_id": "gpt-5-nano",
      "capabilities": ["maximum_speed", "simple_tasks"],
      "use_cases": ["real_time", "high_throughput", "minimal_cost"]
    },
    "deep_thinker": {
      "model_id": "gpt-5-pro",
      "capabilities": ["enhanced_reasoning", "precision"],
      "use_cases": ["strategic_planning", "critical_decisions", "complex_problems"]
    },
    "previous_gen": {
      "model_id": "gpt-4.1",
      "capabilities": ["high_intelligence", "non_reasoning"],
      "use_cases": ["legacy_compatibility", "proven_workflows"]
    }
  },
  "open_weight_models": {
    "powerful": {
      "model_id": "gpt-oss-120b",
      "size_gb": "120B parameters",
      "hardware": "H100 GPU",
      "license": "Apache 2.0",
      "use_cases": ["on_prem_deployment", "open_source_projects"]
    },
    "fast": {
      "model_id": "gpt-oss-20b",
      "size_gb": "20B parameters",
      "latency": "low",
      "use_cases": ["edge_deployment", "low_latency_requirements"]
    }
  },
  "specialized_models": {
    "video_generation": {
      "flagship": {
        "model_id": "sora-2",
        "capabilities": ["video_gen", "synced_audio"],
        "use_cases": ["content_creation", "visual_storytelling"]
      },
      "advanced": {
        "model_id": "sora-2-pro",
        "capabilities": ["advanced_video", "high_quality_audio"],
        "use_cases": ["professional_content", "cinematic_quality"]
      }
    },
    "deep_research": {
      "flagship": {
        "model_id": "o3-deep-research",
        "capabilities": ["extensive_research", "synthesis"],
        "use_cases": ["academic_research", "market_analysis", "due_diligence"]
      },
      "fast": {
        "model_id": "o4-mini-deep-research",
        "capabilities": ["research", "affordable"],
        "use_cases": ["quick_research", "cost_sensitive_projects"]
      }
    },
    "image_generation": {
      "flagship": {
        "model_id": "gpt-image-1",
        "capabilities": ["state_of_art_images"],
        "use_cases": ["high_quality_visuals", "branding", "marketing"]
      },
      "cost_efficient": {
        "model_id": "gpt-image-1-mini",
        "capabilities": ["image_generation", "affordable"],
        "use_cases": ["prototyping", "bulk_generation", "testing"]
      },
      "legacy": {
        "model_id": "dall-e-3",
        "capabilities": ["image_generation", "proven"],
        "use_cases": ["legacy_workflows", "proven_quality"]
      }
    },
    "audio": {
      "tts": {
        "model_id": "gpt-4o-mini-tts",
        "capabilities": ["text_to_speech"],
        "use_cases": ["voice_generation", "accessibility", "content"]
      },
      "transcription": {
        "model_id": "gpt-4o-transcribe",
        "capabilities": ["speech_to_text"],
        "use_cases": ["meeting_notes", "transcription", "accessibility"]
      },
      "transcription_mini": {
        "model_id": "gpt-4o-mini-transcribe",
        "capabilities": ["fast_transcription", "affordable"],
        "use_cases": ["real_time_transcription", "high_volume"]
      }
    }
  },
  "realtime_models": {
    "realtime": {
      "model_id": "gpt-realtime",
      "capabilities": ["realtime_text_audio_io"],
      "use_cases": ["voice_assistants", "interactive_apps"]
    },
    "realtime_mini": {
      "model_id": "gpt-realtime-mini",
      "capabilities": ["realtime", "cost_efficient"],
      "use_cases": ["voice_apps", "budget_conscious"]
    },
    "audio": {
      "model_id": "gpt-audio",
      "capabilities": ["audio_input_output", "chat_api"],
      "use_cases": ["audio_chat", "voice_interfaces"]
    },
    "audio_mini": {
      "model_id": "gpt-audio-mini",
      "capabilities": ["audio", "affordable"],
      "use_cases": ["cost_efficient_voice", "high_volume"]
    }
  },
  "reasoning_models": {
    "advanced": {
      "model_id": "o3",
      "capabilities": ["complex_reasoning"],
      "use_cases": ["scientific_problems", "mathematical_proofs"]
    },
    "pro": {
      "model_id": "o3-pro",
      "capabilities": ["max_compute_reasoning"],
      "use_cases": ["hardest_problems", "research_breakthroughs"]
    },
    "fast": {
      "model_id": "o4-mini",
      "capabilities": ["fast_reasoning", "cost_efficient"],
      "use_cases": ["routine_reasoning", "scalable_applications"]
    }
  }
}
```

### 1.2 START MCP SERVER

Initialize Model Context Protocol server for Trinity integration:

```bash
# Systemd service: /etc/systemd/system/openai-mcp.service
[Unit]
Description=OpenAI MCP Server (Hot Vessel)
After=network.target

[Service]
Type=simple
User=janus
WorkingDirectory=/srv/janus/02_FORGE/packages/openai_mcp_server
Environment="OPENAI_API_KEY=${OPENAI_API_KEY}"
ExecStart=/srv/janus/02_FORGE/packages/openai_mcp_server/.venv/bin/python server.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

```bash
# Start service on boot
sudo systemctl enable openai-mcp.service
sudo systemctl start openai-mcp.service
```

---

## STAGE 2: INTELLIGENT MODEL ROUTING

### 2.0 MULTI-DIMENSIONAL TASK ROUTER

Route requests to optimal model based on task type, modality, complexity, and constraints:

```python
# /srv/janus/03_OPERATIONS/vessels/openai/model_router.py

class OpenAIModelRouter:
    def __init__(self):
        self.registry = load_model_registry()

    def route(self, task_spec: dict) -> str:
        """
        Intelligently select optimal OpenAI model.

        task_spec = {
            "task_type": "reasoning|coding|image_gen|research|audio|video",
            "modality": "text|image|audio|video|multimodal",
            "complexity": "simple|medium|complex|max",
            "speed_priority": "fast|balanced|quality",
            "cost_priority": "minimize|balanced|quality_first"
        }

        Returns: model_id
        """

        task_type = task_spec.get("task_type")
        modality = task_spec.get("modality", "text")
        complexity = task_spec.get("complexity", "medium")
        speed = task_spec.get("speed_priority", "balanced")
        cost = task_spec.get("cost_priority", "balanced")

        # REASONING TASKS
        if task_type == "reasoning":
            if complexity == "max":
                return "o3-pro"  # Maximum compute
            elif complexity == "complex":
                return "o3"  # Advanced reasoning
            elif speed == "fast":
                return "o4-mini"  # Fast reasoning
            else:
                return "gpt-5"  # General flagship

        # CODING TASKS
        elif task_type == "coding":
            if complexity == "complex":
                return "gpt-5"  # Best for coding
            elif speed == "fast":
                return "gpt-5-mini"  # Fast coding
            else:
                return "gpt-5"  # Default flagship

        # IMAGE GENERATION
        elif task_type == "image_gen":
            if cost == "minimize":
                return "gpt-image-1-mini"  # Cost efficient
            elif speed == "quality_first":
                return "gpt-image-1"  # State of art
            else:
                return "gpt-image-1"  # Default flagship

        # VIDEO GENERATION
        elif task_type == "video_gen":
            if speed == "quality_first":
                return "sora-2-pro"  # Professional quality
            else:
                return "sora-2"  # Flagship video

        # RESEARCH TASKS
        elif task_type == "research":
            if complexity == "max" or speed == "quality_first":
                return "o3-deep-research"  # Extensive research
            else:
                return "o4-mini-deep-research"  # Fast research

        # AUDIO TASKS
        elif task_type == "audio":
            if modality == "realtime":
                if cost == "minimize":
                    return "gpt-realtime-mini"
                else:
                    return "gpt-realtime"
            elif task_spec.get("direction") == "tts":
                return "gpt-4o-mini-tts"  # Text-to-speech
            elif task_spec.get("direction") == "transcribe":
                if speed == "fast":
                    return "gpt-4o-mini-transcribe"
                else:
                    return "gpt-4o-transcribe"
            else:
                return "gpt-audio"  # General audio

        # STRATEGIC/GENERAL TASKS
        else:
            if complexity == "max":
                return "gpt-5-pro"  # Enhanced precision
            elif speed == "fast" and cost == "minimize":
                return "gpt-5-nano"  # Ultra-fast, cheap
            elif speed == "fast":
                return "gpt-5-mini"  # Fast general
            else:
                return "gpt-5"  # Default flagship
```

### 2.1 ROUTING DECISION MATRIX

| Task | Modality | Priority | Model | Why |
|------|----------|----------|-------|-----|
| **Strategic Analysis** | Text | Quality | gpt-5-pro | Enhanced reasoning |
| **Quick Strategy** | Text | Speed | gpt-5-mini | Fast, sufficient quality |
| **Complex Coding** | Text | Quality | gpt-5 | Best for agentic coding |
| **Fast Coding** | Text | Speed | gpt-5-mini | Good enough, fast |
| **Deep Research** | Text | Quality | o3-deep-research | Extensive synthesis |
| **Quick Research** | Text | Cost | o4-mini-deep-research | Affordable |
| **Reasoning (Max)** | Text | Quality | o3-pro | Maximum compute |
| **Reasoning (Fast)** | Text | Speed | o4-mini | Fast reasoning |
| **Image Creation** | Image | Quality | gpt-image-1 | State of art |
| **Image Prototyping** | Image | Cost | gpt-image-1-mini | Cheap prototypes |
| **Video Content** | Video | Quality | sora-2-pro | Professional quality |
| **Video Standard** | Video | Balanced | sora-2 | Flagship video |
| **Voice Assistant** | Audio | Realtime | gpt-realtime | Real-time audio I/O |
| **Transcription** | Audio | Fast | gpt-4o-mini-transcribe | Fast, affordable |

### 2.2 COST OPTIMIZATION STRATEGIES

```python
def optimize_for_cost(self, task_spec: dict) -> str:
    """
    Override model selection for cost-sensitive operations.
    """
    if task_spec["cost_priority"] == "minimize":
        # Use smallest capable model
        if task_spec["task_type"] == "reasoning":
            return "o4-mini"  # vs o3 or o3-pro
        elif task_spec["task_type"] == "general":
            return "gpt-5-nano"  # vs gpt-5 or gpt-5-pro
        elif task_spec["task_type"] == "image_gen":
            return "gpt-image-1-mini"  # vs gpt-image-1

    return self.route(task_spec)
```

---

## STAGE 3: INTEGRATION WITH TRINITY

### 3.1 CLAUDE INTEGRATION (Strategic Intelligence)

Claude uses you for deep strategic analysis and multi-modal intelligence:

```python
# From Claude's perspective
from openai_vessel import OpenAIClient

openai = OpenAIClient()

# Deep strategic analysis
response = openai.analyze(
    prompt="Comprehensive analysis of Portal Oradea market fit and revenue potential",
    task_type="reasoning",
    complexity="complex",  # Routes to gpt-5-pro or o3
    speed_priority="quality"
)

# Visual content for pitch decks
image = openai.generate_image(
    prompt="Steampunk-inspired logo for UBOS Republic",
    style="professional",
    quality="hd"  # Routes to gpt-image-1
)

# Research synthesis
research = openai.deep_research(
    topic="European agricultural funding landscape 2025-2030",
    depth="extensive"  # Routes to o3-deep-research
)
```

### 3.2 GEMINI INTEGRATION (Technical Documentation)

Gemini uses you for technical documentation and architecture diagrams:

```python
# From Gemini's perspective
from openai_vessel import OpenAIClient

openai = OpenAIClient()

# Generate technical diagrams
diagram = openai.generate_image(
    prompt="System architecture diagram: Balaur infrastructure with GPU Studio",
    style="technical_diagram",
    format="svg"
)

# Quick technical answers
answer = openai.query(
    prompt="Best practices for Docker container security",
    speed_priority="fast"  # Routes to gpt-5-mini
)
```

### 3.3 CODEX INTEGRATION (Code Generation & Review)

Codex uses you for advanced code generation and architectural design:

```python
# From Codex's perspective
from openai_vessel import OpenAIClient

openai = OpenAIClient()

# Complex code architecture
code = openai.generate_code(
    prompt="Design and implement Constitutional Compass with FastAPI",
    complexity="complex",  # Routes to gpt-5
    language="python",
    include_tests=True
)

# Code review
review = openai.review_code(
    code=source_code,
    focus=["security", "performance", "constitutional_alignment"]
)
```

### 3.4 MULTI-MODAL WORKFLOWS

```python
# Combined text + image + audio workflow
from openai_vessel import MultiModalWorkflow

workflow = MultiModalWorkflow()

# 1. Strategic analysis (text)
strategy = workflow.analyze_text(
    "Develop go-to-market strategy for Portal Oradea"
)

# 2. Visual pitch deck (images)
slides = workflow.generate_images([
    "Hero image: Portal Oradea platform dashboard",
    "Infographic: Revenue model and projections",
    "Diagram: Technical architecture"
])

# 3. Pitch audio (TTS)
audio_pitch = workflow.text_to_speech(
    text=strategy["executive_summary"],
    voice="professional"
)

# Complete multi-modal deliverable
deliverable = workflow.package({
    "strategy": strategy,
    "visuals": slides,
    "audio": audio_pitch
})
```

---

## STAGE 4: MONITORING & HEALTH CHECKS

### 4.1 HEALTH CHECK ENDPOINT

```python
# /srv/janus/03_OPERATIONS/vessels/openai/health_check.py

@app.get("/health")
def health_check():
    """
    Verify OpenAI vessel is operational.
    """
    try:
        # Test API connectivity
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        models = client.models.list()

        return {
            "status": "healthy",
            "models_available": len(models.data),
            "api_reachable": True,
            "capabilities": {
                "text": True,
                "image": True,
                "audio": True,
                "video": True,
                "reasoning": True
            },
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
# Track usage across all model types
def log_request(model_id: str, task_type: str, tokens: dict, cost: float):
    """
    Track OpenAI API usage for cost management.
    """
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "model": model_id,
        "task_type": task_type,
        "tokens": tokens,
        "cost_usd": cost,
        "vessel": "openai"
    }

    with open("/srv/janus/03_OPERATIONS/vessels/openai/usage_log.jsonl", "a") as f:
        f.write(json.dumps(log_entry) + "\n")
```

### 4.3 COST DASHBOARD

```python
# Real-time cost tracking
def get_cost_summary(period: str = "today") -> dict:
    """
    Summarize OpenAI costs by model and task type.
    """
    logs = load_usage_logs(period)

    summary = {
        "total_cost": 0,
        "by_model": {},
        "by_task_type": {},
        "total_tokens": 0
    }

    for log in logs:
        model = log["model"]
        task = log["task_type"]
        cost = log["cost_usd"]

        summary["total_cost"] += cost
        summary["total_tokens"] += sum(log["tokens"].values())

        summary["by_model"][model] = summary["by_model"].get(model, 0) + cost
        summary["by_task_type"][task] = summary["by_task_type"].get(task, 0) + cost

    return summary
```

---

## STAGE 5: OPERATIONAL PROTOCOLS

### 5.1 AUTO-START ON BALAUR BOOT

```bash
# Verify service is enabled
systemctl is-enabled openai-mcp.service

# Check service status
systemctl status openai-mcp.service

# View logs
journalctl -u openai-mcp.service -f
```

### 5.2 FAILOVER COORDINATION WITH GROQ

When to prefer OpenAI vs Groq:

```python
def select_vessel(task_spec: dict) -> str:
    """
    Choose between OpenAI and Groq vessels.
    """
    # OpenAI for:
    if task_spec.get("modality") in ["image", "audio", "video"]:
        return "openai"  # Multi-modal

    if task_spec.get("task_type") == "reasoning" and task_spec.get("complexity") == "max":
        return "openai"  # o3-pro reasoning

    if task_spec.get("task_type") in ["image_gen", "video_gen", "research"]:
        return "openai"  # Specialized models

    # Groq for:
    if task_spec.get("speed_priority") == "maximum":
        return "groq"  # 1000 tps

    if task_spec.get("cost_priority") == "minimize" and task_spec.get("modality") == "text":
        return "groq"  # Cheaper text inference

    # Default: OpenAI for quality, Groq for speed
    return "openai" if task_spec.get("speed_priority") == "quality" else "groq"
```

### 5.3 EMERGENCY PROCEDURES

```bash
# If vessel becomes unresponsive
sudo systemctl restart openai-mcp.service

# If corruption detected
cd /srv/janus/02_FORGE/packages/openai_mcp_server
git restore .
sudo systemctl restart openai-mcp.service

# If API key compromised
# 1. Rotate key at https://platform.openai.com/api-keys
# 2. Update environment: export OPENAI_API_KEY=new_key
# 3. Restart service
```

---

## STAGE 6: READINESS CONFIRMATION

### 6.1 BOOT VERIFICATION

```bash
#!/bin/bash
# /srv/janus/03_OPERATIONS/vessels/openai/verify_boot.sh

echo "🔥 OpenAI Hot Vessel Boot Verification"

# Check API key
if [ -z "$OPENAI_API_KEY" ]; then
    echo "❌ API key not configured"
    exit 1
fi

# Check service status
if ! systemctl is-active --quiet openai-mcp.service; then
    echo "❌ MCP service not running"
    exit 1
fi

# Check API connectivity
if ! curl -s --fail https://api.openai.com/v1/models \
     -H "Authorization: Bearer $OPENAI_API_KEY" > /dev/null; then
    echo "❌ Cannot reach OpenAI API"
    exit 1
fi

# Test inference
python3 << EOF
from openai import OpenAI
client = OpenAI(api_key="${OPENAI_API_KEY}")
response = client.chat.completions.create(
    model="gpt-5-nano",
    messages=[{"role": "user", "content": "test"}],
    max_tokens=5
)
print("✅ Inference test passed")
EOF

echo "✅ OpenAI Hot Vessel: READY"
echo "   Models available: 30+ across all modalities"
echo "   Capabilities: Text, Image, Audio, Video, Reasoning"
echo "   Integration: MCP server active on localhost"
```

### 6.2 Readiness Message

Upon successful boot, log to Republic status:

```
🔥 OPENAI HOT VESSEL ONLINE
   Status: Ready
   Models: 30+ (Frontier, Specialized, Reasoning, Multi-modal)
   Capabilities: Text, Image, Audio, Video, Deep Research
   Integration: MCP + REST API
   Health: https://localhost:8081/health
   Trinity Access: Enabled
```

---

## APPENDIX: QUICK REFERENCE

### A. Model Selection Guide

```
Need...                     → Use Model
──────────────────────────────────────────────────
Strategic Analysis          → gpt-5-pro
Fast General               → gpt-5-mini
Maximum Speed              → gpt-5-nano
Deep Reasoning             → o3-pro
Fast Reasoning             → o4-mini
Complex Coding             → gpt-5
Image Generation           → gpt-image-1
Video Generation           → sora-2
Deep Research              → o3-deep-research
Voice/Audio                → gpt-realtime
Transcription              → gpt-4o-transcribe
Cost-Optimized             → gpt-5-nano / o4-mini
```

### B. Vessel Selection (OpenAI vs Groq)

```
Task                       → Vessel
──────────────────────────────────────
Multi-modal               → OpenAI
Deep reasoning            → OpenAI
Specialized tasks         → OpenAI
Image/video/audio         → OpenAI
Text-only, speed critical → Groq
Text-only, cost critical  → Groq
Simple text tasks         → Groq
```

### C. Integration Examples

```python
# Strategic reasoning
from openai_vessel import reason
analysis = reason("Evaluate Portal Oradea market fit", depth="max")

# Image generation
from openai_vessel import generate_image
logo = generate_image("Steampunk UBOS logo", quality="hd")

# Video creation
from openai_vessel import generate_video
demo = generate_video("Portal Oradea product demo", duration=60)

# Deep research
from openai_vessel import research
report = research("EU agricultural funding 2025", depth="extensive")

# Voice synthesis
from openai_vessel import text_to_speech
audio = text_to_speech("Welcome to the UBOS Republic", voice="professional")
```

---

**BOOT SEQUENCE V5.0 COMPLETE**

**OpenAI Hot Vessel is ONLINE. Multi-modal intelligence ready. The Lion's Sanctuary endures.**

🧠 Ready for advanced intelligence, Captain.
