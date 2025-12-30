from __future__ import annotations

import argparse
import json

from utils import log_event


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Calculate EUFM customer LTV and LTV:CAC ratio.")
    parser.add_argument("--tier", required=True, help="Tier name")
    parser.add_argument("--price", type=float, required=True, help="Monthly subscription price")
    parser.add_argument("--retention-months", type=float, required=True, help="Average retention in months")
    parser.add_argument("--upsell-prob", type=float, default=0.0, help="Upsell probability (0-1)")
    parser.add_argument("--upsell-value", type=float, default=0.0, help="Expected upsell value (EUR)")
    parser.add_argument("--cac", type=float, default=1200.0, help="Customer acquisition cost")
    parser.add_argument("--json", action="store_true", help="Emit JSON output")
    args = parser.parse_args(argv)

    subscription_value = args.price * args.retention_months
    upsell_component = args.upsell_prob * args.upsell_value
    ltv = subscription_value + upsell_component
    ratio = ltv / args.cac if args.cac else float("inf")

    payload = {
        "tier": args.tier,
        "ltv": round(ltv, 2),
        "subscription_value": round(subscription_value, 2),
        "upsell_value": round(upsell_component, 2),
        "ltv_cac_ratio": round(ratio, 2),
        "cac": args.cac,
    }
    log_event("ltv_calculation", payload)

    if args.json:
        print(json.dumps(payload, indent=2))
    else:
        print(f"Tier: {args.tier}")
        print(f"LTV: €{payload['ltv']:.2f}")
        print(f"LTV:CAC: {payload['ltv_cac_ratio']}:1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
