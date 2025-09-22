# Book Onboarding Workflow

Use this checklist when adding a new foundational book to UBOS.

1. **Create Book Folder**
   - Copy the naming pattern `BookXX-<DescriptiveSlug>/` under `UBOS/SystemFundamentals/Books/`.
   - Add `README.md`, `source/`, and `ai-structured/` subdirectories.

2. **Ingest Raw Materials**
   - Place unmodified manuscripts, summaries, and helper scripts in `source/`.
   - Document contents in `source/README.md`.

3. **Bootstrap AI Structure**
   - Copy `Schema/templates/` into the book's `ai-structured/` area as needed.
   - Create `<book-short-name>/` inside `ai-structured/` containing:
     - `book.yaml`
     - `README.md`
     - `ROADMAP.md`
     - `CHAPTER_GUIDE.md`
     - `SPECKIT_HANDOFF.md`
     - `chapters/` skeleton
   - Update paths to reference the new book's `source/` directory.
   - Author a book-specific `tools/parse_book.py` (or equivalent) that:
     - Generates natural titles (trim trailing stop words) and multi-sentence descriptions for each idea.
     - Builds practices by reusing the shared prompt library while sourcing `source_refs` from `source/chapters/<id>/exercises.md`.
     - Normalises quotes (remove chapter headings, join multi-sentence fragments) and points them at `source/chapters/<id>/quotes.md`.
     - Includes helper functions for sentence casing, description enrichment, and chapter-headline filtering (see Books 02–04 for reference implementations).

4. **Record Mapping**
 - Add a `STRUCTURE_MAP.md` summarizing original vs. new locations.
  - Run `ai-structured/tools/generate_markdown_sources.py` to populate `source/chapters/` with normalized chapter text, key ideas, exercises, and quotes.

5. **Prepare Validation**
   - Populate `ai-structured/validation/` with schema and source check scripts (reuse existing utilities where possible).
   - Ensure the validation README lists the exact commands: `python3 parse_book.py`, `python3 build_aggregates.py`, `python3 export_for_agents.py`, `python3 validate_yaml.py`, `python3 check_sources.py`.

6. **Regenerate & Verify Outputs**
   - Run `python3 parse_book.py` to emit chapter YAML, ideas, practices, and quotes.
   - Rebuild aggregates (`python3 build_aggregates.py`) and agent exports (`python3 export_for_agents.py`).
   - Execute validation (`python3 validate_yaml.py`, `python3 check_sources.py`).
   - Spot-check at least one chapter end-to-end:
     - Idea titles read as complete phrases; descriptions add context beyond the one-liner.
     - Practices cite `exercises.md` rather than the main chapter file.
     - Quotes are fully capitalized sentences that exclude chapter headings or repeated titles.
     - No duplicate IDs or truncated slugs remain.

7. **Handoff to SpecsAgent**
   - Ensure ROADMAP and SPECKIT docs clarify expectations.
   - SpecsAgent (or equivalent automation) can rerun the deterministic tooling above as part of SpecKit planning/execution.

8. **Aggregate & Publish**
   - After automation, populate `chapters/all/` with aggregates (JSONL, indexes).
   - Verify validation passes and update status checkboxes in README files.

Repeat this workflow for each new book to keep the knowledge base consistent.
