# SpecKit Handoff — The Art of Strategic Thinking

## Inputs
- Transcript: `UBOS/SystemFundamentals/Books/Book03-The-Art-of-Strategic-Thinking/source/The_Art_of_Strategic_Thinking.md`

## Outputs
- Structured chapter folders under `ai-structured/build-the-art-of-strategic-thinking/chapters/`.
- Aggregated JSONL exports in `chapters/all/`.
- Agent-friendly JSON bundles in `agent_exports/` (to be generated after aggregation).

## Recommended Spec Flow
1. `specify check`
2. `specify init --here --ai <agent>` (optional workspace)
3. `/constitution` referencing schema compliance, timestamp stripping, and topic vocabulary alignment.
4. `/specify` describing transcript parsing goals and outputs.
5. `/plan` detailing parsing, YAML generation, validation, aggregation, and exports.
6. `/tasks` enumerating steps.
7. `/implement` executing `parse_book.py`, `build_aggregates.py`, `export_for_agents.py`, then running validation.

## Validation
- `ai-structured/validation/validate_yaml.py`
- `ai-structured/validation/check_sources.py`

Ensure topics remain within `book.yaml > topics` and every `source_ref` points inside `source/`.
