# Build the System – Structuring Roadmap

This roadmap guides all AI agents that will convert the *Build the System* ebook into the canonical UBOS schema. Automation will eventually run through SpecKit once assets and validation rules are ready.

## Phase 0 — Orientation (COMPLETE)
- Survey source materials in `../source/` (`BuildTheSystem.md`, `docs/chapters/*`, derived summaries).
- Define shared schema and directory layout under `../../Schema/`.
- Document SpecKit expectations (`SPECKIT_HANDOFF.md`).

## Phase 1 — Chapter Template Finalization
**Owner:** Library Architect (this agent)
- Lock field definitions in `../../Schema/templates/`.
- Enumerate chapter coverage requirements (ideas, practices, quotes, optional frameworks).
- Prepare validation scripts (YAML schema check, topic whitelist, source reference resolver).
- Deliver: `validation/` utilities + instructions (to be added).

## Phase 2 — Chapter 01 Deep Pass
**Owner:** Library Architect → SpecsAgent
- Manually outline canonical ideas/practices/quotes for Chapter 01 using templates.
- Record mapping of source excerpts → idea IDs.
- Hand structured outline to SpecsAgent.
- SpecsAgent executes SpecKit flow to generate YAML + aggregates for Chapter 01.
- Deliver: populated `chapters/01-architecture/` with validated data.

## Phase 3 — Systematize Conversion
**Owner:** SpecsAgent
- Clone Chapter 01 spec for remaining chapters.
- Iterate `/specify → /plan → /tasks → /implement` per chapter.
- Generate aggregates after each chapter or in batches (ideas.jsonl, practices.jsonl, quotes.jsonl, topic_index.json).
- Ensure validation passes after every `/implement` run.

## Phase 4 — Cross-Book Expansion
**Owner:** Library Architect + SpecsAgent
- For new ebooks, replicate folder + metadata pattern under `UBOS/SystemFundamentals/Books/`.
- Update shared topic vocabulary if new concepts emerge (coordinate via schema change and validation update).
- Produce inter-book linkage specs (topic clusters, evolution graphs).

## Phase 5 — Maintenance & Evolution
**Owner:** Maintenance Agent (future)
- Monitor for schema changes, new chapters, or errata.
- Run validation suite as part of CI before committing generated assets.
- Keep `SPECKIT_HANDOFF.md` and `ROADMAP.md` synchronized.

## Role Glossary
- **Library Architect (this agent):** Designs schema, prepares outlines, ensures semantic accuracy.
- **SpecsAgent:** Uses SpecKit to codify tasks and produce deterministic outputs.
- **Validation Agent (optional):** Runs schema + consistency checks and reports diffs.

## Key Principles
1. **Source Fidelity:** Every record must cite canonical text in `source/`.
2. **Determinism:** No improvisation—Specs define accepted transformations.
3. **Scalability:** Schema must extend cleanly to future books without renaming fields.
4. **Observability:** Aggregated outputs enable downstream analytics without reprocessing prose.
5. **Version Safety:** Automation only adds or updates files inside `ai-structured/` per schema.

## Immediate Next Actions
1. Draft Chapter 01 outline mapping (ideas/practices/quotes) for SpecsAgent.
2. Implement validation scripts (`validation/validate_yaml.py`, `validation/check_sources.py`).
3. Review `CHAPTER_GUIDE.md` to confirm thematic coverage before structuring remaining chapters.
