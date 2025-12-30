# SpecKit Handoff Notes — Book 02

## Expectations
- Input manuscript: `UBOS/SystemFundamentals/Books/Book02-Build-One-System-at-a-Time/source/Build_One_System_at_a_Time.md`.
- Outputs follow the same schema as Book 01 inside `ai-structured/build-one-system-at-a-time/chapters/*`.
- Automation must produce deterministic YAML files: `chapter.yaml`, `ideas/*.yaml`, `practices/*.yaml`, `quotes/*.yaml`, plus aggregated JSONL and agent exports.

## Recommended Workflow
1. `specify check`
2. `specify init --here --ai <agent>` (if required)
3. `/constitution` referencing schema compliance, topic vocabulary, and validation scripts reused from Book 01.
4. `/specify` describing the parsing/generation goals for Book 02.
5. `/plan` detailing architecture for parsing markdown, generating YAML, running validation, and building aggregates/exports.
6. `/tasks` enumerating actionable steps (parse manuscript, generate chapters, validate, aggregate, export).
7. `/implement` executing the plan.

## Validation
- Reuse Book 01 validation scripts (copy or import) into `../validation/` before running automation.
- Ensure topic tags come from `book.yaml > topics` and `source_refs` reference the Book 02 manuscript lines.

## Deliverables
- Populated chapter directories for `00`–`19`.
- Aggregates under `chapters/all/`.
- Agent exports under `agent_exports/`.
- Updated `README.md` status checkboxes.

Document any deviations or additional tooling requirements here for future runs.
