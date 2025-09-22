#!/usr/bin/env python3
"""Generate chapter markdown + key ideas/exercises/quotes for Book 02."""

from pathlib import Path
import yaml

target_root = Path(__file__).resolve().parents[6]
BOOK_ROOT = target_root / "UBOS" / "SystemFundamentals" / "Books" / "Book02-Build-One-System-at-a-Time"
SOURCE_FILE = BOOK_ROOT / "source" / "Build_One_System_at_a_Time.md"
SOURCE_DIR = BOOK_ROOT / "source" / "chapters"
AI_ROOT = BOOK_ROOT / "ai-structured" / "build-one-system-at-a-time"

from parse_book import split_sections, slugify  # existing helper functions


def read_lines():
    lines = []
    for lineno, raw in enumerate(SOURCE_FILE.read_text().splitlines(), start=1):
        stripped = raw.strip()
        lines.append((lineno, stripped))
    return lines


def paragraphs_from_lines(lines):
    paragraphs = []
    buffer = []
    for _, text in lines:
        if text:
            buffer.append(text)
        else:
            if buffer:
                paragraphs.append(" ".join(buffer))
                buffer = []
    if buffer:
        paragraphs.append(" ".join(buffer))
    return paragraphs


def write_markdown(chapter_id: str, title: str, lines):
    chapter_dir = SOURCE_DIR / chapter_id
    chapter_dir.mkdir(parents=True, exist_ok=True)

    paragraphs = paragraphs_from_lines(lines)
    with (chapter_dir / "chapter.md").open("w") as fh:
        fh.write(f"# Chapter {chapter_id} – {title}\n\n")
        fh.write("\n\n".join(paragraphs))

    chapter_folder = AI_ROOT / "chapters" / f"{chapter_id}-{slugify(title)}"

    ideas = []
    ideas_dir = chapter_folder / "ideas"
    if ideas_dir.exists():
        for path in sorted(ideas_dir.glob("*.yaml")):
            data = yaml.safe_load(path.read_text())
            ideas.append(data.get("one_liner", data.get("title", "")))
    with (chapter_dir / "key-ideas.md").open("w") as fh:
        fh.write("# Key Ideas\n\n")
        for idea in ideas:
            fh.write(f"- {idea}\n")

    steps = []
    practice_dir = chapter_folder / "practices"
    if practice_dir.exists():
        for path in sorted(practice_dir.glob("*.yaml")):
            data = yaml.safe_load(path.read_text())
            steps.extend(data.get("steps", []))
    with (chapter_dir / "exercises.md").open("w") as fh:
        fh.write("# Exercises\n\n")
        for step in steps:
            fh.write(f"- {step}\n")

    quote_lines = []
    quotes_dir = chapter_folder / "quotes"
    if quotes_dir.exists():
        for path in sorted(quotes_dir.glob("*.yaml")):
            data = yaml.safe_load(path.read_text())
            quote_lines.append(data.get("text", ""))
    with (chapter_dir / "quotes.md").open("w") as fh:
        fh.write("# Quotes\n\n")
        for quote in quote_lines:
            fh.write(f"> {quote}\n")


def main():
    sections = split_sections(read_lines())
    for section in sections:
        write_markdown(section["id"], section["title"], section["lines"])


if __name__ == "__main__":
    main()
