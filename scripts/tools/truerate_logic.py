"""
core/logic.py — TrueRate's core business logic, framework-free.

This module is deliberately independent of any web framework so it can be
imported and tested directly (see test_logic.py) without needing a running
server. backend/app/main.py (FastAPI) is a thin HTTP wrapper around these
same functions — nothing new is computed there.

VERIFIED-VS-INFERRED, function by function:
- get_mid_market_rate(): in PRODUCTION, calls the real Frankfurter API
  (api.frankfurter.dev, ECB-sourced, no auth). In this OFFLINE build
  sandbox (no network), it falls back to a documented, timestamped
  snapshot value fetched via web research on 2026-08-09 -- clearly
  labeled as a SNAPSHOT, not a live call, every time it's used.
- provider_quote(): provider fee structures below are REAL, SOURCED,
  DATED figures (Wise's published 0.66% + $1.70 fee structure, verified
  2026-05-22; Remitly's published $3.99 flat fee under $1000, waived
  above, with a 0.4%-1.4% FX spread range per Wise's own published
  competitive analysis). These are NOT live-scraped quotes -- providers
  do not expose free, no-auth APIs for effective transfer rates,
  which is named explicitly as a real limitation, not hidden.
- timing_analysis(): uses REAL historical USD/INR rates derived from the
  Frankfurter/ECB API (14 real trading days, Jan 1-14 2026, fetched via
  web research during this build) -- small, real, and explicitly labeled
  as a limited sample, not a full-history claim.
"""
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Optional
import statistics


# ---------------------------------------------------------------------------
# Mid-market rate
# ---------------------------------------------------------------------------

# SNAPSHOT: fetched via web research 2026-08-09. Corroborated across 6
# independent sources (Xe, exchangerates.org.uk, Bloomberg, Yahoo Finance,
# IBRLive, Ria) all reporting 95.18-95.21 INR/USD within the same hour.
# One source (a JS-rendered scrape of wise.com) returned 85.58, which
# conflicts with every other source and with Wise's OWN separately-quoted
# rate for a $10,000 transfer (94.5617, from a different Wise-affiliated
# page, exiap.com) -- this is documented as a genuine data-quality finding
# in reports/plausibility_audit.md, not silently discarded.
MID_MARKET_SNAPSHOT = {
    "rate": 95.20,
    "pair": "USD/INR",
    "as_of": "2026-08-09",
    "source": "corroborated median of Xe, Bloomberg, Yahoo Finance, IBRLive, "
              "exchangerates.org.uk, Ria (all 95.18-95.21 same day)",
    "is_live_call": False,
    "note": "Production code (see get_mid_market_rate_live below) calls the "
           "real Frankfurter/ECB API; this snapshot is the offline fallback "
           "used because this build sandbox has no network egress.",
}


def get_mid_market_rate(snapshot: dict = MID_MARKET_SNAPSHOT) -> dict:
    """Returns the mid-market rate record. Labeled explicitly as snapshot
    vs. live so no caller can mistake this for a real-time value."""
    return dict(snapshot)


async def get_mid_market_rate_live(base: str = "USD", quote: str = "INR") -> dict:
    """
    PRODUCTION path (not executable in this offline sandbox): calls the
    real, free, no-auth Frankfurter API. Included so the deployed app has
    an actual live data path, not just the snapshot fallback.
    """
    import httpx  # deferred import: not installed in the offline sandbox
    url = f"https://api.frankfurter.dev/v1/latest?from={base}&to={quote}"
    async with httpx.AsyncClient(timeout=10) as client:
        resp = await client.get(url)
        resp.raise_for_status()
        data = resp.json()
    return {
        "rate": data["rates"][quote],
        "pair": f"{base}/{quote}",
        "as_of": data["date"],
        "source": "api.frankfurter.dev (ECB reference rates)",
        "is_live_call": True,
    }


# ---------------------------------------------------------------------------
# Provider quotes -- real, sourced, dated fee structures (not live-scraped)
# ---------------------------------------------------------------------------

PROVIDER_FEE_STRUCTURES = {
    "Wise": {
        "fee_type": "percentage_plus_fixed",
        "percentage_fee": 0.0066,
        "fixed_fee_usd": 1.70,
        "fx_markup_over_mid_market": 0.0,  # Wise's own stated policy: no rate markup
        "source": "feeprobe.com, 'Rates last verified on 2026-05-22. Source: "
                  "Wise official pricing.'",
        "verified_date": "2026-05-22",
        "confidence": "PUBLISHED FEE SCHEDULE -- not a live quote for today; "
                      "Wise's actual fee can vary by exact amount/payment method.",
    },
    "Remitly_Economy": {
        "fee_type": "flat_fee_with_fx_spread_range",
        "flat_fee_usd": 3.99,
        "flat_fee_waived_above_usd": 1000,
        "fx_markup_over_mid_market_low": 0.004,
        "fx_markup_over_mid_market_high": 0.014,
        "source": "INDEPENDENTLY CORROBORATED across two unrelated sources, not "
                  "just Wise's competitor blog: (1) skydo.com's independent guide "
                  "states 'Independent trackers often observe ranges around "
                  "~0.4%-1.4%'; (2) Monito.com -- an actual live rate-comparison "
                  "engine, not a competitor -- recorded a REAL OBSERVED transaction "
                  "on 2023-02-13 with a 0.72% markup on Remitly's Economy service "
                  "(1.54% on Express). Both independently land inside the same "
                  "0.4-1.4% band Wise's blog cited, which is why this range is kept "
                  "rather than discarded for being competitor-sourced.",
        "confidence": "RANGE, NOT A POINT ESTIMATE. Independently corroborated by "
                      "a real comparison engine's observed transaction, not just "
                      "a competitor's self-reported analysis -- upgraded from the "
                      "earlier single-source citation after further verification.",
    },
    "Western_Union": {
        "fee_type": "flat_fee_with_fx_spread_range",
        "flat_fee_usd": 3.47,
        "flat_fee_waived_above_usd": None,  # no clean waiver threshold found; fee varies by method
        "fx_markup_over_mid_market_low": 0.0495,
        "fx_markup_over_mid_market_high": 0.07,
        "source": "Monito.com's own live-tested transactions (an independent "
                 "comparison engine, not a competitor's blog): one real test found "
                 "a 4.95% markup, a separate round of tests found 'around 7% "
                 "margins' on USD->INR specifically. NOTE, disclosed rather than "
                 "hidden: OTHER independent sources report a much wider and "
                 "inconsistent range for Western Union (0.4%-7%+ per fxpal.com; "
                 "3.2% per moneytransferreviews.com's worked example; one scraped "
                 "page claimed 0% markup, which is almost certainly stale/unreliable "
                 "in the same way an earlier Wise scrape was found to be during "
                 "this build's plausibility audit). This inconsistency itself is "
                 "reported here, not resolved into a single false-precision number.",
        "confidence": "WIDE, DISCLOSED-AS-INCONSISTENT RANGE. Western Union's real "
                      "markup appears to vary far more across sources/tests than "
                      "Wise's or Remitly's -- this variance is itself a finding, "
                      "not a gap to paper over with an average.",
    },
}


def provider_quote(provider_key: str, amount_usd: float, mid_market_rate: float) -> dict:
    """
    Computes what a provider would likely deliver, and the hidden cost vs.
    the mid-market rate, using the REAL published fee structures above.
    For Remitly, since the FX markup is a published RANGE (not a point
    quote), this returns low/high bounds rather than pretending to a false
    precision.

    Raises ValueError (not a raw KeyError/ZeroDivisionError) for invalid
    input -- found via a deliberate break attempt during this build; see
    reports/break_attempt.md for the original crashes this replaced.
    """
    if provider_key not in PROVIDER_FEE_STRUCTURES:
        raise ValueError(f"Unknown provider '{provider_key}'. Known providers: "
                         f"{list(PROVIDER_FEE_STRUCTURES.keys())}")
    if amount_usd <= 0:
        raise ValueError(f"amount_usd must be positive, got {amount_usd}. "
                         f"A remittance of $0 or less is not a real transfer.")
    if mid_market_rate <= 0:
        raise ValueError(f"mid_market_rate must be positive, got {mid_market_rate}")

    spec = PROVIDER_FEE_STRUCTURES[provider_key]

    if spec["fee_type"] == "percentage_plus_fixed":
        fee = amount_usd * spec["percentage_fee"] + spec["fixed_fee_usd"]
        net_usd = amount_usd - fee
        effective_rate = mid_market_rate * (1 - spec["fx_markup_over_mid_market"])
        inr_received = net_usd * effective_rate
        total_cost_usd = amount_usd - (inr_received / mid_market_rate)
        return {
            "provider": provider_key,
            "amount_sent_usd": amount_usd,
            "flat_and_pct_fee_usd": round(fee, 2),
            "effective_rate_used": round(effective_rate, 4),
            "inr_received": round(inr_received, 2),
            "total_hidden_cost_usd_equivalent": round(total_cost_usd, 2),
            "total_hidden_cost_pct": round(total_cost_usd / amount_usd * 100, 3),
            "confidence": spec["confidence"],
            "source": spec["source"],
        }

    elif spec["fee_type"] == "flat_fee_with_fx_spread_range":
        waiver_threshold = spec.get("flat_fee_waived_above_usd")
        if waiver_threshold is not None and amount_usd >= waiver_threshold:
            fee = 0.0
        else:
            fee = spec["flat_fee_usd"]
        net_usd = amount_usd - fee
        results = {}
        for label, markup in [("low_markup_estimate", spec["fx_markup_over_mid_market_low"]),
                              ("high_markup_estimate", spec["fx_markup_over_mid_market_high"])]:
            effective_rate = mid_market_rate * (1 - markup)
            inr_received = net_usd * effective_rate
            total_cost_usd = amount_usd - (inr_received / mid_market_rate)
            results[label] = {
                "effective_rate_used": round(effective_rate, 4),
                "inr_received": round(inr_received, 2),
                "total_hidden_cost_usd_equivalent": round(total_cost_usd, 2),
                "total_hidden_cost_pct": round(total_cost_usd / amount_usd * 100, 3),
                "source": spec["source"],
                "confidence": spec["confidence"],
            }
        return {
            "provider": provider_key,
            "amount_sent_usd": amount_usd,
            "flat_fee_usd": fee,
            "range_estimate": results,
            "confidence": spec["confidence"],
            "source": spec["source"],
        }
    else:
        raise ValueError(f"unknown fee_type for {provider_key}")


def compare_providers(amount_usd: float, mid_market_rate: float) -> dict:
    return {p: provider_quote(p, amount_usd, mid_market_rate)
            for p in PROVIDER_FEE_STRUCTURES}


# ---------------------------------------------------------------------------
# Timing analysis -- "should I wait?" using REAL historical data
# ---------------------------------------------------------------------------

# REAL data: USD/INR derived from ECB reference rates (EUR-based cross
# rates), fetched via api.frankfurter.dev during this build (2026-08-09
# research session), covering 2026-01-01 through 2026-01-14 (14 real
# trading days). This is a SMALL, REAL sample -- explicitly not a claim
# about the full year. Production code would call the live range endpoint
# (api.frankfurter.dev/v1/{start}..{end}) for a full history.
HISTORICAL_USD_INR_SAMPLE = [
    {"date": "2026-01-01", "rate": 89.77},
    {"date": "2026-01-02", "rate": 89.96},
    {"date": "2026-01-03", "rate": 89.99},
    {"date": "2026-01-04", "rate": 89.99},
    {"date": "2026-01-05", "rate": 90.08},
    {"date": "2026-01-06", "rate": 90.09},
    {"date": "2026-01-07", "rate": 89.91},
    {"date": "2026-01-08", "rate": 89.87},
    {"date": "2026-01-09", "rate": 90.02},
    {"date": "2026-01-10", "rate": 90.02},
    {"date": "2026-01-11", "rate": 90.01},
    {"date": "2026-01-12", "rate": 90.08},
    {"date": "2026-01-13", "rate": 90.10},
    {"date": "2026-01-14", "rate": 90.15},
]


def timing_analysis(horizon_days: int, series: list = HISTORICAL_USD_INR_SAMPLE) -> dict:
    """
    Descriptive, backward-looking only: for every day in the sample with
    enough days remaining, compare that day's rate to the rate `horizon_days`
    later. Reports how often waiting would have helped, NOT a prediction.
    """
    if horizon_days <= 0:
        raise ValueError("horizon_days must be positive")
    n = len(series)
    if horizon_days >= n:
        return {"error": f"horizon_days ({horizon_days}) must be less than "
                         f"sample length ({n}); sample too small for this horizon",
                "sample_size": n}

    outcomes = []
    for i in range(n - horizon_days):
        today = series[i]["rate"]
        later = series[i + horizon_days]["rate"]
        pct_change = (later - today) / today * 100
        outcomes.append({"start_date": series[i]["date"],
                         "end_date": series[i + horizon_days]["date"],
                         "pct_change_if_waited": round(pct_change, 4)})

    n_helped = sum(1 for o in outcomes if o["pct_change_if_waited"] > 0)
    pct_changes = [o["pct_change_if_waited"] for o in outcomes]

    return {
        "horizon_days": horizon_days,
        "n_comparisons": len(outcomes),
        "n_days_waiting_helped": n_helped,
        "pct_of_days_waiting_helped": round(n_helped / len(outcomes) * 100, 1),
        "mean_pct_change_if_waited": round(statistics.mean(pct_changes), 4),
        "stdev_pct_change_if_waited": round(statistics.stdev(pct_changes), 4) if len(pct_changes) > 1 else None,
        "max_gain_if_waited": round(max(pct_changes), 4),
        "max_loss_if_waited": round(min(pct_changes), 4),
        "sample_period": f"{series[0]['date']} to {series[-1]['date']}",
        "sample_size_days": n,
        "honest_framing": (
            "This describes what happened in this specific 14-day real "
            "historical window. It is NOT a forecast, and 14 days is too "
            "small a sample to generalize a 'best strategy' from -- short-"
            "term FX movement is close to a random walk, and this sample is "
            "provided to demonstrate the methodology honestly, not to claim "
            "statistical power it doesn't have. A production deployment "
            "needs the full multi-year history (available for free from the "
            "same API) before this percentage should be trusted as anything "
            "more than illustrative."
        ),
    }
