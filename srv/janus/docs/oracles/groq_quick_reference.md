# Groq Quick Reference

Location: `/srv/janus/docs/oracles/groq_quick_reference.md`  
Last updated: 2025-10-12

## Essentials
- **API Key:** `GROQ_API_KEY` (load from `/srv/janus/config/.env`)  
- **Fast Model:** `llama-3.3-70b-versatile` (override via `GROQ_FAST_MODEL`)  
- **Compound Model:** `groq/compound` (set `GROQ_COMPOUND_MODEL`)  
- **Rate Limits:** 100 requests/hour, 500 requests/day  
- **Log Files:** `/srv/janus/logs/groq_usage.jsonl`, `/srv/janus/logs/oracle_queries.jsonl`

## Method Cheatsheet
```python
from groq_integration.groq_client import GroqClient
client = GroqClient()

client.fast_think("Explain UBOS Mode Beta in one sentence.")
client.web_search("EU AI Act 2025 implementation timeline")
client.wolfram("Fourier transform of exp(-t^2)")
client.reason("Compare GPU Studio launch vs Oracle activation.")
client.code_exec("print(sum(i*i for i in range(5)))")
client.local_scout("dual_speed", path="/srv/janus/tools")
```

## Common Parameter Overrides
| Variable | Purpose | Suggested Value |
|----------|---------|-----------------|
| `GROQ_TIMEOUT_SECONDS` | Extend timeout for `web_search` | `15` |
| `GROQ_MAX_RETRIES` | Increase resilience | `4` |
| `GROQ_FAST_MODEL` | Swap fast model | `llama-3.1-8b-instant` (cheaper) |
| `GROQ_COMPOUND_MODEL` | Alternate compound profile | `groq/compound-mini` |
| `WOLFRAM_APP_ID` | Enable Groq→Wolfram bridge | `GGJ9JEXKGW` |

## Response Patterns
- `fast_think` → string response.
- `web_search` → Markdown summary with citations.
- `reason` → JSON dict with `answer` (string) and `reasoning` (array of steps).
- `code_exec` → JSON dict (`stdout`, `stderr`, `exit_code`, `summary`).
- `local_scout` → dict with `matches` list and Groq synthesis.

## Troubleshooting
- **`GroqUnavailableError`**: Check API key + network. Fallback to local llama automatically.
- **Reason output not JSON**: Review Groq release notes; if compound ignores JSON instructions, adjust the system prompt in `GroqClient.reason`.
- **Code exec returns prose**: Ensure running latest client (JSON-only prompt + `code_interpreter`). Regenerate if Groq updates tool names again.
- **Timeouts**: Increase `GROQ_TIMEOUT_SECONDS`, retry. Network spikes >10s common for web search.
- **Quota reached**: Pause, continue with llama.cpp. Quota resets top of hour UTC.
- **Nightly watchdog**: `python3 02_FORGE/scripts/groq_watchdog.py --log-file /srv/janus/logs/watchdog/groq_watchdog.jsonl` (expects JSON record with `reason` + `code_exec` statuses).

## Logging Template
```json
{
  "timestamp": "2025-10-12T14:03:05Z",
  "oracle": "groq",
  "method": "web_search",
  "query": "EU funding opportunities for AI research 2025",
  "model": "groq/compound",
  "duration_ms": 8210,
  "status": "ok",
  "response_sha256": "4b6fa4..."
}
```

## Mission Usage Patterns
1. **Scout & Summarise** – `fast_think` to sketch scenario, `web_search` to gather evidence.
2. **Compound Compute** – `wolfram` for quick maths, then local llama for reasoning.
3. **Repository Recon** – `local_scout("Oracle", path="/srv/janus")`, inspect matches, escalate to `fast_think` summary.
4. **Code Validation** – `code_exec` for quick algorithm spot-check (post-hotfix), log outputs before using in production proposals.

## Safety Practices
- Run all Groq outputs through local llama.cpp for constitutional confirmation before execution.
- Attach original Groq response as appendix in mission logs to preserve transparency.
- Avoid sending sensitive credentials or unreleased mission details over external APIs.
