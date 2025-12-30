---
type: dashboard
category: semantic_search
created: 2025-11-20
tags: [dashboard, smart-connections, semantic]
---

# 🧠 Pattern Hunter Dashboard

Smart Connections surfaces precedent across 8.9k notes. Use the canned prompts below or drop your own inside the code blocks.

> **Usage:** Place cursor inside a code block, run `Smart Connections: Run codeblock` (Cmd/Ctrl+P), then review results ≥0.70 score. All blocks exclude archives + trash by default and cap at 20 hits.

## 1. Constitutional Alignment

````smart-connections
search: How do we ensure constitutional alignment?
results_limit: 20
score_threshold: 0.7
exclude_filter: 99_ARCHIVES,.trash
````

## 2. Successful Grant Patterns

````smart-connections
search: What makes grant proposals successful?
results_limit: 20
score_threshold: 0.7
exclude_filter: 99_ARCHIVES,.trash
include_filter: 01_STRATEGY/grant_pipeline
````

## 3. Trinity Coordination

````smart-connections
search: Trinity coordination mechanisms
results_limit: 20
score_threshold: 0.7
exclude_filter: 99_ARCHIVES,.trash
include_filter: trinity
````

## Notes
- Adjust `include_filter` / `exclude_filter` per mission.
- Scores appear next to each hit; tag ones ≥0.80 in your working notes for fast recall.
- Combine with [[_VIEWS/PHILOSOPHY_GRAPH|Philosophy Graph]] to trace lineage visually.
