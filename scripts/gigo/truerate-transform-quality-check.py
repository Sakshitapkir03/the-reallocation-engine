#!/usr/bin/env python3
"""
scripts/gigo/truerate-transform-quality-check.py

Step 4 of the truerate-remittance-cost-audit recipe. Checks that every
provider requested in the run envelope is actually a known, sourced
provider (not silently substituted or dropped), and flags rate staleness.
This is a real check, not a placeholder -- it will genuinely reject an
unknown provider rather than silently skip it.
"""
import json
import os
import sys
from datetime import datetime, timezone, date

sys.path.insert(0, "scripts/tools")
from truerate_logic import PROVIDER_FEE_STRUCTURES, MID_MARKET_SNAPSHOT


def main():
    with open("data/raw/truerate-remittance-cost-audit/ingested-inputs.json") as f:
        raw = json.load(f)
    rec = raw["records"][0]

    verified_records = []
    rejects = []
    for provider in rec["providers"]:
        if provider not in PROVIDER_FEE_STRUCTURES:
            rejects.append({"provider": provider, "reason": "unknown provider -- not in "
                           "PROVIDER_FEE_STRUCTURES, refusing to guess a fee schedule"})
        else:
            verified_records.append(provider)

    # Staleness check: is the mid-market snapshot's as_of date old?
    as_of = date.fromisoformat(MID_MARKET_SNAPSHOT["as_of"])
    days_stale = (date.today() - as_of).days
    flags = []
    if days_stale > 1:
        flags.append(f"mid_market_rate snapshot is {days_stale} day(s) old "
                    f"(as_of={MID_MARKET_SNAPSHOT['as_of']}) -- treat as potentially "
                    f"stale; this recipe has NOT yet implemented an automatic "
                    f"staleness block (see the recipe's Stop Conditions)")

    result = {
        "verified_records": verified_records,
        "record_count": len(verified_records),
        "duplicates": [],
        "rejects": rejects,
        "flags": flags,
        "quality_notes": f"mid-market rate snapshot as_of={MID_MARKET_SNAPSHOT['as_of']}, "
                        f"{days_stale} day(s) old at check time",
    }

    out_path = "data/verified/truerate-remittance-cost-audit/quality-checked.json"
    with open(out_path, "w") as f:
        json.dump(result, f, indent=2)

    print(json.dumps(result, indent=2))
    if not verified_records:
        sys.exit(1)


if __name__ == "__main__":
    main()
