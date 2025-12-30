from __future__ import annotations

import argparse
import json

from utils import PATHS, append_log, assembly_path, load_state, register_assembly, save_state


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else "(section pending)"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Generate LaTeX submission package for a grant assembly.")
    parser.add_argument("--assembly", required=True, help="Assembly identifier")
    parser.add_argument("--coordinator", default="UBOS Constitutional AI", help="Coordinator name")
    parser.add_argument("--submission-date", default="TBD", help="Submission date string")
    args = parser.parse_args(argv)

    assembly_dir = assembly_path(args.assembly)
    metadata = (assembly_dir / "assembly.json").read_text(encoding="utf-8") if (assembly_dir / "assembly.json").exists() else "{}"
    metadata_payload = json.loads(metadata)

    narratives_dir = assembly_dir / "narratives"
    budget_dir = assembly_dir / "budget"
    partners_dir = assembly_dir / "partners"

    excellence = read_text(narratives_dir / "excellence.md")
    impact = read_text(narratives_dir / "impact.md")
    implementation = read_text(narratives_dir / "implementation.md")
    work_plan = read_text(assembly_dir / "workflow.md")
    budget_md = read_text(budget_dir / "budget.md")
    partners_json = read_text(partners_dir / "partners.json")

    template = read_text(PATHS.assets_dir / "latex_proposal_template.tex")
    replacements = {
        "PROJECT_TITLE": metadata_payload.get("project_name", args.assembly).upper(),
        "COORDINATOR_NAME": args.coordinator,
        "SUBMISSION_DATE": args.submission_date,
        "EXCELLENCE_NARRATIVE": excellence,
        "IMPACT_NARRATIVE": impact,
        "IMPLEMENTATION_NARRATIVE": implementation,
        "WORK_PLAN": work_plan,
        "BUDGET_TABLE": budget_md,
        "PARTNER_LETTERS": "See attached scanned letters.",
        "CVS": "See attached CV bundle.",
        "COMPLIANCE_ATTACHMENTS": "Compliance report stored in compliance/compliance_report.json",
    }
    latex_content = template
    for key, value in replacements.items():
        latex_content = latex_content.replace(f"{{{{{key}}}}}", value)

    submission_dir = assembly_dir / "submission"
    submission_dir.mkdir(parents=True, exist_ok=True)
    tex_path = submission_dir / "proposal.tex"
    tex_path.write_text(latex_content, encoding="utf-8")

    metadata_out = {
        "project_name": metadata_payload.get("project_name", args.assembly),
        "coordinator": args.coordinator,
        "submission_date": args.submission_date,
        "assembly": args.assembly,
        "files": {
            "narratives": [str((narratives_dir / name).as_posix()) for name in ("excellence.md", "impact.md", "implementation.md") if (narratives_dir / name).exists()],
            "budget": str((budget_dir / "budget.csv").as_posix()) if (budget_dir / "budget.csv").exists() else None,
            "partners": str((partners_dir / "partners.json").as_posix()) if (partners_dir / "partners.json").exists() else None,
        },
    }
    (submission_dir / "metadata.json").write_text(json.dumps(metadata_out, indent=2), encoding="utf-8")

    state = load_state()
    for assembly in state.get("assemblies", []):
        if assembly.get("id") == args.assembly:
            phases = assembly.setdefault("phases", {})
            phases.setdefault("packaging", {})
            phases["packaging"]["status"] = "complete"
            phases["packaging"]["proposal_tex"] = tex_path.as_posix()
            register_assembly(state, assembly)
            break
    save_state(state)

    append_log("generate_submission_package", {
        "assembly_id": args.assembly,
        "tex_path": tex_path.as_posix(),
    })

    print(f"Submission package generated at {tex_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
