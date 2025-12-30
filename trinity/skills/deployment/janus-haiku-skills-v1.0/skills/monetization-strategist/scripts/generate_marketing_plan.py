from __future__ import annotations

import argparse
import math
from pathlib import Path
from typing import Any

from utils import PATHS, ensure_directories, save_json, log_event

CHANNEL_CAC = {
    "seo": 400,
    "ads": 900,
    "webinar": 600,
    "affiliate": 300,
}


def generate_plan(target_customers: int, budget: float, channels: list[str], months: int) -> dict[str, Any]:
    months = max(1, months)
    monthly_budget = budget / months
    per_channel_budget = monthly_budget / len(channels) if channels else 0.0

    schedule = []
    cumulative_customers = 0.0
    for month in range(1, months + 1):
        month_entry = {"month": month, "spend": 0.0, "customers": 0.0, "channels": []}
        for channel in channels:
            cac = CHANNEL_CAC.get(channel, 600)
            spend = per_channel_budget
            customers = spend / cac
            month_entry["channels"].append({"channel": channel, "spend": round(spend, 2), "expected_customers": round(customers, 2)})
            month_entry["spend"] += spend
            month_entry["customers"] += customers
        cumulative_customers += month_entry["customers"]
        month_entry["cumulative_customers"] = round(cumulative_customers, 2)
        month_entry["spend"] = round(month_entry["spend"], 2)
        month_entry["customers"] = round(month_entry["customers"], 2)
        schedule.append(month_entry)

    projected_customers = round(cumulative_customers, 2)
    attainment = projected_customers / target_customers if target_customers else 0.0
    return {
        "target_customers": target_customers,
        "budget": round(budget, 2),
        "months": months,
        "channels": channels,
        "schedule": schedule,
        "projected_customers": projected_customers,
        "attainment_ratio": round(attainment, 2),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Generate EUFM marketing plan with channel allocations.")
    parser.add_argument("--target-customers", type=int, required=True, help="Target new customers to acquire")
    parser.add_argument("--budget", type=float, required=True, help="Total marketing budget (EUR)")
    parser.add_argument("--channels", type=lambda s: [c.strip() for c in s.split(',') if c.strip()], default="seo,ads,webinar", help="Comma-separated channel list")
    parser.add_argument("--months", type=int, default=6, help="Planning horizon in months")
    parser.add_argument("--output", help="Optional JSON output path")
    args = parser.parse_args(argv)

    ensure_directories()
    plan = generate_plan(args.target_customers, args.budget, args.channels, args.months)

    if args.output:
        save_json(Path(args.output), plan)
        print(f"Marketing plan saved to {args.output}")
    else:
        print(json.dumps(plan, indent=2))

    log_event("marketing_plan", {"target_customers": args.target_customers, "budget": args.budget, "channels": args.channels, "months": args.months})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
