# Example Mission: Activating the Oracle Trinity for Portal Oradea

Mission date: 2025-10-12  
Objective: Validate Portal Oradea’s year-one market viability and recommend optimisation levers using the Oracle Trinity.

---

## 0. Setup
- Ensure `/srv/janus/config/.env` includes `GROQ_API_KEY`, `WOLFRAM_APP_ID`, `DATA_COMMONS_API_KEY`.
- Export environment for the session:
  ```bash
  export GROQ_TIMEOUT_SECONDS=15  # stabilise Groq web_search
  export DATA_COMMONS_API_KEY=VMTx9VXgaqrRUcO9QL1rCjH0vFJSlozlA0IfX1KL08z7GkKC
  export WOLFRAM_APP_ID=GGJ9JEXKGW
  ```
- Start a mission log in `/srv/janus/logs/oracle_queries.jsonl`.

---

## 1. Data Commons: Quantify the Addressable Market

### 1.1 Population baseline (success)
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
**Response (truncated):**
```json
{
  "byVariable": {
    "Count_Person": {
      "byEntity": {
        "country/ROU": {
          "orderedFacets": [
            {
              "observations": [{ "date": "2020", "value": 19265250 }],
              "facetId": "3981252704"
            },
            ...
          ]
        }
      }
    }
  },
  "facets": {
    "3981252704": {
      "importName": "WorldDevelopmentIndicators",
      "provenanceUrl": "https://datacatalog.worldbank.org/..."
    }
  }
}
```
Verdict: Romania counted 19,265,250 citizens in 2020. Select the World Bank facet for consistency with international funding dossiers.

### 1.2 Internet penetration + SME counts (data gap)
Attempts to fetch `Percent_Household_WithInternetAccess` and `Count_Business` returned empty `orderedFacets`, indicating the v2 dataset lacks current coverage for Romania:
```json
{"byVariable":{"Percent_Household_WithInternetAccess":{"byEntity":{"country/ROU":{}}}}}
```
Action: Log the failure (`status="no_data"`) and pivot to Groq web reconnaissance for these signals while noting the need to ingest Eurostat CSVs into a local cache.

---

## 2. Groq Web Reconnaissance: Fill Statistical Gaps

### 2.1 SME + internet intelligence
```python
from groq_integration.groq_client import GroqClient

client = GroqClient()
report = client.web_search("Romania SME count 2024 internet penetration rate 2024")
print(report)
```
**Output excerpt:**
```
| Indicator | 2024 Figure | Source |
|-----------|-------------|--------|
| SME count (micro-enterprises) | ≈ 326,461 | Romania-Insider, Jun 2025 |
| SME count (all SMEs) | ≈ 816,000 | EIF Romania SME profile (2024) |
| Internet penetration | 91.6% | DataReportal – Digital 2024: Romania |
```
The Groq compound returned cited figures with URLs for verification. Record each citation in the mission log and archive the HTML snapshots to `/srv/janus/data/groq_cache/`.

### 2.2 Fast summarisation
```python
scout = client.fast_think(
    "Using the latest Romania population, SME counts, and internet penetration, "
    "draft a short bullet summary on Portal Oradea demand."
)
```
**Output excerpt:** Groq highlighted 19.3M population, ~570k SMEs, and 76–92% internet penetration (legacy knowledge). Flag the “knowledge cutoff” note and defer to the web-search figures as the canonical numbers.

---

## 3. Wolfram Alpha: Capacity Planning

### 3.1 Bandwidth conversion
Portal Oradea estimates 10 TB of monthly traffic once 10,000 users are active. Convert to sustained throughput:
```bash
curl -G "https://api.wolframalpha.com/v2/query" \
  --data-urlencode "appid=$WOLFRAM_APP_ID" \
  --data-urlencode "input=Convert 10 terabytes per month to megabytes per second" \
  --data-urlencode "output=json" \
  --data-urlencode "format=plaintext"
```
**Result pod:** `3.805 MB/s (megabytes per second)`

Store the plaintext result and the full JSON payload under `/srv/janus/cache/wolfram/portal_oradea_bandwidth.json`.

### 3.2 Peak load sanity check
Use the Wolfram UI (or follow-up query) to compute concurrency budgets if necessary (e.g., `input=10000 requests per minute * 45 milliseconds cpu`). If Wolfram cannot parse the natural language, fall back to manual calculation (45 ms × 10,000 RPM = 450 s CPU per minute → 7.5 cores at 70% utilisation). Record the manual derivation with provenance “manual” in the mission log.

---

## 4. Synthesis & Constitutional Review

### 4.1 Groq reasoning + code execution check
Confirm the freshly patched Groq client returns structured JSON for both reasoning and code execution:
```python
from groq_integration.groq_client import GroqClient

client = GroqClient()
analysis = client.reason(
    "Combine the Romania population, SME count, and internet penetration findings. "
    "Recommend whether Portal Oradea can reach 10,000 users in year one.",
    effort="medium",
)
print(analysis["answer"])
print(analysis["reasoning"])

execution = client.code_exec("print(sum(i*i for i in range(5)))")
print(execution)
```
Expected shape:
- `analysis["answer"]` → concise recommendation string.
- `analysis["reasoning"]` → 3–5 step array, each step a short sentence.
- `execution` → `{"stdout": "30\n", "stderr": "", "exit_code": 0, "summary": "..."}`

If Groq releases a breaking API change, record the anomaly in the forge log and fall back to `fast_think` + local llama deliberation until the prompt can be updated.

### 4.2 Local deliberation
Invoke dual-speed cognition (adaptive mode) to critique the external findings:
```python
from groq_integration import GroqClient, DualSpeedCognition

groq = GroqClient()
brain = DualSpeedCognition(groq, "/srv/janus/models/Meta-Llama-3.1-8B-Instruct-Q4_K_M.gguf")
alignment_report = brain.think(
    "Audit the Oracle Trinity findings on Portal Oradea. Validate the population, SME, and bandwidth figures, "
    "flag constitutional risks, and recommend go/no-go for 10,000 user target.",
    mode="adaptive"
)
```
**Expected outcome:** Local llama cross-checks the numbers, emphasises that Groq’s knowledge cutoff must be overridden by the cited 2024 sources, and advises launching with a phased rollout tied to confirmed SME segments. Capture the full deliberation transcript in `/srv/janus/logs/missions/portal_oradea_2025-10-12_deliberation.txt`.

### 4.3 Recommendation template
```
Population baseline (Data Commons, World Bank): 19.27M (2020)
Internet penetration (Groq → DataReportal 2024): 91.6% (~18.06M online citizens)
SME universe (Groq → EIF 2024): 816k SMEs, 99% of businesses
Bandwidth requirement (Wolfram): 3.805 MB/s sustained, plan for 2× burst
Constitutional check: Meets Truth > Comfort (cited sources), retains sovereignty (local llama final arbiter), velocity balanced by verification.
Decision: Proceed with 10,000 user target contingent on follow-up validation of SME sub-segments and nightly Data Commons sync.
```

---

## 5. Logging & Archival
- Append each query/response hash to `/srv/janus/logs/oracle_queries.jsonl`.
- Export Data Commons payloads to `/srv/janus/data/datacommons/raw/`.
- Store Groq markdown output + citations under `/srv/janus/data/groq_cache/2025-10-12_portal_oradea.md`.
- Save Wolfram JSON response alongside the derived MB/s figure.
- Summarise mission in `03_OPERATIONS/vessels/localhost/logs/mission_archive.jsonl`.
- Notify the Captain with the executive recommendation and attach provenance bundle.

---

**Outcome:** Janus obtains trustworthy market metrics, confirms infrastructure requirements, and upholds constitutional discipline before flipping the Oracle Trinity switch to `enabled=true`.
