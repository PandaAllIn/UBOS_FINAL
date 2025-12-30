from __future__ import annotations

import argparse
import json
from typing import Any

from utils import assembly_path, append_log

KEYWORDS = {
    "excellence": ["innovation", "methodology", "ambition", "ai", "constitutional"],
    "impact": ["impact", "benefit", "economic", "social", "environmental", "sustainability"],
    "implementation": ["work package", "milestone", "timeline", "risk", "management"],
}


def load_text(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def score_section(text: str, keywords: list[str]) -> float:
    if not text:
        return 0.0
    text_lower = text.lower()
    hits = sum(1 for word in keywords if word in text_lower)
    density = min(1.0, len(text.split()) / 5000)  # scale by length
    raw = (hits / len(keywords) * 3.5) + (density * 1.5)
    return round(min(5.0, 1.5 + raw), 2)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Simulate EU evaluator scoring for a proposal assembly.")
    parser.add_argument("--assembly", required=True, help="Assembly identifier")
    parser.add_argument("--json", action="store_true", help="Emit JSON output")
    args = parser.parse_args(argv)

    assembly_dir = assembly_path(args.assembly)
    narratives_dir = assembly_dir / "narratives"

    excellence = load_text(narratives_dir / "excellence.md")
    impact = load_text(narratives_dir / "impact.md")
    implementation = load_text(narratives_dir / "implementation.md")

    scores = {
        "excellence": score_section(excellence, KEYWORDS["excellence"]),
        "impact": score_section(impact, KEYWORDS["impact"]),
        "implementation": score_section(implementation, KEYWORDS["implementation"]),
    }
    total = round(sum(scores.values()), 2)
    average = round(total / 3 if scores else 0.0, 2)

    report = {
        "assembly": args.assembly,
        "scores": scores,
        "total": total,
        "average": average,
        "recommendation": "Ready for submission" if average >= 4.6 else "Improve narratives to reach ≥4.6 average",
    }

    if args.json:
        print(json.dumps(report, indent=2))
    else:
        for section, value in scores.items():
            print(f"{section.title()}: {value}/5")
        print(f"Average: {average}/5 (total {total}/15)")
        print(report["recommendation"])

    append_log("simulate_scoring", report)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
