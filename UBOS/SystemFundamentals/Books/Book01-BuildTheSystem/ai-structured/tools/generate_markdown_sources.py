#!/usr/bin/env python3
"""Generate chapter markdown + key ideas/exercises/quotes for Book 01."""

from pathlib import Path
import yaml

from parse_book import slugify
ROOT = Path(__file__).resolve().parents[6]
BOOK_ROOT = ROOT / "UBOS" / "SystemFundamentals" / "Books" / "Book01-BuildTheSystem"
AI_ROOT = BOOK_ROOT / "ai-structured" / "build-the-system"
SOURCE_DIR = BOOK_ROOT / "source" / "chapters"

DOC_CHAPTERS = BOOK_ROOT / "source" / "docs" / "chapters"
INTRO_FILE = BOOK_ROOT / "source" / "BuildTheSystem" / "01-introduction" / "introduction.md"


def ensure_dir(path: Path):
    path.mkdir(parents=True, exist_ok=True)


def read_paragraphs(path: Path) -> list[str]:
    paragraphs = []
    buffer = []
    for line in path.read_text().splitlines():
        stripped = line.strip()
        if stripped:
            buffer.append(line.rstrip())
        else:
            if buffer:
                paragraphs.append(" ".join(buffer))
                buffer = []
    if buffer:
        paragraphs.append(" ".join(buffer))
    return paragraphs


def write_markdown(chapter_id: str, title: str):
    chapter_dir = SOURCE_DIR / chapter_id
    ensure_dir(chapter_dir)

    if chapter_id == "00":
        paragraphs = read_paragraphs(INTRO_FILE)
    else:
        chapter_path = DOC_CHAPTERS / chapter_id / "chapter.md"
        paragraphs = read_paragraphs(chapter_path)

    with (chapter_dir / "chapter.md").open("w") as fh:
        fh.write(f"# Chapter {chapter_id} – {title}\n\n")
        fh.write("\n\n".join(paragraphs))

    ideas_dir = AI_ROOT / "chapters" / f"{chapter_id}-{slugify(title)}" / "ideas"
    if not ideas_dir.exists():
        # fallback slug
        for path in (AI_ROOT / "chapters").glob(f"{chapter_id}-*/ideas"):
            ideas_dir = path
            break

    ideas = []
    if ideas_dir and ideas_dir.exists():
        for idea_path in sorted(ideas_dir.glob("*.yaml")):
            data = yaml.safe_load(idea_path.read_text())
            ideas.append(data.get("one_liner", data.get("title", "")))

    with (chapter_dir / "key-ideas.md").open("w") as fh:
        fh.write("# Key Ideas\n\n")
        for idea in ideas:
            fh.write(f"- {idea}\n")

    practice_dir = ideas_dir.parents[0] / "practices" if ideas_dir else None
    steps = []
    if practice_dir and practice_dir.exists():
        for practice_path in sorted(practice_dir.glob("*.yaml")):
            data = yaml.safe_load(practice_path.read_text())
            steps.extend(data.get("steps", []))
    with (chapter_dir / "exercises.md").open("w") as fh:
        fh.write("# Exercises\n\n")
        for step in steps:
            fh.write(f"- {step}\n")

    quotes_dir = ideas_dir.parents[0] / "quotes" if ideas_dir else None
    quotes = []
    if quotes_dir and quotes_dir.exists():
        for quote_path in sorted(quotes_dir.glob("*.yaml")):
            data = yaml.safe_load(quote_path.read_text())
            quotes.append(data.get("text", ""))
    with (chapter_dir / "quotes.md").open("w") as fh:
        fh.write("# Quotes\n\n")
        for quote in quotes:
            fh.write(f"> {quote}\n")


def main():
    SOURCE_DIR.mkdir(parents=True, exist_ok=True)
    book_yaml = yaml.safe_load((AI_ROOT / "book.yaml").read_text())
    chapters = [
        {"id": "00", "title": "Introduction"},
        *book_yaml["chapters"],
    ]
    for ch in chapters:
        write_markdown(ch["id"], ch["title"])


if __name__ == "__main__":
    main()
