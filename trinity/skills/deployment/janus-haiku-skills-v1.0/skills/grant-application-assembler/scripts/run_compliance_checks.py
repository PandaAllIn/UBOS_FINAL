from __future__ import annotations

import argparse
import json
from typing import Any

from utils import append_log, assembly_path, load_state, register_assembly, save_state

CHECKS = (
    ("excellence narrative", lambda paths: (paths / "narratives" / "excellence.md").exists()),
    ("impact narrative", lambda paths: (paths / "narratives" / "impact.md").exists()),
    ("implementation narrative", lambda paths: (paths / "narratives" / "implementation.md").exists()),
    ("budget tables", lambda paths: (paths / "budget" / "budget.csv").exists()),
    ("partner ledger", lambda paths: (paths / "partners" / "partners.json").exists()),
)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run compliance checks for a grant assembly.")
    parser.add_argument("--assembly", required=True, help="Assembly identifier")
    parser.add_argument("--json", action="store_true", help="Emit JSON report")
    args = parser.parse_args(argv)

    assembly_dir = assembly_path(args.assembly)

    report: list[dict[str, Any]] = []
    passed = True
    for name, predicate in CHECKS:
        status = bool(predicate(assembly_dir))
        report.append({"check": name, "status": "pass" if status else "fail"})
        passed &= status

    compliance_dir = assembly_dir / "compliance"
    compliance_dir.mkdir(parents=True, exist_ok=True)
    report_path = compliance_dir / "compliance_report.json"
    report_payload = {"assembly": args.assembly, "passed": passed, "checks": report}
    report_path.write_text(json.dumps(report_payload, indent=2), encoding="utf-8")

    state = load_state()
    for assembly in state.get("assemblies", []):
        if assembly.get("id") == args.assembly:
            phases = assembly.setdefault("phases", {})
            phases.setdefault("compliance", {})
            phases["compliance"]["status"] = "complete" if passed else "in_progress"
            phases["compliance"]["last_report"] = report_path.as_posix()
            register_assembly(state, assembly)
            break
    save_state(state)

    append_log("compliance_check", {
        "assembly_id": args.assembly,
        "passed": passed,
    })

    if args.json:
        print(json.dumps(report_payload, indent=2))
    else:
        for item in report:
            symbol = "✅" if item["status"] == "pass" else "⚠️"
            print(f"{symbol} {item['check']}: {item['status']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
