from __future__ import annotations

import argparse
from datetime import date
import json
from typing import Any

from utils import (
    PATHS,
    _summarise_revenue,
    compute_health,
    emoji_for_score,
    load_state,
    log_event,
    save_state,
    transmit_puck,
)


def _parse_date(value: str | None) -> date | None:
    if not value:
        return None
    try:
        return date.fromisoformat(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError(f"Invalid date '{value}'") from exc


def _format_currency(value: float) -> str:
    return f"{value:,.2f}".replace(",", " ")


def _render_markdown(template: str, context: dict[str, str]) -> str:
    for key, value in context.items():
        template = template.replace(f"{{{{{key}}}}}", value)
    return template


def _build_actions(health: dict[str, Any]) -> list[str]:
    actions: list[str] = []
    for recommendation in health.get("recommendations", []):
        actions.append(recommendation)
    if not actions:
        actions.append("Maintain current cadence; prepare next revenue outreach wave.")
    return actions


def _cascade_rows(state: dict[str, Any]) -> dict[str, tuple[float, float, float]]:
    rows: dict[str, tuple[float, float, float]] = {}
    for key, info in state.get("cascade", {}).items():
        allocation = float(info.get("allocation", 0.0))
        spent = float(info.get("spent", 0.0))
        remaining = allocation - spent
        rows[key] = (allocation, spent, remaining)
    return rows


def _render_chart(data: dict[str, float]) -> str:
    if not data:
        return "No data"
    lines = []
    max_value = max(data.values()) or 1.0
    for key, value in data.items():
        bar_length = int(30 * (value / max_value))
        bar = "█" * bar_length
        lines.append(f"{key:<24} | {bar} €{value:.2f}")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Generate Malaga Embassy daily briefing and dashboard.")
    parser.add_argument("--date", type=_parse_date, help="Report date (YYYY-MM-DD)")
    parser.add_argument("--no-comms", action="store_true", help="Skip COMMS_HUB transmission")
    parser.add_argument("--json", action="store_true", help="Emit JSON summary")
    args = parser.parse_args(argv)

    state = load_state()
    report_date = args.date or date.today()
    health = compute_health(state, reference=report_date)
    save_state(state)

    revenue_summary = _summarise_revenue(state, reference=report_date)
    cascade_rows = _cascade_rows(state)
    actions = _build_actions(health)

    markdown_template = (PATHS.assets_dir / "daily_briefing_template.md").read_text(encoding="utf-8")
    actions_block = "\n".join(f"- {item}" for item in actions)
    recommendations_block = "\n".join(f"- {item}" for item in health.get("recommendations", [])) or "- All systems nominal."

    capital_remaining = float(state.get("capital", {}).get("remaining", 0.0))
    cascade_context: dict[str, str] = {}
    for key, (allocation, spent, remaining) in cascade_rows.items():
        cascade_context[f"{key}_allocated"] = _format_currency(allocation)
        cascade_context[f"{key}_spent"] = _format_currency(spent)
        cascade_context[f"{key}_remaining"] = _format_currency(remaining)

    context = {
        "date": report_date.isoformat(),
        "day": str(state.get("timeline", {}).get("days_elapsed", 0) + 1),
        "health_score": f"{health['score']:.1f}",
        "health_emoji": emoji_for_score(health["score"]),
        "capital_remaining": _format_currency(capital_remaining),
        "capital_percent": f"{(capital_remaining / 1500.0) * 100:.1f}",
        "burn_rate": f"{health['burn_rate']:.2f}",
        "runway_days": f"{health['runway_days']:.1f}",
        "revenue_today": _format_currency(revenue_summary["today"]),
        "revenue_week": _format_currency(revenue_summary["week"]),
        "revenue_month": _format_currency(revenue_summary["month"]),
        "aas_revenue": _format_currency(revenue_summary["streams"]["agent-as-a-service"]),
        "intel_revenue": _format_currency(revenue_summary["streams"]["intel-services"]),
        "consultation_revenue": _format_currency(revenue_summary["streams"]["proposal-consultation"]),
        "actions_list": actions_block,
        "recommendations_list": recommendations_block,
    }
    context.update(cascade_context)

    briefing_text = _render_markdown(markdown_template, context)
    briefing_path = PATHS.briefings_dir / f"{report_date.isoformat()}.md"
    briefing_path.write_text(briefing_text, encoding="utf-8")

    dashboard_template = (PATHS.assets_dir / "revenue_dashboard.html").read_text(encoding="utf-8")
    html_context = {
        "health_class": "healthy" if health["score"] >= 70 else ("warning" if health["score"] >= 50 else "critical"),
        "health_score": f"{health['score']:.1f}",
        "health_status": "ON TRACK" if health["score"] >= 70 else ("CORRECTIVE ACTION" if health["score"] >= 50 else "CRITICAL"),
        "capital_remaining": _format_currency(capital_remaining),
        "burn_rate": f"{health['burn_rate']:.2f}",
        "runway_days": f"{health['runway_days']:.1f}",
        "revenue_total": _format_currency(revenue_summary["month"]),
        "revenue_chart": _render_chart(revenue_summary["streams"]),
        "cascade_chart": _render_chart({k: v[2] for k, v in cascade_rows.items()}),
        "actions_list": "\n".join(f"<li>{item}</li>" for item in actions),
    }
    dashboard_html = _render_markdown(dashboard_template, html_context)
    PATHS.dashboard_path.write_text(dashboard_html, encoding="utf-8")

    payload = {
        "date": report_date.isoformat(),
        "health_score": health["score"],
        "burn_rate": health["burn_rate"],
        "runway_days": health["runway_days"],
        "revenue_month": revenue_summary["month"],
        "actions": actions,
    }
    log_event("daily_briefing", payload)

    if not args.no_comms:
        puck = {
            "type": "malaga_daily_briefing",
            "date": report_date.isoformat(),
            "health_score": health["score"],
            "runway_days": health["runway_days"],
            "revenue_month": revenue_summary["month"],
            "actions": actions[:3],
        }
        transmit_puck(puck, recipients=("captain", "claude", "gemini", "codex"), rhythm="standard", tone="operational_update")

    if args.json:
        print(json.dumps(payload, indent=2))
    else:
        print(f"Daily briefing generated at {briefing_path} (dashboard updated)")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
