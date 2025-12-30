from __future__ import annotations

import argparse
import json
from datetime import date
from typing import Any

from utils import (
    compute_health,
    emoji_for_score,
    load_state,
    log_event,
    save_state,
)


def _parse_date(value: str | None) -> date | None:
    if not value:
        return None
    try:
        return date.fromisoformat(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError(f"Invalid date '{value}'") from exc


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Calculate Malaga Embassy health score.")
    parser.add_argument("--date", type=_parse_date, help="Report date (YYYY-MM-DD)")
    parser.add_argument("--burn-rate", type=float, help="Override burn rate for this calculation")
    parser.add_argument("--runway", type=float, help="Override runway days")
    parser.add_argument("--capital-remaining", type=float, help="Override capital remaining before calculation")
    parser.add_argument("--json", action="store_true", help="Emit JSON instead of formatted text")
    args = parser.parse_args(argv)

    state = load_state()
    if args.capital_remaining is not None:
        state.setdefault("capital", {})["remaining"] = args.capital_remaining
    if args.burn_rate is not None:
        state.setdefault("metrics", {})["burn_rate"] = args.burn_rate
    if args.runway is not None:
        state.setdefault("metrics", {})["runway_days"] = args.runway

    summary = compute_health(state, reference=args.date)
    save_state(state)

    payload: dict[str, Any] = {
        "score": summary["score"],
        "components": summary["components"],
        "burn_rate": summary["burn_rate"],
        "runway_days": summary["runway_days"],
        "recommendations": summary["recommendations"],
        "date": (args.date or date.today()).isoformat(),
    }
    log_event("health_score", payload)

    if args.json:
        print(json.dumps(payload, indent=2))
    else:
        emoji = emoji_for_score(summary["score"])
        components = summary["components"]
        lines = [
            f"MALAGA EMBASSY HEALTH REPORT {emoji}",
            f"Score: {summary['score']}/100",
            f"  Budget adherence: {components['budget']}/25",
            f"  Runway: {components['runway']}/20",
            f"  Revenue progress: {components['revenue']}/25",
            f"  Constitutional compliance: {components['compliance']}/30",
            f"Burn rate: €{summary['burn_rate']:.2f}/day",
            f"Runway: {summary['runway_days']:.1f} days",
        ]
        if summary["recommendations"]:
            lines.append("Recommendations:")
            for item in summary["recommendations"]:
                lines.append(f"- {item}")
        output = "\n".join(lines)
        print(output)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
