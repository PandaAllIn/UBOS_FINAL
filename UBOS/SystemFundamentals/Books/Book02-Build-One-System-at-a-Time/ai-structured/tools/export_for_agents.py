#!/usr/bin/env python3
"""Produce lightweight agent-friendly exports from the aggregated JSONL files."""

import argparse

import json
import yaml
from pathlib import Path

ROOT = Path(__file__).resolve().parents[6]
BOOK_ROOT = ROOT / "UBOS" / "SystemFundamentals" / "Books" / "Book02-Build-One-System-at-a-Time"
AI_ROOT = BOOK_ROOT / "ai-structured" / "build-one-system-at-a-time"
AGG_ROOT = AI_ROOT / "chapters" / "all"
EXPORT_DIR = AI_ROOT / "agent_exports"


def ensure_exports_dir():
    EXPORT_DIR.mkdir(parents=True, exist_ok=True)


def load_jsonl(path: Path):
    with path.open() as fh:
        for line in fh:
            if line.strip():
                yield json.loads(line)


def export_summary():
    summary = {
        "chapters": [],
        "topics": json.loads((AGG_ROOT / "topic_index.json").read_text())
    }
    for chapter_dir in sorted((AI_ROOT / "chapters").iterdir()):
        if not chapter_dir.is_dir() or chapter_dir.name == "all":
            continue
        chapter_yaml = chapter_dir / "chapter.yaml"
        if chapter_yaml.exists():
            with chapter_yaml.open() as fh:
                summary["chapters"].append(yaml.safe_load(fh))
    (EXPORT_DIR / "summary.json").write_text(json.dumps(summary, indent=2))


def export_quick_lookup():
    ideas = list(load_jsonl(AGG_ROOT / "ideas.jsonl"))
    prompts = list(load_jsonl(AGG_ROOT / "practices.jsonl"))
    quotes = list(load_jsonl(AGG_ROOT / "quotes.jsonl"))

    (EXPORT_DIR / "ideas_quick.json").write_text(json.dumps(ideas, indent=2))
    (EXPORT_DIR / "practices_quick.json").write_text(json.dumps(prompts, indent=2))
    (EXPORT_DIR / "quotes_quick.json").write_text(json.dumps(quotes, indent=2))


def export_for_agents(targets):
    ensure_exports_dir()
    if not targets or "summary" in targets:
        export_summary()
    if not targets or "lookups" in targets:
        export_quick_lookup()


def main():
    parser = argparse.ArgumentParser(description="Create agent-friendly exports")
    parser.add_argument("targets", nargs="*", choices=["summary", "lookups"], help="Optional export set")
    args = parser.parse_args()
    export_for_agents(args.targets)


if __name__ == "__main__":
    main()
