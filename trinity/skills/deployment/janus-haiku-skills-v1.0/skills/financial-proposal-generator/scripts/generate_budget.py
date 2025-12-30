from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

from utils import PATHS, ensure_directories, log_jsonl


def load_work_packages(profile: str | None) -> list[dict[str, float | str]]:
    if not profile:
        return [
            {"id": "WP1", "title": "Research & Intelligence", "share": 0.2},
            {"id": "WP2", "title": "Development & Deployment", "share": 0.35},
            {"id": "WP3", "title": "Field Trials", "share": 0.25},
            {"id": "WP4", "title": "Dissemination & Management", "share": 0.2},
        ]
    with Path(profile).open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    return data if isinstance(data, list) else []


def normalise_shares(work_packages: list[dict[str, float | str]]) -> list[dict[str, float | str]]:
    total = sum(float(item.get("share", 0.0) or 0.0) for item in work_packages)
    if total <= 0:
        equal = 1 / len(work_packages) if work_packages else 1
        for item in work_packages:
            item["share"] = equal
    else:
        for item in work_packages:
            item["share"] = float(item.get("share", 0.0) or 0.0) / total
    return work_packages


def write_budget_files(assembly: str, total: float, work_packages: list[dict[str, float | str]]) -> None:
    budget_dir = PATHS.assemblies_root / assembly / "budget"
    budget_dir.mkdir(parents=True, exist_ok=True)

    csv_path = budget_dir / "budget.csv"
    with csv_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["Work Package", "Title", "Share %", "Direct EUR", "Indirect EUR", "Total EUR"])
        for wp in work_packages:
            share = float(wp["share"])
            direct = total * share / 1.25
            indirect = direct * 0.25
            writer.writerow([
                wp.get("id"),
                wp.get("title"),
                round(share * 100, 2),
                round(direct, 2),
                round(indirect, 2),
                round(direct + indirect, 2),
            ])

    justification = ["# Budget Justification", ""]
    for wp in work_packages:
        share = float(wp["share"])
        allocated = total * share
        justification.extend([
            f"## {wp.get('id')} - {wp.get('title')}",
            f"Allocated Budget: EUR {allocated:,.2f}",
            "- Personnel: 60%",
            "- Travel & field costs: 20%",
            "- Equipment & consumables: 15%",
            "- Dissemination & contingency: 5%",
            "",
        ])
    (budget_dir / "justification.md").write_text("\n".join(justification), encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Generate EU budget tables and justification.")
    parser.add_argument("--assembly", required=True)
    parser.add_argument("--total", type=float, required=True)
    parser.add_argument("--work-packages", help="JSON file describing work package shares")
    args = parser.parse_args(argv)

    ensure_directories()
    work_packages = normalise_shares(load_work_packages(args.work_packages))
    write_budget_files(args.assembly, args.total, work_packages)

    log_jsonl(PATHS.validation_log, {
        "event": "generate_budget",
        "assembly": args.assembly,
        "total": args.total,
    })
    print(f"Budget generated for assembly {args.assembly}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
