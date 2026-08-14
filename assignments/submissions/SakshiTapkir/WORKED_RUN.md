# Worked Run — Gate-Behavior Unit-Test Harness

**Student:** Sakshi Tapkir  
**Date:** 2026-08-14  
**Mode:** `recipes/gate-behavior-harness.md` v0.3.0  
**Lifecycle:** `RUNNABLE-SAMPLE`

## Scenario and Inputs
I tested the mode against a realistic repository scenario: after making the existing Bayesian Role Scorer importable for unit testing, verify that its `liveness` and `timeline` factors still behave as gates rather than ordinary votes.

Inputs:
- `data/examples/ch11-roles.json` — existing repository fixture containing the `ghost-posting` example. This was reused rather than invented for the test.
- `data/examples/gate-harness-timeline-test.json` — explicitly synthetic fixture used to isolate near-zero and exact-zero timeline behavior. It is labeled synthetic in the file.
- `scripts/score/BROKEN-scorer-for-harness-selftest.mjs` — deliberately broken negative-control implementation used only to prove the harness detects the target bug.

No private résumé, contact, application-tracker, or personal employer data is used.

## Commands and Real Terminal Output

### 1. Environment check
```text
$ node --version
v20.20.0
```

### 2. Main harness
```text
$ node scripts/score/gate-behavior-harness.mjs
=== Part 1: real role-scorer.mjs (expected: all PASS) ===

PASS  liveness gate zeroes composite despite high sponsorship (0.9) and fit (0.8)  -- composite=0
PASS  liveness-gated role is classified Skip, not Apply/Consider  -- recommendation=Skip
PASS  the Skip reason names the closed gate, not a low vote score  -- reason="gated: liveness ≈ 0.000 (a closed gate zeroes the composite regardless of votes)"
PASS  near-zero (but nonzero) timeline is still classified Skip, not rescued by high sponsorship/fit  -- recommendation=Skip, composite=0.0114
PASS  the Skip is forced by the explicit gate check, not incidental low vote math  -- reason="gated: timeline ≈ 0.020 (a closed gate zeroes the composite regardless of votes)"
PASS  exact-zero timeline (the multiplicative case) does zero the composite exactly  -- composite=0

=== Part 2: deliberately BROKEN gate-as-vote scorer (expected: FAIL) ===

FAIL  [SELF-TEST] broken scorer: does liveness=0 still zero the composite?  -- composite=0.6825 -- a nonzero value here means the harness correctly caught the gate-as-vote bug (this SHOULD fail)
FAIL  [SELF-TEST] broken scorer: is the ghost posting classified Skip?  -- recommendation=Apply -- if this is Apply/Consider, the harness correctly caught a ghost posting slipping through (this SHOULD fail)
FAIL  [SELF-TEST] broken scorer: does timeline~0 still zero the composite?  -- composite=0.773 -- a nonzero value here means the harness correctly caught the gate-as-vote bug (this SHOULD fail)

=== Summary ===
Part 1 (real scorer):    6/6 passed (correct -- real scorer behaves as a gate)
Part 2 (broken scorer):  3/3 correctly failed (correct -- harness caught the gate-as-vote bug)

Harness self-test: VALID -- passes on correct code, fails on the target bug
```

### 3. Deliberate broken-scorer invocation
```text
$ node scripts/score/gate-behavior-harness.mjs \
  --scorer scripts/score/BROKEN-scorer-for-harness-selftest.mjs
=== Part 1: real role-scorer.mjs (expected: all PASS) ===

PASS  liveness gate zeroes composite despite high sponsorship (0.9) and fit (0.8)  -- composite=0
PASS  liveness-gated role is classified Skip, not Apply/Consider  -- recommendation=Skip
PASS  the Skip reason names the closed gate, not a low vote score  -- reason="gated: liveness ≈ 0.000 (a closed gate zeroes the composite regardless of votes)"
PASS  near-zero (but nonzero) timeline is still classified Skip, not rescued by high sponsorship/fit  -- recommendation=Skip, composite=0.0114
PASS  the Skip is forced by the explicit gate check, not incidental low vote math  -- reason="gated: timeline ≈ 0.020 (a closed gate zeroes the composite regardless of votes)"
PASS  exact-zero timeline (the multiplicative case) does zero the composite exactly  -- composite=0

=== Part 2: deliberately BROKEN gate-as-vote scorer (expected: FAIL) ===

FAIL  [SELF-TEST] broken scorer: does liveness=0 still zero the composite?  -- composite=0.6825 -- a nonzero value here means the harness correctly caught the gate-as-vote bug (this SHOULD fail)
FAIL  [SELF-TEST] broken scorer: is the ghost posting classified Skip?  -- recommendation=Apply -- if this is Apply/Consider, the harness correctly caught a ghost posting slipping through (this SHOULD fail)
FAIL  [SELF-TEST] broken scorer: does timeline~0 still zero the composite?  -- composite=0.773 -- a nonzero value here means the harness correctly caught the gate-as-vote bug (this SHOULD fail)

=== Summary ===
Part 1 (real scorer):    6/6 passed (correct -- real scorer behaves as a gate)
Part 2 (broken scorer):  3/3 correctly failed (correct -- harness caught the gate-as-vote bug)

Harness self-test: VALID -- passes on correct code, fails on the target bug
```

### 4. Stored evidence writer
```text
$ node scripts/score/gate-behavior-harness-report.mjs
Verdict: VALID
Wrote reports/generated/gate-behavior-harness-2026-08-14.md
Wrote logs/gate-behavior-harness-2026-08-14.json
```

## Verified vs. Inferred
| Item | Classification | Basis |
|---|---|---|
| Real scorer passed 6/6 assertions | **Verified** | Deterministic terminal output from `gate-behavior-harness.mjs`. |
| `liveness=0` produced `composite=0` | **Verified** | Direct assertion observation from the production scorer. |
| Ghost posting recommendation was `Skip` | **Verified** | Direct scorer output. |
| Near-zero timeline (`0.02`) forced `Skip` | **Verified** | Direct scorer output and reason string. |
| Exact-zero timeline produced `composite=0` | **Verified** | Direct scorer output. |
| Broken scorer produced `Apply` for the ghost posting | **Verified** | Deliberate negative-control output. |
| Harness detects the implemented gate-as-vote defect | **Verified within tested scope** | All 3 negative-control assertions failed as intended. |
| Markdown and JSON evidence were created | **Verified** | Report-writer terminal output and included generated files. |
| Six assertions cover every possible future gate regression | **Not verified / inferred if claimed** | The test suite covers only the named cases and current entry point. |
| A particular real posting is live | **Not verified** | This mode does not query ATS/liveness data. |
| A particular student's visa timeline is feasible | **Not verified** | This mode is not a timeline adjudicator or immigration counsel. |
| Current weights/thresholds are optimal | **Not verified** | The harness tests behavior against the current contract, not policy optimality. |

## Verification and Deliberate Break Attempt
I did not accept a green run as sufficient evidence. The harness contains a negative control: `BROKEN-scorer-for-harness-selftest.mjs` intentionally implements the gate-as-vote defect. A ghost posting then receives `composite=0.6825` and `recommendation=Apply`, while the near-zero timeline case receives `composite=0.773`. The harness flags all three conditions as failures and summarizes them as `3/3 correctly failed`. This demonstrates that the test can reject the named defect rather than merely agreeing with the current implementation.

I also used the report writer and checked that it produced two separate evidence artifacts: `reports/generated/gate-behavior-harness-2026-08-14.md` and `logs/gate-behavior-harness-2026-08-14.json`.

## Reflection
### What went well
The final harness is deterministic, fast, and grounded in the real scorer. The strongest part is the negative control: passing the production scorer is useful, but proving that the exact broken implementation fails makes the evidence much stronger. The stored-output writer also gives separate artifacts for a human reviewer and an agent/log consumer.

### What the mode got wrong or missed during development
The first version of my test made an incorrect assumption: I expected a near-zero-but-nonzero timeline factor (`0.02`) to make the raw composite exactly zero. Re-reading the scorer contract showed that the explicit threshold forces `Skip`, while the multiplicative composite reaches exact zero only when the factor itself is zero. I changed the assertion to test the real guarantee instead of preserving my assumption.

The integration also exposed four issues that had to be fixed before the harness was trustworthy: the scorer exported nothing, importing it executed its CLI, my first entry-point guard failed for paths containing a space, and the companion `.card.md` initially lacked lifecycle frontmatter expected by the repository checks.

### Next steps
Add boundary tests at exactly the gate threshold, a case with both gates closed simultaneously, and regression coverage for any future scorer entry points. A future live run could also pair the harness with verified Job-Ops liveness evidence; until then, the correct lifecycle remains `RUNNABLE-SAMPLE`, not `VERIFIED`.

## Attestation
- **Recipe:** `gate-behavior-harness` v0.3.0
- **By:** Sakshi Tapkir · 2026-08-14

### Tested
| Ran | Saw | Expected |
|---|---|---|
| `node --version` | `v20.20.0` | Supported Node runtime available. |
| `node scripts/score/gate-behavior-harness.mjs` | Real scorer `6/6 passed`; broken scorer `3/3 correctly failed`; `VALID` | Correct scorer passes and target bug is rejected. |
| Deliberate broken-scorer self-test | Ghost posting became `Apply`; bad composites `0.6825` and `0.773`; assertions failed | Harness should catch the gate-as-vote defect. |
| `node scripts/score/gate-behavior-harness-report.mjs` | `Verdict: VALID`; Markdown + JSON written | Stored evidence artifacts are produced. |

### Did not test
- A live ATS posting through `npm run ats:liveness` as part of this mode.
- A real student's private visa/application timeline.
- Every possible future scorer refactor or caller.
- Boundary cases exactly at the gate threshold or both gates closed simultaneously.

### Broke during testing, fixed
- `role-scorer.mjs` originally exported no scorer functions; added exports and regression-checked the CLI behavior.
- Importing the scorer originally executed `main()`; added an entry-point guard.
- The first guard failed for a repository path containing a space; replaced it with an absolute decoded path comparison using `fileURLToPath()` and `path.resolve()`.
- The companion `.card.md` initially failed lifecycle/frontmatter checks; matching lifecycle metadata was added.
- An early test incorrectly required a near-zero timeline to make the raw composite exactly zero; corrected the assertion to match the actual threshold contract.
