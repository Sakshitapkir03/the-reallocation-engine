# Honest Run — Gate-Behavior Unit-Test Harness

## Plausibility audit
Before trusting the harness's own verdict, I checked whether its fixtures
were themselves plausible: the `ghost-posting` role already exists,
unmodified, in the repo's own `data/examples/ch11-roles.json` — it isn't
something I invented to make the test easy. The synthetic timeline-gate
fixture is explicitly labeled `SYNTHETIC` and carries a `_note` field
explaining exactly why it was constructed, so nobody downstream mistakes
it for a real posting.

## Real terminal output (pasted, not described)

```
$ node scripts/score/role-scorer.mjs data/examples/ch11-roles.json --out-dir /tmp
✓ scored 5 roles → Apply 2 · Consider 1 · Skip 2 (skip 40%)

$ node scripts/score/gate-behavior-harness.mjs
=== Part 1: real role-scorer.mjs (expected: all PASS) ===

PASS  liveness gate zeroes composite despite high sponsorship (0.9) and fit (0.8)  -- composite=0
PASS  liveness-gated role is classified Skip, not Apply/Consider  -- recommendation=Skip
PASS  the Skip reason names the closed gate, not a low vote score  -- reason="gated: liveness ≈ 0.000 ..."
PASS  near-zero (but nonzero) timeline is still classified Skip, not rescued by high sponsorship/fit  -- recommendation=Skip, composite=0.0114
PASS  the Skip is forced by the explicit gate check, not incidental low vote math  -- reason="gated: timeline ≈ 0.020 ..."
PASS  exact-zero timeline (the multiplicative case) does zero the composite exactly  -- composite=0

=== Part 2: deliberately BROKEN gate-as-vote scorer (expected: FAIL) ===

FAIL  [SELF-TEST] broken scorer: does liveness=0 still zero the composite?  -- composite=0.6825
FAIL  [SELF-TEST] broken scorer: is the ghost posting classified Skip?  -- recommendation=Apply
FAIL  [SELF-TEST] broken scorer: does timeline~0 still zero the composite?  -- composite=0.773

=== Summary ===
Part 1 (real scorer):    6/6 passed (correct -- real scorer behaves as a gate)
Part 2 (broken scorer):  3/3 correctly failed (correct -- harness caught the gate-as-vote bug)

Harness self-test: VALID -- passes on correct code, fails on the target bug
```

## The deliberate break attempt
This harness's entire design *is* the break attempt the assignment asks
for: `BROKEN-scorer-for-harness-selftest.mjs` deliberately reimplements
the exact bug the capstone brief names ("the gate-as-vote bug") and proves
the harness catches it — a ghost posting (liveness=0) that the broken
scorer wrongly classifies **Apply** with a composite of 0.6825, when it
should be zeroed and Skipped. This is not a hypothetical risk: it is the
literal failure mode this harness exists to prevent, reproduced and shown
failing on purpose.

Beyond that designed break attempt, two *unplanned* real bugs surfaced
while building the harness itself, before any of the above output was
achievable:

1. **`role-scorer.mjs` exported nothing.** `scoreRole`, `applyProfile`,
   and `CONFIG` were only reachable via the CLI's `main()`. Fixed by
   adding three `export` keywords -- verified behavior-preserving by
   regression-checking the CLI's exact output against what's already on
   record in `logs/RUN_LOG.md` (2026-06-14 entry).
2. **`main()` had no entry-point guard.** Importing the file for testing
   also *ran* its CLI against the harness's own `process.argv`, printing
   a usage error and killing the process before any test executed. Fixed
   with the standard `import.meta.url === file://${process.argv[1]}`
   guard, then re-verified the CLI regression held.

A third, more interesting finding came from my own test being wrong, not
the code: an early assertion expected `composite === 0` for a near-zero
(0.02) timeline factor, and it failed. Investigating showed the code's
real contract is narrower than I'd assumed -- it forces the
*recommendation* to Skip via an explicit threshold check, but doesn't
force the *raw composite number* to exactly zero unless the gate factor
is literally `0`. Re-reading Chapter 11's own language confirmed this is
correct: it says liveness "approaching zero" makes the composite
"approach zero" -- not that it hits zero. I fixed the test to check the
actual guarantee, not my assumption about it.

## Metric readout
- **6/6** assertions pass against the real, unmodified-in-behavior scorer
- **3/3** assertions correctly fail against the deliberately-broken version
- **2** real bugs found and fixed in the process of making the code testable
- **1** incorrect assumption found and fixed in my own test

## What the machine could not know
- Whether `role-scorer.mjs`'s weights (0.35 sponsorship, 0.30 fit) are the
  *right* weights for any given student -- the harness proves the gate
  mechanism works as designed, not that the design's parameters are
  correct. That's a judgment the chapter itself defers to the reader.
- Whether some other, not-yet-written caller of `role-scorer.mjs`'s
  exports might reintroduce a gate-as-vote bug in a different way this
  harness doesn't check -- the harness tests the two named gates
  (liveness, timeline) via the one entry point (`scoreRole`) that
  currently exists; it doesn't prove no future refactor could break the
  guarantee.
- Whether a human reviewing this harness would agree that 6 assertions is
  sufficient coverage, or would want more edge cases (e.g. both gates
  closed simultaneously, a gate factor exactly at the 0.05 threshold
  boundary) -- that adequacy judgment is the human half of the
  verification stack this repo's own constitution describes, not
  something the harness can certify about itself.
