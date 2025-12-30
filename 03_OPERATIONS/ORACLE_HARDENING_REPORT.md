# Oracle Hardening Report – Oracle Bridge Resilience Upgrade

## 1. Fallback Chains & Error Surfacing
- `trinity/oracle_bridge.py:168` now documents the research contract and enforces the Perplexity → Groq fallback pipeline, recording every failure in `errors` so `[Fallback: Groq web]` results are clearly marked and logged.
- `trinity/oracle_bridge.py:213-226` caches Groq responses, prefixes fallback output, and routes unrecoverable failures through `OracleError` to `/srv/janus/logs/oracle_errors.jsonl`.
- `trinity/oracle_bridge.py:249-277` keeps matching resilience for Wolfram and Data Commons by caching successes and promoting Groq synthesis when primaries fail.

## 2. Health Monitoring CLI
- `trinity/oracle_health_check.py:1-147` exposes the `OracleHealthChecker` with per-oracle latency, structured logging to `/srv/janus/logs/oracle_health.jsonl`, and a `--json` CLI for mission pre-flight checks.

## 3. Response Caching
- `trinity/oracle_cache.py:1-87` persists responses under `/srv/janus/03_OPERATIONS/vessels/balaur/intel_cache/oracles/`, normalises legacy timestamps to UTC, and enforces TTLs (Perplexity 12h, Wolfram 6h, Data Commons 24h).

## 4. Skill Resilience Patterns
- `trinity/skills/eu-grant-hunter/scripts/scan_eu_databases.py:386-417` runs the oracle health check before scans, toggling fallback-only mode and surfacing status in telemetry.
- `trinity/skills/treasury-administrator/scripts/analyze_financials.py:57-85` performs the same health check, toggles Data Commons fallback automatically, and captures Groq recovery when primary economics calls fail.

## 5. Verification
- Command: `pytest trinity/tests/test_oracle_bridge_resilience.py -q`
- Result: validates primary success, Groq fallback activation, cache reuse, economics Groq synthesis, and error logging.

## 6. Change Surfaces
- Core logic: `trinity/oracle_bridge.py`, `trinity/oracle_cache.py`, `trinity/oracle_health_check.py`
- Skill integrations: `trinity/skills/eu-grant-hunter/scripts/scan_eu_databases.py`, `trinity/skills/treasury-administrator/scripts/analyze_financials.py`
