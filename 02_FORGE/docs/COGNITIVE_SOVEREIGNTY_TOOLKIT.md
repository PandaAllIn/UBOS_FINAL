# Cognitive Sovereignty Toolkit

This document captures the operational details for the two core tools that enable
constitutional context streaming for the Trinity vessels.

## Narrative Warehouse Query Engine (`narrative_query`)

### Purpose
- Provides Claude with focused access to constitutional, strategic, and doctrinal material.
- Replaces bulk ROADMAP/constitution loading with semantic retrieval of the exact passages needed for the current directive.

### Index Construction
```bash
python3 02_FORGE/scripts/build_narrative_index.py \
  --max-words 200 \
  --scope 00_CONSTITUTION \
  --scope 01_STRATEGY \
  --scope 02_FORGE/docs
```
- Default index location: `03_OPERATIONS/vessels/localhost/state/narrative_warehouse.index/`
- Falls back to a deterministic hashing encoder if `sentence-transformers` is not installed.
- Chunking limit is configurable via `--max-words`.

### Query Usage
```bash
python3 02_FORGE/scripts/narrative_query_tool.py \
  --query "Explain the Lion's Sanctuary doctrine" \
  --top-k 4 \
  --scope 00_CONSTITUTION
```
- Returns JSON with ranked passages (source path, excerpt, cosine score).
- Optional `--scope` arguments constrain results to selected territories.

## Codebase Oracle (`code_oracle`)

### Purpose
- Gives Codex a structural understanding of the codebase before touching a line of code.
- Surfaces imports, dependency chains, and inbound/outbound call relationships for modules and functions.

### Commands
```bash
# Module-level dependency view
python3 02_FORGE/scripts/code_oracle_tool.py \
  --command get_dependencies \
  --target 02_FORGE/scripts/daemon.py

# Function-level call graph
python3 02_FORGE/scripts/code_oracle_tool.py \
  --command get_call_graph \
  --target 02_FORGE/scripts/daemon.py::run_service
```
- Available commands: `get_dependencies`, `get_dependents`, `get_call_graph`.
- Targets use repo-relative paths with optional `::qualname` for functions/methods.
- Analyzer gracefully skips malformed/generated files and reports them in stderr.

### Output Highlights
- Dependencies distinguish between internal modules (indexed files) and external imports.
- Function graphs provide inbound/outbound call stacks plus unresolved identifiers for manual inspection.
- Results are JSON payloads ready for MCP transport.

## Operational Notes
- Both tools add their client packages under `02_FORGE/packages/`.
- CLI adapters live in `02_FORGE/scripts/` and inject the packages directory at runtime.
- Generated artefacts (embeddings, JSONL metadata) live under `03_OPERATIONS/vessels/localhost/state/`.
- Subsequent MCP integration only needs to wrap these CLIs or import the packages directly.
