"""CLI adapter for the code_oracle MCP tool."""
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

from code_oracle import CodeOracle

LOGGER = logging.getLogger(__name__)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Inspect codebase dependencies using the Code Oracle.")
    parser.add_argument(
        "--command",
        required=True,
        choices=["get_dependencies", "get_dependents", "get_call_graph"],
        help="Code Oracle command to execute.",
    )
    parser.add_argument(
        "--target",
        required=True,
        help="Target module or function (e.g., 02_FORGE/scripts/daemon.py or scripts/daemon.py::main).",
    )
    parser.add_argument(
        "--workspace",
        type=Path,
        default=SCRIPT_DIR.parents[1],
        help="Workspace root containing the 02_FORGE directory.",
    )
    return parser.parse_args()


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(name)s: %(message)s")
    args = parse_args()
    workspace = args.workspace.resolve()
    oracle = CodeOracle(workspace_root=workspace)

    command = getattr(oracle, args.command)
    try:
        result = command(args.target)
    except Exception as exc:  # pragma: no cover - CLI safety
        LOGGER.error("Code Oracle command failed: %s", exc)
        raise SystemExit(1) from exc

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
