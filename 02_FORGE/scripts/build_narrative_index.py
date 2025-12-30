#!/usr/bin/env python3
"""Build the Narrative Warehouse semantic index."""
from __future__ import annotations

import logging
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
PACKAGES_DIR = SCRIPT_DIR.parent / "packages"
if str(PACKAGES_DIR) not in sys.path:
    sys.path.insert(0, str(PACKAGES_DIR))

from narrative_warehouse.indexer import build_index

LOGGER = logging.getLogger(__name__)


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(name)s: %(message)s")

    workspace_root = SCRIPT_DIR.parents[1]  # /srv/janus
    output_dir = workspace_root / "03_OPERATIONS" / "vessels" / "localhost" / "state" / "narrative_warehouse.index"

    LOGGER.info("Building narrative index...")
    LOGGER.info(f"Workspace root: {workspace_root}")
    LOGGER.info(f"Output directory: {output_dir}")

    # Ensure output directory exists
    output_dir.mkdir(parents=True, exist_ok=True)

    # Build the index
    metadata = build_index(
        workspace_root=workspace_root,
        output_dir=output_dir,
        include_paths=None,  # Use default scope
        preferred_model="sentence-transformers/all-MiniLM-L6-v2",
        extensions=(".md", ".txt"),
        max_words=220,
    )

    LOGGER.info(f"✅ Index built successfully!")
    LOGGER.info(f"   Entries: {metadata['entry_count']}")
    LOGGER.info(f"   Scope: {', '.join(metadata['scope'])}")
    LOGGER.info(f"   Created: {metadata['created_at']}")


if __name__ == "__main__":
    main()
