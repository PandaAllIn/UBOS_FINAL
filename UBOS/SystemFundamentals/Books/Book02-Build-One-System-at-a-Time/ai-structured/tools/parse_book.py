#!/usr/bin/env python3
"""Generate curated AI-structured assets for 'Build One System at a Time'."""

import re
import shutil
from pathlib import Path
from textwrap import dedent

import yaml

ROOT = Path(__file__).resolve().parents[6]
BOOK_ROOT = ROOT / "UBOS" / "SystemFundamentals" / "Books" / "Book02-Build-One-System-at-a-Time"
SOURCE_ROOT = BOOK_ROOT / "source"
CHAPTER_SOURCE_ROOT = SOURCE_ROOT / "chapters"
AI_ROOT = BOOK_ROOT / "ai-structured" / "build-one-system-at-a-time"
CHAPTERS_ROOT = AI_ROOT / "chapters"
BOOK_YAML_PATH = AI_ROOT / "book.yaml"

AUTHOR = "Justice O. Malcolm"
SUMMARY_SENTENCE_LIMIT = 6

TOPIC_MAP = {
    "00": ["abundance", "mindset", "system"],
    "01": ["mindset", "abundance", "system"],
    "02": ["system", "structure", "clarity"],
    "03": ["clarity", "leverage", "feedback", "resilience"],
    "04": ["alignment", "leverage", "clarity"],
    "05": ["automation", "resilience", "structure"],
    "06": ["environment", "alignment", "automation"],
    "07": ["integration", "rhythm", "system"],
    "08": ["feedback", "adaptability", "clarity"],
    "09": ["leverage", "alignment", "system"],
    "10": ["energy", "routine", "resilience"],
    "11": ["time", "leverage", "automation"],
    "12": ["network", "contribution", "identity"],
    "13": ["resilience", "system", "risk"],
    "14": ["adaptability", "feedback", "structure"],
    "15": ["mindset", "abundance", "awareness"],
    "16": ["futurecasting", "identity", "alignment"],
    "17": ["legacy", "contribution", "structure"],
    "18": ["contribution", "network", "alignment"],
    "19": ["mindset", "rhythm", "resilience"],
}

OBJECTIVES = {
    "00": [
        "Recognize that durable transformation is built by deliberate systems, not one-off goals.",
        "Differentiate scarcity defences from abundance-driven creation.",
        "Commit to sequencing growth through one high-leverage system at a time.",
    ],
    "01": [
        "Identify how scarcity thinking reinforces defensive routines and hesitation.",
        "Describe how abundance thinking widens opportunities through design.",
        "Adopt systems thinking as the metric for sustainable results.",
    ],
    "02": [
        "Explain why outcomes collapse without a repeatable supporting system.",
        "Shift focus from goal chasing to process design.",
        "Map willpower-heavy routines into dependable structures.",
    ],
    "03": [
        "Internalize the ten principles that define abundant systems.",
        "Assess a system against sustainability, leverage, and feedback.",
        "Design for identity alignment so upgrades feel natural, not forced.",
    ],
    "04": [
        "Evaluate potential starting points by impact, confidence, and alignment.",
        "Select one high-leverage system that unlocks cascading benefits.",
        "Translate vision into a clear system definition for the current season.",
    ],
    "05": [
        "Engineer routines for effortless repeatability instead of heroic effort.",
        "Use triggers, automation, and friction removal to stabilize execution.",
        "Build resilient systems that work on hard days as well as ideal ones.",
    ],
    "06": [
        "Recognize environment as silent architecture shaping behaviour.",
        "Audit physical, digital, and social spaces for alignment with systems.",
        "Deliberately embed cues that keep priority work on autopilot.",
    ],
    "07": [
        "Link systems so energy and insight compound across domains.",
        "Identify hinge habits that can be stacked for leverage.",
        "Draft rhythm maps that keep linked systems synchronized.",
    ],
    "08": [
        "Construct feedback loops that inform both outcomes and process.",
        "Distinguish between momentum signals and warning indicators.",
        "Schedule reviews that translate data into actionable refinements.",
    ],
    "09": [
        "Pinpoint the keystone system that amplifies multiple results.",
        "Score systems by breadth of impact and ease of maintenance.",
        "Sequence supporting systems around the keystone for momentum.",
    ],
    "10": [
        "Manage four dimensions of energy as the currency of systems.",
        "Diagnose leaks in physical, emotional, mental, and spiritual energy.",
        "Design replenishment rituals that stabilize performance.",
    ],
    "11": [
        "Differentiate between spending time and multiplying time with leverage.",
        "Apply automation, delegation, and elimination to reclaim capacity.",
        "Map leverage plays to the system’s maturity curve.",
    ],
    "12": [
        "View networks as strategic assets, not passive connections.",
        "Design systems that keep relationships reciprocal and purposeful.",
        "Integrate contribution into network rhythms to compound trust.",
    ],
    "13": [
        "Architect fail-safes that keep systems operational during disruption.",
        "Define reduced modes and safety nets before crises arrive.",
        "Test resilience plans so they activate without hesitation.",
    ],
    "14": [
        "Recognize signals that a system has been outgrown.",
        "Design upgrade loops that rebuild without losing momentum.",
        "Document post-mortems to inform the next iteration.",
    ],
    "15": [
        "Detect scarcity traps disguised as productivity or success.",
        "Challenge scripts that push reactive, fear-driven behaviour.",
        "Replace hidden scarcity reflexes with abundance-based responses.",
    ],
    "16": [
        "Treat the future as a living system under active construction.",
        "Use scenario design to test resilience of long-term plans.",
        "Anchor daily actions in the identity of the future builder.",
    ],
    "17": [
        "Extend systems thinking to generational impact and stewardship.",
        "Define what legacy-quality systems look like in practice.",
        "Create governance rhythms that keep successors empowered.",
    ],
    "18": [
        "Align personal systems with contribution and service.",
        "Design impact loops that deliver value to others reliably.",
        "Measure contribution alongside personal metrics of success.",
    ],
    "19": [
        "Adopt a life-long posture of building one system at a time.",
        "Sustain growth by iterating with patience and rhythm.",
        "Celebrate identity evolution as the true reward of systems work.",
    ],
}

PRACTICES = {
    "00": {
        "title": "Launch Your Systems Mindset",
        "prompt": "Use this reflection to shift from goal chasing to system architecture.",
        "steps": [
            "List three ambitions currently dependent on willpower alone.",
            "Describe the supporting system that would make each ambition inevitable.",
            "Identify one system to build first and note why it offers the greatest leverage.",
            "Schedule a weekly checkpoint to monitor the new system’s momentum.",
        ],
        "expected_outcome": "Clear commitment to start with one high-leverage system anchored in abundance thinking.",
    },
    "01": {
        "title": "Scarcity-to-Abundance Audit",
        "prompt": "Contrast scarcity defences with abundance design across core routines.",
        "steps": [
            "Catalog routines or beliefs currently driven by protection or fear.",
            "Describe the abundance-based alternative for each pattern.",
            "Select one area to rebuild using system design rather than effort.",
            "Document how success will be measured by system quality, not short-term outcomes.",
        ],
        "expected_outcome": "A reframed routine that moves from defensive scarcity to expansive system design.",
    },
    "02": {
        "title": "Process Before Outcome Planner",
        "prompt": "Transform a lingering goal into a dependable system.",
        "steps": [
            "State the goal that has stalled or repeatedly reset.",
            "Define the repeatable actions that would guarantee progress regardless of motivation.",
            "Design checkpoints and triggers that keep the process running automatically.",
            "Write a personal rule that prioritizes running the system over chasing the metric.",
        ],
        "expected_outcome": "A documented system that makes the desired outcome a byproduct of consistent execution.",
    },
    "03": {
        "title": "Abundant System Scorecard",
        "prompt": "Evaluate a current system against the ten abundant system principles.",
        "steps": [
            "Select one existing system to assess in depth.",
            "Score the system 1-5 for each principle: clarity, sustainability, leverage, adaptability, feedback, integration, identity alignment, scalability, resilience, contribution.",
            "Highlight principles scoring three or below and note specific shortcomings.",
            "Design targeted upgrades for the weakest principles and schedule implementation dates.",
        ],
        "expected_outcome": "Prioritized upgrade plan that strengthens the system across all abundance principles.",
    },
    "04": {
        "title": "High-Leverage Start Blueprint",
        "prompt": "Choose the first system with maximum upside and realistic capacity.",
        "steps": [
            "Brainstorm potential starting systems and note why each matters now.",
            "Rate candidates on urgency, confidence, and alignment with your long-term vision.",
            "Select the top-scoring system and write a precise problem statement it will solve.",
            "Define what early momentum looks like in the next 30 days and set checkpoints.",
        ],
        "expected_outcome": "Clarity on the single system to build first, backed by a motivation and capacity map.",
    },
    "05": {
        "title": "Repeatability Design Lab",
        "prompt": "Refine a system so it runs smoothly even on chaotic days.",
        "steps": [
            "Document the current steps of the system you want to stabilize.",
            "List friction points or dependencies that cause inconsistency.",
            "Introduce triggers, automation, or support assets that remove those frictions.",
            "Stress-test the redesign against a low-energy day and adjust until it still performs.",
        ],
        "expected_outcome": "A simplified, automation-ready routine that works under pressure and fatigue.",
    },
    "06": {
        "title": "Environment Alignment Sweep",
        "prompt": "Engineer spaces that make your priority system the default.",
        "steps": [
            "Walk through your physical workspace and mark any element that disrupts focus.",
            "Audit your digital environment for notifications, tabs, or files that create drag.",
            "Identify people or contexts that reinforce or erode the system and plan adjustments.",
            "Install cues, tools, or boundaries that keep the environment reinforcing your design.",
        ],
        "expected_outcome": "An environment intentionally configured to keep the target system on autopilot.",
    },
    "07": {
        "title": "System Stack Mapping",
        "prompt": "Link complementary systems so they compound energy and output.",
        "steps": [
            "List current systems and note the trigger that begins each one.",
            "Highlight natural handoffs where one system’s output feeds another’s input.",
            "Design a daily or weekly rhythm map that orders systems for the least friction.",
            "Pilot the sequence and adjust timing until the stack feels fluid and sustainable.",
        ],
        "expected_outcome": "An integrated rhythm that chains key systems together for compounding momentum.",
    },
    "08": {
        "title": "Feedback Loop Builder",
        "prompt": "Create data-driven reviews that keep systems on course.",
        "steps": [
            "Define the outcome metric and leading indicators that matter for the system.",
            "Decide when and how those indicators will be captured without adding heavy overhead.",
            "Write three review questions that convert data into decisions.",
            "Schedule recurring reflection blocks to close the loop and apply adjustments.",
        ],
        "expected_outcome": "A feedback cadence that keeps the system adaptive instead of reactive.",
    },
    "09": {
        "title": "Keystone System Discovery",
        "prompt": "Surface the single system that multiplies results elsewhere.",
        "steps": [
            "Create a matrix of current systems versus domains they influence (health, work, finances, relationships).",
            "Score each system on breadth of impact and ease of maintenance.",
            "Select the system with the highest combined score as your keystone.",
            "Design supporting routines that protect and amplify the keystone system.",
        ],
        "expected_outcome": "Focused attention on the keystone system with supporting structures to magnify its reach.",
    },
    "10": {
        "title": "Energy Portfolio Review",
        "prompt": "Balance the four energy dimensions that fuel every system.",
        "steps": [
            "Rate physical, emotional, mental, and spiritual energy on a 1-5 scale.",
            "Note patterns or behaviours currently draining each category.",
            "Design replenishment rituals tailored to the lowest-scoring dimension.",
            "Schedule those rituals inside the system cadence and set a follow-up review date.",
        ],
        "expected_outcome": "A replenishment plan that keeps energy available for system execution.",
    },
    "11": {
        "title": "Time Multiplication Canvas",
        "prompt": "Apply leverage to reclaim meaningful hours.",
        "steps": [
            "List recurring tasks consuming the most time inside the system.",
            "Decide which tasks can be automated, delegated, or eliminated entirely.",
            "Design SOPs or automations for the top leverage opportunities.",
            "Track the hours saved and reinvest them into higher-value work.",
        ],
        "expected_outcome": "A leverage playbook that multiplies available time for the system.",
    },
    "12": {
        "title": "Network Flywheel Sprint",
        "prompt": "Design relationship systems that compound trust and opportunity.",
        "steps": [
            "Map the relationships most critical to your current strategic goals.",
            "Define the value you can contribute to each connection on a recurring basis.",
            "Build a follow-up rhythm (calendar, CRM, or ritual) that keeps interactions intentional.",
            "Set a contribution metric that signals the network is strengthening.",
        ],
        "expected_outcome": "A reciprocal relationship system that turns your network into a growth engine.",
    },
    "13": {
        "title": "Failsafe Design Drill",
        "prompt": "Prepare your system to operate during turbulence.",
        "steps": [
            "List realistic stress scenarios that could derail the system.",
            "For each scenario, define the reduced mode that keeps progress alive.",
            "Assign responsibilities or triggers for activating each failsafe.",
            "Run a tabletop simulation to ensure the plan works when pressure hits.",
        ],
        "expected_outcome": "Documented contingency plans that keep the system resilient under pressure.",
    },
    "14": {
        "title": "System Upgrade Review",
        "prompt": "Decide when to redesign versus maintain.",
        "steps": [
            "List signals that the system is producing diminishing returns or friction.",
            "Capture lessons learned from recent breakdowns or plateaus.",
            "Draft the next version of the system, noting what to preserve and what to replace.",
            "Plan a pilot period and review criteria for the upgraded system.",
        ],
        "expected_outcome": "Clarity on how to rebuild the system without losing accumulated momentum.",
    },
    "15": {
        "title": "Scarcity Trap Detector",
        "prompt": "Reveal sophisticated scarcity patterns hiding in plain sight.",
        "steps": [
            "Review recent decisions that felt urgent or fear-driven and note the trigger.",
            "Identify the scarcity story underneath each decision.",
            "Rewrite the story using abundance language and desired identity.",
            "Define the system change that will prevent the scarcity reflex from returning.",
        ],
        "expected_outcome": "Rewritten scripts that keep advanced scarcity traps from steering your systems.",
    },
    "16": {
        "title": "Future System Sketch",
        "prompt": "Design today with the future builder in mind.",
        "steps": [
            "Write a narrative describing your life three years from now with systems fully mature.",
            "List systems that must exist to make that future inevitable.",
            "Identify one system capable of bridging a present gap toward that future.",
            "Schedule quarterly scenario reviews to stress-test the plan against change.",
        ],
        "expected_outcome": "A living roadmap that keeps current actions aligned with long-range identity.",
    },
    "17": {
        "title": "Legacy Stewardship Plan",
        "prompt": "Extend system thinking beyond your personal involvement.",
        "steps": [
            "Define the values and outcomes your legacy system must protect.",
            "List stakeholders who will inherit or benefit from the system.",
            "Document governance rhythms (reviews, decision rights, escalation paths).",
            "Create onboarding materials that teach successors how to maintain and evolve the system.",
        ],
        "expected_outcome": "A stewardship framework that keeps the system thriving across generations.",
    },
    "18": {
        "title": "Contribution Alignment Session",
        "prompt": "Ensure your systems deliver value beyond personal gain.",
        "steps": [
            "Name the communities or audiences you intend to serve consistently.",
            "Match existing systems with the contribution each audience receives.",
            "Identify gaps where service is inconsistent or transactional.",
            "Design a contribution loop that delivers value and captures learning from recipients.",
        ],
        "expected_outcome": "Aligned systems that create meaningful impact while reinforcing personal growth.",
    },
    "19": {
        "title": "Forever Builder Ritual",
        "prompt": "Anchor the identity of building one system at a time for life.",
        "steps": [
            "Review the systems created this year and document the lesson each delivered.",
            "Choose one system to retire, one to refine, and one to build next.",
            "Establish a celebration ritual that honors progress over perfection.",
            "Write a pledge describing how you will keep iterating with patience and rhythm.",
        ],
        "expected_outcome": "A personal operating rhythm that sustains lifelong system building.",
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
    if not text.endswith(('.', '!', '?')):
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
    candidate = re.sub(r"^(this chapter|the chapter|it|they|these|systems?|let's|lets)\s+", "", candidate, flags=re.I).strip()
    candidate = re.sub(r"^(focuses on|explores|examines|describes|introduces)\s+", "", candidate, flags=re.I).strip()
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
    topics = TOPIC_MAP.get(chapter_id, ["system"])
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
            one_liner = cleaned.split(".")[0].strip()
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
    topics = TOPIC_MAP.get(chapter_id, ["system"])
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
    topics = TOPIC_MAP.get(chapter_id, ["system"])
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
        "topics": TOPIC_MAP.get(chapter_id, ["system"]),
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
