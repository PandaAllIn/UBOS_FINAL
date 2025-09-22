#!/usr/bin/env python3
"""Regenerate curated AI-structured assets for 'The Tactical Mindset'."""

import re
import shutil
from pathlib import Path
from textwrap import dedent

import yaml

ROOT = Path(__file__).resolve().parents[6]
BOOK_ROOT = ROOT / "UBOS" / "SystemFundamentals" / "Books" / "Book04-The-Tactical-Mindset"
SOURCE_ROOT = BOOK_ROOT / "source"
CHAPTER_SOURCE_ROOT = SOURCE_ROOT / "chapters"
AI_ROOT = BOOK_ROOT / "ai-structured" / "build-the-tactical-mindset"
CHAPTERS_ROOT = AI_ROOT / "chapters"
BOOK_YAML_PATH = AI_ROOT / "book.yaml"

AUTHOR = "Narrator"
SUMMARY_SENTENCE_LIMIT = 6

TOPIC_MAP = {
    "00": ["strategy", "mindset", "response"],
    "01": ["resilience", "strategy", "decision"],
    "02": ["calm", "discipline", "precision"],
    "03": ["anticipation", "planning", "clarity"],
    "04": ["mindset", "emotional-control", "focus"],
    "05": ["discipline", "habit", "momentum"],
    "06": ["patience", "timing", "response"],
    "07": ["adaptability", "resilience", "leadership"],
    "08": ["emotional-intelligence", "communication", "energy"],
    "09": ["recovery", "resilience", "leverage"],
    "10": ["environment", "planning", "execution"],
}

OBJECTIVES = {
    "00": [
        "Frame the tactical mindset as proactive rather than reactive.",
        "Shift focus from chaos to controlled response.",
        "Commit to training composure alongside strategy.",
    ],
    "01": [
        "Respond instead of react when adversity hits.",
        "Build emotional control that keeps decisions sharp.",
        "Choose next moves deliberately even when momentum stalls.",
    ],
    "02": [
        "Craft routines that keep you calm under pressure.",
        "Drill slow, precise practice so execution becomes automatic.",
        "Train patience as a performance advantage.",
    ],
    "03": [
        "Think in contingencies, not catastrophes.",
        "Plan branches for likely scenarios before they appear.",
        "Convert fear of uncertainty into readiness.",
    ],
    "04": [
        "Rewrite internal dialogue into tactical self-talk.",
        "Replace emotional spirals with focused commands.",
        "Align self-talk with mission, not moods.",
    ],
    "05": [
        "Win micro-battles that compound into momentum.",
        "Deploy discipline on daily decisions.",
        "Stack small wins to stay mission-ready.",
    ],
    "06": [
        "Install the 24-hour rule to prevent impulsive action.",
        "Channel emotions through deliberate reflection.",
        "Respond with intent rather than adrenaline.",
    ],
    "07": [
        "Adapt plans without losing commander's intent.",
        "Design pivot protocols before chaos arrives.",
        "Lead with flexibility when the terrain shifts.",
    ],
    "08": [
        "Read emotional and social terrain before making a move.",
        "Use empathy as a tactical sensor.",
        "Direct energy in the room toward productive outcomes.",
    ],
    "09": [
        "Transform setbacks into leverage for the next campaign.",
        "Codify lessons from losses into new plays.",
        "Rebuild faster with structured recovery rituals.",
    ],
    "10": [
        "Own your environment like a war map.",
        "Design terrain that supports tactical routines.",
        "Ensure every zone has a purpose aligned with mission objectives.",
    ],
}

PRACTICES = {
    "00": {
        "title": "Tactical Mindset Inventory",
        "prompt": "Assess where you currently react and where you respond with intent.",
        "steps": [
            "List three recent situations where you defaulted to reaction.",
            "Describe the tactical alternative response you wish you had used.",
            "Identify habits that keep you in control during stress.",
            "Commit to one daily drill that reinforces calm execution.",
        ],
        "expected_outcome": "Awareness of current reflexes and a plan to build tactical composure.",
    },
    "01": {
        "title": "Setback Response Plan",
        "prompt": "Design a response kit for the next unexpected hit.",
        "steps": [
            "Define the most common setbacks in your arena.",
            "Write your default emotional reaction and its cost.",
            "Script the tactical response that keeps you moving forward.",
            "Choose a grounding ritual that activates the plan.",
        ],
        "expected_outcome": "Confidence that setbacks will trigger strategy instead of spirals.",
    },
    "02": {
        "title": "Slow Is Smooth Drill",
        "prompt": "Train precision before speed.",
        "steps": [
            "Select a high-stakes routine that collapses when rushed.",
            "Break the routine into three deliberate micro-steps.",
            "Practice each step slowly while narrating the desired outcome.",
            "Gradually reintroduce speed without losing form.",
        ],
        "expected_outcome": "Calibrated execution that remains steady when pressure rises.",
    },
    "03": {
        "title": "Contingency Builder",
        "prompt": "Capture scenarios before they catch you.",
        "steps": [
            "List the most probable ways your current mission can go sideways.",
            "Assign early warning signals for each scenario.",
            "Define the first corrective move you will take when the signal appears.",
            "Schedule a quarterly review to refresh scenarios.",
        ],
        "expected_outcome": "A playbook that turns uncertainty into calculated readiness.",
    },
    "04": {
        "title": "Self-Talk Command Rewrite",
        "prompt": "Replace negative loops with tactical language.",
        "steps": [
            "Journal the phrases you use when stress spikes.",
            "Translate each into a concise command that supports execution.",
            "Create a pocket-sized card with your new tactical prompts.",
            "Run a daily rehearsal reciting the commands aloud.",
        ],
        "expected_outcome": "Internal dialogue that keeps focus, not fear, in charge.",
    },
    "05": {
        "title": "Micro-Battle Tracker",
        "prompt": "Stack daily wins that keep momentum alive.",
        "steps": [
            "Determine the three micro-battles that define a successful day.",
            "Record a simple win/lose score for each battle.",
            "Note the trigger that helped you win or lose the battle.",
            "Plan the next day's adjustments based on the tracker.",
        ],
        "expected_outcome": "Quantified micro wins that preserve long-term momentum.",
    },
    "06": {
        "title": "24-Hour Response Protocol",
        "prompt": "Build a buffer between emotion and action.",
        "steps": [
            "Document scenarios where you commit to waiting 24 hours before responding.",
            "List reflection questions you will answer during the delay.",
            "Identify a mentor or ally to consult before final decisions.",
            "Review the result after the waiting period to refine the protocol.",
        ],
        "expected_outcome": "A tested waiting ritual that prevents impulsive moves.",
    },
    "07": {
        "title": "Adaptation War Game",
        "prompt": "Practice pivoting while staying on mission.",
        "steps": [
            "Choose a current objective and list variables that could change rapidly.",
            "Design three pivot options that still protect the objective.",
            "Assign roles or resources required for each pivot.",
            "Run a quick simulation to ensure the team can execute when change hits.",
        ],
        "expected_outcome": "A flexible battle plan that keeps intent intact when reality shifts.",
    },
    "08": {
        "title": "Room Intelligence Brief",
        "prompt": "Prepare to read and direct the emotional climate.",
        "steps": [
            "Before a key interaction, note the stakeholders and likely emotional states.",
            "Decide the energy you want to project and why.",
            "Plan questions that surface hidden tension without escalating it.",
            "Outline closing actions that align everyone around the mission.",
        ],
        "expected_outcome": "A deliberate influence plan that keeps the room aligned and calm.",
    },
    "09": {
        "title": "Bounce-Back Blueprint",
        "prompt": "Turn losses into leverage for the next fight.",
        "steps": [
            "Document the setback and the specific system that failed.",
            "Extract three lessons that will prevent a repeat.",
            "Design a recovery ritual that restores confidence quickly.",
            "Plan the comeback move and metrics that will prove progress.",
        ],
        "expected_outcome": "Structured recovery that converts setbacks into renewed strength.",
    },
    "10": {
        "title": "Terrain Control Session",
        "prompt": "Design an environment that guarantees tactical readiness.",
        "steps": [
            "Map the spaces you use daily and assign each a tactical purpose.",
            "Remove objects or distractions that contradict the mission.",
            "Add tools or cues that trigger your best routines in each zone.",
            "Schedule a weekly terrain inspection to keep the map current.",
        ],
        "expected_outcome": "A controlled environment that supports every strategic objective.",
    },
}


def slugify(text: str) -> str:
    text = re.sub(r"[^a-zA-Z0-9\s-]", "", text)
    text = re.sub(r"\s+", "-", text.strip().lower())
    text = re.sub(r"-+", "-", text)
    return text or "entry"


def _sentence_case(text: str) -> str:
    text = text.strip()
    if not text:
        return text
    first = text[0]
    if first.isalpha() and first.islower():
        text = f"{first.upper()}{text[1:]}"
    return text


def _ensure_sentence(text: str) -> str:
    text = _sentence_case(text)
    if not text:
        return text
    if not text.endswith((".", "!", "?")):
        text = f"{text}."
    return text


def clean_markdown(text: str) -> str:
    return re.sub(r"[*_]{1,2}", "", text).strip()


def split_sentences(paragraph: str) -> list[str]:
    parts = re.split(r"(?<=[.!?])\s+", paragraph.strip())
    return [p.strip() for p in parts if p.strip()]


def make_description(primary_sentence: str, sentences: list[str], index: int) -> str:
    primary = _ensure_sentence(primary_sentence)
    for offset in range(index + 1, min(index + 3, len(sentences))):
        candidate = clean_markdown(sentences[offset])
        candidate = _sentence_case(candidate)
        if len(candidate.split()) >= 6 and candidate.lower() != primary.lower():
            return f"{primary} {_ensure_sentence(candidate)}"
    return primary


def first_content_line(path: Path) -> int:
    for idx, line in enumerate(path.read_text().splitlines(), start=1):
        if line.strip() and not line.lstrip().startswith("#"):
            return idx
    return 1


def load_paragraphs(chapter_id: str) -> list[str]:
    path = CHAPTER_SOURCE_ROOT / chapter_id / "chapter.md"
    paragraphs = []
    current: list[str] = []
    for line in path.read_text().splitlines():
        if line.startswith("#"):
            continue
        if not line.strip():
            if current:
                paragraphs.append(" ".join(current).strip())
                current = []
            continue
        current.append(line.strip())
    if current:
        paragraphs.append(" ".join(current).strip())
    return paragraphs


def generate_summary(chapter_id: str) -> tuple[str, list[str]]:
    paragraphs = load_paragraphs(chapter_id)
    raw_sentences = split_sentences(paragraphs[0]) if paragraphs else []
    summary_sentences = [_sentence_case(clean_markdown(s)) for s in raw_sentences]
    summary = " ".join(summary_sentences[:SUMMARY_SENTENCE_LIMIT]) if summary_sentences else ""
    return summary, summary_sentences


def read_markdown_list(path: Path) -> list[tuple[int, str]]:
    items: list[tuple[int, str]] = []
    buffer = []
    start_line = None
    for idx, line in enumerate(path.read_text().splitlines(), start=1):
        if line.startswith("- "):
            if buffer:
                items.append((start_line, " ".join(buffer).strip()))
                buffer = []
            start_line = idx
            buffer.append(line[2:].strip())
        elif buffer and (line.startswith("  ") or line.startswith("    ")):
            buffer.append(line.strip())
        elif buffer and line.strip():
            buffer.append(line.strip())
    if buffer:
        items.append((start_line, " ".join(buffer).strip()))
    deduped: list[tuple[int, str]] = []
    seen = set()
    for line_no, text in items:
        norm = clean_markdown(text).lower()
        if norm in seen or not norm:
            continue
        seen.add(norm)
        deduped.append((line_no, text))
    return deduped


def derive_title(text: str) -> str:
    cleaned = clean_markdown(text)
    candidate = re.split(r"[.!?]", cleaned)[0]
    candidate = candidate.split(":", 1)[0]
    candidate = candidate.split(",", 1)[0]
    candidate = re.sub(r"^(this chapter|the chapter|it|they|these|tactical|let's|lets)\s+", "", candidate, flags=re.I).strip()
    candidate = re.sub(r"^(focuses on|explores|examines|describes|introduces|lets talk about)\s+", "", candidate, flags=re.I).strip()
    candidate = re.sub(r"\s+", " ", candidate)
    words = candidate.split()
    if len(words) > 16:
        words = words[:16]
    while words and words[-1].lower() in {"of", "and", "to", "the", "a", "an", "as", "when"}:
        words.pop()
    candidate = " ".join(words).strip("- ")
    return (candidate.title() if candidate else "Core Insight")


def create_idea(chapter_id: str, title: str, one_liner: str, description: str, topics: list[str], source_ref: str) -> dict:
    slug = slugify(title)
    normalized_description = description.strip()
    if normalized_description:
        normalized_description = _sentence_case(normalized_description)
        if not normalized_description.endswith((".", "!", "?")):
            normalized_description = f"{normalized_description}."
    return {
        "id": f"idea-{chapter_id}-{slug}",
        "chapter": chapter_id,
        "kind": "principle",
        "title": title,
        "one_liner": _ensure_sentence(one_liner),
        "description": normalized_description,
        "topics": topics[:3],
        "source_refs": [source_ref],
    }


def generate_ideas(chapter_id: str, summary_sentences: list[str], chapter_ref: str) -> list[dict]:
    topics = TOPIC_MAP.get(chapter_id, ["strategy"])
    ideas: list[dict] = []
    used_titles = set()

    for idx, sentence in enumerate(summary_sentences[:SUMMARY_SENTENCE_LIMIT]):
        cleaned_sentence = clean_markdown(sentence)
        if len(cleaned_sentence.split()) < 6:
            continue
        bolds = re.findall(r"\*\*(.+?)\*\*", sentence)
        if bolds:
            for phrase in bolds:
                title = phrase.strip().title()
                if title.lower() in used_titles:
                    continue
                description = make_description(cleaned_sentence, summary_sentences, idx)
                ideas.append(create_idea(chapter_id, title, cleaned_sentence, description, topics, chapter_ref))
                used_titles.add(title.lower())
        else:
            title = derive_title(cleaned_sentence)
            if title.lower() in used_titles:
                continue
            description = make_description(cleaned_sentence, summary_sentences, idx)
            ideas.append(create_idea(chapter_id, title, cleaned_sentence, description, topics, chapter_ref))
            used_titles.add(title.lower())

    key_ideas_path = CHAPTER_SOURCE_ROOT / chapter_id / "key-ideas.md"
    if key_ideas_path.exists():
        for line_no, raw in read_markdown_list(key_ideas_path):
            cleaned = clean_markdown(raw)
            if len(cleaned.split()) < 6:
                continue
            title = derive_title(raw)
            if title.lower() in used_titles:
                continue
            source_ref = f"{key_ideas_path.relative_to(ROOT)}:{line_no}"
            description = _ensure_sentence(cleaned)
            one_liner = cleaned.split(".")[0].strip() or cleaned
            ideas.append(create_idea(chapter_id, title, one_liner, description, topics, source_ref))
            used_titles.add(title.lower())

    return ideas


def exercises_source_ref(chapter_id: str) -> str:
    path = CHAPTER_SOURCE_ROOT / chapter_id / "exercises.md"
    if not path.exists():
        chapter_md = CHAPTER_SOURCE_ROOT / chapter_id / "chapter.md"
        return f"{chapter_md.relative_to(ROOT)}:{first_content_line(chapter_md)}"
    for idx, line in enumerate(path.read_text().splitlines(), start=1):
        if line.lstrip().startswith("- "):
            return f"{path.relative_to(ROOT)}:{idx}"
    return f"{path.relative_to(ROOT)}:1"


def build_practice(chapter_id: str) -> dict:
    meta = PRACTICES[chapter_id]
    topics = TOPIC_MAP.get(chapter_id, ["strategy"])
    slug = slugify(meta['title'])
    return {
        "id": f"practice-{chapter_id}-{slug}",
        "chapter": chapter_id,
        "kind": "checklist",
        "title": meta["title"],
        "prompt": meta["prompt"],
        "steps": meta["steps"],
        "expected_outcome": meta["expected_outcome"],
        "topics": topics[:3],
        "source_refs": [exercises_source_ref(chapter_id)],
    }


def load_quotes(chapter_id: str) -> list[tuple[int, str]]:
    path = CHAPTER_SOURCE_ROOT / chapter_id / "quotes.md"
    if not path.exists():
        return []
    quotes: list[tuple[int, str]] = []
    block: list[str] = []
    start_line = None
    for idx, line in enumerate(path.read_text().splitlines(), start=1):
        if line.startswith(">"):
            if start_line is None:
                start_line = idx
            block.append(line.lstrip(">").strip())
        else:
            if block:
                quotes.append((start_line, " ".join(block).strip()))
                block = []
                start_line = None
    if block:
        quotes.append((start_line, " ".join(block).strip()))
    deduped = []
    seen = set()
    for line_no, text in quotes:
        if not text or text.lower() in seen:
            continue
        seen.add(text.lower())
        deduped.append((line_no, text))
    return deduped[:3]


def normalize_for_compare(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", text.lower()).strip()


def build_quotes(chapter_id: str, chapter_title: str) -> list[dict]:
    records = []
    topics = TOPIC_MAP.get(chapter_id, ["strategy"])
    path = CHAPTER_SOURCE_ROOT / chapter_id / "quotes.md"
    chapter_title_norm = normalize_for_compare(chapter_title)
    for index, (line_no, text) in enumerate(load_quotes(chapter_id), start=1):
        raw = clean_markdown(text)
        segments = [seg.strip() for seg in re.split(r"(?<=[.!?])\s+", raw) if seg.strip()]
        filtered_segments = []
        for seg in segments:
            normalized = normalize_for_compare(seg)
            if not normalized or normalized == chapter_title_norm or normalized.startswith(chapter_title_norm + " "):
                continue
            filtered_segments.append(seg)
        if filtered_segments:
            segments = filtered_segments
        if segments:
            cleaned_text = " ".join(_ensure_sentence(seg) for seg in segments)
        else:
            cleaned_text = _ensure_sentence(raw)
        slug = slugify(f"{chapter_id}-{cleaned_text[:40]}")
        records.append(
            {
                "id": f"quote-{chapter_id}-{slug}",
                "chapter": chapter_id,
                "kind": "quote",
                "speaker": AUTHOR,
                "text": cleaned_text,
                "context": "Key statement from the chapter.",
                "topics": topics[:2],
                "source_refs": [f"{path.relative_to(ROOT)}:{line_no}"],
            }
        )
    return records


def write_yaml(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w") as fh:
        yaml.safe_dump(data, fh, sort_keys=False, allow_unicode=False)


def reset_chapter_dir(path: Path) -> None:
    if path.exists():
        shutil.rmtree(path)
    path.mkdir(parents=True, exist_ok=True)


def generate_chapter(chapter_meta: dict) -> None:
    chapter_id = chapter_meta["id"]
    chapter_title = chapter_meta["title"]
    dir_slug = slugify(chapter_title)
    chapter_dir = CHAPTERS_ROOT / f"{chapter_id}-{dir_slug}"
    reset_chapter_dir(chapter_dir)
    (chapter_dir / "ideas").mkdir()
    (chapter_dir / "practices").mkdir()
    (chapter_dir / "quotes").mkdir()
    (chapter_dir / "indices").mkdir()

    summary, summary_sentences = generate_summary(chapter_id)
    chapter_md = CHAPTER_SOURCE_ROOT / chapter_id / "chapter.md"
    chapter_ref = f"{chapter_md.relative_to(ROOT)}:{first_content_line(chapter_md)}"

    chapter_yaml = {
        "id": chapter_id,
        "slug": f"chapter-{chapter_id}-{slugify(chapter_title)}",
        "title": chapter_title,
        "summary": summary,
        "objectives": OBJECTIVES[chapter_id],
        "dependencies": [],
        "topics": TOPIC_MAP.get(chapter_id, ["strategy"]),
        "source_refs": [chapter_ref],
        "assets": {},
    }
    write_yaml(chapter_dir / "chapter.yaml", chapter_yaml)

    for idea in generate_ideas(chapter_id, summary_sentences, chapter_ref):
        write_yaml(chapter_dir / "ideas" / f"{idea['id']}.yaml", idea)

    practice = build_practice(chapter_id)
    write_yaml(chapter_dir / "practices" / f"{practice['id']}.yaml", practice)

    for quote in build_quotes(chapter_id, chapter_title):
        write_yaml(chapter_dir / "quotes" / f"{quote['id']}.yaml", quote)

    outline_text = dedent(
        f"""# Chapter {chapter_id} Outline\n\nRegenerated from curated summary and supporting assets."""
    )
    (chapter_dir / "OUTLINE.md").write_text(outline_text, encoding="utf-8")


def main() -> None:
    book_meta = yaml.safe_load(BOOK_YAML_PATH.read_text())
    for chapter_meta in book_meta["chapters"]:
        generate_chapter(chapter_meta)


if __name__ == "__main__":
    main()
