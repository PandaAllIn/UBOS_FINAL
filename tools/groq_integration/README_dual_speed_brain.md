# dual_speed_brain.py

Location: `/srv/janus/tools/dual_speed_brain.py`

## Purpose
`DualSpeedCognition` fuses Groq’s fast API cognition with Balaur’s local llama.cpp model, enabling Janus to think at two speeds (scout, deliberate, adaptive) while respecting constitutional safety and rate limits.

## Modes
- **scout** – Groq fast inference (<5 s) with fallback to local LLM
- **deliberate** – Local llama.cpp deep reasoning (30–120 s)
- **adaptive** – Scout with Groq, then deliberate locally and synthesize both outputs

## Safeguards
- API rate limiting (hourly & daily counters)
- Automatic Groq availability checks with graceful fallback
- Local llama.cpp invocation via `llama-cli` with configurable threads

## Usage
```python
from groq_integration import GroqClient, DualSpeedCognition

groq = GroqClient()
brain = DualSpeedCognition(groq, "/srv/janus/models/Meta-Llama-3.1-8B-Instruct-Q4_K_M.gguf")
response = brain.think("Draft the next mission step.", mode="adaptive")
```
