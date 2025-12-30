"""CLI adapter for the narrative_query MCP tool."""
from __future__ import annotations

import argparse
import json
import logging
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
PACKAGES_DIR = SCRIPT_DIR.parent / "packages"
if str(PACKAGES_DIR) not in sys.path:
    sys.path.insert(0, str(PACKAGES_DIR))

from narrative_warehouse import NarrativeQueryEngine

LOGGER = logging.getLogger(__name__)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Query the Narrative Warehouse semantic index.")
    parser.add_argument("--query", required=True, help="Natural language query to execute.")
    parser.add_argument(
        "--scope",
        action="append",
        default=None,
        help="Optional relative path prefix to constrain search scope (may be supplied multiple times).",
    )
    parser.add_argument(
        "--index-dir",
        type=Path,
        default=None,
        help="Directory containing the narrative index artefacts.",
    )
    parser.add_argument(
        "--top-k",
        type=int,
        default=5,
        help="Maximum number of results to return.",
    )
    return parser.parse_args()


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(name)s: %(message)s")
    args = parse_args()

    workspace = SCRIPT_DIR.parents[1]
    index_dir = args.index_dir or workspace / "03_OPERATIONS" / "vessels" / "localhost" / "state" / "narrative_warehouse.index"
    if not index_dir.exists():
        raise SystemExit(f"Index directory {index_dir} does not exist. Build the index with build_narrative_index.py first.")

    engine = NarrativeQueryEngine(index_dir=index_dir)
    results = engine.query(query=args.query, scope=args.scope, top_k=args.top_k)
    payload = {
        "query": args.query,
        "scope": args.scope or [],
        "results": [
            {
                "source_file": result.source_file,
                "content": result.content,
                "score": result.score,
            }
            for result in results
        ],
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
