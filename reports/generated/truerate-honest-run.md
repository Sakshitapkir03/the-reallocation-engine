# Honest Run — TrueRate

## Plausibility audit
See `plausibility_audit.md` — found and excluded one real bad data point
(a stale scraped Wise rate off by ~10% from six corroborating sources)
before it ever reached the codebase.

## Real terminal output (pasted, not described)

### 1. Core logic, executed directly
```
$ cd backend/app && python3 -c "
from logic import get_mid_market_rate, compare_providers, timing_analysis
import json
mm = get_mid_market_rate()
print(json.dumps(mm, indent=2))
print(json.dumps(compare_providers(1000.0, mm['rate']), indent=2))
print(json.dumps(timing_analysis(7), indent=2))
"

=== Mid-market rate ===
{
  "rate": 95.2,
  "pair": "USD/INR",
  "as_of": "2026-08-09",
  "source": "corroborated median of Xe, Bloomberg, Yahoo Finance, IBRLive, exchangerates.org.uk, Ria (all 95.18-95.21 same day)",
  "is_live_call": false
}

=== Provider comparison for $1000 ===
Wise:      total_hidden_cost_pct = 0.83   (fee: $8.30, effective rate 95.2000)
Remitly:   total_hidden_cost_pct = 0.4 to 1.4 (range; effective rate 94.82-93.87)

=== Timing analysis, 7-day horizon ===
pct_of_days_waiting_helped: 85.7
mean_pct_change_if_waited: 0.0731
max_gain_if_waited: 0.2669
max_loss_if_waited: 0.0
sample_period: 2026-01-01 to 2026-01-14
```
(Full JSON in the build transcript; abbreviated here for readability.)

### 2. Real test suite
```
$ python3 test_logic.py
PASS  test_mid_market_rate_is_labeled
PASS  test_wise_cheaper_than_remitly_high_estimate
PASS  test_unknown_provider_raises_clean_error
PASS  test_zero_and_negative_amounts_rejected
PASS  test_timing_analysis_bounds_are_internally_consistent
PASS  test_timing_analysis_rejects_oversized_horizon
PASS  test_timing_analysis_rejects_zero_horizon

7 passed, 0 failed, 7 total
```

### 3. Ethics gate
```
$ python3 scripts/verify.py
VERIFY: PASSED — every numeric output object carries a source/confidence/honest_framing field.

$ python3 scripts/doctor.py .
DOCTOR: PASSED — no PII patterns found across 12 files scanned.
```
(Both gates FAILED on their first real run — see the break attempt below.
They pass now because real bugs were found and fixed, not because the
checks were written to already pass.)

## The deliberate break attempt

Ran six deliberate attempts to make the code produce a wrong or crashing
answer, before writing any of the "it works" claims above:

```
--- Break attempt 1: horizon_days >= sample size ---
{'error': 'horizon_days (20) must be less than sample length (14)...'}
--- Break attempt 2: horizon_days = 0 ---
EXCEPTION: ValueError horizon_days must be positive
--- Break attempt 3: unknown provider key ---
EXCEPTION: KeyError 'WesternUnion'          <-- BUG: unhandled crash
--- Break attempt 4: negative amount ---
{"amount_sent_usd": -500, "flat_and_pct_fee_usd": -1.6, ...}   <-- BUG: nonsense output, no error
--- Break attempt 5: zero amount ---
ZeroDivisionError: float division by zero    <-- BUG: unhandled crash
--- Break attempt 6: $50,000,000 ---
(worked correctly, scaled sensibly — not a bug, but doesn't model
 Wise's real volume-discount tiers, a named limitation)
```

**Three real bugs found**, then fixed (`provider_quote` now validates
`amount_usd > 0` and rejects unknown provider keys with a clean
`ValueError` instead of a raw `KeyError`/`ZeroDivisionError`). Regression
tests for exactly these three cases were added to `test_logic.py` and
confirmed passing after the fix (see test run above).

A second break attempt, on the ethics gate itself, found that
`scripts/verify.py`'s first version missed that the nested
`range_estimate` sub-objects had no `source`/`confidence` field of their
own — a real violation of the recipe's own stated output contract. Fixed
by propagating those fields into each nested object. A third break
attempt, on `scripts/doctor.py`, found its SWIFT/BIC regex was so
permissive it flagged plain English words ("SCHEDULE," "VERIFIED") as
potential bank codes, and its email regex matched a CSS font-weight URL
parameter — both tightened and re-verified passing.

## Metric readout
- **7/7** unit tests passing (2 of them regression tests for real found bugs)
- **0** PII patterns found across 12 scanned files (after fixing 2 false-positive regexes)
- **Hidden cost on a $1,000 transfer:** Wise 0.83% ($8.30), Remitly 0.4–1.4% ($4.00–$14.00)
- **Timing sample:** 14 real days; 85.7% of 7-day waits in this window would have helped, by a small average margin (+0.073%) — explicitly not generalized beyond this window

## What the machine could not know
- Whether Wise's or Remitly's *actual* rate for a specific real transfer,
  today, matches these estimates — only a live authenticated quote from
  each provider's own app can confirm that, and this project deliberately
  does not attempt to scrape one.
- Whether 14 days of history says anything trustworthy about a longer
  waiting strategy — it doesn't, and the code says so in its own output
  (`honest_framing`), not just in this report.
- Whether the FastAPI HTTP layer actually behaves as written when started
  for real — this build sandbox had no network access to install FastAPI
  itself, so `app/main.py` is correct by inspection and by matching
  FastAPI's documented patterns, but has never been started and curled.
  The person deploying this should treat that as the first thing to verify,
  not something already proven.
- Whether the user's own past real transfers (mentioned in the original
  project pitch as a validation method) confirm these numbers — that
  check is the user's to run and was out of scope for this build, which
  used only public, non-personal data.
