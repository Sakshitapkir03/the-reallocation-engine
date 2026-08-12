#!/usr/bin/env python3
"""
scripts/tools/truerate-verify-provenance.py

Step 1 of the truerate-remittance-cost-audit recipe. Checks that the
sourced facts this recipe depends on (mid-market rate corroboration,
provider fee-schedule citations, historical rate series) are documented
with a real source, not invented. This is a structural presence check --
it confirms a source STRING exists for each fact, not that the source is
correct (that's the human gate, per SNICKERDOODLE.md's P4: machines verify
conformance, humans verify adequacy).
"""
import json
import sys
from datetime import datetime, timezone

sys.path.insert(0, "scripts/tools")
from truerate_logic import MID_MARKET_SNAPSHOT, PROVIDER_FEE_STRUCTURES, HISTORICAL_USD_INR_SAMPLE


def main():
    checked_at = datetime.now(timezone.utc).isoformat()
    checks = []

    # Mid-market rate source
    checks.append({
        "fact": "mid_market_rate_snapshot",
        "source_path": "reports/generated/truerate-plausibility-audit.md",
        "source_present": bool(MID_MARKET_SNAPSHOT.get("source")),
        "parsed_ok": True,
    })

    # Provider fee structures
    for provider, spec in PROVIDER_FEE_STRUCTURES.items():
        checks.append({
            "fact": f"provider_fee_structure:{provider}",
            "source_path": "inline citation in scripts/tools/truerate_logic.py",
            "source_present": bool(spec.get("source")),
            "parsed_ok": True,
        })

    # Historical series
    checks.append({
        "fact": "historical_usd_inr_sample",
        "source_path": "derived from api.frankfurter.dev during build; see truerate-plausibility-audit.md",
        "source_present": len(HISTORICAL_USD_INR_SAMPLE) > 0,
        "parsed_ok": all(isinstance(d.get("rate"), (int, float)) for d in HISTORICAL_USD_INR_SAMPLE),
    })

    result = {
        "workflow": "truerate-remittance-cost-audit",
        "step": "verify-provenance",
        "source_paths": [c["source_path"] for c in checks],
        "exists": all(c["source_present"] for c in checks),
        "parsed_ok": all(c["parsed_ok"] for c in checks),
        "approval_state": "not_required",  # read-only provenance check, no live/external action
        "checked_at": checked_at,
        "checks": checks,
    }

    import os
    os.makedirs("logs", exist_ok=True)
    log_path = f"logs/truerate-remittance-cost-audit-verify-provenance.json"
    with open(log_path, "w") as f:
        json.dump(result, f, indent=2)

    print(json.dumps(result, indent=2))
    if not (result["exists"] and result["parsed_ok"]):
        sys.exit(1)


if __name__ == "__main__":
    main()
