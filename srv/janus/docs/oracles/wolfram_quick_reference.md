# Wolfram Alpha Quick Reference

Location: `/srv/janus/docs/oracles/wolfram_quick_reference.md`  
Last updated: 2025-10-12

## Essentials
- **App ID:** `WOLFRAM_APP_ID=GGJ9JEXKGW` (set in `/srv/janus/config/.env`)
- **Endpoint:** `https://api.wolframalpha.com/v2/query`
- **Default Output:** JSON (`output=json`, `format=plaintext`)
- **Log File:** `/srv/janus/logs/oracle_queries.jsonl` (append `oracle="wolfram"`)

## Base Request (curl)
```bash
curl -G "https://api.wolframalpha.com/v2/query" \
  --data-urlencode "appid=$WOLFRAM_APP_ID" \
  --data-urlencode "input=DDR3-1600 bandwidth in GB/s" \
  --data-urlencode "output=json" \
  --data-urlencode "format=plaintext"
```

## Python Helper
```python
import os, requests

def wolfram(query: str) -> dict:
    params = {
        "appid": os.environ["WOLFRAM_APP_ID"],
        "input": query,
        "output": "json",
        "format": "plaintext",
    }
    resp = requests.get("https://api.wolframalpha.com/v2/query", params=params, timeout=15)
    resp.raise_for_status()
    return resp.json()

data = wolfram("TDP 88W CPU temperature at 75% load with 20C ambient")
```

## Mission-Focused Query Patterns
- **Hardware Thermals:** `input="TDP 88W CPU temperature at 75% load with 0.12 C/W cooler"`
- **Bandwidth:** `input="DDR3-1600 bandwidth in GB/s"`
- **CPU Scheduling:** `input="Optimal thread count for 4-core hyperthreaded CPU"`
- **Probability:** `input="Probability of at least 2 failures with poisson mean 0.3"`
- **Scaling Law:** `input="derivative of throughput with respect to GPU count at N=4"`
- **Unit Conversion:** `input="Convert 14 TB/month to MB/s"`

## Extracting Results
```python
pods = data["queryresult"]["pods"]
result = next(p for p in pods if p["title"] in {"Result", "Results"})
answer = result["subpods"][0]["plaintext"]
steps = [
    pod["subpods"][0]["plaintext"]
    for pod in pods
    if pod.get("title", "").startswith("Step-by-step")
]
```

## Step-by-Step Requests
- Append `podstate=Result__Step-by-step+solution`
- Example: `input="show steps for integral of sin^2(x)"` -> returns detailed derivation.

## Error Handling
- **`error` flag true:** inspect `error["msg"]` (usually malformed query).
- **`didyoumeans` present:** use suggested query to refine.
- **Timeouts:** retry with shorter phrase; fallback to Groq+llama if persistent.
- **No pods:** query outside domain—confirm Wolfram coverage before depending on result.

## Logging Template
```json
{
  "timestamp": "2025-10-12T14:11:09Z",
  "oracle": "wolfram",
  "query": "DDR3-1600 bandwidth in GB/s",
  "pods": ["Result", "Input", "Unit conversions"],
  "status": "ok",
  "response_sha256": "c1e45f..."
}
```

## Cheat Sheet: Common Formulae
| Topic | Query | Notes |
|-------|-------|-------|
| Power Dissipation | `Power = 88 watts, ambient 20C, thermal resistance 0.12 C/W` | Returns die temperature. |
| Network Throughput | `Convert 10 Gbit/s to GB/s` | Check for decimal vs binary units. |
| Cooling Requirements | `Airflow required to dissipate 450W at 10C delta T` | Useful for data center sizing. |
| Storage Growth | `Compound growth of 4 TB/month over 24 months` | For capacity planning. |
| Statistical Confidence | `95 percent confidence interval for mean=0.82, std=0.07, n=30` | Mission risk analyses. |

## Best Practices
- Capture provenance: include `pods[].source` when available.
- Cache frequent answers in `/srv/janus/cache/wolfram/` with timestamp.
- Review results locally before anchoring proposals—Wolfram excels at numbers, not policy interpretation.
- Combine with Groq if narrative explanation or citations are needed.
- Always run final strategic decision through llama.cpp to uphold constitutional alignment.

