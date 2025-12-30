from __future__ import annotations

import argparse
import json
from pathlib import Path

from utils import read_markdown, write_markdown

SUGGESTIONS = {
    "ambition": "Add quantitative targets and timeline milestones.",
    "impact": "Quantify beneficiaries and link to EU policies.",
    "sustainability": "Detail post-project governance and funding.",
    "communication": "Define audience-specific channels with metrics.",
    "consortium": "Highlight partner track record and complementary expertise.",
}


def apply_suggestions(text: str, target_score: float) -> dict[str, str]:
    improvements = {}
    if target_score >= 4.6 and "impact" in text.lower():
        improvements["impact"] = "Include impact pathway table with KPIs and diffusion assumptions."
    if "governance" not in text.lower():
        improvements["implementation"] = "Describe management bodies, decision processes, and risk response triggers."
    return improvements


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Suggest narrative improvements towards target score.")
    parser.add_argument("--narrative", required=True)
    parser.add_argument("--target-score", type=float, default=4.6)
    parser.add_argument("--feedback", help="Optional JSON feedback file")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)

    text = read_markdown(Path(args.narrative))
    improvements = apply_suggestions(text, args.target_score)
    external_feedback = {}
    if args.feedback and Path(args.feedback).exists():
        external_feedback = json.loads(Path(args.feedback).read_text(encoding="utf-8"))
        improvements.update(external_feedback)

    payload = {"target_score": args.target_score, "recommendations": improvements}
    if args.json:
        print(json.dumps(payload, indent=2))
    else:
        for key, value in improvements.items():
            print(f"- {key}: {value}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
