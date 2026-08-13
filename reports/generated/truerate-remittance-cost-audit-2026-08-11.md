# TrueRate Remittance Cost Audit — 2026-08-11

## Run Summary
Compared ['Wise', 'Remitly_Economy'] against the mid-market rate for a $1000 transfer.

## Purpose
Shows the real mid-market USD/INR rate against what each provider would likely deliver, and whether waiting has historically helped.

## Source Inventory
- `reports/generated/truerate-plausibility-audit.md`
- `inline citation in scripts/tools/truerate_logic.py`
- `inline citation in scripts/tools/truerate_logic.py`
- `derived from api.frankfurter.dev during build; see truerate-plausibility-audit.md`

## Phase-Gate Results
- Provenance gate: PASS
- Data-shape gate: PASS (see data/verified/.../data-shape-check.json)
- Quality-check gate: 0 provider(s) rejected, 1 flag(s) raised

## Records Seen / Rejects / Flags
- Verified providers: ['Wise', 'Remitly_Economy']
- Rejects: none
- Flags: ["mid_market_rate snapshot is 2 day(s) old (as_of=2026-08-09) -- treat as potentially stale; this recipe has NOT yet implemented an automatic staleness block (see the recipe's Stop Conditions)"]

## Verified Findings
- Mid-market rate: **95.2 USD/INR**, as_of 2026-08-09 (corroborated median of Xe, Bloomberg, Yahoo Finance, IBRLive, exchangerates.org.uk, Ria (all 95.18-95.21 same day))
- **Wise**: estimated hidden cost 0.83% (PUBLISHED FEE SCHEDULE -- not a live quote for today; Wise's actual fee can vary by exact amount/payment method.)
- **Remitly_Economy**: estimated hidden cost 0.4%–1.4% (range, RANGE, NOT A POINT ESTIMATE -- and sourced from a competitor's analysis of Remitly, not Remitly's own disclosure, which is a real conflict-of-interest caveat named explicitly, not hidden.)

## Inferred Findings
- Timing (backward-looking, 14-day real sample): waiting 7 days helped in 85.7% of cases in this window. This describes what happened in this specific 14-day real historical window. It is NOT a forecast, and 14 days is too small a sample to generalize a 'best strategy' from -- short-term FX movement is close to a random walk, and this sample is provided to demonstrate the methodology honestly, not to claim statistical power it doesn't have. A production deployment needs the full multi-year history (available for free from the same API) before this percentage should be trusted as anything more than illustrative.

## Decision Recommendation
This report identifies the cheaper published-fee-schedule provider for this specific amount. It does NOT recommend a real-time provider choice without a human confirming the quote in that provider's own app first, and does NOT recommend a waiting strategy based on a 14-day sample. Human decision required before acting on either.