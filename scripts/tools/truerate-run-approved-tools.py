#!/usr/bin/env python3
"""
scripts/tools/truerate-run-approved-tools.py

Step 5 of the truerate-remittance-cost-audit recipe. Runs the actual
comparison: mid-market rate vs. each verified provider's estimated
delivered amount, plus the timing analysis. No live network/external
writes happen here -- everything is a pure computation over already-
verified local data, so no approval gate is required for this run.
"""
import json
import os
import sys
from datetime import datetime, timezone

sys.path.insert(0, "scripts/tools")
from truerate_logic import get_mid_market_rate, compare_providers, timing_analysis


def main():
    with open("data/raw/truerate-remittance-cost-audit/ingested-inputs.json") as f:
        raw = json.load(f)
    rec = raw["records"][0]

    with open("data/verified/truerate-remittance-cost-audit/quality-checked.json") as f:
        quality = json.load(f)

    amount = rec["amount_usd"]
    horizon = rec["horizon_days"]
    verified_providers = quality["verified_records"]

    mm = get_mid_market_rate()
    all_comparisons = compare_providers(amount, mm["rate"])
    comparisons = {p: all_comparisons[p] for p in verified_providers}

    try:
        timing = timing_analysis(horizon)
    except ValueError as e:
        timing = {"error": str(e)}

    result = {
        "tool_name": "truerate_logic.compare_providers + timing_analysis",
        "input_path": "data/verified/truerate-remittance-cost-audit/quality-checked.json",
        "output_path": "data/verified/truerate-remittance-cost-audit/comparison-result.json",
        "action_taken": "computed rate comparison and timing analysis over local/verified data",
        "approval_id": None,
        "no_write_mode": False,
        "mid_market": mm,
        "comparisons": comparisons,
        "timing": timing,
        "computed_at": datetime.now(timezone.utc).isoformat(),
    }

    out_path = "data/verified/truerate-remittance-cost-audit/comparison-result.json"
    with open(out_path, "w") as f:
        json.dump(result, f, indent=2)

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
