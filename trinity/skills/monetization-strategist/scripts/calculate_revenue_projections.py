from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from typing import Any, Dict

from utils import PATHS, ensure_directories, log_event, random_seed, save_json

DEFAULT_PARAMS = {
    "freemium_users": 1000,
    "signup_growth": 1.25,  # 25% monthly growth of freemium base
    "conversion_pro": 0.04,
    "conversion_enterprise": 0.01,
    "conversion_consortium": 0.003,
    "price_pro": 299,
    "price_enterprise": 799,
    "price_consortium": 1999,
    "churn_pro": 0.02,
    "churn_enterprise": 0.015,
    "churn_consortium": 0.01,
}

SCENARIO_FACTORS = {
    "conservative": 0.7,
    "base": 1.0,
    "optimistic": 1.3,
}


def simulate_month(params: Dict[str, float], state: Dict[str, float], rng) -> Dict[str, float]:
    freemium = state["freemium"] * params["signup_growth"]
    pro_new = freemium * params["conversion_pro"] * rng.uniform(0.85, 1.15)
    ent_new = freemium * params["conversion_enterprise"] * rng.uniform(0.85, 1.15)
    cons_new = freemium * params["conversion_consortium"] * rng.uniform(0.85, 1.15)

    pro_active = (state["pro_customers"] * (1 - params["churn_pro"])) + pro_new
    ent_active = (state["enterprise_customers"] * (1 - params["churn_enterprise"])) + ent_new
    cons_active = (state["consortium_customers"] * (1 - params["churn_consortium"])) + cons_new

    mrr = (
        pro_active * params["price_pro"]
        + ent_active * params["price_enterprise"]
        + cons_active * params["price_consortium"]
    )

    return {
        "freemium": freemium,
        "pro_customers": pro_active,
        "enterprise_customers": ent_active,
        "consortium_customers": cons_active,
        "mrr": mrr,
    }


def run_simulation(months: int, params: Dict[str, float], runs: int, seed: int | None) -> Dict[str, Any]:
    rng = random_seed(seed)
    trajectories = []
    for _ in range(runs):
        state = {
            "freemium": params["freemium_users"],
            "pro_customers": 0.0,
            "enterprise_customers": 0.0,
            "consortium_customers": 0.0,
            "mrr": 0.0,
        }
        history = []
        for _ in range(months):
            state = simulate_month(params, state, rng)
            history.append(state["mrr"])
        trajectories.append(history)

    transposed = list(zip(*trajectories))
    quantiles = []
    for month_idx, month_values in enumerate(transposed, start=1):
        sorted_vals = sorted(month_values)
        p30 = sorted_vals[int(0.30 * len(sorted_vals))]
        p50 = sorted_vals[int(0.50 * len(sorted_vals))]
        p70 = sorted_vals[int(0.70 * len(sorted_vals))]
        quantiles.append({
            "month": month_idx,
            "mrr_p30": round(p30, 2),
            "mrr_p50": round(p50, 2),
            "mrr_p70": round(p70, 2),
            "arr_p50": round(p50 * 12, 2),
        })
    return {"months": months, "runs": runs, "quantiles": quantiles}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run Monte Carlo revenue projections for EUFM.")
    parser.add_argument("--scenario", choices=sorted(SCENARIO_FACTORS.keys()), default="base", help="Projection scenario")
    parser.add_argument("--months", type=int, default=12, help="Number of months to project")
    parser.add_argument("--runs", type=int, default=5000, help="Monte Carlo runs")
    parser.add_argument("--seed", type=int, help="Random seed")
    parser.add_argument("--output", help="Output JSON path")
    args = parser.parse_args(argv)

    factor = SCENARIO_FACTORS[args.scenario]
    params = {key: (value * factor if key.startswith("conversion") or key.endswith("_users") else value) for key, value in DEFAULT_PARAMS.items()}
    params.update({"price_pro": DEFAULT_PARAMS["price_pro"], "price_enterprise": DEFAULT_PARAMS["price_enterprise"], "price_consortium": DEFAULT_PARAMS["price_consortium"]})

    ensure_directories()
    result = run_simulation(args.months, params, args.runs, args.seed)

    if args.output:
        output_path = Path(args.output)
        save_json(output_path, result)
        print(f"Projections saved to {output_path}")
    else:
        print(json.dumps(result, indent=2))

    log_event("revenue_projection", {"scenario": args.scenario, "months": args.months, "runs": args.runs})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
