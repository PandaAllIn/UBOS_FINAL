from __future__ import annotations

import argparse
import json
import logging
from dataclasses import asdict, dataclass
from typing import Any, Dict

import sys
from pathlib import Path

# Add the janus root to the path to allow trinity imports
JANUS_ROOT = Path("/srv/janus")
if str(JANUS_ROOT) not in sys.path:
    sys.path.append(str(JANUS_ROOT))

from trinity.config import load_configuration
from trinity.oracle_bridge import OracleBridge, OracleError
from trinity.oracle_health_check import OracleHealthChecker, OracleHealth


LOGGER = logging.getLogger("treasury.analyze_financials")
logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(message)s")


@dataclass(slots=True)
class FinancialSnapshot:
    region: str
    fallback_used: bool
    economics: str
    demographics: str
    oracle_status: Dict[str, OracleHealth]

    def to_json(self) -> str:
        payload: Dict[str, Any] = {
            "region": self.region,
            "fallback_used": self.fallback_used,
            "economics": self.economics,
            "demographics": self.demographics,
            "oracle_status": {name: asdict(health) for name, health in self.oracle_status.items()},
        }
        return json.dumps(payload, indent=2)

    def to_text(self) -> str:
        lines = [
            f"Region: {self.region}",
            f"Fallback used: {'yes' if self.fallback_used else 'no'}",
            "",
            "Economic Indicators:",
            self.economics.strip(),
            "",
            "Demographic Indicators:",
            self.demographics.strip(),
            "",
            "Oracle Status:",
        ]
        for name, health in self.oracle_status.items():
            status = "healthy" if health.status else "degraded"
            lines.append(f"- {name}: {status} ({health.latency_ms:.1f}ms)")
            if health.error:
                lines.append(f"  ↳ {health.error}")
        return "\n".join(lines)


def run_analysis(region: str) -> FinancialSnapshot:
    _, keys = load_configuration()
    health_checker = OracleHealthChecker()
    oracle_status = health_checker.check_all()

    datacommons_healthy = oracle_status.get("datacommons")
    fallback_required = not (datacommons_healthy.status if datacommons_healthy else True)

    bridge = OracleBridge(keys)
    try:
        economics = bridge.query_economics(region, fallback=fallback_required)
    except OracleError as exc:
        LOGGER.warning("Economics query failed; forcing Groq fallback. reason=%s", exc.message)
        economics = bridge.research(f"Economic profile for {region}", fallback=True, mode="balanced")
        fallback_required = True

    try:
        demographics = bridge.query_demographics(region)
    except OracleError as exc:  # pragma: no cover - future-proofing
        LOGGER.warning("Demographics query failed; returning advisory message. reason=%s", exc.message)
        demographics = f"Unable to retrieve demographics for {region}. Error: {exc.message}"

    return FinancialSnapshot(
        region=region,
        fallback_used=fallback_required,
        economics=economics,
        demographics=demographics,
        oracle_status=oracle_status,
    )


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Analyze regional financial health using UBOS oracles.")
    parser.add_argument("--region", default="country/ROU", help="Data Commons DCID for region (default: country/ROU)")
    parser.add_argument("--json", action="store_true", help="Emit machine-readable JSON payload.")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    snapshot = run_analysis(args.region)
    if args.json:
        print(snapshot.to_json())
    else:
        print(snapshot.to_text())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
