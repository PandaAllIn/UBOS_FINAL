from __future__ import annotations

import argparse
import copy
import json
from datetime import date
from typing import Any

from utils import (
    compute_health,
    load_state,
    log_event,
    register_spending,
    save_state,
)

CATEGORIES = {"research", "emergency", "operations", "projects", "strategic"}


def _parse_date(value: str | None) -> date | None:
    if not value:
        return None
    try:
        return date.fromisoformat(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError(f"Invalid date '{value}'") from exc


def evaluate_spending(state: dict[str, Any], *, amount: float, category: str, description: str, requester: str, event_date: date | None) -> dict[str, Any]:
    current = state.get("cascade", {}).get(category, {})
    allocation = float(current.get("allocation", 0.0))
    spent = float(current.get("spent", 0.0))
    remaining = allocation - spent
    metrics = state.get("metrics", {})
    runway = float(metrics.get("runway_days", 0.0))

    projected_state = copy.deepcopy(state)
    register_spending(projected_state, amount=amount, category=category, description=description, requester=requester, event_date=event_date)
    projected_health = compute_health(projected_state, reference=event_date)

    delta_score = projected_health["score"] - state.get("health", {}).get("last_score", projected_health["score"])
    gap = amount - remaining

    decision = "APPROVE"
    notes: list[str] = []

    if category == "strategic" and amount > 0:
        decision = "BLOCK"
        notes.append("Strategic reserve locked for Month 1; choose alternative funding.")
    elif category == "emergency" and runway >= 14:
        decision = "CAUTION"
        notes.append("Emergency reserve intended for runway <14 days; consider deferment or smaller spend.")
    elif gap > 0:
        over_pct = (gap / allocation * 100) if allocation else 0.0
        if over_pct <= 5:
            decision = "CAUTION"
            notes.append(f"Request exceeds allocation by €{gap:.2f} ({over_pct:.1f}%). Rebalance from Strategic reserve or reduce scope.")
        else:
            decision = "BLOCK"
            notes.append(f"Request exceeds allocation by €{gap:.2f} ({over_pct:.1f}%). Recommend reducing to €{max(0.0, remaining):.2f} or awaiting revenue inflow.")

    impact = {
        "current_score": state.get("health", {}).get("last_score"),
        "projected_score": projected_health["score"],
        "delta": delta_score,
        "runway_after": projected_health["runway_days"],
    }

    alternatives: list[str] = []
    if decision != "APPROVE":
        alternatives.append("Option A: Reduce request to remain within allocation limits.")
        alternatives.append("Option B: Reallocate small portion from Strategic reserve (requires human approval).")
        alternatives.append("Option C: Defer until revenue replenishes Projects budget.")

    return {
        "decision": decision,
        "allocation": allocation,
        "spent": spent,
        "remaining": remaining,
        "gap": max(0.0, gap),
        "runway": runway,
        "impact": impact,
        "notes": notes,
        "alternatives": alternatives,
        "projected": projected_state,
    }


def format_response(amount: float, category: str, evaluation: dict[str, Any]) -> str:
    lines = [
        "SPENDING PROPOSAL ANALYSIS",
        f"Amount: €{amount:.2f}",
        f"Category: {category.title()}",
        f"Decision: {evaluation['decision']}",
        f"Allocation Remaining: €{evaluation['remaining']:.2f}",
    ]
    impact = evaluation["impact"]
    if impact["current_score"] is not None:
        lines.append(
            f"Health Score Impact: {impact['current_score']:.1f} → {impact['projected_score']:.1f} ({impact['delta']:+.1f})"
        )
    else:
        lines.append(f"Projected Health Score: {impact['projected_score']:.1f}")
    lines.append(f"Runway After Spend: {impact['runway_after']:.1f} days")
    if evaluation["notes"]:
        lines.append("")
        lines.append("Guidance:")
        for note in evaluation["notes"]:
            lines.append(f"- {note}")
    if evaluation["alternatives"]:
        lines.append("")
        lines.append("Alternatives:")
        for alt in evaluation["alternatives"]:
            lines.append(f"- {alt}")
    lines.extend(["", "Captain retains final authority. Recommendation is advisory only."])
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Evaluate Malaga Embassy spending proposal against constitutional cascade.")
    parser.add_argument("--amount", type=float, required=True, help="Proposed spend amount in euros")
    parser.add_argument("--category", type=str, required=True, choices=sorted(CATEGORIES), help="Cascade category")
    parser.add_argument("--requester", type=str, default="unknown", help="Requester name")
    parser.add_argument("--description", type=str, default="", help="Short description of the spend")
    parser.add_argument("--date", type=_parse_date, help="Event date (YYYY-MM-DD)")
    parser.add_argument("--apply", action="store_true", help="Commit spending entry if decision is APPROVE or CAUTION")
    parser.add_argument("--json", action="store_true", help="Emit JSON output")
    args = parser.parse_args(argv)

    state = load_state()
    baseline_health = compute_health(state, reference=args.date)
    state.setdefault("health", {})["last_score"] = baseline_health["score"]

    evaluation = evaluate_spending(
        state,
        amount=args.amount,
        category=args.category,
        description=args.description or "",
        requester=args.requester,
        event_date=args.date,
    )

    payload = {
        "amount": args.amount,
        "category": args.category,
        "description": args.description,
        "requester": args.requester,
        "decision": evaluation["decision"],
        "notes": evaluation["notes"],
        "alternatives": evaluation["alternatives"],
        "impact": evaluation["impact"],
        "remaining": evaluation["remaining"],
    }
    log_event("spending_analysis", payload)

    if args.apply and evaluation["decision"] in {"APPROVE", "CAUTION"}:
        register_spending(
            state,
            amount=args.amount,
            category=args.category,
            description=args.description or "",
            requester=args.requester,
            event_date=args.date,
        )
        save_state(state)
    else:
        save_state(state)

    if args.json:
        print(json.dumps(payload, indent=2))
    else:
        print(format_response(args.amount, args.category, evaluation))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
