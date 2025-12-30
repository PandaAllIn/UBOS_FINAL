from __future__ import annotations

import argparse
import json
from typing import Sequence

from utils import (  # type: ignore
    Opportunity,
    append_log,
    ensure_directories,
    format_euro,
    load_pipeline_state,
    resolve_paths,
    save_pipeline_state,
    transmit_puck,
    utc_now,
)

REMINDER_THRESHOLDS = (90, 60, 30, 7)
PROJECT_ACTIONS: dict[str, list[str]] = {
    "GeoDataCenter Oradea": [
        "Finalise consortium partner agreements",
        "Complete geothermal feasibility model",
        "Schedule internal budget review",
    ],
    "Xylella Stage 2 (XYL-PHOS-CURE)": [
        "Confirm farmer cooperative participation",
        "Prepare phytosanitary compliance dossier",
        "Draft field trial timeline",
    ],
    "EU Funding Mastermind (EUFM)": [
        "Align product roadmap with call requirements",
        "Collect customer validation metrics",
        "Update ARR growth projections",
    ],
    "Malaga Embassy Operations": [
        "Book field deployment logistics",
        "Confirm on-site partner meetings",
        "Prepare embassy operating budget",
    ],
    "Portal Oradea": [
        "Gather latest municipal datasets",
        "Update investor outreach narrative",
        "Review platform infrastructure requirements",
    ],
}


def generate_actions(opportunity: Opportunity) -> list[str]:
    if opportunity.ubos_project_match and opportunity.ubos_project_match in PROJECT_ACTIONS:
        return PROJECT_ACTIONS[opportunity.ubos_project_match]
    return [
        "Review proposal status and outstanding documents",
        "Confirm consortium roles and compliance checks",
        "Schedule internal readiness review",
    ]


def build_alert(opportunity: Opportunity, days_remaining: int) -> dict[str, object]:
    action_items = generate_actions(opportunity)
    return {
        "type": "grant_deadline_alert",
        "opportunity_id": opportunity.opportunity_id,
        "title": opportunity.title,
        "program": opportunity.program,
        "deadline": opportunity.deadline.isoformat() if opportunity.deadline else None,
        "days_remaining": days_remaining,
        "fit_score": opportunity.fit_score,
        "project": opportunity.ubos_project_match,
        "budget_range": (format_euro(opportunity.budget_min), format_euro(opportunity.budget_max)),
        "next_actions": action_items,
        "discovered": opportunity.discovered_date.isoformat(),
    }


def track_deadlines(dry_run: bool = False) -> int:
    paths = resolve_paths()
    ensure_directories(paths)
    payload = load_pipeline_state(paths)
    opportunities: list[Opportunity] = payload.get("opportunities", [])
    alerts_dispatched = 0
    now = utc_now()

    for opportunity in opportunities:
        if not opportunity.deadline:
            continue
        days = opportunity.days_until_deadline(now)
        if days is None or days < 0:
            continue
        if days not in REMINDER_THRESHOLDS:
            continue
        if days in opportunity.reminders_sent:
            continue
        alert = build_alert(opportunity, days)
        if not dry_run:
            transmit_puck(
                alert,
                recipients=("claude", "gemini", "codex", "captain"),
                rhythm="urgent_burst" if days <= 30 else "standard",
                tone="time_sensitive",
                paths=paths,
            )
            append_log("deadline_alert", alert, paths=paths)
            opportunity.reminders_sent.append(days)
        alerts_dispatched += 1

    if not dry_run:
        save_pipeline_state(opportunities, metadata={"generated_at": now.isoformat(), "source": "deadline_tracker"}, paths=paths)

    return alerts_dispatched


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Trigger multi-stage deadline reminders for grant opportunities.")
    parser.add_argument("--dry-run", action="store_true", help="Do not send alerts or persist changes")
    args = parser.parse_args(argv)

    count = track_deadlines(dry_run=args.dry_run)
    result = {"alerts_sent": count, "dry_run": args.dry_run}
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
