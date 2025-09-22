# Build One System at a Time

Canonical machine-readable representation of *Transform Your Future: Learn to Build One System at a Time*.

Status:
- [x] Chapters 00-19 structured (ideas/practices/quotes) via curated regeneration (2025-02)
- [x] Aggregates generated
- [x] Validation scripts configured
- [x] Agent exports generated

Tooling:
- `tools/parse_book.py` converts the manuscript into chapter folders.
- `tools/build_aggregates.py` creates JSONL aggregates in `chapters/all/`.
- `tools/export_for_agents.py` produces quick-reference JSON bundles in `agent_exports/`.
- Validation scripts reside in `../validation/`.

Consult `SPECKIT_HANDOFF.md` before re-running automation.
