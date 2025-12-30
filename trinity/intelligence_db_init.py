from __future__ import annotations

import argparse
import sqlite3
from pathlib import Path

from trinity.config import load_configuration

DEFAULT_SCHEMA = Path(__file__).with_name("intelligence_schema.sql")


def initialise_database(db_path: Path | str | None = None, schema_path: Path | str | None = None) -> Path:
    """Create the intelligence database if it does not already exist."""
    paths, _ = load_configuration()
    resolved_db = Path(db_path).expanduser().resolve() if db_path else paths.memory_dir / "intelligence.db"
    resolved_db.parent.mkdir(parents=True, exist_ok=True)

    resolved_schema = Path(schema_path).expanduser().resolve() if schema_path else DEFAULT_SCHEMA
    if not resolved_schema.exists():
        raise FileNotFoundError(f"Schema file not found: {resolved_schema}")

    script = resolved_schema.read_text(encoding="utf-8")
    with sqlite3.connect(resolved_db) as connection:
        connection.execute("PRAGMA foreign_keys = ON;")
        connection.execute("PRAGMA journal_mode = WAL;")
        connection.executescript(script)
        connection.commit()
    return resolved_db


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Initialise intelligence database schema.")
    parser.add_argument("--db", type=Path, help="Path to intelligence.db (defaults to Trinity memory dir).")
    parser.add_argument("--schema", type=Path, help="Path to intelligence_schema.sql.")
    return parser.parse_args()


def main() -> None:
    args = _parse_args()
    db_path = initialise_database(args.db, args.schema)
    print(db_path)


if __name__ == "__main__":
    main()
