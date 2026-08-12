# Plausibility Audit

Before trusting any fetched number, it was sanity-checked against
independent sources. This is the audit trail, including the one real
discrepancy found.

## Mid-market rate cross-check (2026-08-09)

| Source | Reported USD/INR | Notes |
|---|---|---|
| Xe.com | 95.1961 | live-quoted |
| exchangerates.org.uk | 95.2105 | live-quoted |
| Bloomberg | 95.2075 | live-quoted, 08/07/26 timestamp |
| Yahoo Finance (INR=X) | 95.1980 | delayed quote, Aug 9 |
| IBRLive | 95.1810 | live-quoted |
| Ria Money Transfer | (mid-market ref only, no number captured) | — |
| **wise.com (fetched)** | **85.58** | **conflicts with every other source** |

Six independent sources cluster tightly at 95.18–95.21. The Wise figure is
~10% off from that cluster, and — separately — Wise's own fee-calculator
page (exiap.com, citing Wise) quoted a *different* number for a $10,000
transfer: 94.5617, from 2026, which is much closer to the corroborated
cluster than the 85.58 figure from the scraped wise.com page.

**Conclusion:** the 85.58 figure is treated as unreliable, most likely a
stale cached page returned by the scraping tool (the page's own metadata
was dated "May 30, 2026," while the other sources were dated to the
current day) rather than a real live rate. It was excluded, not averaged
in. This is exactly the kind of "ran, looked reasonable, and was wrong in
exactly the way fluency hides" failure the assignment asks builders to
catch — a scraped number that looks like a real quote but is actually
stale JS-rendered content.

**What this means for the rest of the project:** `MID_MARKET_SNAPSHOT` in
`logic.py` uses 95.20 (the corroborated median), not the Wise figure, and
this audit trail is the documented reason why.

## Provider fee-structure cross-check

Wise's fee structure (0.66% + $1.70) was corroborated across two
independent secondary sources (feeprobe.com and skydo.com both describe
Wise's USD-corridor pricing consistently, though skydo.com frames it as
"~2% effective cost" when including a $2 FIRA charge that only applies to
*business receiving* payments in India, not to a personal remittance send
— this is a real scope mismatch that was caught and excluded; the FIRA
charge does not apply to the person-to-person remittance use case this
project targets).
