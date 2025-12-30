from __future__ import annotations

import argparse
import csv
from typing import Any, Iterable

from utils import (
    append_log,
    assembly_path,
    load_state,
    register_assembly,
    save_state,
)

DEFAULT_WPS = [
    {"id": "WP1", "title": "Research & Intelligence", "share": 0.2},
    {"id": "WP2", "title": "Development & Deployment", "share": 0.35},
    {"id": "WP3", "title": "Validation & Field Trials", "share": 0.25},
    {"id": "WP4", "title": "Dissemination & Management", "share": 0.2},
]


def load_work_packages(path: str | None) -> list[dict[str, Any]]:
    if not path:
        return DEFAULT_WPS
    with Path(path).open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, list):
        raise ValueError("Work packages file must contain a list")
    return data


def normalise_shares(work_packages: Iterable[dict[str, Any]]) -> list[dict[str, Any]]:
    wps = []
    total_share = 0.0
    fallback_count = 0
    for item in work_packages:
        share = float(item.get("share", 0.0)) if item.get("share") is not None else 0.0
        total_share += share
        if share == 0.0:
            fallback_count += 1
        wps.append({"id": item.get("id", "WP"), "title": item.get("title", "Work Package"), "share": share})
    if total_share == 0.0:
        equal = 1.0 / len(wps) if wps else 1.0
        for item in wps:
            item["share"] = equal
    elif total_share != 1.0:
        remainder = max(0.0, 1.0 - total_share)
        if fallback_count:
            bonus = remainder / fallback_count
            for item in wps:
                if item["share"] == 0.0:
                    item["share"] = bonus
        factor = sum(item["share"] for item in wps)
        for item in wps:
            item["share"] /= factor or 1.0
    return wps


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Assemble EU-compliant budget tables for a grant assembly.")
    parser.add_argument("--assembly", required=True, help="Assembly identifier")
    parser.add_argument("--total", type=float, required=True, help="Total project budget in euros")
    parser.add_argument("--work-packages", help="JSON file describing work packages with shares")
    parser.add_argument("--indirect-rate", type=float, default=0.25, help="Indirect cost rate (e.g., 0.25 for 25% flat)")
    args = parser.parse_args(argv)

    assembly_dir = assembly_path(args.assembly)
    budget_dir = assembly_dir / "budget"
    budget_dir.mkdir(parents=True, exist_ok=True)

    work_packages = normalise_shares(load_work_packages(args.work_packages))
    total_direct = args.total / (1 + args.indirect_rate)

    rows = []
    for wp in work_packages:
        direct = total_direct * wp["share"]
        indirect = direct * args.indirect_rate
        total = direct + indirect
        rows.append({
            "work_package": f"{wp['id']} - {wp['title']}",
            "direct_costs": round(direct, 2),
            "indirect_costs": round(indirect, 2),
            "total_cost": round(total, 2),
            "share": round(wp["share"] * 100, 2),
        })

    csv_path = budget_dir / "budget.csv"
    with csv_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["work_package", "share", "direct_costs", "indirect_costs", "total_cost"])
        writer.writeheader()
        for row in rows:
            writer.writerow(row)

    markdown_lines = ["| Work Package | Share % | Direct (€) | Indirect (€) | Total (€) |", "|---|---|---|---|---|"]
    for row in rows:
        markdown_lines.append(
            f"| {row['work_package']} | {row['share']} | {row['direct_costs']:,} | {row['indirect_costs']:,} | {row['total_cost']:,} |"
        )
    (budget_dir / "budget.md").write_text("\n".join(markdown_lines) + "\n", encoding="utf-8")

    state = load_state()
    for assembly in state.get("assemblies", []):
        if assembly.get("id") == args.assembly:
            phases = assembly.setdefault("phases", {})
            phases.setdefault("budget", {})
            phases["budget"]["status"] = "complete"
            phases["budget"]["total"] = args.total
            phases["budget"]["indirect_rate"] = args.indirect_rate
            phases["budget"]["entries"] = rows
            register_assembly(state, assembly)
            break
    save_state(state)

    append_log("assemble_budget", {
        "assembly_id": args.assembly,
        "total": args.total,
        "indirect_rate": args.indirect_rate,
        "work_packages": rows,
    })

    print(f"Budget generated at {csv_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
