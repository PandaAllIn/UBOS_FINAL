from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

from utils import PATHS, log_jsonl

CLAIM_PATTERN = re.compile(r"([€$]?\d+[\d%,\.\- ]*(?:million|billion|ha|%|years|month|people|farmers)?)", re.IGNORECASE)


def extract_claims(text: str) -> list[str]:
    claims = set()
    for match in CLAIM_PATTERN.findall(text):
        claim = match.strip()
        if claim:
            claims.add(claim)
    return sorted(claims)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Extract quantitative claims for validation.")
    parser.add_argument("--narrative", required=True)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)

    path = Path(args.narrative)
    text = path.read_text(encoding="utf-8") if path.exists() else ""
    claims = extract_claims(text)
    suggestions = [f"Verify '{claim}' using Oracle Trinity (Perplexity + Data Commons)." for claim in claims]
    payload = {"narrative": str(path), "claims": claims, "actions": suggestions}

    log_jsonl(PATHS.validation_log, {"event": "validate_claims", "narrative": str(path), "claim_count": len(claims)})

    if args.json:
        print(json.dumps(payload, indent=2))
    else:
        for claim in claims:
            print(f"- {claim}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
