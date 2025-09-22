#!/usr/bin/env python3
"""Generate aggregated JSONL files for Build the System."""

import json
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[6]
BOOK_ROOT = ROOT / "UBOS" / "SystemFundamentals" / "Books" / "Book03-The-Art-of-Strategic-Thinking"
AI_ROOT = BOOK_ROOT / "ai-structured" / "build-the-art-of-strategic-thinking"
CHAPTERS_ROOT = AI_ROOT / "chapters"
AGG_ROOT = CHAPTERS_ROOT / "all"


def iter_records(kind: str):
    for chapter_dir in CHAPTERS_ROOT.iterdir():
        if not chapter_dir.is_dir() or chapter_dir.name == "all":
            continue
        folder = chapter_dir / kind
        if not folder.exists():
            continue
        for path in sorted(folder.glob("*.yaml")):
            with path.open() as fh:
                data = yaml.safe_load(fh)
            data["path"] = path.relative_to(ROOT).as_posix()
            yield data


def write_jsonl(path: Path, records):
    with path.open("w") as fh:
        for record in records:
            fh.write(json.dumps(record, ensure_ascii=True) + "\n")


def main():
    AGG_ROOT.mkdir(parents=True, exist_ok=True)

    ideas = list(iter_records("ideas"))
    practices = list(iter_records("practices"))
    quotes = list(iter_records("quotes"))

    write_jsonl(AGG_ROOT / "ideas.jsonl", ideas)
    write_jsonl(AGG_ROOT / "practices.jsonl", practices)
    write_jsonl(AGG_ROOT / "quotes.jsonl", quotes)

    topic_index = {}
    for idea in ideas:
        for topic in idea.get("topics", []):
            topic_index.setdefault(topic, []).append(idea["id"])

    with (AGG_ROOT / "topic_index.json").open("w") as fh:
        json.dump(topic_index, fh, ensure_ascii=True, indent=2)


if __name__ == "__main__":
    main()
