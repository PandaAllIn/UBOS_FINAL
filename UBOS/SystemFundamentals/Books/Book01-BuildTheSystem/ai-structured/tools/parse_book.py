#!/usr/bin/env python3
"""Generate AI-structured assets for Build the System (Book 01)."""

import re
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[6]
BOOK_ROOT = ROOT / "UBOS" / "SystemFundamentals" / "Books" / "Book01-BuildTheSystem"
SOURCE_FILE = BOOK_ROOT / "source" / "BuildTheSystem.md"
AI_ROOT = BOOK_ROOT / "ai-structured" / "build-the-system"
CHAPTERS_DIR = AI_ROOT / "chapters"

TOPIC_MAP = {
    "00": ["systems", "abundance", "design"],
    "01": ["architecture", "system", "alignment"],
    "02": ["rhythm", "energy", "structure"],
    "03": ["clarity", "system", "structure"],
    "04": ["identity", "system", "routine"],
    "05": ["habit", "routine", "clarity"],
    "06": ["time", "design", "system"],
    "07": ["input", "rhythm", "energy"],
    "08": ["design", "system", "energy"],
    "09": ["alignment", "abundance", "identity"],
    "10": ["environment", "system", "alignment"],
    "11": ["tools", "system", "clarity"],
    "12": ["architecture", "structure", "identity"],
    "13": ["system", "structure", "scale"],
    "14": ["feedback", "system", "identity"],
    "15": ["identity", "system", "habit"],
    "16": ["delegation", "structure", "clarity"],
    "17": ["system", "structure", "upgrade"],
    "18": ["design", "system", "future"],
    "19": ["feedback", "system", "alignment"],
    "20": ["identity", "design", "structure"],
}
DEFAULT_TOPICS = ["system"]

CHAPTER_RE = re.compile(r"^Chapter\s+(\d+):\s*(.*)")


def load_lines():
    lines = []
    for lineno, raw in enumerate(SOURCE_FILE.read_text().splitlines(), start=1):
        lines.append((lineno, raw.rstrip()))
    return lines


def split_sections(lines):
    sections = []
    current = {"id": "00", "title": "Introduction", "start": 1, "lines": []}
    for lineno, text in lines:
        match = CHAPTER_RE.match(text.strip())
        if match:
            if current["lines"]:
                sections.append(current)
            chap = match.group(1).zfill(2)
            title = match.group(2).strip() or f"Chapter {chap}"
            current = {"id": chap, "title": title, "start": lineno + 1, "lines": []}
        else:
            current["lines"].append((lineno, text))
    if current["lines"]:
        sections.append(current)
    return sections


def slugify(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s-]", "", text)
    return re.sub(r"\s+", "-", text.strip())


def extract_text(lines):
    paragraphs = []
    buffer = []
    for _, text in lines:
        stripped = text.strip()
        if stripped:
            buffer.append(stripped)
        else:
            if buffer:
                paragraphs.append(" ".join(buffer))
                buffer = []
    if buffer:
        paragraphs.append(" ".join(buffer))
    return paragraphs


def build_chapter_yaml(chapter_id: str, title: str, paragraphs, start_line):
    summary = " ".join(paragraphs[:1])
    objectives = paragraphs[1:4]
    return {
        "id": chapter_id,
        "slug": f"chapter-{chapter_id}-{slugify(title)}",
        "title": title,
        "summary": summary,
        "objectives": objectives,
        "dependencies": [],
        "topics": TOPIC_MAP.get(chapter_id, DEFAULT_TOPICS),
        "source_refs": [f"{SOURCE_FILE.relative_to(ROOT)}:{start_line}"]
    }


def write_files(section):
    chapter_id = section["id"]
    title = section["title"]
    chapter_dir = CHAPTERS_DIR / f"{chapter_id}-{slugify(title)}"
    if chapter_dir.exists():
        for path in chapter_dir.glob("**/*"):
            if path.is_file():
                path.unlink()
        for path in sorted(chapter_dir.glob("**/*"), reverse=True):
            if path.is_dir():
                path.rmdir()
    chapter_dir.mkdir(parents=True, exist_ok=True)
    (chapter_dir / "ideas").mkdir()
    (chapter_dir / "practices").mkdir()
    (chapter_dir / "quotes").mkdir()
    (chapter_dir / "indices").mkdir()

    paragraphs = extract_text(section["lines"])
    chapter_yaml = build_chapter_yaml(chapter_id, title, paragraphs, section["start"])
    with (chapter_dir / "chapter.yaml").open("w") as fh:
        yaml.safe_dump(chapter_yaml, fh, sort_keys=False)

    # leave ideas/practices/quotes to manual curation (existing Book 01 content)


def main():
    sections = split_sections(load_lines())
    CHAPTERS_DIR.mkdir(parents=True, exist_ok=True)
    for section in sections:
        write_files(section)


if __name__ == "__main__":
    main()
