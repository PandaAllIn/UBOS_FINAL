from __future__ import annotations

import argparse
from datetime import date, timedelta

from utils import (
    PATHS,
    append_log,
    assembly_path,
    compute_progress,
    get_opportunity,
    load_state,
    register_assembly,
    save_state,
    slugify,
    write_json,
)


def _parse_date(value: str | None) -> date:
    if not value:
        return date.today()
    return date.fromisoformat(value)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Initialize a grant assembly workspace from an EU Grant Hunter opportunity.")
    parser.add_argument("--opportunity-id", required=True, help="Opportunity ID from pipeline_state.json")
    parser.add_argument("--project", required=True, help="Project/proposal codename")
    parser.add_argument("--rapid", action="store_true", help="Use rapid (72-hour) schedule estimate")
    parser.add_argument("--start-date", help="Assembly start date (YYYY-MM-DD)")
    args = parser.parse_args(argv)

    opportunity = get_opportunity(args.opportunity_id)
    if opportunity is None:
        parser.error(f"Opportunity '{args.opportunity_id}' not found in pipeline state")

    assembly_id = slugify(args.project)
    state = load_state()

    start_date = _parse_date(args.start_date)
    deadline = opportunity.get("deadline")
    deadline_str = deadline or "unknown"
    budget_min = opportunity.get("budget_min")
    budget_max = opportunity.get("budget_max")
    fit_score = opportunity.get("fit_score") or 0.0
    estimated_duration = timedelta(days=3) if args.rapid else timedelta(days=45)
    completion_date = start_date + estimated_duration

    phases = {
        "intelligence": {"status": "pending"},
        "narratives": {"status": "pending"},
        "budget": {"status": "pending"},
        "partners": {"status": "pending"},
        "compliance": {"status": "pending"},
        "packaging": {"status": "pending"},
    }

    entry = {
        "id": assembly_id,
        "project_name": args.project,
        "opportunity_id": args.opportunity_id,
        "deadline": deadline_str,
        "budget_min": budget_min,
        "budget_max": budget_max,
        "fit_score": fit_score,
        "start_date": start_date.isoformat(),
        "estimated_completion": completion_date.isoformat(),
        "rapid_mode": args.rapid,
        "phases": phases,
        "progress": 0.0,
    }

    register_assembly(state, entry)
    save_state(state)

    assembly_dir = assembly_path(assembly_id)
    for subdir in ("narratives", "budget", "partners", "compliance", "submission", "workplan"):
        (assembly_dir / subdir).mkdir(parents=True, exist_ok=True)

    placeholders = {
        "PROJECT_NAME": args.project,
        "OPPORTUNITY_ID": args.opportunity_id,
        "DEADLINE": deadline_str,
        "FIT_SCORE": f"{fit_score:.1f}" if isinstance(fit_score, (int, float)) else str(fit_score),
        "BUDGET_MIN": f"{budget_min:,}" if isinstance(budget_min, (int, float)) else "unknown",
        "BUDGET_MAX": f"{budget_max:,}" if isinstance(budget_max, (int, float)) else "unknown",
        "START_DATE": start_date.isoformat(),
        "COMPLETION_DATE": completion_date.isoformat(),
        "PARTNER_COUNT": str(len(opportunity.get("partners", []))) if isinstance(opportunity.get("partners"), list) else "TBD",
    }

    workflow_template = (PATHS.assets_dir / "assembly_workflow_template.md").read_text(encoding="utf-8")
    workflow_text = workflow_template
    for key, value in placeholders.items():
        workflow_text = workflow_text.replace(f"{{{{{key}}}}}", value)

    workflow_path = assembly_dir / "workflow.md"
    workflow_path.write_text(workflow_text, encoding="utf-8")

    metadata_path = assembly_dir / "assembly.json"
    write_json(metadata_path, entry)

    append_log("initialize_assembly", {
        "assembly_id": assembly_id,
        "project": args.project,
        "opportunity_id": args.opportunity_id,
        "rapid_mode": args.rapid,
    })

    print(f"Assembly '{assembly_id}' initialized at {assembly_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
