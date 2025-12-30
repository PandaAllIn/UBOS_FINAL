# Groq MCP Server — Oracle Suite

Production-grade Model Context Protocol (MCP) server that exposes the Groq API as constitutional tools for the Trinity vessels (Claude, Gemini, Codex).

## Features
- Six Groq-backed tools for fast reasoning, web reconnaissance, Wolfram|Alpha, deep analysis, sandboxed code execution, and hybrid repo search.
- Constitutional safety: audit logging, graceful error handling, rate-limit backoff, token guardrails, and environment validation.
- Local intelligence via `groq_local_scout` (ripgrep + Groq synthesis) for rapid repository triage.

## Installation
```bash
cd 02_FORGE/packages/groq_mcp_server
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Environment Configuration
| Variable | Purpose | Required |
|----------|---------|----------|
| `GROQ_API_KEY` | Auth token for Groq API access | ✅ |
| `WOLFRAM_APP_ID` | Wolfram Alpha integration key (for `groq_wolfram`) | ✅ (tool-specific) |
| `GROQ_TIMEOUT_SECONDS` | Override default 5s API timeout | Optional |
| `GROQ_MAX_RETRIES` | Override default retry budget (3 attempts) | Optional |

Store secrets in `.env` (loaded automatically):
```env
GROQ_API_KEY=sk-...
WOLFRAM_APP_ID=...
```

## Running the Server
```bash
python3 server.py
```
The server automatically discovers a `run`/`serve_forever` entry point from the MCP runtime.

## Tool Inventory

| Tool | Description | Signature |
|------|-------------|-----------|
| `groq_fast_think` | Rapid reconnaissance on `llama-3.3-70b-versatile` | `(prompt: str, model?: str) -> str` |
| `groq_web_search` | Tavily-powered live search with citations | `(query: str, max_results?: int) -> dict` |
| `groq_wolfram` | Precise computation via Wolfram Alpha | `(math_query: str) -> str` |
| `groq_reason` | Deep reasoning with parsed steps | `(problem: str, effort: {'low','medium','high'}) -> dict` |
| `groq_code_exec` | Sandboxed execution through Groq compound tooling | `(code: str, language: str) -> dict` |
| `groq_local_scout` | Local ripgrep + Groq synthesis | `(pattern: str, path?: str) -> dict` |

### Example Usage
```python
# Claude Desktop (example)
# /Users/me/.config/anthropic/mcp/groq-mcp-server/package.json -> points to this directory
# Invoke inside Claude: /mcp groq_fast_think "Status update on Balaur"
```

Within MCP-compatible clients (Claude Desktop, Gemini CLI, Codex CLI), register `package.json` and invoke tools directly.

## Integration Guide
1. Add `package.json` to your MCP client registry.
2. Export required environment variables (or `.env`).
3. Launch the MCP server (`python3 server.py`) alongside the client.
4. In Claude/Gemini/Codex vessels, call tools by name (`groq_fast_think`, etc.).

## Testing
```bash
python3 -m pytest test_server.py  # requires pytest
```
The suite provides:
- Mocked API coverage for all tools.
- Optional integration test (skipped unless `GROQ_API_KEY` present).
- Error handling validation for missing keys, rate limits, and timeouts.
- Performance benchmark assertion (tokens/sec logging).

## Troubleshooting
- **Missing API key**: ensure `GROQ_API_KEY` is exported before invoking tools.
- **Timeouts**: adjust `GROQ_TIMEOUT_SECONDS` or reduce prompt size.
- **Rate limits**: the server retries automatically; increase delay using `GROQ_MAX_RETRIES` if needed.
- **ripgrep unavailable**: `groq_local_scout` falls back to a pure-Python search (slower).
- **Wolfram errors**: confirm `WOLFRAM_APP_ID` and that the key has API access.

## License
Internal use for the UBOS Republic. Crafted by Codex, the Forgemaster.
