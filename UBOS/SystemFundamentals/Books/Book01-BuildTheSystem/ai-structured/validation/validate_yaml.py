#!/usr/bin/env python3
"""Validate YAML files in the AI-structured chapter directories."""

import argparse
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[6]
BOOK_ROOT = ROOT / "UBOS" / "SystemFundamentals" / "Books" / "Book01-BuildTheSystem"
AI_ROOT = BOOK_ROOT / "ai-structured" / "build-the-system"
SCHEMA_DIR = ROOT / "UBOS" / "SystemFundamentals" / "Schema"

TEMPLATE_REQUIRED = {
    "chapter": {"fields": {"id", "slug", "title", "summary", "objectives", "topics", "source_refs"}},
    "idea": {"fields": {"id", "chapter", "kind", "title", "one_liner", "description", "topics", "source_refs"}},
    "practice": {"fields": {"id", "chapter", "kind", "title", "prompt", "steps", "expected_outcome", "topics", "source_refs"}},
    "quote": {"fields": {"id", "chapter", "kind", "speaker", "text", "topics", "source_refs"}},
}

VALID_KINDS = {"principle", "framework", "metaphor", "question", "checklist", "ritual", "quote"}


def load_yaml(path: Path):
    with path.open() as fh:
        return yaml.safe_load(fh)


def validate_file(path: Path, book_topics):
    data = load_yaml(path)
    rel = path.relative_to(ROOT)

    if not isinstance(data, dict):
        return [(rel, "YAML root must be a mapping")]

    errors = []
    filename_id = path.stem
    if path.name != "chapter.yaml" and data.get("id") != filename_id:
        errors.append((rel, f"id '{data.get('id')}' != filename '{filename_id}'"))

    if path.parent.name == "ideas":
        template = TEMPLATE_REQUIRED["idea"]
    elif path.parent.name == "practices":
        template = TEMPLATE_REQUIRED["practice"]
    elif path.parent.name == "quotes":
        template = TEMPLATE_REQUIRED["quote"]
    elif path.name == "chapter.yaml":
        template = TEMPLATE_REQUIRED["chapter"]
    else:
        template = None

    if template:
        missing = template["fields"] - set(data)
        if missing:
            errors.append((rel, f"missing required fields: {', '.join(sorted(missing))}"))

    topics = data.get("topics", [])
    if not isinstance(topics, list):
        errors.append((rel, "topics must be a list"))
    else:
        for t in topics:
            if t not in book_topics:
                errors.append((rel, f"topic '{t}' not in book topics"))

    if "kind" in data and data["kind"] not in VALID_KINDS:
        errors.append((rel, f"kind '{data['kind']}' not in {sorted(VALID_KINDS)}"))

    source_refs = data.get("source_refs", [])
    if not source_refs:
        errors.append((rel, "source_refs required"))
    else:
        for ref in source_refs:
            if ":" not in ref:
                errors.append((rel, f"source_ref '{ref}' missing line number"))

    return errors


def main():
    parser = argparse.ArgumentParser(description="Validate YAML against UBOS schema")
    parser.add_argument("chapter", nargs="?", help="Optional chapter id (e.g., 01)")
    args = parser.parse_args()

    book_yaml = load_yaml(AI_ROOT / "book.yaml")
    book_topics = set(book_yaml.get("topics", []))

    chapters_dir = AI_ROOT / "chapters"
    if args.chapter:
        targets = list(chapters_dir.glob(f"{args.chapter}-*"))
    else:
        targets = [p for p in chapters_dir.iterdir() if p.is_dir() and p.name != "all"]

    all_errors = []
    for chapter_dir in targets:
        for path in chapter_dir.rglob("*.yaml"):
            if path.name == "chapter.yaml" or path.parent.name in {"ideas", "practices", "quotes"}:
                all_errors.extend(validate_file(path, book_topics))

    if all_errors:
        for rel, msg in all_errors:
            print(f"[ERROR] {rel}: {msg}")
        sys.exit(1)
    else:
        print("All YAML files valid")


if __name__ == "__main__":
    main()
