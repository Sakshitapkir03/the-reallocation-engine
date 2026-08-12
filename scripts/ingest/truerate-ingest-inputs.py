#!/usr/bin/env python3
"""
scripts/ingest/truerate-ingest-inputs.py

Step 2 of the truerate-remittance-cost-audit recipe. Reads the declared
run inputs (amount_usd, providers to compare, timing horizon_days) from a
run envelope JSON, validates presence, and writes a raw record to
data/raw/truerate-remittance-cost-audit/.

Usage:
    python3 scripts/ingest/truerate-ingest-inputs.py <path-to-run-envelope.json>
"""
import json
import sys
import os
from datetime import datetime, timezone

REQUIRED_FIELDS = ["amount_usd", "providers", "horizon_days"]


def main():
    if len(sys.argv) < 2:
        print(json.dumps({"error": "usage: ingest-inputs.py <run-envelope.json>"}))
        sys.exit(1)

    envelope_path = sys.argv[1]
    with open(envelope_path) as f:
        envelope = json.load(f)

    rejects = []
    for field in REQUIRED_FIELDS:
        if field not in envelope:
            rejects.append({"field": field, "reason": "missing required field"})

    record = {
        "records": [envelope] if not rejects else [],
        "source_name": os.path.basename(envelope_path),
        "source_type": "student run envelope",
        "fetched_at": datetime.now(timezone.utc).isoformat(),
        "sample_mode": envelope.get("sample_mode", True),
        "rejects": rejects,
    }

    os.makedirs("data/raw/truerate-remittance-cost-audit", exist_ok=True)
    out_path = "data/raw/truerate-remittance-cost-audit/ingested-inputs.json"
    with open(out_path, "w") as f:
        json.dump(record, f, indent=2)

    print(json.dumps(record, indent=2))
    if rejects:
        sys.exit(1)


if __name__ == "__main__":
    main()
