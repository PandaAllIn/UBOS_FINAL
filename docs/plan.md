# Blueprint: Hydraulic Constitution Graph (unify_constitution.py)

## Objective
Upgrade `scripts/unify_constitution.py` from a YAML scanner to a constitution graph builder that:
- Scans `UBOS/SystemFundamentals/Books/` recursively for YAML documents.
- Creates a directed knowledge graph (NetworkX) with one node per YAML document.
- Uses each document’s top-level `id` as the node identifier when present.
- Stores all remaining top‑level fields as node attributes (e.g., `title`, `description`, `kind`, `topics`, etc.).
- Adds directed edges based on `related_ids` and `dependencies` fields.
- Optionally visualizes the graph to `reports/hydraulic_constitution.png` using Graphviz layout.

## Dependencies
- Required:
  - `pyyaml` (YAML parsing via `yaml.safe_load_all`)
  - `networkx` (graph construction)
- Visualization (best-effort):
  - Preferred layout: `graphviz` via `networkx.nx_pydot.graphviz_layout` (requires `pydot` and Graphviz binaries installed)
  - Fallback layout: `networkx.spring_layout` + `matplotlib` (if available)
  - Last-resort: write a DOT file and attempt `dot -Tpng` if Graphviz is installed but matplotlib is not

The script should import visualization dependencies lazily to avoid hard failures when `--visualize` isn’t used.

## CLI
- `--root PATH` (Path): Root directory to scan. Default: `/Users/apple/Desktop/UBOS/UBOS/SystemFundamentals/Books`.
- `--visualize` (flag): If set, render a PNG to `reports/hydraulic_constitution.png`.
- `--out PATH` (Path): Output PNG path (default: `reports/hydraulic_constitution.png`).

Standard output retains the original per-document listing: `id=<val or None> | path=<absolute>`.
Summary counts (files, documents, errors, nodes, edges, placeholders, duplicates) are written to stderr.

## Data Model
- Node key:
  - Primary: `doc['id']` (string).
  - If missing: generate a stable fallback key based on path + document index (e.g., `path:<abs>#<i>`), and mark `missing_id=True`.
  - If duplicate `id` encountered: preserve the first as primary. Create additional nodes with suffixed keys (e.g., `id#dup2`) and mark `duplicate_of=<id>`. The edge resolver will target the primary by default.
- Node attributes:
  - `path` (absolute string)
  - `doc_index` (int within file)
  - `placeholder` (bool) for nodes created only because another node referenced them
  - All top-level YAML fields merged in (shallow copy). If document is not a dict, store it under `raw` attribute.

## Edge Construction
- After all nodes are created, iterate through node attributes to resolve:
  - `related_ids`
  - `dependencies`
- Normalize each to a list of strings. Accept string or list-of-strings. Ignore other types gracefully.
- For each target ID:
  - If a primary node exists for that ID, add `source -> target`.
  - Else create a placeholder node keyed by the raw ID (`placeholder=True`) and add the edge.
- Edge attributes:
  - `type`: `related` or `depends_on`.

## Visualization
- Only when `--visualize` is set:
  1. Ensure `reports/` exists.
  2. Try `nx.nx_pydot.graphviz_layout(G, prog='dot')` for positions.
  3. If unavailable, fall back to `spring_layout`. If matplotlib is missing but Graphviz binary exists, write DOT and shell out to `dot -Tpng`.
  4. Node styling:
     - placeholders: gray
     - duplicates: light orange
     - others: light blue
  5. Save PNG to `--out` path.

## Error Handling & Logging
- YAML parse failures: increment error counter and continue.
- Missing `id`: allowed; node is created with `missing_id=True` and fallback key.
- Duplicate `id`: keep first as primary, suffix others, record in `duplicates` list.
- Non-dict documents: allowed; captured under `raw`.
- All warnings and summary printed to stderr; stdout reserved for `id | path` listings for easy piping.

## Performance Considerations
- Use `os.walk` to stream files.
- Avoid holding large intermediate structures beyond what’s needed for graph edges.
- Only import heavy visualization modules when requested.

## Functions & Structure
- `iter_yaml_files(root: Path) -> Iterator[Path]`
- `normalize_id_list(value) -> list[str]` — accepts str or list-of-str
- `class GraphBuilder`:
  - `G: nx.DiGraph`
  - `id_index: dict[str, str]`  (id -> primary node key)
  - `duplicates: list[tuple[str, str]]`  (dup_key, primary_id)
  - `placeholders: set[str]`
  - `stats`: counts (files, docs, errors)
  - `add_document(doc, path, doc_index) -> str` — creates node, returns node key
  - `forge_edges() -> None` — iterates nodes, adds edges based on `related_ids` and `dependencies`
  - `visualize(out: Path) -> bool` — renders PNG; returns True on success
- `main(argv) -> int` handles args, scanning, building, optional visualization, and prints summary.

## Edge Cases
- Multi-document YAML files: each doc becomes its own node (`doc_index` identifies ordering).
- `related_ids`/`dependencies` with mixed or invalid types: ignore non-string entries.
- Extremely large graphs: position calculation may be slow; spring layout fallback still works but may be heavy. Leave tuning for future.

## Future Enhancements (not in scope now)
- `--json` manifest export of nodes/edges.
- `--graphml` or `--gexf` exports for downstream tools.
- Strict ID uniqueness validation with a `--fail-on-duplicate` flag.
- Schema validation for known node kinds.

