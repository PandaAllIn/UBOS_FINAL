from __future__ import annotations

import argparse
import json
import textwrap

from utils import PATHS, ensure_directories, write_markdown, log_jsonl

SECTION_TEMPLATES = {
    "excellence": textwrap.dedent(
        """
        1.1 Objectives and Ambition
        - Summarise innovation, objectives, and ambition.

        1.2 Methodology and Approach
        - Outline work packages, tasks, and deliverables.

        1.3 Concept and Innovation
        - Compare with state of the art, highlight novelty.

        1.4 Research Infrastructure and Resources
        - Detail facilities, teams, and data assets.
        """
    ),
    "impact": textwrap.dedent(
        """
        2.1 Project Impact Pathway
        - Quantify beneficiaries, economic/social/environmental outcomes.

        2.2 Measures to Maximise Impact
        - Describe exploitation, dissemination, and communication strategies.

        2.3 Communication and Engagement
        - Define audiences, channels, and KPIs.

        2.4 Sustainability and Scalability
        - Explain post-project governance and funding model.
        """
    ),
    "implementation": textwrap.dedent(
        """
        3.1 Work Plan
        - Summarise work packages, deliverables, milestones.

        3.2 Management Structure
        - Governance, decision processes, risk management.

        3.3 Consortium Composition
        - Partner roles, expertise, and complementarity.

        3.4 Resources
        - Person-months, budget allocation, ethics, and security.
        """
    ),
}


def load_opportunity(assembly: str) -> dict[str, str]:
    metadata_path = PATHS.assemblies_root / assembly / "assembly.json"
    if not metadata_path.exists():
        return {}
    try:
        return json.loads(metadata_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Generate proposal narrative scaffold.")
    parser.add_argument("--assembly", required=True)
    parser.add_argument("--section", choices=sorted(SECTION_TEMPLATES.keys()), required=True)
    parser.add_argument("--project", required=True)
    parser.add_argument("--call", required=True)
    parser.add_argument("--overwrite", action="store_true")
    args = parser.parse_args(argv)

    ensure_directories()
    narratives_dir = PATHS.assemblies_root / args.assembly / "narratives"
    narratives_dir.mkdir(parents=True, exist_ok=True)
    target = narratives_dir / f"{args.section}.md"

    if target.exists() and not args.overwrite:
        parser.error(f"Narrative already exists at {target}. Use --overwrite to replace it.")

    opportunity = load_opportunity(args.assembly)
    header = textwrap.dedent(
        f"""
        # {args.section.title()} Narrative

        Call: {args.call}
        Project: {args.project}
        Budget Range: EUR {opportunity.get('budget_min', '?')} - EUR {opportunity.get('budget_max', '?')}
        Fit Score: {opportunity.get('fit_score', '?')}
        """
    )
    body = SECTION_TEMPLATES[args.section]
    write_markdown(target, header + "\n" + body + "\n")

    log_jsonl(PATHS.validation_log, {
        "event": "generate_narrative",
        "assembly": args.assembly,
        "section": args.section,
    })

    print(f"Narrative generated at {target}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
