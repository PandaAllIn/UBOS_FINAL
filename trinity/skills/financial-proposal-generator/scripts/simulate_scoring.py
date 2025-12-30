from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Dict

from utils import tokenize

KEYWORDS = json.loads((Path(__file__).resolve().parents[1] / "assets" / "scoring_rubric.json").read_text(encoding="utf-8"))

SECTION_WEIGHTS = {
    "innovation": ["innovation", "novel", "unique", "first", "state-of-the-art"],
    "methodology": ["methodology", "approach", "work package", "task", "deliverable"],
    "track_record": ["track record", "experience", "previous", "award", "publication"],
    "infrastructure": ["infrastructure", "facility", "equipment", "resource"],
    "pathway": ["impact", "benefit", "milestone", "kpi"],
    "measures": ["dissemination", "exploitation", "communication", "strategy"],
    "communication": ["policy", "public", "engagement", "stakeholder"],
    "sustainability": ["sustainability", "long-term", "business model", "scaling"],
    "work_plan": ["work plan", "wp", "gantt", "timeline"],
    "management": ["management", "governance", "oversight", "risk"],
    "consortium": ["consortium", "partner", "expertise"],
    "resources": ["budget", "person-month", "resource"]
}

SECTION_SPLIT = {
    "excellence": ["innovation", "methodology", "track_record", "infrastructure"],
    "impact": ["pathway", "measures", "communication", "sustainability"],
    "implementation": ["work_plan", "management", "consortium", "resources"],
}


def score_section(text: str, section: str) -> Dict[str, float]:
    tokens = tokenize(text)
    scores = {}
    for dimension in SECTION_SPLIT[section]:
        keywords = SECTION_WEIGHTS[dimension]
        hits = sum(1 for token in tokens if token in keywords)
        ratio = hits / max(1, len(text.split()) / 200)  # heuristic density per 200 words
        weight = KEYWORDS[section].get(dimension, 0.25)
        raw = min(5.0, 1.5 + ratio * 1.5)
        scores[dimension] = round(raw * weight, 2)
    return scores


def aggregate(scores: Dict[str, float], section: str) -> float:
    weight_map = KEYWORDS[section]
    total = 0.0
    for dimension, value in scores.items():
        weight = weight_map.get(dimension, 0.25)
        total += value / weight * weight
    return round(min(5.0, total), 2)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Simulate evaluator scoring for proposal narratives.")
    parser.add_argument("--narrative", required=True, help="Narrative markdown path")
    parser.add_argument("--section", choices=sorted(SECTION_SPLIT.keys()), required=True)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)

    text = Path(args.narrative).read_text(encoding="utf-8") if Path(args.narrative).exists() else ""
    component_scores = score_section(text, args.section)
    total = aggregate(component_scores, args.section)
    payload = {
        "section": args.section,
        "score": total,
        "components": component_scores,
        "recommendation": "Review keywords and add quantitative evidence" if total < KEYWORDS["thresholds"]["excellent"] else "Section meets excellence target",
    }
    if args.json:
        print(json.dumps(payload, indent=2))
    else:
        print(f"Section score: {total}/5")
        for dimension, value in component_scores.items():
            print(f"- {dimension}: {value}")
        print(payload["recommendation"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
