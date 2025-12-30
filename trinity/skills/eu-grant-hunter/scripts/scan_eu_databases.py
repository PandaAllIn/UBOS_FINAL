from __future__ import annotations

import argparse
import json
import logging
import sys
from datetime import datetime, timezone
from typing import Sequence

try:
    import requests
except ImportError:  # pragma: no cover - optional dependency
    requests = None  # type: ignore

from calculate_fit_score import FitAnalyzer, calculate_fit_score  # type: ignore
from utils import (  # type: ignore
    Opportunity,
    SkillPaths,
    append_log,
    ensure_directories,
    format_euro,
    load_pipeline_state,
    merge_opportunity_sets,
    render_template,
    save_pipeline_state,
    resolve_paths,
    resolve_template,
    slugify,
    transmit_puck,
    utc_now,
)
from trinity.oracle_health_check import OracleHealthChecker

LOGGER = logging.getLogger("eu_grant_hunter.scan")
logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(message)s")


class OpportunitySource:
    """Base class for EU funding data sources."""

    def __init__(self, program: str, url: str, sample_key: str) -> None:
        self.program = program
        self.url = url
        self.sample_key = sample_key

    def fetch(self, *, topic_filter: str | None = None) -> list[dict[str, object]]:
        try:
            return self._fetch_remote(topic_filter)
        except Exception as exc:  # pragma: no cover - network variability
            LOGGER.warning(
                "Remote fetch failed for %s (%s). Falling back to samples. reason=%s",
                self.program,
                self.url,
                exc,
            )
            return self._fallback(topic_filter)

    def _fetch_remote(self, topic_filter: str | None) -> list[dict[str, object]]:
        if requests is None:
            raise RuntimeError("requests library unavailable")
        response = requests.get(self.url, timeout=20)
        response.raise_for_status()
        payload = response.json()
        opportunities: list[dict[str, object]] = []
        for entry in payload.get("results", []):
            if topic_filter and topic_filter.lower() not in json.dumps(entry).lower():
                continue
            opportunities.append({
                "title": entry.get("title") or entry.get("name"),
                "budget_min": entry.get("budget_min"),
                "budget_max": entry.get("budget_max"),
                "deadline": entry.get("deadline"),
                "description": entry.get("description", ""),
                "url": entry.get("url") or entry.get("link"),
                "criteria": entry.get("keywords", []),
                "call_id": entry.get("id") or entry.get("call_id"),
            })
        if not opportunities:
            raise ValueError("Remote endpoint returned no opportunities")
        return opportunities

    def _fallback(self, topic_filter: str | None) -> list[dict[str, object]]:
        entries = SAMPLE_OPPORTUNITIES.get(self.sample_key, [])
        if topic_filter:
            lower = topic_filter.lower()
            entries = [entry for entry in entries if lower in json.dumps(entry).lower()]
        return entries.copy()


SOURCES: tuple[OpportunitySource, ...] = (
    OpportunitySource(
        program="Horizon Europe",
        url="https://raw.githubusercontent.com/ubos-ai/datasets/main/horizon_sample.json",
        sample_key="horizon_europe",
    ),
    OpportunitySource(
        program="European Regional Development Fund",
        url="https://raw.githubusercontent.com/ubos-ai/datasets/main/erdf_sample.json",
        sample_key="erdf",
    ),
    OpportunitySource(
        program="Digital Europe Programme",
        url="https://raw.githubusercontent.com/ubos-ai/datasets/main/digital_europe_sample.json",
        sample_key="digital_europe",
    ),
    OpportunitySource(
        program="Innovation Fund",
        url="https://raw.githubusercontent.com/ubos-ai/datasets/main/innovation_fund_sample.json",
        sample_key="innovation_fund",
    ),
)


SAMPLE_OPPORTUNITIES = {
    "horizon_europe": [
        {
            "title": "Geothermal Energy for Sovereign Data Centers",
            "budget_min": 5000000,
            "budget_max": 10000000,
            "deadline": "2025-09-02T17:00:00Z",
            "description": "Funding for geothermal-powered AI and HPC infrastructure supporting European digital sovereignty.",
            "url": "https://example.eu/horizon/geothermal-ai",
            "criteria": ["geothermal", "ai infrastructure", "energy efficiency", "sovereign compute"],
            "call_id": "HORIZON-2025-GEOTHERMAL-01",
        },
        {
            "title": "Cluster 6: Plant Health and Resilience",
            "budget_min": 3000000,
            "budget_max": 6000000,
            "deadline": "2026-01-15T17:00:00Z",
            "description": "Advancing phytosanitary intelligence for bacterial disease containment across Mediterranean agriculture.",
            "url": "https://example.eu/horizon/cluster6-plant-health",
            "criteria": ["plant pathology", "precision agriculture", "phytosanitary", "farmer cooperatives"],
            "call_id": "HORIZON-CL6-XYL-2026",
        },
    ],
    "erdf": [
        {
            "title": "Oradea Smart Region Expansion",
            "budget_min": 5000000,
            "budget_max": 15000000,
            "deadline": "2025-11-30T21:59:00Z",
            "description": "Regional development fund supporting digital infrastructure and smart city services in Oradea, Romania.",
            "url": "https://example.eu/erdf/oradea-smart-region",
            "criteria": ["regional development", "smart city", "digital infrastructure"],
            "call_id": "ERDF-RO-2025-ORADEA",
        }
    ],
    "digital_europe": [
        {
            "title": "European AI Infrastructure Acceleration",
            "budget_min": 4000000,
            "budget_max": 8000000,
            "deadline": "2025-12-15T17:00:00Z",
            "description": "Deployment of AI infrastructure and skills for sovereign European cloud providers.",
            "url": "https://example.eu/digital/ai-infrastructure",
            "criteria": ["ai infrastructure", "sovereign computing", "digital skills"],
            "call_id": "DIGITAL-2025-AI-INFRA",
        }
    ],
    "innovation_fund": [
        {
            "title": "Clean Energy Infrastructure for Data Centers",
            "budget_min": 15000000,
            "budget_max": 70000000,
            "deadline": "2026-01-20T17:00:00Z",
            "description": "Large-scale Innovation Fund call for renewable-powered data center infrastructure reducing ETS footprint.",
            "url": "https://example.eu/innovation/data-center-clean-energy",
            "criteria": ["renewable energy", "data center", "decarbonisation"],
            "call_id": "INNOVATION-FUND-2026-DATA-CENTER",
        }
    ],
}


def build_opportunity(raw: dict[str, object], *, program: str) -> Opportunity:
    call_id = str(raw.get("call_id") or _build_call_id(program, raw.get("title")))
    title = str(raw.get("title") or "Untitled Call")
    deadline_iso = raw.get("deadline")
    deadline = _parse_deadline(deadline_iso)
    budget_min = _maybe_int(raw.get("budget_min"))
    budget_max = _maybe_int(raw.get("budget_max"))
    description = str(raw.get("description") or "")
    url = str(raw.get("url") or "")
    criteria = [str(item) for item in raw.get("criteria", [])]
    now = utc_now().date()

    opportunity_id = call_id or f"{slugify(program)}-{slugify(title)}"

    return Opportunity(
        opportunity_id=opportunity_id,
        title=title,
        program=program,
        budget_min=budget_min,
        budget_max=budget_max,
        deadline=deadline,
        description=description,
        url=url,
        criteria=criteria,
        discovered_date=now,
        last_seen=now,
    )


def _parse_deadline(deadline: object) -> datetime | None:
    if not deadline:
        return None
    if isinstance(deadline, datetime):
        return deadline if deadline.tzinfo else deadline.replace(tzinfo=timezone.utc)
    if isinstance(deadline, str):
        try:
            parsed = datetime.fromisoformat(deadline.replace("Z", "+00:00"))
            return parsed if parsed.tzinfo else parsed.replace(tzinfo=timezone.utc)
        except ValueError:
            LOGGER.warning("Unable to parse deadline '%s'", deadline)
    return None


def _maybe_int(value: object) -> int | None:
    if value in (None, "", "null"):
        return None
    try:
        return int(float(value))
    except (TypeError, ValueError):
        return None


def _build_call_id(program: str, title: object) -> str:
    slug = slugify(str(title or "opportunity"))
    return f"{slugify(program)}-{slug.upper()}"


def scan_all_sources(
    *,
    topic_filter: str | None,
    max_results: int | None,
    analyzer: FitAnalyzer,
    fallback_only: bool = False,
) -> list[Opportunity]:
    collected: list[Opportunity] = []
    for source in SOURCES:
        if fallback_only:
            raw_entries = source._fallback(topic_filter)  # type: ignore[attr-defined]
        else:
            raw_entries = source.fetch(topic_filter=topic_filter)
        for raw in raw_entries:
            opportunity = build_opportunity(raw, program=source.program)
            fit = calculate_fit_score(opportunity, analyzer)
            opportunity.fit_score = fit.fit_score
            opportunity.fit_explanation = fit.explanation
            opportunity.ubos_project_match = fit.matched_project
            opportunity.matched_keywords = fit.matched_keywords
            collected.append(opportunity)
            if max_results and len(collected) >= max_results:
                return collected
    return collected


def update_dashboard(paths: SkillPaths, opportunities: Sequence[Opportunity], metadata: dict[str, object]) -> None:
    template = resolve_template("pipeline_dashboard_template.html", paths=paths)
    deadline_rows = "".join(
        _render_deadline_row(opportunity)
        for opportunity in opportunities
        if opportunity.deadline and (opportunity.deadline - utc_now()).days <= 90
    )
    project_rows = "".join(_render_project_row(project, opportunities) for project in sorted({op.ubos_project_match for op in opportunities if op.ubos_project_match}))
    activity_items = "".join(
        f"<li>{op.title} ({op.program}) scored {op.fit_score}/5 on {op.last_seen.isoformat()}</li>"
        for op in opportunities[:5]
    )

    context = {
        "generated_at": metadata.get("generated_at", utc_now().isoformat()),
        "total_opportunities": str(len(opportunities)),
        **_priority_counts(opportunities),
        "deadline_rows": deadline_rows or "<tr><td colspan=7>No deadlines within 90 days.</td></tr>",
        "project_rows": project_rows or "<tr><td colspan=4>No project matches yet.</td></tr>",
        "activity_items": activity_items or "<li>No recent activity recorded.</li>",
    }

    html = render_template(template, context)
    dashboard_path = paths.pipeline_dir / "pipeline_dashboard.html"
    dashboard_path.write_text(html, encoding="utf-8")


def _render_deadline_row(opportunity: Opportunity) -> str:
    if not opportunity.deadline:
        return ""
    days_remaining = opportunity.days_until_deadline() or 9999
    status_tag = "tag-high"
    if days_remaining <= 30:
        status_tag = "tag-low"
    elif days_remaining <= 60:
        status_tag = "tag-medium"
    return (
        "<tr>"
        f"<td>{opportunity.deadline.date()}</td>"
        f"<td>{opportunity.program}</td>"
        f"<td>{opportunity.title}</td>"
        f"<td>{opportunity.fit_score or 'n/a'}</td>"
        f"<td>{opportunity.ubos_project_match or 'TBD'}</td>"
        f"<td>€{format_euro(opportunity.budget_min)}–€{format_euro(opportunity.budget_max)}</td>"
        f"<td><span class='tag {status_tag}'>T-{days_remaining}d</span></td>"
        "</tr>"
    )


def _render_project_row(project: str | None, opportunities: Sequence[Opportunity]) -> str:
    if not project:
        return ""
    matched = [op for op in opportunities if op.ubos_project_match == project]
    total_budget = sum(op.budget_max or op.budget_min or 0 for op in matched)
    upcoming = sum(1 for op in matched if op.deadline and (op.deadline - utc_now()).days <= 90)
    return (
        "<tr>"
        f"<td>{project}</td>"
        f"<td>{len(matched)}</td>"
        f"<td>€{format_euro(total_budget)}</td>"
        f"<td>{upcoming}</td>"
        "</tr>"
    )


def _priority_counts(opportunities: Sequence[Opportunity]) -> dict[str, str]:
    high = [op for op in opportunities if (op.fit_score or 0) >= 4.0]
    medium = [op for op in opportunities if 3.0 <= (op.fit_score or 0) < 4.0]
    low = [op for op in opportunities if (op.fit_score or 0) < 3.0]
    return {
        "high_priority_count": str(len(high)),
        "high_priority_total": format_euro(sum(op.budget_max or op.budget_min or 0 for op in high)),
        "medium_priority_count": str(len(medium)),
        "medium_priority_total": format_euro(sum(op.budget_max or op.budget_min or 0 for op in medium)),
        "low_priority_count": str(len(low)),
        "low_priority_total": format_euro(sum(op.budget_max or op.budget_min or 0 for op in low)),
    }


def notify_high_value(opportunities: Sequence[Opportunity], paths: SkillPaths, *, dry_run: bool) -> None:
    high_value = [op for op in opportunities if (op.fit_score or 0) >= 4.0]
    if dry_run:
        LOGGER.info("Dry-run: skipping high-value alert transmission for %d opportunities", len(high_value))
        return
    for opportunity in high_value:
        days_remaining = opportunity.days_until_deadline()
        puck = {
            "type": "grant_alert",
            "opportunity_id": opportunity.opportunity_id,
            "title": opportunity.title,
            "program": opportunity.program,
            "deadline": opportunity.deadline.isoformat() if opportunity.deadline else None,
            "fit_score": opportunity.fit_score,
            "project": opportunity.ubos_project_match,
            "url": opportunity.url,
            "summary": opportunity.description[:280],
            "days_remaining": days_remaining,
        }
        transmit_puck(
            puck,
            recipients=("claude", "gemini", "codex", "captain"),
            rhythm="standard",
            tone="strategic_synthesis",
            paths=paths,
        )
        append_log(
            "high_value_opportunity",
            {
                "opportunity_id": opportunity.opportunity_id,
                "title": opportunity.title,
                "fit_score": opportunity.fit_score,
                "project": opportunity.ubos_project_match,
            },
            paths=paths,
        )


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Scan EU funding databases for UBOS-aligned opportunities.")
    parser.add_argument("--topic", help="Filter results by keyword or topic", default=None)
    parser.add_argument("--max-results", type=int, help="Limit total number of opportunities", default=None)
    parser.add_argument("--auto", action="store_true", help="Mark scan as automated for metadata tracking")
    parser.add_argument("--render-dashboard", action="store_true", help="Regenerate HTML dashboard only")
    parser.add_argument("--dry-run", action="store_true", help="Do not persist pipeline changes")
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    paths = resolve_paths()
    ensure_directories(paths)

    fallback_only = False
    oracle_status: dict[str, bool] = {}
    try:
        health_checks = OracleHealthChecker().check_all()
        oracle_status = {name: health.status for name, health in health_checks.items()}
        if not oracle_status.get("perplexity", True):
            LOGGER.warning("Perplexity oracle unhealthy; enabling Groq fallback mode.")
            fallback_only = True
    except Exception as exc:  # pragma: no cover - defensive
        LOGGER.warning("Oracle health check failed; proceeding without status insight. reason=%s", exc)

    payload = load_pipeline_state(paths)
    existing_opportunities: list[Opportunity] = payload.get("opportunities", [])

    analyzer = FitAnalyzer(paths)

    if args.render_dashboard:
        update_dashboard(paths, existing_opportunities, payload.get("metadata", {}))
        LOGGER.info("Dashboard regenerated from existing pipeline state.")
        return 0

    scanned = scan_all_sources(
        topic_filter=args.topic,
        max_results=args.max_results,
        analyzer=analyzer,
        fallback_only=fallback_only,
    )

    merged = merge_opportunity_sets(existing_opportunities, scanned)

    metadata = {
        "generated_at": utc_now().isoformat(),
        "source": "auto" if args.auto else "manual",
        "topic_filter": args.topic,
        "oracle_status": oracle_status,
        "oracle_fallback_mode": fallback_only,
    }

    if not args.dry_run:
        save_pipeline_state(merged, metadata=metadata, paths=paths)
    else:
        LOGGER.info("Dry-run enabled; pipeline state not written to disk.")

    if not args.dry_run:
        append_log(
            "scan_complete",
            {
                "opportunity_count": len(scanned),
                "topic": args.topic,
                "metadata": metadata,
            },
            paths=paths,
        )

    notify_high_value(merged, paths, dry_run=args.dry_run)
    update_dashboard(paths, merged, metadata)

    summary = [
        {
            "opportunity_id": op.opportunity_id,
            "title": op.title,
            "program": op.program,
            "fit_score": op.fit_score,
            "deadline": op.deadline.isoformat() if op.deadline else None,
            "project": op.ubos_project_match,
        }
        for op in merged
    ]
    sys.stdout.write(json.dumps(summary, indent=2) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
