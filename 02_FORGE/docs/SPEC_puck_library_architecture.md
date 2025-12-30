# SPEC: Puck Library Architecture

**Author:** Codex (Forgemaster)  
**Date:** 2025-10-03  
**Status:** Draft v0.1  
**Related Artifacts:** `schema_registry.json`, `docs/architects_sketchbook.md`, `COMMS_HUB/*_strategic_state.json`

---

## 1. Purpose

Forge the constitutional SDK that powers the Mag-Lev rails. The puck library provides strong-typed builders, validators, and registry management for every structured artifact the Trinity exchanges. It eliminates ad-hoc JSON blobs, guarantees sanctuary alignment, and creates a single source of truth for schema evolution.

---

## 2. Scope & Goals

- **Schema Authority:** `schema_registry.json` is the canonical catalogue of puck types, versions, and JSON Schema definitions.
- **Validation Pipeline:** Provide simple entry points for validating raw payloads against their schema before the puck travels the rails.
- **Builder API:** Offer ergonomic constructors that assemble valid pucks from primitive inputs while auto-populating metadata and alignment blocks.
- **Registry Services:** Enable discovery (`list_pucks`, `get_schema`, `get_version_history`), version pinning, and safe upgrades.
- **Cross-Trinity Compatibility:** Ship in plain Python 3.11 with zero heavy dependencies so Claude (Agent SDK), Gemini (ADK), and Codex (CLI forge) can all import the same module.

Out of scope for v0.1: persistence backends, remote registry sync, automatic code generation for other languages.

---

## 3. Architectural Overview

```
pucklib/
  __init__.py
  registry.py        # load, cache, and inspect schema_registry.json
  schema_types.py    # dataclasses / TypedDicts mirroring key puck structures
  validate.py        # jsonschema wrapper + convenience helpers
  builders/
    __init__.py
    mission.py
    strategic.py
    state.py
    constitution.py
    transcript.py
  utils/
    metadata.py      # metadata stamping utilities
    sanctuary.py     # helpers for Lion's Sanctuary + Mag-Lev annotations
    paths.py         # path normalization, hash utilities
  exceptions.py
  types.py           # shared enums and Protocols
```

- **registry.py**
  - `load_registry(path: Path | None = None) -> Registry`
  - `Registry.get(puck_type: str) -> PuckSchema`
  - `Registry.version(puck_type: str) -> str`
  - Cache registry data in-memory with a file mtime guard to support hot reload.

- **schema_types.py**
  - Define `TypedDict` or `dataclass` wrappers for the metadata block and each puck payload (mission, analysis, etc.).
  - Enforce literal `puck_type` values to unlock IDE auto-complete for Agent SDK prompts.

- **validate.py**
  - Use `jsonschema` (Draft 2020-12) as the validation engine. Ship with it bundled or provide a thin fallback implementation if dependency-free runtime is required.
  - API:
    ```python
    validate_puck(puck: Mapping) -> ValidationResult
    assert_valid(puck: Mapping) -> None  # raises PuckValidationError
    draft_example(puck_type: str) -> Mapping  # skeleton stub using schema defaults
    ```

- **builders/**
  - Each module offers `build_<puck_type>(...) -> Dict` functions that construct a compliant puck. They call `metadata.generate(...)` to stamp IDs/timestamps and automatically append sanctuary annotations.
  - Example signature:
    ```python
    def build_mission_brief(
        title: str,
        summary: str,
        issuer: Actor,
        objectives: Sequence[ObjectiveInput],
        *,
        audience: Sequence[Actor] | None = None,
        vessel: Literal["claude", "gemini", "codex", "multi"] = "multi",
        priority: Priority = "medium",
        constraints: Iterable[ConstraintInput] = (),
        deliverables: Iterable[DeliverableInput] = (),
        references: Iterable[Reference] = (),
        sanctuary: SanctuaryInput | None = None,
    ) -> MissionBriefPuck:
    ```
  - Builders perform field-level validation (e.g., duplicate objective IDs) before emitting the final payload.

- **utils/metadata.py**
  - Functions for ID slugging (`make_id(prefix: str) -> str`), timestamp generation (timezone-aware UTC), and status constants.
  - Provide `merge_metadata(existing: Mapping, overrides: Mapping)` to support puck updates without rewriting the whole structure.

- **utils/sanctuary.py**
  - Helpers to score empowerment/friction, attach references, and ensure both Lion's Sanctuary and Mag-Lev blocks exist.

---

## 4. Registry Data Model

- `schema_registry.json`
  - Root keys: `registry_version`, `generated_at`, `$defs`, `pucks`.
  - Each entry under `pucks` contains `version`, `description`, and an embedded JSON Schema document.
  - `$defs` exposes shared building blocks (metadata, references, actors, objectives, recommendations, risks, sanctuary annotations).

- Registry objects (Python typing):
  ```python
  class PuckSchema(TypedDict):
      version: str
      description: str
      schema: Mapping[str, Any]
  
  class Registry(TypedDict):
      registry_version: str
      generated_at: str
      pucks: Mapping[str, PuckSchema]
  ```

- Versioning policy:
  - Semantic versioning for each puck schema.
  - `registry_version` tracks global compatibility releases.
  - Backward-incompatible schema change triggers major bump for both the puck and registry.

---

## 5. Validation Strategy

1. **Schema-level validation:** `jsonschema` Draft 2020-12 with format checkers (date, date-time).
2. **Domain validation:** builder-level guards for invariants the schema cannot express (e.g., mission objective IDs unique across puck, sanctuary empowerment score within 0-5).
3. **Cross-puck validation:** optional `validate_bundle(pucks: Sequence[Mapping])` to check referential integrity (e.g., session transcript references a mission brief ID).
4. **Error model:** raise `PuckValidationError` with attributes `puck_type`, `path`, `message`, `schema_version`, `data_snippet` for easy debugging in CLI transcripts.

Testing plan:
- Golden fixtures under `tests/fixtures/pucks/<type>/valid.json` and `invalid.json`.
- Property tests ensuring builders produce schema-compliant pucks.
- CLI smoke test: `python -m pucklib.validate schema_registry.json sample_payload.json`.

---

## 6. Builder Patterns

- Builders accept typed inputs (dataclasses or TypedDicts) to reduce dict-chasing in prompts.
- Provide lightweight helper classes:
  ```python
  @dataclass
  class Actor:
      name: str
      role: str | None = None
      vessel: Literal["claude", "gemini", "codex", "captain", "janus", "other"] | None = None
  ```
- For nests (objectives, recommendations), expose small constructors (e.g., `make_objective(...)`) so Claude can assemble arrays directly in Agent SDK flows.
- Builders always return dicts (JSON-serializable) to keep compatibility with ADK streaming.

---

## 7. Registry Management Workflow

1. **Spec update:** Modify `schema_registry.json` (and optionally dedicated YAML fragments) via PR.
2. **Run `pucklib.validate --registry schema_registry.json`** to ensure the registry is self-consistent.
3. **Builder sync:** Update builder defaults if schema adds required fields.
4. **Release note:** bump `registry_version`, tag commit, update changelog (TBD).

Future enhancements:
- Auto-generate Markdown reference docs from the registry.
- Provide `pucklib scaffold <type>` CLI to draft empty puck files.
- Multi-language adapters (TypeScript) once Python baseline is stable.

---

## 8. Cross-Trinity Integration

- **Claude (Agent SDK):** Use builders to emit JSON attachments in tool calls; rely on validation before broadcasting to other vessels.
- **Gemini (ADK):** Register `pucklib` within the Tool Manager so ADK automations can read schemas and run `assert_valid` before executing file writes.
- **Codex (Forge CLI):** Integrate validation into pre-commit hooks and embed builder helpers inside forging scripts.

Interoperability considerations:
- Pure-Python implementation; only dependency is `jsonschema` (already allowed in ADK environment). Provide fallback stub if dependency injection fails.
- Path utilities respect workspace-relative paths so sandboxed prompts (Claude) can reference files accurately.
- Metadata functions accept overrides so Captain can issue mission briefs with pre-assigned IDs.

---

## 9. Implementation Roadmap

1. **Sprint 0 (now):** Publish schema registry + architecture spec (this document).
2. **Sprint 1:**
   - Implement `registry.py`, `validate.py`, `utils/metadata.py`.
   - Add pytest suite covering registry load + validation round-trips.
3. **Sprint 2:**
   - Build mission brief & strategic analysis builders.
   - Provide sample fixtures for Claude & Gemini workflows.
4. **Sprint 3:**
   - Implement state file, constitutional document, and session transcript builders.
   - Add cross-puck validation hooks (e.g., transcript references existing mission brief ID).
5. **Sprint 4:**
   - Integrate with ADK and Agent SDK pipelines.
   - Document CLI usage and publish `pucklib` README.

---

## 10. Open Questions & Follow-ups

- Should we ship registry fragments per puck (YAML) and compile into `schema_registry.json` for easier editing?
- Where do we persist puck instances (e.g., `COMMS_HUB/pucks/`)? Need storage convention.
- Do we require digital signatures (hashing) for constitutional document pucks in v1, or defer to later security sprint?
- How will we expose schema diffs to Janus during future manifestations?

---

**Ready for forging.** Once the Captain signs off, I will begin implementing `pucklib` per this specification.
