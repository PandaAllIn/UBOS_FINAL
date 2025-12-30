# Data Commons Quick Reference

Location: `/srv/janus/docs/oracles/datacommons_quick_reference.md`  
Last updated: 2025-10-12

## Essentials
- **API Key:** `DATA_COMMONS_API_KEY=VMTx9VXgaqrRUcO9QL1rCjH0vFJSlozlA0IfX1KL08z7GkKC`
- **Endpoint Root:** `https://api.datacommons.org/v2/`
- **Authentication:** `X-API-Key` header (GET currently returns HTTP 415; use POST)
- **Primary Services:** `observation`, `stat/value`, `stat/series`, `resolve`, `node`
- **Log File:** `/srv/janus/logs/oracle_queries.jsonl` (`oracle="datacommons"`)

## Priority DCIDs
| Region | DCID | Notes |
|--------|------|-------|
| Romania (country) | `country/ROU` | National aggregates |
| Bihor County | `wikidataId/Q79968` or `nuts/RO111` | Portal Oradea base |
| Oradea City | `wikidataId/Q1723` | Urban statistics |
| European Union | `wikidataId/Q458` | EU27 aggregates |
| United States | `country/USA` | Benchmarking |
| California | `geoId/06` | GPU Studio comparative data |
| Cluj-Napoca | `wikidataId/Q212272` | Romanian tech cluster |

## Variable Shortlist
| Category | DCID | Description |
|----------|------|-------------|
| Demographics | `Count_Person` | Population |
| Demographics | `Median_Age_Person` | Median age |
| Demographics | `Count_Household` | Households |
| Economics | `Amount_EconomicActivity_GrossValue` | Gross value added |
| Economics | `UnemploymentRate_Person` | Unemployment %
| Economics | `Median_Income_Person` | Personal income |
| Technology | `Percent_Household_WithInternetAccess` | Connectivity |
| Technology | `Count_Business_Information` | ICT businesses |
| Energy | `Annual_Consumption_Electricity` | Electricity use |
| Energy | `Annual_Emissions_GreenhouseGas` | GHG emissions |
| Education | `Percent_Person_CollegeGraduate` | Education level |

## Workflow Cheat Sheet
1. **Resolve human names → DCIDs**
   ```bash
   curl -s -X POST \
     -H "X-API-Key: $DATA_COMMONS_API_KEY" \
     https://api.datacommons.org/v2/resolve \
     -d '{"nodes":["Oradea"],"property":"<-name"}'
   ```
   Result includes `wikidataId/Q1723`.

2. **Fetch observation snapshot**
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

3. **Time series (Python)**
   ```python
   import os, requests

   payload = {
       "entity": {"dcids": ["country/ROU"]},
       "variable": {"dcids": ["Percent_Household_WithInternetAccess"]},
       "select": ["date", "value", "entity", "variable"],
       "orderBy": "date",
       "limit": 30
   }
   resp = requests.post(
       "https://api.datacommons.org/v2/observation",
       headers={"X-API-Key": os.environ["DATA_COMMONS_API_KEY"]},
       json=payload,
       timeout=15,
   )
   series = resp.json()["byVariable"]["Percent_Household_WithInternetAccess"]["byEntity"]["country/ROU"]["orderedFacets"][0]["observations"]
   ```

4. **Multiple variables in one call**
   ```json
   {
     "entity": { "dcids": ["wilidataId/Q79968"] },
     "variable": { "dcids": ["Count_Person", "UnemploymentRate_Person", "Amount_EconomicActivity_GrossValue"] },
     "select": ["entity", "variable", "date", "value"],
     "orderBy": "date",
     "limit": 5
   }
   ```
   *Tip: iterate `orderedFacets` to pick the source with freshest `latestDate`.*

## Response Anatomy
```json
{
  "byVariable": {
    "Count_Person": {
      "byEntity": {
        "country/ROU": {
          "orderedFacets": [
            {
              "facetId": "3981252704",
              "observations": [
                { "date": "2020", "value": 19265250 }
              ]
            }
          ]
        }
      }
    }
  },
  "facets": {
    "3981252704": {
      "importName": "WorldDevelopmentIndicators",
      "observationPeriod": "P1Y",
      "provenanceUrl": "https://datacatalog.worldbank.org/..."
    }
  }
}
```

## Troubleshooting
- **415 Unsupported Media Type (GET)**: switch to `POST` with JSON payload + `X-API-Key` header.
- **400 “Must select 'variable' and 'entity'”**: ensure `select` array includes both strings.
- **Empty `orderedFacets`**: dataset unavailable—try broader entity (country) or alternative variable.
- **429 rate limit**: exponential backoff (10s → 30s → 60s), reduce `limit`, or schedule nightly sync.
- **Inconsistent values across facets**: choose facet whose `importName` matches mission requirement (Eurostat vs World Bank). Document the choice.

## Logging Template
```json
{
  "timestamp": "2025-10-12T14:19:55Z",
  "oracle": "datacommons",
  "entity": "country/ROU",
  "variable": "Count_Person",
  "date_range": ["2015", "2020"],
  "facet": "WorldDevelopmentIndicators",
  "status": "ok",
  "response_sha256": "0f58a7..."
}
```

## Operational Tips
- Keep a local DCID registry at `/srv/janus/data/datacommons/dcid_catalog.yaml`.
- Cache important time series under `/srv/janus/data/datacommons/cache/<entity>_<variable>.json`.
- Layer Groq citations on top of Data Commons numbers for context before presenting to humans.
- Validate mission-critical figures with a second dataset (Eurostat vs OECD) to reinforce Truth over Comfort.
- Always conclude with llama.cpp review to ensure the statistical interpretation aligns with constitutional intent.

