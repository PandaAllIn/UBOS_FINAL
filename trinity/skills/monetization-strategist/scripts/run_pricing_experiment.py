from __future__ import annotations

import argparse
import json
import math

from utils import log_event


def parse_conversion(value: str) -> tuple[int, int]:
    try:
        wins, total = value.split("/")
        return int(wins), int(total)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("Conversion must be in wins/total format") from exc


def z_test(conv_a: tuple[int, int], conv_b: tuple[int, int]) -> float:
    wins_a, total_a = conv_a
    wins_b, total_b = conv_b
    p1 = wins_a / total_a
    p2 = wins_b / total_b
    p_pool = (wins_a + wins_b) / (total_a + total_b)
    se = math.sqrt(p_pool * (1 - p_pool) * (1 / total_a + 1 / total_b))
    if se == 0:
        return 0.0
    return (p1 - p2) / se


def recommendation(price_a: float, price_b: float, conv_a: tuple[int, int], conv_b: tuple[int, int]) -> dict[str, str]:
    mrr_a = price_a * (conv_a[0])
    mrr_b = price_b * (conv_b[0])
    decision = "A" if mrr_a > mrr_b else "B"
    reasoning = []
    reasoning.append(f"Variant A (€{price_a}) MRR: €{mrr_a:.2f}")
    reasoning.append(f"Variant B (€{price_b}) MRR: €{mrr_b:.2f}")
    z = z_test(conv_a, conv_b)
    reasoning.append(f"Z-score: {z:.2f}")
    p_value = 1 - math.erf(abs(z) / math.sqrt(2))
    reasoning.append(f"Approx. two-tailed p-value: {p_value:.3f}")
    if p_value > 0.05:
        reasoning.append("Difference not statistically significant; choose based on strategic positioning.")
    else:
        reasoning.append("Difference statistically significant (p ≤ 0.05).")
    if mrr_a == mrr_b:
        decision = "strategic"
        reasoning.append("MRR identical; decide via value perception / bundling.")
    return {"decision": decision, "notes": reasoning}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Evaluate SaaS pricing experiment results.")
    parser.add_argument("--experiment", required=True, help="Experiment identifier")
    parser.add_argument("--variant-a", type=float, required=True, help="Price for variant A")
    parser.add_argument("--variant-b", type=float, required=True, help="Price for variant B")
    parser.add_argument("--conversions-a", type=parse_conversion, required=True, help="wins/total for variant A")
    parser.add_argument("--conversions-b", type=parse_conversion, required=True, help="wins/total for variant B")
    parser.add_argument("--json", action="store_true", help="Emit JSON output")
    args = parser.parse_args(argv)

    result = recommendation(args.variant_a, args.variant_b, args.conversions_a, args.conversions_b)
    payload = {
        "experiment": args.experiment,
        "variant_a": {"price": args.variant_a, "conversions": args.conversions_a},
        "variant_b": {"price": args.variant_b, "conversions": args.conversions_b},
        "decision": result["decision"],
        "notes": result["notes"],
    }
    log_event("pricing_experiment", payload)

    if args.json:
        print(json.dumps(payload, indent=2))
    else:
        print(f"Decision: {result['decision']}")
        for note in result["notes"]:
            print(f"- {note}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
