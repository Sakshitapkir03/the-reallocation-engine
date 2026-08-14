---
status: DRAFT
todos_open: 1
last_gate: null
attestation: null
recipe_version: 0.2.0
---

# Gate-Behavior Unit-Test Harness — AI Recipe

*Companion file: `gate-behavior-harness.card.md` (the human-facing card).
Update both in the same commit — see `SNICKERDOODLE.md`'s two-customer
rule.*

## Executive Summary
This recipe runs a unit-test harness that proves
`scripts/score/role-scorer.mjs`'s liveness and timeline factors behave as
**multiplicative gates** — closing regardless of how strong sponsorship
and fit votes are — rather than as **additive votes**. This is the exact
gap the capstone brief names: *"prove liveness and timeline zero the
composite, catching the gate-as-vote bug that is the capstone's named
build failure."* The recipe does two things in one run: (1) asserts the
real scorer behaves correctly, and (2) asserts the same checks correctly
FAIL against a deliberately-broken version, proving the harness itself
has real detection power rather than passing on anything handed to it.
No live network calls, no writes to private data, no model calls — this
is a pure, deterministic computation over local fixtures.

## Required Reads
Before running or modifying this recipe, read, in this order:
1. `SNICKERDOODLE.md` — the constitution; governs any conflict below.
2. `chapters/11-the-bayesian-role-scorer.md`, section "Why liveness and
   timeline are multipliers, not addends" — the exact contract this
   recipe tests, quoted directly in its assertions.
3. `scripts/score/role-scorer.mjs` — the code under test. Note the three
   exports (`CONFIG`, `applyProfile`, `scoreRole`) and the entry-point
   guard were added as part of this contribution — read the inline
   comments explaining why (a naive guard silently failed on paths
   containing spaces; see the honest-run report for the full story).
4. `data/examples/ch11-roles.json` — the existing, unmodified fixture
   whose `ghost-posting` role this recipe reuses as-is.
5. `reports/gate-harness-honest-run.md` — what was actually found the
   first time this recipe was run for real, including 3 bugs.

## Phase Gates
Do not move to a later step until the earlier gate has passed.

1. **Export gate.** `scoreRole`, `applyProfile`, `CONFIG` must be
   importable from `role-scorer.mjs`.
   Test: `node -e "import('./scripts/score/role-scorer.mjs').then(m=>console.log(typeof m.scoreRole))"` — must print `function`.
   **Failure path:** if it prints `undefined`, the exports regressed —
   stop, do not run the harness, fix the exports first.
2. **Regression gate.** Adding those exports/guard must not change the
   CLI's pre-existing, documented output.
   Test: `node scripts/score/role-scorer.mjs data/examples/ch11-roles.json --out-dir /tmp` — must print `Apply 2 · Consider 1 · Skip 2 (skip 40%)`, matching `logs/RUN_LOG.md`'s 2026-06-14 entry.
   **Failure path:** if the counts differ, something in this contribution
   broke the existing scorer — stop, do not proceed, revert the export/guard
   change and re-diagnose before touching anything else.
3. **Real-scorer gate.** The harness's 6 assertions against the real
   `scoreRole` must all pass.
   **Failure path:** if any fail, the real scorer has a gate-as-vote
   regression. Stop. Do not promote this recipe past DRAFT. File it as a
   defect against `role-scorer.mjs`, not against this harness.
4. **Self-test gate.** The same-shaped 3 assertions run against the
   deliberately-broken scorer must all FAIL.
   **Failure path:** if any pass, the harness has no real detection power
   and must not be trusted for anything — regardless of what Gate 3
   reported. Stop and rebuild the assertion, don't just note it as a
   caveat.

## Primary Stored Tools
- `scripts/score/gate-behavior-harness.mjs` — the harness itself (this
  contribution's only stored script; nothing else needed to exist for
  this recipe to run).
- `scripts/score/role-scorer.mjs` — the code under test (pre-existing;
  3 exports and 1 entry-point-guard fix added as part of this
  contribution, both regression-checked — see Phase Gate 2).
- `scripts/score/BROKEN-scorer-for-harness-selftest.mjs` — test-only code
  for Gate 4; never used for real scoring, never called from any
  production path.

No part of this recipe currently lacks a stored script — there is no
"not implemented yet" step in this workflow. (The one thing this recipe
does *not* yet do — write a `reports/generated/*.md` file in the format
the other 43 recipes use — is named as an open TODO in Stop Conditions,
not silently treated as done.)

## Workflow
1. Run `node scripts/score/role-scorer.mjs data/examples/ch11-roles.json --out-dir /tmp` and confirm Phase Gate 2's expected output.
2. Run `node scripts/score/gate-behavior-harness.mjs`.
3. Read the printed output: Part 1 (real scorer) should show 6/6 PASS;
   Part 2 (broken scorer) should show 3/3 correctly FAIL.
4. Confirm the final line reads `Harness self-test: VALID` and the
   process exit code is `0` (`echo $?` immediately after, on macOS/Linux).
5. If VALID: the real scorer's gate behavior is confirmed correct for
   this run. Log the result per Logging Rules below.
6. If INVALID (either Part 1 has a failure or Part 2 has an unexpected
   pass): stop per the relevant Phase Gate's failure path — do not log
   this as a routine result, escalate it.

## Output Contract
Currently: stdout only (per-assertion PASS/FAIL lines, a Part 1/Part 2
summary, a final VALID/INVALID verdict, and a matching process exit code).
**Not yet implemented** (named explicitly, not silently skipped — this is
the recipe's 1 open TODO): a `reports/generated/gate-behavior-harness-[DATE].md`
human report and a `logs/gate-behavior-harness-[DATE].json` agent log in
the format the other 43 recipes use.

## Verification Checks
- `node scripts/score/gate-behavior-harness.mjs` exits `0`.
- Its stdout contains the exact line `Harness self-test: VALID`.
- Part 1 shows `6/6 passed`; Part 2 shows `3/3 correctly failed`.
- The Phase Gate 2 regression check (`Apply 2 · Consider 1 · Skip 2`)
  still holds — re-run it any time `role-scorer.mjs` changes.

## Logging Rules
Log to `logs/RUN_LOG.md` whenever this harness is run to inform a real
decision about trusting `role-scorer.mjs`'s gate behavior (not required
for routine re-runs during development). Entry format matches this file's
existing convention: date, recipe name, inputs, outputs, result, open
issues. See the 2026-08-12 entry already logged for this contribution as
the template.

## Stop Conditions
- Stop and do not promote this recipe past DRAFT if Phase Gate 3 fails.
- Stop and distrust the entire harness if Phase Gate 4 fails (any broken-scorer
  assertion unexpectedly passes).
- `[TODO: DEV]` This harness does not yet write a `reports/generated/*.md`
  or `logs/*.json` artifact in the format the other 43 recipes use — it
  currently only prints to stdout. This is the 1 open TODO on this recipe,
  and it stays DRAFT (not RUNNABLE-SAMPLE) until a human attests to it —
  see the card for what attestation requires here.
