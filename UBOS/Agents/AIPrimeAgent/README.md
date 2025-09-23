# UBOS AI Prime Agent

The AI Prime Agent is the orchestrator for the UBOS ecosystem. It coordinates independent agents (e.g., Master Librarian, Research Agent) through a versioned communication protocol, a capability-aware registry, and a strategic workflow that embodies UBOS principles.

- Protocol: strict message envelope (v0.1) for clean delegation and tracing
- Registry: tracks agents, capabilities, status, and heartbeat telemetry
- Workflow: pilot “Research & Synthesize” with Strategic Pause and Validation
- Adapters: Librarian (REST), Research Agent (CLI), plus test-friendly stubs
- Observability: transcript logging (JSONL) and report generation (JSON/Markdown)

## Quick start

- Python 3.11+
- Install dependencies: `pip install -r requirements.txt`
- Run tests: `PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 pytest -q`

## CLI usage

- Minimal pilot (stubs only; artifacts are gitignored):
```
PYTHONPATH=UBOS/Agents/AIPrimeAgent \
python3 -m ai_prime_agent.cli research-synthesize \
  --query "How to orchestrate agents under UBOS?" \
  --depth medium \
  --report-dir UBOS/Agents/AIPrimeAgent/artifacts \
  --transcript /tmp/prime_transcript.jsonl
```

- With real agents (Librarian REST + Research CLI):
```
# Start Librarian API in another terminal
export UBOS_BOOKS_PATH="$PWD/UBOS/SystemFundamentals/Books"
PYTHONPATH=UBOS/Agents/KnowledgeAgent/MasterLibrarianAgent \
python3 -c "from master_librarian.api.app import create_app; create_app().run(host='127.0.0.1', port=5025)"

# Then run Prime
PYTHONPATH=UBOS/Agents/AIPrimeAgent \
python3 -m ai_prime_agent.cli research-synthesize \
  --query "Production deployment roadmap for UBOS" \
  --depth medium \
  --librarian-url "http://127.0.0.1:5025" \
  --librarian-timeout 90 \
  --research-cli "UBOS/Agents/ResearchAgent/ubos_research_agent.py" \
  --research-timeout 120 \
  --report-dir UBOS/Agents/AIPrimeAgent/artifacts \
  --transcript /tmp/prime_transcript.jsonl
```

## Environment variables

- `GEMINI_API_KEY` (required by Librarian for Gemini; can operate heuristically without)
- `PERPLEXITY_API_KEY` (required by Research Agent CLI)
- `UBOS_BOOKS_PATH` (required by Librarian ingestion)

## Code map

- `ai_prime_agent/bus/` — protocol + in‑process bus
- `ai_prime_agent/registry/` — agent registry and telemetry
- `ai_prime_agent/orchestrator/` — orchestrator + workflows
- `ai_prime_agent/adapters/` — Librarian HTTP, Research CLI, stubs
- `ai_prime_agent/pause/` — Strategic Pause module
- `ai_prime_agent/validation/` — Blueprint Validation service
- `ai_prime_agent/reporting/` — Report generator (JSON/MD/Mermaid)
- `ai_prime_agent/cli.py` — CLI entry

## Security note

- Do not commit secrets. Use environment variables and rotate any keys present in local `.env`.

## Artifacts & retention
- Reports (JSON/MD/HTML) are written under `ai_prime_agent --report-dir`, e.g. `UBOS/Agents/AIPrimeAgent/artifacts/` which is gitignored.
- Transcripts default to `/tmp/*.jsonl` or a path you provide via `--transcript` (also gitignored if under artifacts/).
- To prune old reports locally, you can run `bash UBOS/Agents/AIPrimeAgent/scripts/clean_artifacts.sh` (see below).

## E2E testing (optional, off by default)
- Unit/integration tests (no network):
  - `cd UBOS/Agents/AIPrimeAgent && PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 pytest -q`
- E2E test (network + keys):
  - Set `RUN_UBOS_E2E=1` and ensure `GEMINI_API_KEY` and `PERPLEXITY_API_KEY` are exported
  - `cd UBOS/Agents/AIPrimeAgent && PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 RUN_UBOS_E2E=1 pytest -q -k e2e`

## Auth for Librarian REST
- Set `LIBRARIAN_API_TOKEN` (or `ML_API_TOKEN`) on the server side; Prime can pass `--librarian-auth <token>`.

## Scripts
- `scripts/clean_artifacts.sh` — prune reports older than N days (default 14);
  not required for operation, but helps keep local disk tidy.
