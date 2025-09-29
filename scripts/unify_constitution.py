#!/usr/bin/env python3
"""
unify_constitution.py

Builds the Hydraulic Constitution knowledge graph from structured YAML files.

- Recursively scans the UBOS SystemFundamentals Books directory for YAML files.
- Parses each YAML document, prints its `id` and path, and adds a graph node.
- After ingestion, forges edges via `related_ids` and `dependencies`.
- Optionally renders a PNG visualization via Graphviz layout.

Usage:
  python scripts/unify_constitution.py \
      --root /Users/apple/Desktop/UBOS/UBOS/SystemFundamentals/Books [--visualize] [--out reports/hydraulic_constitution.png]

Defaults:
- Root: /Users/apple/Desktop/UBOS/UBOS/SystemFundamentals/Books
- Output: reports/hydraulic_constitution.png (created on --visualize)

Notes:
- Supports multi-document YAML files; prints one line per document to stdout.
- Uses yaml.safe_load_all; ensure PyYAML is installed (`pip install pyyaml`).
- Graph requires `networkx`. Visualization prefers Graphviz via `nx_pydot` with fallbacks.
"""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path
from typing import Iterator, Optional, Any

try:
    import yaml  # type: ignore
except Exception:  # pragma: no cover
    sys.stderr.write("Error: PyYAML is required. Install with `pip install pyyaml`\n")
    raise

try:
    import networkx as nx  # type: ignore
except Exception:  # pragma: no cover
    sys.stderr.write("Error: networkx is required. Install with `pip install networkx`\n")
    raise


DEFAULT_ROOT = Path("/Users/apple/Desktop/UBOS/UBOS/SystemFundamentals/Books")


def iter_yaml_files(root: Path) -> Iterator[Path]:
    """Yield all .yaml and .yml files under root recursively."""
    # Use os.walk vs rglob for explicit control and speed on large trees.
    for dirpath, _dirnames, filenames in os.walk(root):
        for name in filenames:
            # Case-insensitive match for safety
            lower = name.lower()
            if lower.endswith(".yaml") or lower.endswith(".yml"):
                yield Path(dirpath) / name


def normalize_id_list(value: Any) -> list[str]:
    """Normalize a value into a list of strings for ID fields.

    Accepts a string, list of strings, or returns empty for anything else.
    """
    if value is None:
        return []
    if isinstance(value, str):
        return [value]
    if isinstance(value, (list, tuple)):
        return [str(v) for v in value if isinstance(v, (str, int, float))]
    return []


class GraphBuilder:
    """Constructs a directed knowledge graph from YAML documents."""

    def __init__(self, quiet: bool = False) -> None:
        self.G = nx.DiGraph()
        self.id_index: dict[str, str] = {}  # id -> primary node key
        self.duplicates: list[tuple[str, str]] = []  # (dup_key, primary_id)
        self.placeholders: set[str] = set()
        self.stats = {"files": 0, "docs": 0, "errors": 0}
        self.quiet = quiet

    def _unique_dup_key(self, base_id: str, n: int) -> str:
        return f"{base_id}#dup{n}"

    def _fallback_key(self, path: Path, doc_index: int) -> str:
        return f"path:{path.resolve()}#{doc_index}"

    def add_document(self, doc: Any, path: Path, doc_index: int) -> str:
        """Create a node for a YAML document and return its node key."""
        self.stats["docs"] += 1
        abs_path = path.resolve()

        if isinstance(doc, dict):
            node_id = doc.get("id")
            attrs: dict[str, Any] = dict(doc)  # shallow copy of top-level fields
        else:
            node_id = None
            attrs = {"raw": doc}

        if node_id is None:
            key = self._fallback_key(abs_path, doc_index)
            attrs["missing_id"] = True
        else:
            # Ensure uniqueness of node key for duplicates, but keep primary mapping
            if node_id not in self.id_index and node_id not in self.G:
                key = str(node_id)
                self.id_index[str(node_id)] = key
            else:
                # Duplicate encountered; suffix a key but keep id_index pointing to the first
                i = 2
                key = self._unique_dup_key(str(node_id), i)
                while key in self.G:
                    i += 1
                    key = self._unique_dup_key(str(node_id), i)
                self.duplicates.append((key, str(node_id)))
                attrs["duplicate_of"] = str(node_id)

        attrs["path"] = str(abs_path)
        attrs["doc_index"] = doc_index

        # Add node with attributes
        self.G.add_node(key, **attrs)

        # Maintain stdout contract: print id + path per document (unless quiet)
        if not self.quiet:
            print(f"id={node_id} | path={abs_path}")
        return key

    def ensure_placeholder(self, target_id: str) -> str:
        """Ensure a placeholder node exists for a referenced but unknown id."""
        # If we already know a primary mapping for the id, use it
        if target_id in self.id_index:
            return self.id_index[target_id]

        # If node with exact key exists, return it
        if target_id in self.G:
            return target_id

        # Create a placeholder node with minimal attributes
        self.G.add_node(target_id, placeholder=True)
        self.placeholders.add(target_id)
        return target_id

    def forge_edges(self) -> None:
        """Iterate nodes and add directed edges for related_ids and dependencies."""
        for node, data in self.G.nodes(data=True):
            # Skip placeholder-only nodes; they won't define edges
            if data.get("placeholder") is True:
                continue

            # Resolve edge lists
            related = normalize_id_list(data.get("related_ids"))
            depends = normalize_id_list(data.get("dependencies"))

            # related edges
            for rid in related:
                target = self.id_index.get(rid) or self.ensure_placeholder(rid)
                if node != target:
                    self.G.add_edge(node, target, type="related")

            # dependency edges
            for dep in depends:
                target = self.id_index.get(dep) or self.ensure_placeholder(dep)
                if node != target:
                    self.G.add_edge(node, target, type="depends_on")

    def visualize(self, out: Path) -> bool:
        """Render the graph to a PNG. Returns True if successful."""
        out.parent.mkdir(parents=True, exist_ok=True)

        # Try Graphviz via nx_pydot for layout
        pos = None
        layout_used = None
        try:
            from networkx.drawing.nx_pydot import graphviz_layout  # type: ignore

            pos = graphviz_layout(self.G, prog="dot")
            layout_used = "graphviz"
        except Exception:
            # Fallback to spring layout
            try:
                pos = None  # late compute with spring_layout
                layout_used = "spring"
            except Exception:
                pass

        # Attempt matplotlib rendering
        try:
            import matplotlib
            matplotlib.use("Agg")  # headless
            import matplotlib.pyplot as plt

            if pos is None:
                pos = nx.spring_layout(self.G, seed=42)

            # Node styling
            placeholder_nodes = [n for n, d in self.G.nodes(data=True) if d.get("placeholder") is True]
            duplicate_nodes = [n for n, d in self.G.nodes(data=True) if d.get("duplicate_of")]
            regular_nodes = [n for n in self.G.nodes() if n not in placeholder_nodes and n not in duplicate_nodes]

            plt.figure(figsize=(16, 12))
            nx.draw_networkx_edges(self.G, pos, alpha=0.2, width=0.8)
            nx.draw_networkx_nodes(self.G, pos, nodelist=regular_nodes, node_color="#9ecae1", node_size=120)
            nx.draw_networkx_nodes(self.G, pos, nodelist=placeholder_nodes, node_color="#c7c7c7", node_size=90)
            nx.draw_networkx_nodes(self.G, pos, nodelist=duplicate_nodes, node_color="#fdd0a2", node_size=110)

            # Draw small labels for readability on dense graphs
            labels = {n: str(n) for n in regular_nodes[:150]}  # cap labels for density
            nx.draw_networkx_labels(self.G, pos, labels=labels, font_size=6)

            plt.axis("off")
            plt.tight_layout()
            plt.savefig(out, dpi=200)
            return True
        except Exception as e:
            # If matplotlib path failed, try DOT export + dot CLI
            try:
                from networkx.drawing.nx_pydot import write_dot  # type: ignore
                tmp_dot = out.with_suffix(".dot")
                write_dot(self.G, tmp_dot)

                import shutil, subprocess
                dot_bin = shutil.which("dot")
                if dot_bin:
                    subprocess.run([dot_bin, "-Tpng", str(tmp_dot), "-o", str(out)], check=True)
                    return True
                else:
                    sys.stderr.write("Graphviz 'dot' not found; cannot render PNG.\n")
            except Exception as e2:
                sys.stderr.write(f"Visualization failed: {e2}\n")
        return False


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Scan UBOS Books for YAML files and print their id and path."
        )
    )
    parser.add_argument(
        "--root",
        type=Path,
        default=DEFAULT_ROOT,
        help=(
            "Root directory to scan (defaults to UBOS/SystemFundamentals/Books)."
        ),
    )
    parser.add_argument(
        "--visualize",
        action="store_true",
        help="Render a PNG visualization to reports/hydraulic_constitution.png",
    )
    parser.add_argument(
        "--out",
        type=Path,
        default=Path("reports/hydraulic_constitution.png"),
        help="Output image path when using --visualize.",
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="Suppress per-document output (only show summary).",
    )
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    root: Path = args.root

    # Resolve to absolute for consistent output
    root = root.expanduser().resolve()
    if not root.exists() or not root.is_dir():
        sys.stderr.write(f"Error: root directory not found: {root}\n")
        return 2

    builder = GraphBuilder(quiet=args.quiet)

    for path in iter_yaml_files(root):
        builder.stats["files"] += 1
        abs_path = path.resolve()
        try:
            with path.open("r", encoding="utf-8") as f:
                docs = list(yaml.safe_load_all(f))
        except Exception as e:
            builder.stats["errors"] += 1
            sys.stderr.write(f"Failed to parse YAML: {abs_path} ({e})\n")
            continue

        # Empty YAML file still yields one printed entry with id=None
        if not docs:
            builder.add_document({}, abs_path, 0)
            continue

        for i, doc in enumerate(docs):
            builder.add_document(doc, abs_path, i)

    # Forge edges after all nodes are present
    builder.forge_edges()

    # Optionally visualize
    rendered = False
    if args.visualize:
        out_path: Path = args.out
        try:
            rendered = builder.visualize(out_path)
        except Exception as e:
            sys.stderr.write(f"Visualization error: {e}\n")

    # Summary to stderr to keep stdout parseable
    summary = (
        f"Scanned files: {builder.stats['files']}, documents: {builder.stats['docs']}, "
        f"errors: {builder.stats['errors']}, nodes: {builder.G.number_of_nodes()}, "
        f"edges: {builder.G.number_of_edges()}, placeholders: {len(builder.placeholders)}, "
        f"duplicates: {len(builder.duplicates)}"
    )
    if args.visualize:
        summary += f", visualize: {'ok' if rendered else 'skipped'}"
    sys.stderr.write(summary + "\n")
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main(sys.argv[1:]))
