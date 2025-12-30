# Build the System

Canonical machine-readable representation of *Build the System*. Chapter folders follow the shared schema in `../../../Schema/SCHEMA.md`.

Status:
- [x] Chapters 01-20 structured (ideas/practices/quotes)
- [x] Aggregates generated
- [x] Validation scripts defined

Tooling:
- `tools/generate_chapters.py` regenerates chapter folders (use `--force` to overwrite).
- `tools/build_aggregates.py` creates `chapters/all/*.jsonl` and the topic index.
- Validation lives in `../validation/` (`validate_yaml.py`, `check_sources.py`).

Agents should consult `SPECKIT_HANDOFF.md` before creating specs.
