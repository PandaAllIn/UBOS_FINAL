from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Sequence

from deadline_tracker import generate_actions  # type: ignore
from utils import (  # type: ignore
    Opportunity,
    SkillPaths,
    append_log,
    format_euro,
    load_pipeline_state,
    render_template,
    resolve_paths,
    resolve_template,
    slugify,
    utc_now,
)


def classify_fit(score: float | None) -> str:
    if score is None:
        return "Unscored"
    if score >= 4.5:
        return "Exceptional"
    if score >= 4.0:
        return "High"
    if score >= 3.0:
        return "Medium"
    return "Needs Review"


def brief_filename(opportunity: Opportunity) -> str:
    base = slugify(opportunity.title or opportunity.opportunity_id)
    return f"{opportunity.opportunity_id.lower()}_{base}.md"


def build_context(opportunity: Opportunity, paths: SkillPaths) -> dict[str, str]:
    days_remaining = opportunity.days_until_deadline()
    matched_keywords = ", ".join(opportunity.matched_keywords) or "None"
    fit_explanation = "\n".join(f"- {line}" for line in opportunity.fit_explanation) or "- Fit score pending human analysis"
    actions = generate_actions(opportunity)
    if days_remaining is None:
        deadline_status = "deadline unknown"
    elif days_remaining < 0:
        deadline_status = f"{abs(days_remaining)} days overdue"
    else:
        deadline_status = f"{days_remaining} days remaining"
    context = {
        "title": opportunity.title,
        "opportunity_id": opportunity.opportunity_id,
        "program": opportunity.program,
        "deadline_human": opportunity.deadline.strftime("%Y-%m-%d %H:%M UTC") if opportunity.deadline else "TBD",
        "deadline_status": deadline_status,
        "budget_min_fmt": format_euro(opportunity.budget_min),
        "budget_max_fmt": format_euro(opportunity.budget_max),
        "fit_score": f"{opportunity.fit_score:.1f}" if opportunity.fit_score is not None else "N/A",
        "fit_classification": classify_fit(opportunity.fit_score),
        "ubos_project_match": opportunity.ubos_project_match or "TBD",
        "executive_summary": opportunity.description or "Awaiting description." ,
        "program_focus": opportunity.program,
        "criteria_list": ", ".join(opportunity.criteria) or "N/A",
        "discovered_date": opportunity.discovered_date.isoformat(),
        "matched_keywords": matched_keywords,
        "fit_explanation": fit_explanation,
        "capability_alignment": matched_keywords if matched_keywords != "None" else "Flag required: add capability rationale.",
        "budget_strategy": _budget_strategy(opportunity),
        "next_action_1": actions[0],
        "next_action_2": actions[1] if len(actions) > 1 else "Confirm stakeholder ownership.",
        "next_action_3": actions[2] if len(actions) > 2 else "Schedule constitutional compliance review.",
        "alignment_summary": "Lion's Sanctuary compliant; empowers partners."
        if opportunity.ubos_project_match
        else "Verify constitutional alignment before submission.",
        "oversight_notes": "Ensure Trinity approvals prior to submission.",
        "pipeline_entry_path": str(paths.pipeline_state),
        "deadline_calendar_path": str(paths.deadline_calendar),
        "related_briefs": _related_briefs(paths, opportunity),
        "url": opportunity.url or "https://",  # placeholder if missing
    }
    return context


def _budget_strategy(opportunity: Opportunity) -> str:
    project = (opportunity.ubos_project_match or "UBOS project")
    return (
        f"Align requested funding with {project} objectives. Structure budget to honour the constitutional cascade "
        "(20/10/15/40/15) and highlight sustainability contributions."
    )


def _related_briefs(paths: SkillPaths, opportunity: Opportunity) -> str:
    directory = paths.grant_opportunities_dir
    if not directory.exists():
        return "None yet"
    project = opportunity.ubos_project_match
    briefs = sorted(directory.glob("*.md"))
    matches = [brief.name for brief in briefs if project and project.lower() in brief.name.lower()]
    return ", ".join(matches) if matches else "None yet"


def write_brief(opportunity: Opportunity, *, force: bool, paths: SkillPaths) -> Path:
    template = resolve_template("opportunity_brief_template.md", paths=paths)
    context = build_context(opportunity, paths)
    output_dir = paths.grant_opportunities_dir
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / brief_filename(opportunity)

    if output_path.exists() and not force:
        raise FileExistsError(f"Brief already exists: {output_path}")

    content = render_template(template, context)
    output_path.write_text(content, encoding="utf-8")
    append_log(
        "opportunity_brief_generated",
        {
            "opportunity_id": opportunity.opportunity_id,
            "path": str(output_path),
            "generated_at": utc_now().isoformat(),
        },
        paths=paths,
    )
    return output_path


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Generate a markdown brief for a specific opportunity.")
    parser.add_argument("--id", required=True, help="Opportunity ID to render")
    parser.add_argument("--force", action="store_true", help="Overwrite existing brief if present")
    parser.add_argument("--json", action="store_true", help="Emit JSON summary instead of plain text")
    args = parser.parse_args(argv)

    paths = resolve_paths()
    payload = load_pipeline_state(paths)
    opportunities: list[Opportunity] = payload.get("opportunities", [])
    target = next((op for op in opportunities if op.opportunity_id == args.id), None)
    if target is None:
        raise SystemExit(f"Opportunity '{args.id}' not found in pipeline_state.json")

    if target.fit_score is None:
        raise SystemExit("Opportunity has no fit score yet; run scan_eu_databases.py first.")

    path = write_brief(target, force=args.force, paths=paths)

    result = {
        "opportunity_id": target.opportunity_id,
        "brief_path": str(path),
        "fit_score": target.fit_score,
        "project": target.ubos_project_match,
    }
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(f"Brief generated at {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
