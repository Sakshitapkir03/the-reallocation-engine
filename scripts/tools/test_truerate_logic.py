"""
test_truerate_logic.py — real, executable tests validating every step of
the TrueRate pipeline, run against the actual logic module.

Run: python3 scripts/tools/test_truerate_logic.py
"""
import sys
sys.path.insert(0, "scripts/tools")
from truerate_logic import (get_mid_market_rate, provider_quote, compare_providers,
                           timing_analysis, PROVIDER_FEE_STRUCTURES)


def test_mid_market_rate_is_labeled():
    mm = get_mid_market_rate()
    assert mm["is_live_call"] is False
    assert "source" in mm and len(mm["source"]) > 0
    assert 80 < mm["rate"] < 120


def test_all_three_providers_present():
    assert set(PROVIDER_FEE_STRUCTURES.keys()) == {"Wise", "Remitly_Economy", "Western_Union"}


def test_western_union_no_waiver_threshold_does_not_crash():
    """Regression test for the None-comparison bug found and fixed during
    this update -- Western Union has no waiver threshold at all."""
    mm = get_mid_market_rate()
    result = provider_quote("Western_Union", 1000, mm["rate"])
    assert result["flat_fee_usd"] == 3.47


def test_remitly_waiver_threshold_still_works():
    """Regression test confirming the fix to the None-comparison bug didn't
    break Remitly's existing (non-None) waiver threshold."""
    mm = get_mid_market_rate()
    below = provider_quote("Remitly_Economy", 500, mm["rate"])
    above = provider_quote("Remitly_Economy", 1000, mm["rate"])
    assert below["flat_fee_usd"] == 3.99
    assert above["flat_fee_usd"] == 0.0


def test_western_union_is_worse_than_wise_and_remitly():
    """Sanity check against real-world reputation: WU should show up as
    meaningfully more expensive than Wise or Remitly's low estimate."""
    mm = get_mid_market_rate()
    comp = compare_providers(1000, mm["rate"])
    wu_low = comp["Western_Union"]["range_estimate"]["low_markup_estimate"]["total_hidden_cost_pct"]
    wise_cost = comp["Wise"]["total_hidden_cost_pct"]
    assert wu_low > wise_cost, "Western Union's cheapest estimate should still exceed Wise's cost"


def test_compare_providers_returns_all_three():
    mm = get_mid_market_rate()
    comp = compare_providers(1000, mm["rate"])
    assert set(comp.keys()) == {"Wise", "Remitly_Economy", "Western_Union"}


def test_unknown_provider_raises_clean_error():
    try:
        provider_quote("DefinitelyNotARealProvider", 1000, 95.2)
        assert False, "should have raised ValueError"
    except ValueError as e:
        assert "Unknown provider" in str(e)


def test_zero_and_negative_amounts_rejected():
    for bad_amount in [0, -1, -500]:
        try:
            provider_quote("Wise", bad_amount, 95.2)
            assert False, f"should have rejected amount={bad_amount}"
        except ValueError:
            pass


def test_timing_analysis_bounds_are_internally_consistent():
    result = timing_analysis(7)
    assert result["n_comparisons"] == 7
    assert result["max_loss_if_waited"] <= result["mean_pct_change_if_waited"] <= result["max_gain_if_waited"]
    assert 0 <= result["pct_of_days_waiting_helped"] <= 100


def test_timing_analysis_rejects_oversized_horizon():
    result = timing_analysis(999)
    assert "error" in result


def test_timing_analysis_rejects_zero_horizon():
    try:
        timing_analysis(0)
        assert False, "should have raised ValueError"
    except ValueError:
        pass


if __name__ == "__main__":
    tests = [v for k, v in list(globals().items()) if k.startswith("test_")]
    passed, failed = 0, 0
    for t in tests:
        try:
            t()
            print(f"PASS  {t.__name__}")
            passed += 1
        except AssertionError as e:
            print(f"FAIL  {t.__name__}: {e}")
            failed += 1
        except Exception as e:
            print(f"ERROR {t.__name__}: {type(e).__name__}: {e}")
            failed += 1
    print(f"\n{passed} passed, {failed} failed, {len(tests)} total")
    sys.exit(1 if failed else 0)
