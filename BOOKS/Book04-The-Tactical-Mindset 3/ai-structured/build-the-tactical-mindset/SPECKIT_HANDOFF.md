# SpecKit Handoff — The Tactical Mindset

## Inputs
- Transcript: `UBOS/SystemFundamentals/Books/Book04-The-Tactical-Mindset/source/The_Tactical_Mindset.md`

## Outputs
- Chapter directories under `ai-structured/build-the-tactical-mindset/chapters/`.
- Aggregates in `chapters/all/`.
- Agent exports in `agent_exports/`.
- Chapter markdown + key ideas/exercises/quotes in `source/chapters/`.

## Recommended Spec Flow
1. `specify check`
2. `specify init --here --ai <agent>`
3. `/constitution` referencing schema constraints, topic vocab, validation scripts, and timestamp stripping.
4. `/specify` describing parsing goals and chapter outputs.
5. `/plan` covering parsing, YAML generation, markdown sync, validation, aggregation, exports.
6. `/tasks`
7. `/implement`

## Validation
- `ai-structured/validation/validate_yaml.py`
- `ai-structured/validation/check_sources.py`

Ensure `source_refs` point to `source/` and topics match `book.yaml`.
