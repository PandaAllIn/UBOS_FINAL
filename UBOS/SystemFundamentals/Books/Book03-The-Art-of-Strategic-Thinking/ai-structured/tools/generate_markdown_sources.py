#!/usr/bin/env python3
"""Generate chapter markdown + key ideas/exercises/quotes for Book 03."""

from pathlib import Path
import yaml

from parse_book import load_entries, split_sections, slugify

ROOT = Path(__file__).resolve().parents[6]
BOOK_ROOT = ROOT / "UBOS" / "SystemFundamentals" / "Books" / "Book03-The-Art-of-Strategic-Thinking"
AI_ROOT = BOOK_ROOT / "ai-structured" / "build-the-art-of-strategic-thinking"
SOURCE_DIR = BOOK_ROOT / "source" / "chapters"


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


def write_markdown_chapter(chapter_id: str, title: str, lines):
    chapter_dir = SOURCE_DIR / chapter_id
    chapter_dir.mkdir(parents=True, exist_ok=True)

    paragraphs = paragraphs_from_lines(lines)
    chapter_md = chapter_dir / "chapter.md"
    with chapter_md.open("w") as fh:
        fh.write(f"# Chapter {chapter_id} – {title}\n\n")
        fh.write("\n\n".join(paragraphs))

    ideas_dir = AI_ROOT / "chapters" / f"{chapter_id}-{slugify(title)}" / "ideas"
    key_ideas_md = chapter_dir / "key-ideas.md"
    bullets = []
    if ideas_dir.exists():
        for idea_path in sorted(ideas_dir.glob("*.yaml")):
            data = yaml.safe_load(idea_path.read_text())
            bullets.append(data.get("one_liner", data.get("title", "")))
    with key_ideas_md.open("w") as fh:
        fh.write("# Key Ideas\n\n")
        for bullet in bullets:
            fh.write(f"- {bullet}\n")

    practice_dir = AI_ROOT / "chapters" / f"{chapter_id}-{slugify(title)}" / "practices"
    exercises_md = chapter_dir / "exercises.md"
    steps = []
    if practice_dir.exists():
        for practice_path in sorted(practice_dir.glob("*.yaml")):
            data = yaml.safe_load(practice_path.read_text())
            for step in data.get("steps", []):
                steps.append(step)
    with exercises_md.open("w") as fh:
        fh.write("# Exercises\n\n")
        for step in steps:
            fh.write(f"- {step}\n")

    quotes_dir = AI_ROOT / "chapters" / f"{chapter_id}-{slugify(title)}" / "quotes"
    quotes_md = chapter_dir / "quotes.md"
    quotes = []
    if quotes_dir.exists():
        for quote_path in sorted(quotes_dir.glob("*.yaml")):
            data = yaml.safe_load(quote_path.read_text())
            quotes.append(data.get("text", ""))
    with quotes_md.open("w") as fh:
        fh.write("# Quotes\n\n")
        for quote in quotes:
            fh.write(f"> {quote}\n")


def main():
    sections = split_sections(load_entries())
    for section in sections:
        write_markdown_chapter(section["id"], section["title"], section["lines"])


if __name__ == "__main__":
    main()
