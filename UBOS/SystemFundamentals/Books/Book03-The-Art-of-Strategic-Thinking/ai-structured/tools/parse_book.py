#!/usr/bin/env python3
"""Regenerate curated AI-structured assets for 'The Art of Strategic Thinking'."""

import re
import shutil
from pathlib import Path
from textwrap import dedent

import yaml

ROOT = Path(__file__).resolve().parents[6]
BOOK_ROOT = ROOT / "UBOS" / "SystemFundamentals" / "Books" / "Book03-The-Art-of-Strategic-Thinking"
SOURCE_ROOT = BOOK_ROOT / "source"
CHAPTER_SOURCE_ROOT = SOURCE_ROOT / "chapters"
AI_ROOT = BOOK_ROOT / "ai-structured" / "build-the-art-of-strategic-thinking"
CHAPTERS_ROOT = AI_ROOT / "chapters"
BOOK_YAML_PATH = AI_ROOT / "book.yaml"

AUTHOR = "Narrator"
SUMMARY_SENTENCE_LIMIT = 6

TOPIC_MAP = {
    "00": ["strategy", "mindset", "clarity"],
    "01": ["mindset", "strategy", "decision"],
    "02": ["clarity", "vision", "alignment"],
    "03": ["information", "strategy", "execution"],
    "04": ["systems", "vision", "analysis"],
    "05": ["anticipation", "foresight", "planning"],
    "06": ["timing", "precision", "decision"],
    "07": ["leverage", "resources", "efficiency"],
    "08": ["adaptability", "resilience", "change"],
    "09": ["psychology", "influence", "communication"],
    "10": ["execution", "discipline", "action"],
}

OBJECTIVES = {
    "00": [
        "Define strategic thinking as an everyday practice, not an elite talent.",
        "Recognize the shift from reacting impulsively to choosing intentional responses.",
        "Commit to building discipline that keeps decisions aligned with long-term aim.",
    ],
    "01": [
        "Pause before reacting so emotion serves execution instead of derailing it.",
        "Train the mind to evaluate options under pressure.",
        "Adopt strategic questions that turn impulses into deliberate moves.",
    ],
    "02": [
        "Establish a clear endgame that directs strategy.",
        "Reverse engineer outcomes into concrete milestones.",
        "Eliminate haze by deciding what success actually looks like.",
    ],
    "03": [
        "Treat research as ammunition that improves timing and execution.",
        "Develop filters for separating noise from actionable intelligence.",
        "Integrate learning loops that inform every major move.",
    ],
    "04": [
        "Zoom out to see interlocking systems before acting.",
        "Map the terrain, players, and leverage points on the strategic board.",
        "Position yourself for advantage rather than chasing random wins.",
    ],
    "05": [
        "Anticipate obstacles before they materialize.",
        "Practice scenario planning that keeps moves two steps ahead.",
        "Build contingency responses that convert uncertainty into readiness.",
    ],
    "06": [
        "Respect timing as a strategic lever, not a coincidence.",
        "Balance patience and precision when selecting the next move.",
        "Create readiness rituals so opportunity meets prepared execution.",
    ],
    "07": [
        "Leverage assets—skills, tools, relationships—to multiply effort.",
        "Choose moves that create asymmetrical outcomes with minimal waste.",
        "Design leverage plays that protect energy for the highest value work.",
    ],
    "08": [
        "Stay agile without losing sight of long-term vision.",
        "Adapt plans when reality shifts while holding strategy steady.",
        "Build resilience muscles that thrive amid volatility.",
    ],
    "09": [
        "Understand psychological drivers behind every negotiation or conflict.",
        "Use empathy and influence with integrity.",
        "Design communication that aligns motives, not just words.",
    ],
    "10": [
        "Bridge strategy to disciplined execution.",
        "Translate plans into operating rhythms and scoreboards.",
        "Sustain follow-through until results compound.",
    ],
}

PRACTICES = {
    "00": {
        "title": "Strategic Mindset Primer",
        "prompt": "Anchor the introductory lessons by defining your strategic posture.",
        "steps": [
            "List three moments this week when you reacted instead of responded.",
            "Describe how a strategic pause would have changed each outcome.",
            "Write a one-sentence definition of strategic thinking for your life.",
            "Choose one daily cue that will remind you to slow down and think before acting.",
        ],
        "expected_outcome": "Personal definition and trigger that begin the strategic mindset shift.",
    },
    "01": {
        "title": "Pause-and-Plan Drill",
        "prompt": "Train your response loop to default to evaluation over impulse.",
        "steps": [
            "Identify a recurring trigger that usually provokes a fast reaction.",
            "Script three questions you will ask yourself before responding.",
            "Role-play or journal the strategic response you will use next time.",
            "Debrief after the next trigger to refine the pause practice.",
        ],
        "expected_outcome": "A rehearsed response protocol that keeps emotions in strategic service.",
    },
    "02": {
        "title": "Endgame Clarity Map",
        "prompt": "Translate strategic clarity into measurable checkpoints.",
        "steps": [
            "Write the future state you are building in vivid detail.",
            "List three milestone outcomes that prove you are on track.",
            "Define inputs and behaviours required for the next milestone.",
            "Schedule a monthly review to adjust targets as clarity sharpens.",
        ],
        "expected_outcome": "A reverse-engineered roadmap that keeps execution tethered to the vision.",
    },
    "03": {
        "title": "Intelligence Gathering Framework",
        "prompt": "Install a repeatable system for turning information into action.",
        "steps": [
            "State the strategic decision you need to support with research.",
            "List trusted sources and criteria for what counts as quality intel.",
            "Capture insights in a single document with signals, assumptions, and implications.",
            "Decide how new intelligence will alter timing, resources, or tactics.",
        ],
        "expected_outcome": "A living intelligence file that guides smarter strategic moves.",
    },
    "04": {
        "title": "Board Mapping Session",
        "prompt": "Visualize the system you are playing within before choosing moves.",
        "steps": [
            "Sketch the key players, resources, and constraints influencing your objective.",
            "Mark leverage points where small actions create big shifts.",
            "Identify blind spots requiring more data.",
            "Choose the single positioning move that strengthens your advantage this week.",
        ],
        "expected_outcome": "A systems view that informs where to stand and what to influence next.",
    },
    "05": {
        "title": "Scenario Anticipation Drill",
        "prompt": "Practice staying ahead of obstacles before they become emergencies.",
        "steps": [
            "List the three most likely disruptions to your current plan.",
            "For each, write the earliest signal that the scenario is emerging.",
            "Decide on your first strategic response if the signal appears.",
            "Schedule a review cadence to refresh scenarios as conditions change.",
        ],
        "expected_outcome": "Confidence that you can adapt quickly because contingencies are pre-planned.",
    },
    "06": {
        "title": "Timing Precision Check",
        "prompt": "Align decisions with the ripest moment for impact.",
        "steps": [
            "Review a decision you rushed or delayed and note the cost.",
            "Define criteria that signal the right time to move in similar situations.",
            "Outline preparatory actions required so you can act fast when timing is right.",
            "Document a pre-mortem to ensure patience never becomes paralysis.",
        ],
        "expected_outcome": "A timing framework that balances readiness with decisive action.",
    },
    "07": {
        "title": "Leverage Inventory Sprint",
        "prompt": "Locate assets that can multiply results with less exertion.",
        "steps": [
            "List resources—skills, technology, relationships—you are underutilizing.",
            "Brainstorm leverage moves that would expand results without proportional effort.",
            "Prioritize one leverage play and design the first experiment.",
            "Track hours saved or output gained to validate the leverage.",
        ],
        "expected_outcome": "A tested leverage play that magnifies output while protecting energy.",
    },
    "08": {
        "title": "Adaptive Pulse Review",
        "prompt": "Ensure agility without losing the throughline of your strategy.",
        "steps": [
            "Audit recent pivots and rank whether they were reactive or strategic.",
            "Clarify which elements of the vision are fixed versus flexible.",
            "Create a checklist that triggers adaptation only when criteria are met.",
            "Plan a resilience ritual that keeps morale high during shifts.",
        ],
        "expected_outcome": "An adaptation protocol that keeps change intentional and values-based.",
    },
    "09": {
        "title": "Influence Calibration Session",
        "prompt": "Use psychology and empathy to design the next persuasive move.",
        "steps": [
            "Clarify the other party’s motives, concerns, and desired wins.",
            "Craft a message that aligns their incentives with your strategic objective.",
            "Decide what emotional tone best opens the conversation.",
            "Plan follow-up actions that reinforce trust after the interaction.",
        ],
        "expected_outcome": "A thoughtful influence plan that advances results while preserving integrity.",
    },
    "10": {
        "title": "Execution Launch Plan",
        "prompt": "Convert a strategic initiative into disciplined rhythm.",
        "steps": [
            "Break the initiative into weekly commitments with owners and deadlines.",
            "Define the scorecard that will show momentum or drift.",
            "Schedule implementation reviews that protect focus.",
            "Document lessons learned to fuel the next strategic cycle.",
        ],
        "expected_outcome": "A cadence that keeps strategy alive through consistent, measurable execution.",
    },
}


def slugify(text: str) -> str:
    text = re.sub(r"[^a-zA-Z0-9\s-]", "", text)
    text = re.sub(r"\s+", "-", text.strip().lower())
    text = re.sub(r"-+", "-", text)
    return text or "entry"


def _ensure_sentence(text: str) -> str:
    text = _sentence_case(text)
    if not text:
        return text
    if not text.endswith((".", "!", "?")):
        text = f"{text}."
    return text


def _sentence_case(text: str) -> str:
    text = text.strip()
    if not text:
        return text
    first = text[0]
    if first.isalpha() and first.islower():
        text = f"{first.upper()}{text[1:]}"
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
    candidate = re.sub(r"^(this chapter|the chapter|it|they|these|strategy|let's|lets)\s+", "", candidate, flags=re.I).strip()
    candidate = re.sub(r"^(focuses on|explores|examines|describes|introduces|lets begin with)\s+", "", candidate, flags=re.I).strip()
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
