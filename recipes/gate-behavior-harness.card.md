---
status: RUNNABLE-SAMPLE
todos_open: 0
last_gate: "sample-run, 2026-08-14, logs/RUN_LOG.md#2026-08-14"
attestation: null
recipe_version: 0.3.0
---

# Gate-Behavior Unit-Test Harness — Human Card

*Companion file: `gate-behavior-harness.md` (the AI-facing recipe). Update
both in the same commit.*

## Purpose
Tells you whether `role-scorer.mjs`'s liveness and timeline factors are
actually acting as hard gates — zeroing a role's score no matter how
strong sponsorship and fit are — or have quietly degraded into ordinary
weighted votes. That distinction matters because a ghost posting or an
impossible start date should never be rescued by a high fit score; if the
gate silently became a vote, a student could burn real application effort
on a role that was never real, while the tool still hands them a
confident "Apply."

## What it can verify
- Whether the real scorer's liveness/timeline factors mathematically
  zero the composite (exact-zero case) or force the recommendation to
  Skip via an explicit threshold check (near-zero case) — both tested
  directly, not inferred.
- Whether a known-broken implementation of the same contract is correctly
  rejected by this harness's own assertions (the self-test).
- Whether the CLI's pre-existing, documented output is unchanged after
  the export/guard fixes this contribution required.

## What it cannot verify
- Whether the scorer's *weights* (0.35 sponsorship, 0.30 fit) are the
  right weights for any given student -- that's a values judgment the
  book itself defers to the reader, not something this harness checks.
- Whether some future refactor, or a caller that doesn't exist yet, could
  reintroduce a gate-as-vote bug in a shape these two specific fixtures
  don't happen to cover. This harness proves the contract holds *today*,
  for the *one entry point and two gates that exist right now* -- it is
  not a permanent guarantee against every possible future regression.
- Whether 6 assertions constitute *sufficient* coverage (e.g., both gates
  closed simultaneously, a factor exactly at the 0.05 threshold boundary)
  -- that adequacy judgment is the human half of this repo's verification
  stack, not something the harness can certify about itself.

## Dependencies
- Node.js (tested on v20.20.0, the version already in use in this repo)
- No npm packages beyond what `role-scorer.mjs` already needs (`node:fs`,
  `node:path`, `node:url` -- all built-in, no new `package.json`
  dependency added)

## Annotated commands
```bash
# Confirm the CLI's existing behavior is unchanged (Phase Gate 2):
node scripts/score/role-scorer.mjs data/examples/ch11-roles.json --out-dir /tmp
# Expected: "Apply 2 - Consider 1 - Skip 2 (skip 40%)"

# Run the actual harness (both halves, one invocation):
node scripts/score/gate-behavior-harness.mjs
# Expected: Part 1 = 6/6 PASS, Part 2 = 3/3 correctly FAIL, final line "VALID"

# Confirm the process exit code matches the printed verdict:
echo $?
# Expected: 0
```

## What it produces
Printed stdout only, right now: per-assertion PASS/FAIL lines with the
actual observed value, a two-part summary, a final VALID/INVALID verdict,
and a matching process exit code. It does NOT yet produce a
`reports/generated/*.md` file or a `logs/*.json` agent log in the format
the other 43 recipes use -- see Failure Mode 4 below.

## Attestation (why this recipe stays DRAFT, not RUNNABLE-SAMPLE)
The recipe's frontmatter carries `attestation: null` on purpose. Per this
repo's own constitution, a recipe is not promoted past DRAFT until a
named human signs off that they've read the honest-run report, re-run the
harness themselves, and judged the result adequate -- not just that the
machine conformance checks passed. This card is where that attestation
belongs once given:

> Attested by: [your name]
> Date: [date]
> I confirm: I ran `node scripts/score/gate-behavior-harness.mjs` myself,
> read the honest-run report, and judge the 6/6-pass / 3/3-fail result
> adequate evidence that the real scorer's gates behave correctly.
> Reservations, if any: [state here, or "none"]

Until that block above is filled in by an actual person, this recipe's
`status` correctly stays `DRAFT` regardless of how many assertions pass --
machine conformance is not the same claim as human-attested adequacy.

## Failure modes (4, including drift and contract-violation)

1. **Drift.** If `role-scorer.mjs` is refactored later and this harness
   isn't updated alongside it, the harness could keep reporting `VALID`
   against code whose gate logic has silently changed shape (e.g., a new
   third gate added that this harness never checks). The harness's
   coverage is frozen to today's two named gates at today's one entry
   point -- it does not automatically track future changes to the file it
   tests. Mitigation: Required Reads item 3 explicitly tells a future
   maintainer to re-read the current state of `role-scorer.mjs` before
   trusting an old harness result.

2. **Contract-violation.** If a future change to `role-scorer.mjs` adds a
   new required export this harness doesn't import, or renames
   `scoreRole`/`applyProfile`/`CONFIG`, the harness will fail at Phase
   Gate 1 (the export gate) -- loudly, with a clear `undefined` signal.
   That's the intended, safe failure mode. The unsafe version of this
   same risk is the one already found and fixed during this build: a
   naive entry-point guard that failed silently (no error, no crash,
   simply never running) rather than loudly -- see the honest-run report.
   Any future modification to the guard logic should be re-tested against
   a path containing a space before being trusted, exactly as this one
   was.

3. **Fixture staleness.** The `ghost-posting` role this harness reuses
   from `data/examples/ch11-roles.json` is not owned by this
   contribution -- if a future edit to that shared fixture changes its
   `liveness` value away from `0.0`, this harness's Phase Gate 3
   assertions would silently start testing a different case than
   intended, without any warning. Mitigation: Required Reads item 4 flags
   this dependency explicitly.

4. **False confidence from the self-test alone.** A harness that passes
   its own self-test (Phase Gate 4) has only proven it can catch this one
   specific broken implementation
   (`BROKEN-scorer-for-harness-selftest.mjs`'s particular gate-as-vote
   shape). It has not proven it would catch every possible way a gate
   could be broken (e.g., a gate that's multiplicative but uses the wrong
   threshold, or one that's correct for liveness but broken only for
   timeline in a way the current fixtures don't isolate). Treat "the
   self-test passed" as "this harness has some real teeth," not as "this
   harness has caught every possible variant of this bug."
