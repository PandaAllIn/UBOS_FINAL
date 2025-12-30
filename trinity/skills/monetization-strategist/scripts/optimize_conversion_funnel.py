from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from utils import log_event

STEPS_ORDER = ["visitors", "signups", "trials", "customers"]


def load_funnel(path: str) -> dict[str, float]:
    with Path(path).open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    return {k: float(v) for k, v in data.items()}


def analyse_funnel(funnel: dict[str, float]) -> list[dict[str, Any]]:
    items = []
    for idx in range(len(STEPS_ORDER) - 1):
        current = STEPS_ORDER[idx]
        nxt = STEPS_ORDER[idx + 1]
        current_val = funnel.get(current, 0.0)
        next_val = funnel.get(nxt, 0.0)
        if current_val <= 0:
            rate = 0.0
        else:
            rate = next_val / current_val
        drop = 1 - rate
        items.append({
            "stage": f"{current} → {nxt}",
            "conversion": round(rate * 100, 2),
            "drop": round(drop * 100, 2),
            "priority": drop,
        })
    items.sort(key=lambda item: item["priority"], reverse=True)
    return items


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Analyse conversion funnel and suggest optimizations.")
    parser.add_argument("--funnel-data", required=True, help="JSON file with visitors/signups/trials/customers counts")
    parser.add_argument("--json", action="store_true", help="Emit JSON output")
    args = parser.parse_args(argv)

    funnel = load_funnel(args.funnel_data)
    insights = analyse_funnel(funnel)
    recommendations = []
    for item in insights:
        if "visitors" in item["stage"]:
            recommendations.append("Improve landing page messaging (headline + social proof).")
        elif "signups" in item["stage"]:
            recommendations.append("Optimize onboarding email sequence to encourage trial activation.")
        elif "trials" in item["stage"]:
            recommendations.append("Introduce in-app checklist and trial CTA for upgrade.")
    payload = {"funnel": funnel, "insights": insights, "recommendations": recommendations[:3]}

    log_event("funnel_analysis", payload)

    if args.json:
        print(json.dumps(payload, indent=2))
    else:
        for idx, item in enumerate(insights, start=1):
            print(f"{idx}. Stage {item['stage']}: conversion {item['conversion']}%, drop {item['drop']}%")
        if recommendations:
            print("\nRecommended actions:")
            for rec in recommendations[:3]:
                print(f"- {rec}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
