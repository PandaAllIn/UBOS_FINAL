from __future__ import annotations

import argparse
import textwrap

from utils import (
    PATHS,
    assembly_path,
    append_log,
    load_state,
    read_json,
    register_assembly,
    save_state,
)

SECTIONS = {"excellence", "impact", "implementation"}

EXCELLENCE_TEMPLATE = textwrap.dedent(
    """
    ## Objectives and Ambition
    - Deliver {project} aligned with {call}.
    - Harness UBOS constitutional AI governance for transparent, human-centred deployment.
    - Demonstrate innovation via Oracle Trinity integration and sovereign infrastructure.
    """
)

IMPACT_TEMPLATE = textwrap.dedent(
    """
    ## Impact Pathway
    - Economic: Expected to unlock €{economic}M across consortium regions.
    - Social: Benefits {beneficiaries} through co-designed services.
    - Environmental: Supports EU Green Deal via {environmental}.

    ## Measures to Maximise Impact
    - Communication: Monthly COMMS_HUB updates plus partner newsletters.
    - Exploitation: Joint IP committee chaired by the UBOS Treasury Administrator.
    - Open Science: Data management plan ensuring FAIR datasets (with farmer consent safeguards).
    """
)

IMPLEMENTATION_TEMPLATE = textwrap.dedent(
    """
    ## Work Plan Overview
    - WP1: Intelligence & Research (UBOS lead, Months 1-6).
    - WP2: Development & Deployment (Consortium, Months 4-18).
    - WP3: Validation & Demonstration (User partners, Months 10-22).
    - WP4: Dissemination & Exploitation (All partners, Months 6-24).

    ## Governance
    - Mode Beta supervisory loop keeps humans-in-the-loop for high-risk actions.
    - Treasury Cascade enforces constitutional budgeting across work packages.
    - Emergency stop procedures integrated with partner operations and EU ethics guidance.
    """
)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Compile core narratives for a grant assembly.")
    parser.add_argument("--assembly", required=True, help="Assembly identifier (slug)")
    parser.add_argument("--section", choices=sorted(SECTIONS), required=True, help="Narrative section to generate")
    parser.add_argument("--economic", default="50", help="Projected economic benefit (numeric string)")
    parser.add_argument("--beneficiaries", default="European stakeholders", help="Primary beneficiaries description")
    parser.add_argument("--environmental", default="renewable-powered infrastructure", help="Environmental contribution summary")
    parser.add_argument("--overwrite", action="store_true", help="Overwrite existing narrative file")
    args = parser.parse_args(argv)

    state = load_state()
    assembly_dir = assembly_path(args.assembly)
    metadata = read_json(assembly_dir / "assembly.json", {}) or {
        "project_name": args.assembly,
        "opportunity_id": "unknown",
    }

    narratives_dir = assembly_dir / "narratives"
    narratives_dir.mkdir(parents=True, exist_ok=True)
    target_path = narratives_dir / f"{args.section}.md"
    if target_path.exists() and not args.overwrite:
        parser.error(f"Narrative {args.section} already exists; use --overwrite to replace")

    if args.section == "excellence":
        body = EXCELLENCE_TEMPLATE.format(
            project=metadata.get("project_name", args.assembly),
            call=metadata.get("opportunity_id", "the call"),
        )
    elif args.section == "impact":
        body = IMPACT_TEMPLATE.format(
            economic=args.economic,
            beneficiaries=args.beneficiaries,
            environmental=args.environmental,
        )
    else:
        body = IMPLEMENTATION_TEMPLATE

    header = f"# {args.section.title()} Narrative\n\n"
    target_path.write_text(header + body + "\n", encoding="utf-8")

    for assembly in state.get("assemblies", []):
        if assembly.get("id") == args.assembly:
            phases = assembly.setdefault("phases", {})
            narratives = phases.setdefault("narratives", {})
            completed = set(narratives.get("completed", []))
            completed.add(args.section)
            narratives["completed"] = sorted(completed)
            narratives["status"] = "complete" if completed >= SECTIONS else "in_progress"
            register_assembly(state, assembly)
            break
    save_state(state)

    append_log(
        "compile_narrative",
        {
            "assembly_id": args.assembly,
            "section": args.section,
            "path": str(target_path),
        },
    )

    print(f"Narrative '{args.section}' generated at {target_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
