from __future__ import annotations

import argparse
import json
from datetime import date

from utils import (
    PATHS,
    append_jsonl,
    compute_health,
    load_state,
    log_event,
    save_state,
    transmit_puck,
)

TARGET_BURN = 35.0


def _parse_date(value: str | None) -> date | None:
    if not value:
        return None
    try:
        return date.fromisoformat(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError(f"Invalid date '{value}'") from exc


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run Malaga Embassy emergency protocol checks.")
    parser.add_argument("--date", type=_parse_date, help="Reference date (YYYY-MM-DD)")
    parser.add_argument("--dry-run", action="store_true", help="Evaluate only; do not log or notify")
    parser.add_argument("--json", action="store_true", help="Emit JSON report")
    args = parser.parse_args(argv)

    state = load_state()
    health = compute_health(state, reference=args.date)
    save_state(state)

    runway = health["runway_days"]
    burn_rate = health["burn_rate"]
    emergency_spent = float(state.get("cascade", {}).get("emergency", {}).get("spent", 0.0))
    emergency_allocation = float(state.get("cascade", {}).get("emergency", {}).get("allocation", 0.0))
    emergency_available = emergency_spent < emergency_allocation

    triggers = []
    if runway < 14:
        triggers.append(f"Runway below 14 days ({runway:.1f})")
    if burn_rate > TARGET_BURN * 1.5:
        triggers.append(f"Burn rate spike detected (€{burn_rate:.2f}/day)")

    status = "STABLE" if not triggers else "CRITICAL"

    response_plan = []
    if triggers:
        response_plan.append("Freeze non-essential spending (Operations & Projects).")
        if emergency_available:
            response_plan.append("Activate 10% Emergency Reserve to restore runway.")
        else:
            response_plan.append("Emergency Reserve already used; seek immediate revenue or external funding.")
        response_plan.append("Accelerate revenue outreach (all three streams) with incentives.")
        response_plan.append("Audit last 7 days of spending for anomalies.")

    report = {
        "status": status,
        "triggers": triggers,
        "health_score": health["score"],
        "runway_days": runway,
        "burn_rate": burn_rate,
        "emergency_available": emergency_available,
        "response_plan": response_plan,
        "timestamp": (args.date or date.today()).isoformat(),
    }

    if not args.dry_run and triggers:
        append_jsonl(PATHS.emergency_log, report)
        log_event("emergency_protocol", report)
        puck = {
            "type": "malaga_emergency_alert",
            "triggers": triggers,
            "runway_days": runway,
            "burn_rate": burn_rate,
            "actions": response_plan[:3],
        }
        transmit_puck(puck, recipients=("captain", "claude", "gemini", "codex"), rhythm="urgent_burst", tone="critical_alert")

    if args.json:
        print(json.dumps(report, indent=2))
    else:
        if triggers:
            print("🚨 EMERGENCY PROTOCOL ACTIVATED 🚨")
            for trigger in triggers:
                print(f"- {trigger}")
            print()
            print("Response Plan:")
            for action in response_plan:
                print(f"- {action}")
        else:
            print("No emergency triggers detected. Systems nominal.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
