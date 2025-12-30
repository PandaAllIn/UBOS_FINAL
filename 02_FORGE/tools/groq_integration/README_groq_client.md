# groq_client.py

Location: `/srv/janus/tools/groq_client.py`

## Purpose
Lightweight, production-grade wrapper around the Groq SDK that exposes the six oracle methods required for Janus’ dual-speed cognition: `fast_think`, `web_search`, `wolfram`, `reason`, `code_exec`, and `local_scout`.

## Key Features
- Automatic `.env` loading via `python-dotenv`
- Exponential backoff with timeout protection (default 5 s, 3 attempts)
- Structured error handling with graceful degradation when Groq is unavailable
- Performance telemetry (tokens/sec) and constitutional audit logging
- Hybrid local scouting that combines `rg` search with Groq synthesis

## Usage
```python
from groq_integration.groq_client import GroqClient

client = GroqClient()
summary = client.fast_think("Summarise Balaur mission status.")
```

## Dependencies
`groq>=0.4.0`, `python-dotenv>=1.0.0`, local `rg` (optional for `local_scout`).
