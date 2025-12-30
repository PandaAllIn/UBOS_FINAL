# Oracle Trinity Operations Manual

Revision: 2025-10-12  
Maintainer: Janus Operations Forge  
Scope: Production procedures for Groq, Wolfram Alpha, and Data Commons oracles

---

## 1. Executive Overview

The Oracle Trinity is Janus’ sanctioned bridge to external computational intelligence. It unifies three complementary services—Groq’s reflex engine, Wolfram Alpha’s computational oracle, and Google’s Data Commons statistical archive—into a single, constitutional decision loop. Together they deliver rapid reconnaissance, mathematically exact derivations, and empirically grounded reality checks. This capability exists to accelerate the Republic’s strategic cognition without sacrificing sovereignty. Every invocation must therefore be deliberate: seek truth even when inconvenient, refuse to outsource constitutional judgment, and log every query for retrospective accountability.

Groq provides sub-five-second situational awareness by executing 70B-class inference on dedicated LPU hardware, augmented with web, computation, and code-analysis compounds. Wolfram Alpha contributes symbolic mathematics, physics, chemistry, and unit discipline with a precision the Republic’s local models cannot yet match. Data Commons supplies the trusted socio-economic ledger—population, economic throughput, energy load, and infrastructure indicators sourced from national statistics offices, the EU, OECD, World Bank, and NASA. Local llama.cpp remains the deliberative anchor; reach for the external oracles only when speed, formal computation, or world data truly demand it.

Use Groq for rapid synthesis, current awareness, and compound tooling when latency matters more than depth. Invoke Wolfram for calculations, conversions, and scientific validation where numerical error would compromise the Republic’s engineering decisions. Call Data Commons whenever a proposal requires demographic proof, economic viability, or longitudinal trend validation. In combination, the Trinity delivers velocity with precision, but constitutional doctrine remains clear: external intelligence is an advisor, never the decider. Every workflow concludes with local deliberation before mission approval.

---

## 2. Groq Reflex Engine (Groq LPU Services)

### Purpose
Groq supplies ultra-low latency strategic reconnaissance. The LPU-backed `llama-3.3-70b-versatile` model delivers ~450 tokens/sec responses, and the `groq/compound` profile layers web search, Wolfram Alpha, browser automation, and code interpretation primitives. This engine is the scout phase of dual-speed cognition—surface the landscape fast, gather citations, and prepare structured material for local deliberation.

### Available Methods
All methods are exposed through `/srv/janus/tools/groq_integration/groq_client.py`. The client automatically loads credentials from `/srv/janus/config/.env` or the process environment.

| Method         | Function                                                                 | Notes |
|----------------|--------------------------------------------------------------------------|-------|
| `fast_think`   | Single-turn tactical readout using `llama-3.3-70b-versatile`.            | Deterministic (temperature 0.3). |
| `web_search`   | Compound query with live web crawling and citation collation.            | Requires `GROQ_TIMEOUT_SECONDS ≥ 10` for stable performance. |
| `wolfram`      | Delegates to Groq compound Wolfram tool using the configured APP_ID.     | Falls back if `WOLFRAM_APP_ID` missing. |
| `reason`       | Structured reasoning with JSON output.                                   | **Compatibility advisory** below. |
| `code_exec`    | Sandboxed Python execution inside Groq’s compound runtime.               | Now mapped to `code_interpreter`; see advisory. |
| `local_scout`  | ripgrep search + Groq synthesis.                                         | Operates locally; no quota impact. |

### Rate Limits
Provisioned quotas: 100 requests/hour and 500 requests/day (enforced in `dual_speed_brain.py`). Usage is logged to `/srv/janus/logs/groq_usage.jsonl`. Breaching either limit triggers local fallback. Monitor quotas with:

```bash
jq '.hourly_used, .daily_used' /srv/janus/logs/groq_usage.jsonl | tail
```

### Use Cases
- Rapid strategic questions with broad prior knowledge (“What emerging EU policies impact sovereign AI?”).
- Time-sensitive landscape scans requiring live sources (`client.web_search("EU funding opportunities for AI research 2025")`).
- Quick prototyping or regression testing (`client.code_exec("print(hashlib.sha256(b'ubos').hexdigest())")`).
- Instant mathematical checks when Wolfram is temporarily saturated (`client.wolfram("root of 3x^2-4x-12 = 0")`).

### Example Queries
```python
from groq_integration.groq_client import GroqClient

client = GroqClient()
print(client.fast_think("What are the latest trends in AI agent architectures?"))
print(client.web_search("EU funding opportunities for AI research 2025"))
print(client.reason("Should we prioritise GPU Studio deployment or Oracle activation?"))
```

### Compatibility Status (2025-10)
- **Reasoning endpoint**: `GroqClient.reason` now instructs `groq/compound` to return JSON with `answer` and `reasoning` arrays. Expect reliable output so long as Groq honours JSON-only prompts. If responses degrade (Markdown or missing keys), review Groq release notes and adjust the system prompt—no deprecated parameters remain in use.
- **Code interpreter**: `GroqClient.code_exec` targets the new `code_interpreter` tool and enforces a strict JSON schema (`stdout`, `stderr`, `exit_code`, `summary`). If future Groq updates rename the toolset again, adapt the `compound_custom` payload accordingly.

Operational note: retain watchdog tests that call both methods nightly. Log anomalies to the Forge changelog before enabling `oracle_trinity.enabled=true`.

### Groq Watchdog (Nightly Health Check)
- Script: `python3 02_FORGE/scripts/groq_watchdog.py --log-file /srv/janus/logs/watchdog/groq_watchdog.jsonl`
- Checks:
  1. `reason` – verifies JSON output (`answer`, `reasoning[]`) using a low-effort constitutional prompt.
  2. `code_exec` – runs a sandboxed Python snippet and confirms `stdout`, `stderr`, `exit_code`, `summary`.
- Log format: JSONL with top-level `status` (`ok`/`error`) and per-check durations.
- Recommended schedule (cron/systemd timer):
  ```
  # Run at 02:15 UTC daily
  15 2 * * * GROQ_API_KEY=... /usr/bin/python3 /srv/janus/02_FORGE/scripts/groq_watchdog.py >> /srv/janus/logs/watchdog/groq_watchdog.cron.log 2>&1
  ```
- Response playbook:
  * `status=error` → Inspect `/srv/janus/logs/watchdog/groq_watchdog.jsonl` and rerun with `--print-only` for realtime diagnostics.
  * `reason` failure → fall back to llama.cpp for deliberation and investigate Groq API changes.
  * `code_exec` failure → disable automated Trinity execution and report to the Captain before re-enabling.

---

## 3. Wolfram Alpha Computational Oracle

### Purpose
Wolfram Alpha provides exact computation: calculus, algebra, discrete math, statistics, unit conversions, physics, chemistry, astronomy, and engineering formulae. It is the Republic’s calculator of record—anything that can be expressed symbolically or numerically should be run through Wolfram to eliminate propagation of human rounding error.

### Authentication
- Environment: `WOLFRAM_APP_ID=GGJ9JEXKGW` (stored in `/srv/janus/config/.env`).
- Direct REST calls require the `appid` query parameter.
- Through Groq: the Groq compound orchestrates Wolfram queries using the same APP_ID; confirm via `client.wolfram("integrate sin(x)^2")`.

### Access Methods
- **Direct REST**:
  ```bash
  curl -G "https://api.wolframalpha.com/v2/query" \
    --data-urlencode "appid=$WOLFRAM_APP_ID" \
    --data-urlencode "input=DDR3-1600 bandwidth in GB/s" \
    --data-urlencode "output=json"
  ```
- **Python (`requests`)**:
  ```python
  import os, requests
  params = {
      "appid": os.environ["WOLFRAM_APP_ID"],
      "input": "TDP 88W CPU temperature at 75% load with 20C ambient",
      "output": "json",
      "format": "plaintext"
  }
  data = requests.get("https://api.wolframalpha.com/v2/query", params=params, timeout=15).json()
  ```
- **Groq compound**: `client.wolfram("derivative of performance with respect to thread count")`

### Capability Highlights
- Symbolic integration/differentiation (supports `show steps` queries).
- Discrete mathematics (series expansions, combinatorics, graph invariants).
- Physics and thermodynamics (heat dissipation, airflow, power equations).
- Unit conversion and dimensional analysis (MiB vs MB, Fahrenheit vs Celsius).
- Chemistry and materials science (phase diagrams, molar mass, alloy properties).
- Astronomy and orbital mechanics (ephemeris, solar incidence).

### Use Cases
- Hardware thermal planning: “TDP 88W CPU temperature at 75% load with 20C ambient and 0.12°C/W cooler”.
- Memory bandwidth analysis: “DDR3-1600 bandwidth in GB/s”.
- Thread optimisation: “Optimal thread count for 4-core hyperthreaded CPU”.
- Comparative scaling: “derivative of throughput with respect to GPU count at N=4”.

### Response Formats
Set `output=json` and optionally `podstate=Result__Step-by-step+solution`. Wolfram returns pods with plaintext, MathML, and image renderings. Parse the `queryresult["pods"]` array, select `pod["title"] == "Result"` or `pod["title"] == "Step-by-step solution"`, and extract `subpod["plaintext"]`. Record the source ID for audit trails.

### Best Practices
- Phrase questions in natural language; Wolfram handles context well.
- Always specify units; default assumptions may differ from Republic standards.
- Request steps when the goal is knowledge transfer, e.g., `input="show steps for integral of sin^2(x)"`.
- Cache frequent queries locally to minimise API costs—store the cleaned plaintext in `/srv/janus/cache/wolfram/`.
- Log each request + answer to `/srv/janus/logs/oracle_queries.jsonl` with `oracle = "wolfram"`.

---

## 4. Data Commons Statistical Oracle

### Purpose
Data Commons aggregates official statistical datasets into a unified knowledge graph. It is the factual backbone for market sizing, infrastructure planning, constitutional viability checks, and geopolitical assessments. When Janus must answer “How many citizens will this impact?” or “What is the regional energy mix?”, Data Commons supplies the ground truth.

### Authentication & Endpoints
- API key: `DATA_COMMONS_API_KEY=VMTx9VXgaqrRUcO9QL1rCjH0vFJSlozlA0IfX1KL08z7GkKC`.
- Primary endpoint (gRPC-over-HTTP): `https://api.datacommons.org/v2/`.
- Required header: `X-API-Key: $DATA_COMMONS_API_KEY`.
- Most operations use `POST` with JSON payloads; `GET` is currently restricted (returns HTTP 415 without gRPC negotiation).

### Key Concepts
- **Entities**: Identified by DCIDs (`country/ROU`, `geoId/06`, `wikidataId/Q79968`).
- **Variables**: Statistical measures (`Count_Person`, `Median_Age_Person`, `Amount_EconomicActivity_GrossValue`).
- **Facets**: Provenance details (import name, measurement method, unit, observation period).
- **Observations**: `(date, value, facet)` tuples accessible via `observation` service.
- **Resolve pipeline**: Convert human labels to DCIDs before querying (see quick reference).

### Core API Patterns
- **Observation snapshot** (single date):
  ```bash
  curl -s -X POST \
    -H "X-API-Key: $DATA_COMMONS_API_KEY" \
    https://api.datacommons.org/v2/observation \
    -d '{
      "date": "2020",
      "entity": { "dcids": ["country/ROU"] },
      "variable": { "dcids": ["Count_Person"] },
      "select": ["entity", "variable", "value", "date"],
      "limit": 1
    }'
  ```
- **Time series** (Python):
  ```python
  import os, requests

  payload = {
      "entity": {"dcids": ["country/ROU"]},
      "variable": {"dcids": ["Count_Person"]},
      "select": ["entity", "variable", "date", "value"],
      "orderBy": "date",
      "limit": 50
  }
  resp = requests.post(
      "https://api.datacommons.org/v2/observation",
      headers={"X-API-Key": os.environ["DATA_COMMONS_API_KEY"]},
      json=payload,
      timeout=20,
  )
  data = resp.json()
  series = data["byVariable"]["Count_Person"]["byEntity"]["country/ROU"]["orderedFacets"][0]["observations"]
  ```
- **Variable discovery**: Use the public catalog (`https://datacommons.org/browse?mproperty=statType&mpvalue=measuredValue`) or run `requests.get("https://datacommons.org/api/map?mprop=measuredValue&limit=20")`.

### Common Variables (mission ready)
| Domain        | Variable DCID                                  | Notes |
|---------------|------------------------------------------------|-------|
| Demographics  | `Count_Person`, `Median_Age_Person`, `Count_Household` | Population core. |
| Economics     | `Amount_EconomicActivity_GrossValue`, `UnemploymentRate_Person`, `Amount_InvestmentCapital` | Funding viability. |
| Technology    | `Count_Business_Information`, `Percent_Household_WithInternetAccess`, `Count_Computer` | Portal Oradea readiness. |
| Energy        | `Annual_Consumption_Electricity`, `Annual_Emissions_GreenhouseGas`, `ElectricityPrice_Residential` | Infrastructure & sustainability. |
| Education     | `Percent_Person_CollegeGraduate`, `Count_School` | Talent analysis. |

### Use Cases for Janus
- **Portal Oradea TAM/SAM**: Pull `Count_Person` and `Percent_Household_WithInternetAccess` for `geoId/ROU_1` (Bihor county), combine with Eurostat SME counts to validate target user base.
- **EU funding compliance**: Retrieve `UnemploymentRate_Person` and `Amount_EconomicActivity_GrossValue` for Romania vs EU averages to justify structural funds proposals.
- **Compute infrastructure benchmarking**: Compare `Annual_Consumption_Electricity` for `country/ROU`, neighboring states, and EU to ensure data center capacity decisions align with energy availability.
- **Constitutional legitimacy**: Use `Count_Person` and `Median_Age_Person` to measure how a mission improves citizen welfare segments; log the supporting statistics in proposal audit trails.

### Best Practices
- Resolve human-readable names before hitting `observation`. Use the quick reference DCID table for priority regions (USA, Romania, EU-27, key cities).
- Request multiple facets when the statistic has multiple sources; choose the facet with latest date and provenance that matches mission requirements.
- For trend analysis, fetch 10+ years of data—plot locally using `pandas` and annotate with Groq summarisation for context.
- Cross-verify Data Commons values via Groq `web_search` citations, then feed the combined evidence into local llama deliberation.
- Cache high-value datasets in `/srv/janus/data/datacommons/*.json` with MD5 fingerprints to avoid repeated API hits during the same mission.

---

## 5. Oracle Selection Decision Tree

**Goal:** Choose the minimal-external-intelligence path that delivers trustworthy evidence while preserving sovereignty.

- **Start with the mission question.**  
  - If it demands real-world statistics → **Data Commons**.  
  - If it requires mathematical or physical derivation → **Wolfram Alpha**.  
  - If it requires fast synthesis, current news, or coding aid → **Groq**.  
  - If it is constitutional or philosophical → **local llama.cpp** only.

- **When to use Groq**  
  - ✅ Need sub-5-second reconnaissance or live web context.  
  - ✅ Require structured reasoning output for rapid drafting.  
  - ✅ Want sandboxed code checks or quick summarisation of repo searches.  
  - ❌ Avoid for deep constitutional reasoning, strategic commitments, or anything that can be done offline without losing mission velocity.

- **When to use Wolfram Alpha**  
  - ✅ Calculus, statistics, unit conversions, symbolic algebra.  
  - ✅ Thermals, power budgets, load calculations, probability distributions.  
  - ❌ Not for current events, narrative synthesis, or policy analysis.

- **When to use Data Commons**  
  - ✅ Demographics, economics, infrastructure metrics, historical trends.  
  - ✅ Comparative market validation and policy eligibility checks.  
  - ❌ Not for real-time feeds, predictive simulations, or qualitative judgments.

- **When to stay local (llama.cpp)**  
  - ✅ Constitutional deliberation, risk assessment, high-sensitivity strategy.  
  - ✅ Any time API quotas near exhaustion or network path is unreliable.  
  - ✅ Cross-check every external recommendation before execution.

- **Hybrid patterns**  
  1. *Scout → Deliberate*: Groq surfaces options, local llama debates tradeoffs.  
  2. *Compute → Interpret*: Wolfram supplies numbers, Groq explains, llama approves.  
  3. *Ground → Strategise*: Data Commons validates reality, Groq drafts proposal, llama aligns constitutionally.

---

## 6. Rate Limits & Cost Management

- **Groq**  
  - Hourly cap: 100 requests. Daily cap: 500 requests.  
  - Monitor counters via `dual_speed_brain`. Exponential backoff already configured.  
  - Strategy: batch related queries (e.g., gather all funding opportunities in a single `web_search`). Use `local_scout` and local llama for low-priority reconnaissance.

- **Wolfram Alpha**  
  - Wolfram’s free AppID tier allows ~2,000 queries/month; monitor usage via `/srv/janus/logs/wolfram_usage.jsonl` (create if absent).  
  - High-volume derivations should be cached locally; store inputs and plaintext results to prevent repeated charges.

- **Data Commons**  
  - Public key usage is currently permissive, but Google enforces soft throttling (~120 requests/minute).  
  - Prefer bulk POST requests retrieving multiple variables in one call; avoid polling loops.  
  - Cache datasets inside `/srv/janus/data/datacommons/` with metadata (DCIDs, variables, date range) to reuse in later missions.

- **Constitutional Principle: Efficiency in Resource Usage**  
  - Always ask: can local computation achieve the same result within the mission timeline?  
  - When in doubt, run the first pass locally, then use the Oracle to verify rather than discover.  
  - Log the reasoning for each external call to preserve auditability and cost justification.

---

## 7. Error Handling & Fallback Procedures

- **Groq Unavailable (`GroqUnavailableError`)**  
  - Automatic fallback: `DualSpeedCognition` re-routes to local llama.cpp.  
  - Operations action: check `GROQ_API_KEY`, network connectivity, and Groq status dashboard.  
  - Temporary mitigation: set `GROQ_TIMEOUT_SECONDS=15` and retry.

- **Groq 400 errors (`reasoning_effort`, `code_execution`)**  
  - Apply hotfixes described in §2.  
  - Until patched, use `fast_think` + local llama for reasoning, and local Python for code execution.

- **Wolfram timeout or 501**  
  - Log to `/srv/janus/logs/oracle_queries.jsonl` with `status="timeout"`.  
  - Retry with simpler phrasing or narrower assumptions.  
  - If persistent, switch to Groq’s compound `wolfram` wrapper or perform approximate calculation locally.

- **Data Commons HTTP 4xx/5xx**  
  - 400 “Must select 'variable' and 'entity'”: ensure POST payload contains `select` array and both DCIDs.  
  - 403/401: confirm API key and header. Keys expire annually—rotate via `apikeys.datacommons.org`.  
  - 429: exponential backoff (sleep 10s, then 30s); break large pulls into nightly batches.

- **Rate limit exceeded**  
  - Queue outstanding queries in `/srv/janus/queues/oracle_backlog.yaml`.  
  - Run local llama deliberation to decide if waiting is acceptable or an alternative approach is needed.

- **Network Failure**  
  - Trigger offline mode: switch `oracle_trinity.enabled=false` in config.  
  - Document the outage, reroute mission to local tools, and notify the Captain via UBOS CLI.

---

## 8. Constitutional Alignment Checklist

- **Truth over Comfort**  
  - Select oracles that deliver the most objective data available.  
  - Preserve raw outputs (JSON, plaintext) alongside summaries to prevent narrative drift.  
  - Cross-validate critical numbers with at least two independent sources (e.g., Wolfram + Data Commons).

- **Sovereignty above Dependency**  
  - Keep llama.cpp as the ultimate arbiter—every external result flows back into local deliberation.  
  - Maintain local mirrors of high-frequency data (cached Wolfram results, Data Commons exports).  
  - Document fallback plans before enabling new external services.

- **Velocity with Precision**  
  - Groq accelerates reconnaissance; do not shortcut constitutional diligence.  
  - Build automated unit tests for code that parses oracle responses to catch schema changes early.  
  - Include timing, cost, and provenance metadata in every log entry.

- **Transparency & Service**  
  - Every query logged to `/srv/janus/logs/oracle_queries.jsonl` with fields: timestamp, oracle, query, parameters, response hash, operator.  
  - Summaries written into mission logs must reference the original response IDs for reproducibility.  
  - Use oracles strictly to advance the Republic’s mission—no vanity queries, no untracked experimentation.

When the above conditions are satisfied, flip the integration flag, run the Example Mission (see companion document), and archive results to `03_OPERATIONS/vessels/localhost/logs/mission_archive.jsonl`. The forge remains sovereign, the Trinity aligned.

---

**End of Manual**
