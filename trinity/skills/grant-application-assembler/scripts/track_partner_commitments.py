from __future__ import annotations

import argparse
import json
from typing import Any

from utils import append_log, assembly_path, load_state, register_assembly, save_state

VALID_STATUSES = {"pending", "received", "missing", "reminder_sent"}


def load_partners(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8") as handle:
        try:
            data = json.load(handle)
        except json.JSONDecodeError:
            return []
    return data if isinstance(data, list) else []


def save_partners(path: Path, partners: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(partners, handle, indent=2, sort_keys=True)


def update_partner(partners: list[dict[str, Any]], name: str, status: str, contact: str | None) -> list[dict[str, Any]]:
    updated = []
    found = False
    for entry in partners:
        if entry.get("name", "").lower() == name.lower():
            entry = {**entry, "name": name, "status": status}
            if contact:
                entry["contact"] = contact
            entry["updated"] = True
            found = True
        updated.append(entry)
    if not found:
        updated.append({"name": name, "status": status, "contact": contact})
    for entry in updated:
        entry.pop("updated", None)
    return updated


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Track partner commitment status for a grant assembly.")
    parser.add_argument("--assembly", required=True, help="Assembly identifier")
    parser.add_argument("--partner", help="Partner name")
    parser.add_argument("--status", choices=sorted(VALID_STATUSES), help="Status update")
    parser.add_argument("--contact", help="Contact email or handle")
    parser.add_argument("--list", action="store_true", help="List partner status")
    args = parser.parse_args(argv)

    assembly_dir = assembly_path(args.assembly)
    partners_path = assembly_dir / "partners" / "partners.json"
    partners = load_partners(partners_path)

    if args.list and (args.partner or args.status):
        parser.error("--list cannot be combined with update flags")

    if args.list:
        if not partners:
            print("No partner records found.")
            return 0
        for entry in partners:
            line = f"- {entry.get('name', 'Unknown')}: {entry.get('status', 'pending')}"
            if entry.get("contact"):
                line += f" (contact: {entry['contact']})"
            print(line)
        return 0

    if not args.partner or not args.status:
        parser.error("--partner and --status are required when not using --list")

    partners = update_partner(partners, args.partner, args.status, args.contact)
    save_partners(partners_path, partners)

    state = load_state()
    for assembly in state.get("assemblies", []):
        if assembly.get("id") == args.assembly:
            phases = assembly.setdefault("phases", {})
            partners_phase = phases.setdefault("partners", {})
            partners_phase["status"] = "complete" if all(p.get("status") == "received" for p in partners) else "in_progress"
            partners_phase["count"] = len(partners)
            partners_phase["received"] = sum(1 for p in partners if p.get("status") == "received")
            register_assembly(state, assembly)
            break
    save_state(state)

    append_log("partner_update", {
        "assembly_id": args.assembly,
        "partner": args.partner,
        "status": args.status,
    })

    print(f"Partner '{args.partner}' marked as {args.status}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
