#!/usr/bin/env python3
"""Verify that source_refs point to existing files within the source directory."""

import argparse
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[6]
BOOK_ROOT = ROOT / "UBOS" / "SystemFundamentals" / "Books" / "Book03-The-Art-of-Strategic-Thinking"
AI_ROOT = BOOK_ROOT / "ai-structured" / "build-the-art-of-strategic-thinking"
SOURCE_ROOT = BOOK_ROOT / "source"


def load_yaml(path: Path):
    with path.open() as fh:
        return yaml.safe_load(fh)


def parse_ref(ref: str):
    if ":" not in ref:
        return ref, None
    path, line = ref.rsplit(":", 1)
    try:
        line_no = int(line)
    except ValueError:
        line_no = None
    return path, line_no


def main():
    parser = argparse.ArgumentParser(description="Validate source_refs point to actual files")
    parser.add_argument("chapter", nargs="?", help="Optional chapter id filter (e.g., 01)")
    args = parser.parse_args()

    chapters_dir = AI_ROOT / "chapters"
    if args.chapter:
        targets = list(chapters_dir.glob(f"{args.chapter}-*"))
    else:
        targets = [p for p in chapters_dir.iterdir() if p.is_dir() and p.name != "all"]

    errors = []
    for chapter_dir in targets:
        for path in chapter_dir.rglob("*.yaml"):
            if path.name == "chapter.yaml" or path.parent.name in {"ideas", "practices", "quotes"}:
                data = load_yaml(path)
                for ref in data.get("source_refs", []) or []:
                    src_path, line_no = parse_ref(ref)
                    src_abs = (ROOT / src_path).resolve()
                    try:
                        src_abs.relative_to(SOURCE_ROOT.resolve())
                    except ValueError:
                        errors.append((path.relative_to(ROOT), f"source_ref '{ref}' not under source/"))
                        continue
                    if not src_abs.exists():
                        errors.append((path.relative_to(ROOT), f"source file '{src_path}' missing"))
                    elif line_no is not None:
                        with src_abs.open() as fh:
                            for idx, _ in enumerate(fh, start=1):
                                if idx == line_no:
                                    break
                            else:
                                errors.append((path.relative_to(ROOT), f"line {line_no} missing in '{src_path}'"))

    if errors:
        for rel, msg in errors:
            print(f"[ERROR] {rel}: {msg}")
        raise SystemExit(1)
    print("All source_refs valid")


if __name__ == "__main__":
    main()
