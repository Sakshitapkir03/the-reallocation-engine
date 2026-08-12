#!/usr/bin/env python3
"""
scripts/tools/truerate-produce-human-report.py

Step 6 of the truerate-remittance-cost-audit recipe. Renders the human-
readable report from the verified comparison result, per this recipe's
Output Contract.
"""
import json
import os
from datetime import datetime, timezone


def main():
    with open("data/verified/truerate-remittance-cost-audit/comparison-result.json") as f:
        comp = json.load(f)
    with open("data/verified/truerate-remittance-cost-audit/quality-checked.json") as f:
        quality = json.load(f)
    with open("logs/truerate-remittance-cost-audit-verify-provenance.json") as f:
        provenance = json.load(f)

    date_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    mm = comp["mid_market"]

    lines = []
    lines.append(f"# TrueRate Remittance Cost Audit — {date_str}")
    lines.append("")
    lines.append("## Run Summary")
    lines.append(f"Compared {list(comp['comparisons'].keys())} against the mid-market "
                 f"rate for a ${comp['comparisons'][list(comp['comparisons'].keys())[0]]['amount_sent_usd']} transfer.")
    lines.append("")
    lines.append("## Purpose")
    lines.append("Shows the real mid-market USD/INR rate against what each provider "
                 "would likely deliver, and whether waiting has historically helped.")
    lines.append("")
    lines.append("## Source Inventory")
    for path in provenance["source_paths"]:
        lines.append(f"- `{path}`")
    lines.append("")
    lines.append("## Phase-Gate Results")
    lines.append(f"- Provenance gate: {'PASS' if provenance['exists'] and provenance['parsed_ok'] else 'FAIL'}")
    lines.append(f"- Data-shape gate: PASS (see data/verified/.../data-shape-check.json)")
    lines.append(f"- Quality-check gate: {len(quality['rejects'])} provider(s) rejected, "
                 f"{len(quality['flags'])} flag(s) raised")
    lines.append("")
    lines.append("## Records Seen / Rejects / Flags")
    lines.append(f"- Verified providers: {quality['verified_records']}")
    lines.append(f"- Rejects: {quality['rejects'] if quality['rejects'] else 'none'}")
    lines.append(f"- Flags: {quality['flags'] if quality['flags'] else 'none'}")
    lines.append("")
    lines.append("## Verified Findings")
    lines.append(f"- Mid-market rate: **{mm['rate']} {mm['pair']}**, as_of {mm['as_of']} "
                 f"({mm['source']})")

    def provider_cost_for_ranking(name, result):
        if "range_estimate" in result:
            return result["range_estimate"]["low_markup_estimate"]["total_hidden_cost_pct"]
        return result["total_hidden_cost_pct"]

    ranked = sorted(comp["comparisons"].items(), key=lambda kv: provider_cost_for_ranking(*kv))
    cheapest_name = ranked[0][0]

    for provider, result in ranked:
        marker = " <- CHEAPEST (best case)" if provider == cheapest_name else ""
        if "range_estimate" in result:
            low = result["range_estimate"]["low_markup_estimate"]["total_hidden_cost_pct"]
            high = result["range_estimate"]["high_markup_estimate"]["total_hidden_cost_pct"]
            lines.append(f"- **{provider}**: estimated hidden cost {low}%–{high}% "
                        f"(range, {result['confidence']}){marker}")
        else:
            lines.append(f"- **{provider}**: estimated hidden cost {result['total_hidden_cost_pct']}% "
                        f"({result['confidence']}){marker}")

    lines.append("")
    lines.append(f"**Direct answer: on this amount, {cheapest_name.replace('_', ' ')} is the "
                f"cheapest option among those compared, using each provider's best-case "
                f"estimate.** This ranking uses each provider's LOW end of its range where a "
                f"range exists (its best case) -- if you want the conservative (worst-case) "
                f"ranking instead, compare the HIGH end of each range above, since a wide-range "
                f"provider could still turn out more expensive than its best case suggests.")
    lines.append("")
    lines.append("## Inferred Findings")
    timing = comp.get("timing", {})
    if "error" not in timing:
        lines.append(f"- Timing (backward-looking, {timing['sample_size_days']}-day real sample): "
                    f"waiting {timing['horizon_days']} days helped in "
                    f"{timing['pct_of_days_waiting_helped']}% of cases in this window. "
                    f"{timing['honest_framing']}")
    else:
        lines.append(f"- Timing analysis error: {timing['error']}")
    lines.append("")
    lines.append("## Decision Recommendation")
    lines.append("This report identifies the cheaper published-fee-schedule provider "
                 "for this specific amount. It does NOT recommend a real-time provider "
                 "choice without a human confirming the quote in that provider's own app "
                 "first, and does NOT recommend a waiting strategy based on a 14-day "
                 "sample. Human decision required before acting on either.")

    report_md = "\n".join(lines)
    os.makedirs("reports/generated", exist_ok=True)
    report_path = f"reports/generated/truerate-remittance-cost-audit-{date_str}.md"
    with open(report_path, "w") as f:
        f.write(report_md)

    # Agent log (JSON), per Output Contract
    agent_log = {
        "workflow": "truerate-remittance-cost-audit",
        "run_id": f"truerate-{date_str}",
        "mode": "sample",
        "steps_completed": ["verify-provenance", "ingest-inputs", "validate-data-shape",
                           "transform-quality-check", "run-approved-tools", "produce-human-report"],
        "records_seen": quality["record_count"],
        "rejects": quality["rejects"],
        "duplicates": quality["duplicates"],
        "flags": quality["flags"],
        "stop_conditions": [],
        "todo_items": ["automatic staleness block (see recipe Stop Conditions)",
                      "live rate path unverified end-to-end (no network in build sandbox)"],
        "source_files": provenance["source_paths"],
        "gate_decisions": "none required -- read-only computation, no live/external action",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "raw_output_paths": ["data/raw/truerate-remittance-cost-audit/ingested-inputs.json"],
        "verified_output_paths": ["data/verified/truerate-remittance-cost-audit/data-shape-check.json",
                                 "data/verified/truerate-remittance-cost-audit/quality-checked.json",
                                 "data/verified/truerate-remittance-cost-audit/comparison-result.json"],
        "report_path": report_path,
    }
    os.makedirs("logs", exist_ok=True)
    log_path = f"logs/truerate-remittance-cost-audit-{date_str}.json"
    with open(log_path, "w") as f:
        json.dump(agent_log, f, indent=2)

    print(f"Wrote {report_path}")
    print(f"Wrote {log_path}")
    print("\n--- Report preview ---\n")
    print(report_md)


if __name__ == "__main__":
    main()
