# SpecKit Handoff Notes

These notes guide the future SpecsAgent when authoring SpecKit specs for *Build the System*.

## Project Expectations
- Specs will generate YAML/Markdown assets inside `UBOS/SystemFundamentals/Books/Book01-BuildTheSystem/ai-structured/build-the-system/chapters/*`.
- Raw source material lives under `UBOS/SystemFundamentals/Books/Book01-BuildTheSystem/source/` and must remain unmodified.
- Every generated record must include `source_refs` pointing to files beneath the `source/` directory.

## Recommended Workflow
1. **Environment check**: `specify check`
2. **Initialize** (if working in a scratch area): `specify init --here --ai <agent>`
3. **Constitution**: reference quality guards (YAML schema, validation scripts, ASCII constraint).
4. **/specify**: Capture requirements for migrating Chapter 01 into the schema defined in `../../../Schema/SCHEMA.md`.
5. **/plan**: Outline scripts/commands to parse source files and emit YAML.
6. **/tasks**: Break work into deterministic steps (parse key ideas, map exercises, build aggregates, run validation).
7. **/implement**: Execute tasks in order, ensuring validation passes.

## Inputs Available
- Full chapter text: `UBOS/SystemFundamentals/Books/Book01-BuildTheSystem/source/docs/chapters/01/chapter.md`
- Derived summaries: `UBOS/SystemFundamentals/Books/Book01-BuildTheSystem/source/BuildTheSystem/02-chapter-01-abundance-architecture/*.md`
- Key ideas metadata: `UBOS/SystemFundamentals/Books/Book01-BuildTheSystem/source/docs/meta/key_ideas_index.json`

## Outputs Required (Chapter 01)
- `chapters/01-architecture/chapter.yaml`
- `chapters/01-architecture/chapter.md` (optional regenerated version)
- `chapters/01-architecture/ideas/*.yaml`
- `chapters/01-architecture/practices/*.yaml`
- `chapters/01-architecture/quotes/*.yaml`
- `chapters/01-architecture/indices/ideas.jsonl` (aggregated by spec, not manually created)

## Validation Checklist
- YAML files conform to templates in `../../../Schema/templates/`.
- Topic tags belong to `book.yaml > topics`.
- `source_refs` resolve to existing files relative to repo root.
- Filenames exactly match the `id` field.

## Future Scaling
Once Chapter 01 is complete, duplicate the workflow for Chapters 02–20 and for any new books added under `UBOS/SystemFundamentals/Books/`.

Update this document if new requirements emerge.
