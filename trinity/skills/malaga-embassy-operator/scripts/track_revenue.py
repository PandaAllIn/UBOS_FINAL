from __future__ import annotations

import argparse
import json
from datetime import date

from utils import (
    PATHS,
    compute_health,
    load_state,
    log_event,
    register_revenue,
    save_state,
    transmit_puck,
)

STREAM_CHOICES = ["agent-as-a-service", "intel-services", "proposal-consultation"]


def _parse_date(value: str | None) -> date | None:
    if not value:
        return None
    try:
        return date.fromisoformat(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError(f"Invalid date '{value}'") from exc


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Track Malaga Embassy revenue event across streams.")
    parser.add_argument("--stream", choices=STREAM_CHOICES, required=True, help="Revenue stream identifier")
    parser.add_argument("--amount", type=float, required=True, help="Revenue amount in euros")
    parser.add_argument("--client", type=str, default="Unknown Client", help="Client or counterparty name")
    parser.add_argument("--date", type=_parse_date, help="Event date (YYYY-MM-DD)")
    parser.add_argument("--notes", type=str, default="", help="Optional notes")
    parser.add_argument("--dry-run", action="store_true", help="Do not persist changes or send COMMS")
    parser.add_argument("--json", action="store_true", help="Emit JSON output")
    args = parser.parse_args(argv)

    state = load_state()
    event_date = args.date or date.today()

    entry = register_revenue(
        state,
        amount=args.amount,
        stream=args.stream,
        client=args.client,
        event_date=event_date,
    )
    health = compute_health(state, reference=event_date)

    payload = {
        "stream": args.stream,
        "amount": round(args.amount, 2),
        "client": args.client,
        "date": event_date.isoformat(),
        "notes": args.notes,
        "health_score": health["score"],
        "runway_days": health["runway_days"],
    }

    if not args.dry_run:
        append = {
            "timestamp": event_date.isoformat(),
            "stream": args.stream,
            "amount": round(args.amount, 2),
            "client": args.client,
            "notes": args.notes,
        }
        from utils import append_jsonl  # local import to avoid circular at top

        append_jsonl(PATHS.revenue_log, append)
        log_event("revenue_event", payload)
        save_state(state)

        puck = {
            "type": "malaga_revenue_event",
            "stream": args.stream,
            "amount": round(args.amount, 2),
            "client": args.client,
            "date": event_date.isoformat(),
            "health_score": health["score"],
            "runway_days": health["runway_days"],
        }
        transmit_puck(puck, recipients=("captain", "claude", "gemini", "codex"), rhythm="standard", tone="strategic_synthesis")
    else:
        # Restore original state by dropping entry when dry-run
        state["revenue"]["history"].pop()
        state["revenue"]["streams"][args.stream] -= args.amount

    if args.json:
        print(json.dumps(payload, indent=2))
    else:
        print(
            f"Logged €{args.amount:.2f} to {args.stream} (client: {args.client}) | "
            f"Health {health['score']:.1f}/100, Runway {health['runway_days']:.1f} days"
        )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
