#!/usr/bin/env python3
"""
UBOS Knowledge Extractor - Consolidate Books & Extract Endless Scroll

This script:
1. Consolidates existing Book structured data into BOOKS_MASTER_INDEX.json
2. Uses Groq (fast + cheap) to categorize the Endless Scroll

Usage:
    python3 knowledge_extractor.py --books      # Consolidate books only
    python3 knowledge_extractor.py --scroll     # Extract scroll only
    python3 knowledge_extractor.py --all        # Both
"""

import json
import os
import re
import sys
from pathlib import Path
from datetime import datetime, timezone
from typing import Optional

# Add trinity to path
sys.path.insert(0, str(Path(__file__).parent.parent))

JANUS_ROOT = Path("/srv/janus")
BOOKS_DIR = JANUS_ROOT / "BOOKS"
ARCHIVES_DIR = JANUS_ROOT / "99_ARCHIVES" / "UBOS"
OUTPUT_DIR = JANUS_ROOT / "knowledge_graphs"
SCROLL_PATH = JANUS_ROOT / "endless_scroll.md"

# Scroll categories for extraction
SCROLL_CATEGORIES = {
    "ARCH": "Architecture decisions and system design",
    "STEAMPUNK": "Steampunk metaphors and aesthetic concepts",
    "TOOL": "Tool and script concepts",
    "SKILL": "Autonomous skill ideas",
    "ORACLE": "Oracle integration ideas",
    "REVENUE": "Monetization and revenue strategies",
    "CONST": "Constitutional principles",
    "TRINITY": "Trinity coordination patterns",
    "MISSION": "Mission and project concepts",
    "CODE": "Code patterns and implementations",
}


def load_jsonl(path: Path) -> list[dict]:
    """Load JSONL file into list of dicts."""
    items = []
    if not path.exists():
        return items
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                try:
                    items.append(json.loads(line))
                except json.JSONDecodeError:
                    continue
    return items


def find_book_data(book_num: int) -> dict:
    """Find structured data for a book from archives."""
    book_names = {
        1: "Book01-BuildTheSystem",
        2: "Book02-Build-One-System-at-a-Time",
        3: "Book03-The-Art-of-Strategic-Thinking",
        4: "Book04-The-Tactical-Mindset",
    }
    book_slugs = {
        1: "build-the-system",
        2: "build-one-system-at-a-time",
        3: "build-the-art-of-strategic-thinking",
        4: "build-the-tactical-mindset",
    }
    book_roles = {
        1: "WHY",
        2: "HOW",
        3: "WHAT",
        4: "WHEN",
    }

    book_name = book_names.get(book_num)
    book_slug = book_slugs.get(book_num)
    book_role = book_roles.get(book_num)

    if not book_name:
        return {}

    # Try to find in archives
    archive_path = ARCHIVES_DIR / book_name / "ai-structured" / book_slug / "chapters" / "all"

    if not archive_path.exists():
        # Try with numbered suffix
        for suffix in ["", " 2", " 3", " 4"]:
            test_path = ARCHIVES_DIR / f"{book_name}{suffix}" / "ai-structured" / book_slug / "chapters" / "all"
            if test_path.exists():
                archive_path = test_path
                break

    result = {
        "book_id": f"book{book_num:02d}",
        "book_name": book_name,
        "book_slug": book_slug,
        "role": book_role,
        "role_description": {
            "WHY": "Philosophical foundation - the purpose behind building systems",
            "HOW": "Methodology - the process of building one system at a time",
            "WHAT": "Strategic patterns - the art of strategic thinking",
            "WHEN": "Execution timing - the tactical mindset for action",
        }.get(book_role, ""),
        "ideas": [],
        "practices": [],
        "quotes": [],
        "topics": [],
        "idea_count": 0,
        "source_path": str(archive_path) if archive_path.exists() else None,
    }

    if archive_path.exists():
        # Load ideas
        ideas = load_jsonl(archive_path / "ideas.jsonl")
        result["ideas"] = ideas
        result["idea_count"] = len(ideas)

        # Load practices
        result["practices"] = load_jsonl(archive_path / "practices.jsonl")

        # Load quotes
        result["quotes"] = load_jsonl(archive_path / "quotes.jsonl")

        # Extract unique topics
        all_topics = set()
        for idea in ideas:
            all_topics.update(idea.get("topics", []))
        result["topics"] = sorted(list(all_topics))

    return result


def consolidate_books() -> dict:
    """Consolidate all book data into master index."""
    print("Consolidating Books into BOOKS_MASTER_INDEX.json...")

    master_index = {
        "meta": {
            "created": datetime.now(timezone.utc).isoformat(),
            "description": "UBOS Knowledge Base - The Four Books (WHY/HOW/WHAT/WHEN)",
            "source": "Extracted from /srv/janus/99_ARCHIVES/UBOS/Book*",
            "version": "1.0.0",
        },
        "framework": {
            "model": "WHY-HOW-WHAT-WHEN",
            "description": "The Four Books form an integrated framework for system building",
            "flow": [
                {"step": 1, "book": "Book01", "role": "WHY", "question": "Why build systems?"},
                {"step": 2, "book": "Book02", "role": "HOW", "question": "How to build them?"},
                {"step": 3, "book": "Book03", "role": "WHAT", "question": "What to build?"},
                {"step": 4, "book": "Book04", "role": "WHEN", "question": "When to execute?"},
            ],
        },
        "books": {},
        "all_topics": [],
        "all_ideas_count": 0,
        "topic_to_ideas": {},
    }

    all_topics = set()
    total_ideas = 0
    topic_to_ideas = {}

    for book_num in [1, 2, 3, 4]:
        book_data = find_book_data(book_num)
        book_id = book_data.get("book_id", f"book{book_num:02d}")
        master_index["books"][book_id] = book_data

        # Aggregate topics
        all_topics.update(book_data.get("topics", []))
        total_ideas += book_data.get("idea_count", 0)

        # Build topic-to-ideas index
        for idea in book_data.get("ideas", []):
            for topic in idea.get("topics", []):
                if topic not in topic_to_ideas:
                    topic_to_ideas[topic] = []
                topic_to_ideas[topic].append({
                    "id": idea.get("id"),
                    "book": book_id,
                    "one_liner": idea.get("one_liner", "")[:100],
                })

        print(f"  Book {book_num}: {book_data.get('idea_count', 0)} ideas, {len(book_data.get('topics', []))} topics")

    master_index["all_topics"] = sorted(list(all_topics))
    master_index["all_ideas_count"] = total_ideas
    master_index["topic_to_ideas"] = topic_to_ideas

    # Save master index
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    output_path = OUTPUT_DIR / "BOOKS_MASTER_INDEX.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(master_index, f, indent=2, ensure_ascii=False)

    print(f"\nSaved: {output_path}")
    print(f"Total: {total_ideas} ideas across {len(all_topics)} topics")

    return master_index


def extract_scroll_section(text: str, start_marker: str, end_marker: Optional[str] = None) -> str:
    """Extract a section from the scroll between markers."""
    start_idx = text.find(start_marker)
    if start_idx == -1:
        return ""

    start_idx += len(start_marker)

    if end_marker:
        end_idx = text.find(end_marker, start_idx)
        if end_idx == -1:
            return text[start_idx:]
        return text[start_idx:end_idx]

    return text[start_idx:]


def extract_scroll_entries(scroll_text: str) -> list[dict]:
    """Extract timestamped entries from the endless scroll."""
    entries = []

    # Pattern for timestamped entries: [2025-12-30T...] or similar
    timestamp_pattern = r'\[(\d{4}-\d{2}-\d{2}[T\s]\d{2}:\d{2}:\d{2}[Z\+\-\d:]*)\]'

    # Split by timestamps
    parts = re.split(timestamp_pattern, scroll_text)

    for i in range(1, len(parts), 2):
        if i + 1 < len(parts):
            timestamp = parts[i]
            content = parts[i + 1].strip()

            # Skip empty entries
            if len(content) < 10:
                continue

            # Take first 500 chars for categorization
            preview = content[:500]

            entries.append({
                "timestamp": timestamp,
                "content": content,
                "preview": preview,
            })

    return entries


def categorize_with_groq(entries: list[dict], batch_size: int = 10) -> list[dict]:
    """Use Groq to categorize scroll entries."""
    try:
        from groq import Groq
    except ImportError:
        print("Groq SDK not installed. Install with: pip install groq")
        return entries

    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        # Try loading from config
        env_path = Path("/etc/janus/trinity.env")
        if env_path.exists():
            with open(env_path) as f:
                for line in f:
                    if line.startswith("GROQ_API_KEY="):
                        api_key = line.split("=", 1)[1].strip().strip('"').strip("'")
                        break

    if not api_key:
        print("GROQ_API_KEY not found. Skipping AI categorization.")
        return entries

    client = Groq(api_key=api_key)

    category_prompt = f"""You are categorizing entries from a project journal called "The Endless Scroll".

Categories:
{json.dumps(SCROLL_CATEGORIES, indent=2)}

For each entry, respond with ONLY a JSON object like:
{{"category": "ARCH", "confidence": 0.9, "keywords": ["system", "design"]}}

If multiple categories apply, pick the PRIMARY one. If none fit well, use "OTHER".
"""

    categorized = []

    for i, entry in enumerate(entries):
        if i >= 100:  # Limit for cost control
            entry["category"] = "UNCATEGORIZED"
            entry["confidence"] = 0
            categorized.append(entry)
            continue

        try:
            response = client.chat.completions.create(
                model="llama-3.1-8b-instant",  # Fast and cheap
                messages=[
                    {"role": "system", "content": category_prompt},
                    {"role": "user", "content": f"Categorize this entry:\n\n{entry['preview']}"},
                ],
                temperature=0.1,
                max_tokens=100,
            )

            result_text = response.choices[0].message.content.strip()

            # Parse JSON response
            try:
                # Find JSON in response
                json_match = re.search(r'\{[^}]+\}', result_text)
                if json_match:
                    result = json.loads(json_match.group())
                    entry["category"] = result.get("category", "OTHER")
                    entry["confidence"] = result.get("confidence", 0.5)
                    entry["keywords"] = result.get("keywords", [])
                else:
                    entry["category"] = "OTHER"
                    entry["confidence"] = 0.3
            except json.JSONDecodeError:
                entry["category"] = "OTHER"
                entry["confidence"] = 0.3

            categorized.append(entry)

            if (i + 1) % 10 == 0:
                print(f"  Categorized {i + 1}/{min(len(entries), 100)} entries...")

        except Exception as e:
            print(f"  Error categorizing entry {i}: {e}")
            entry["category"] = "ERROR"
            entry["confidence"] = 0
            categorized.append(entry)

    return categorized


def extract_scroll() -> dict:
    """Extract and categorize the endless scroll."""
    print("Extracting Endless Scroll...")

    if not SCROLL_PATH.exists():
        print(f"ERROR: Scroll not found at {SCROLL_PATH}")
        return {}

    with open(SCROLL_PATH, "r", encoding="utf-8") as f:
        scroll_text = f.read()

    print(f"  Scroll size: {len(scroll_text):,} characters")

    # Extract entries
    entries = extract_scroll_entries(scroll_text)
    print(f"  Found {len(entries)} timestamped entries")

    # Categorize with Groq (first 100 for cost control)
    print("  Categorizing with Groq (llama-3.1-8b-instant)...")
    categorized = categorize_with_groq(entries[:100])

    # Build structured output
    scroll_index = {
        "meta": {
            "created": datetime.now(timezone.utc).isoformat(),
            "description": "UBOS Endless Scroll - Categorized Project Journal",
            "source": str(SCROLL_PATH),
            "total_entries": len(entries),
            "categorized_entries": len(categorized),
            "categories": SCROLL_CATEGORIES,
        },
        "entries_by_category": {},
        "entries": [],
    }

    # Group by category
    for cat in SCROLL_CATEGORIES:
        scroll_index["entries_by_category"][cat] = []
    scroll_index["entries_by_category"]["OTHER"] = []
    scroll_index["entries_by_category"]["UNCATEGORIZED"] = []

    for entry in categorized:
        cat = entry.get("category", "OTHER")
        if cat not in scroll_index["entries_by_category"]:
            scroll_index["entries_by_category"]["OTHER"].append(entry)
        else:
            scroll_index["entries_by_category"][cat].append(entry)

        # Add to flat list (without full content to save space)
        scroll_index["entries"].append({
            "timestamp": entry.get("timestamp"),
            "category": cat,
            "confidence": entry.get("confidence", 0),
            "keywords": entry.get("keywords", []),
            "preview": entry.get("preview", "")[:200],
        })

    # Print summary
    print("\n  Category counts:")
    for cat, items in scroll_index["entries_by_category"].items():
        if items:
            print(f"    {cat}: {len(items)}")

    # Save
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    output_path = OUTPUT_DIR / "ENDLESS_SCROLL_INDEX.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(scroll_index, f, indent=2, ensure_ascii=False)

    print(f"\nSaved: {output_path}")

    return scroll_index


def main():
    import argparse

    parser = argparse.ArgumentParser(description="UBOS Knowledge Extractor")
    parser.add_argument("--books", action="store_true", help="Consolidate books only")
    parser.add_argument("--scroll", action="store_true", help="Extract scroll only")
    parser.add_argument("--all", action="store_true", help="Both books and scroll")

    args = parser.parse_args()

    if not any([args.books, args.scroll, args.all]):
        args.all = True  # Default to all

    print("=" * 60)
    print("UBOS Knowledge Extractor")
    print("=" * 60)

    if args.books or args.all:
        print("\n[1/2] BOOKS CONSOLIDATION")
        print("-" * 40)
        consolidate_books()

    if args.scroll or args.all:
        print("\n[2/2] ENDLESS SCROLL EXTRACTION")
        print("-" * 40)
        extract_scroll()

    print("\n" + "=" * 60)
    print("DONE! Knowledge graphs saved to:", OUTPUT_DIR)
    print("=" * 60)


if __name__ == "__main__":
    main()
