# Gate-Behavior Harness Report — 2026-08-14

## Run Summary
Part 1 (real scorer): 6/6 passed. Part 2 (broken scorer self-test): 3/3 correctly failed. **Verdict: VALID**

## Part 1 — Real Scorer (expected: all PASS)
| Assertion | Result | Detail |
|---|---|---|
| liveness gate zeroes composite despite high sponsorship (0.9) and fit (0.8) | PASS | composite=0 |
| liveness-gated role is classified Skip | PASS | recommendation=Skip |
| Skip reason names the closed gate | PASS | reason="gated: liveness ≈ 0.000 (a closed gate zeroes the composite regardless of votes)" |
| near-zero timeline still classified Skip | PASS | recommendation=Skip, composite=0.0114 |
| Skip forced by explicit gate check | PASS | reason="gated: timeline ≈ 0.020 (a closed gate zeroes the composite regardless of votes)" |
| exact-zero timeline zeroes composite exactly | PASS | composite=0 |

## Part 2 — Deliberately Broken Scorer (expected: all FAIL)
| Assertion | Result | Detail |
|---|---|---|
| [SELF-TEST] broken scorer: liveness=0 zeroes composite? | FAIL (correct) | composite=0.6825 |
| [SELF-TEST] broken scorer: ghost posting classified Skip? | FAIL (correct) | recommendation=Apply |
| [SELF-TEST] broken scorer: timeline~0 zeroes composite? | FAIL (correct) | composite=0.773 |

## Verdict
**VALID** — the real scorer behaves as a gate, and this harness proved it can detect the specific gate-as-vote bug it targets.
