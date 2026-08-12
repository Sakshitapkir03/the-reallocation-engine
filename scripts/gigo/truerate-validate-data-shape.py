#!/usr/bin/env python3
"""
scripts/gigo/truerate-validate-data-shape.py

Step 3 of the truerate-remittance-cost-audit recipe. Checks that the
ingested record from Step 2 has the required fields, correct types, and
sane ranges, before any computation runs. This is the "GIGO gate" layer --
named per the repo's own convention (scripts live under scripts/gigo/).
"""
import json
import os
import sys


def main():
    in_path = "data/raw/truerate-remittance-cost-audit/ingested-inputs.json"
    with open(in_path) as f:
        raw = json.load(f)

    parse_errors = []
    missing_fields = []
    if not raw["records"]:
        parse_errors.append("no records present -- Step 2 rejected all input")
    else:
        rec = raw["records"][0]
        if "amount_usd" not in rec:
            missing_fields.append("amount_usd")
        elif not isinstance(rec["amount_usd"], (int, float)) or rec["amount_usd"] <= 0:
            parse_errors.append(f"amount_usd must be a positive number, got {rec.get('amount_usd')}")

        if "providers" not in rec:
            missing_fields.append("providers")
        elif not isinstance(rec["providers"], list) or len(rec["providers"]) == 0:
            parse_errors.append("providers must be a non-empty list")

        if "horizon_days" not in rec:
            missing_fields.append("horizon_days")
        elif not isinstance(rec["horizon_days"], int) or rec["horizon_days"] <= 0:
            parse_errors.append(f"horizon_days must be a positive integer, got {rec.get('horizon_days')}")

    result = {
        "record_count": len(raw["records"]),
        "required_fields_present": len(missing_fields) == 0,
        "missing_fields": missing_fields,
        "parse_errors": parse_errors,
        "schema_version": "0.1.0",
    }

    os.makedirs("data/verified/truerate-remittance-cost-audit", exist_ok=True)
    out_path = "data/verified/truerate-remittance-cost-audit/data-shape-check.json"
    with open(out_path, "w") as f:
        json.dump(result, f, indent=2)

    print(json.dumps(result, indent=2))
    if missing_fields or parse_errors:
        sys.exit(1)


if __name__ == "__main__":
    main()
