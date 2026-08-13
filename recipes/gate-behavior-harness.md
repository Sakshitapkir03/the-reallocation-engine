---
status: RUNNABLE-SAMPLE
todos_open: 1
last_gate: null
attestation: null
recipe_version: 0.1.0
---

# Gate-Behavior Unit-Test Harness

## Purpose
Proves that `scripts/score/role-scorer.mjs`'s liveness and timeline factors
behave as **multiplicative gates** — closing regardless of how strong
sponsorship and fit are — rather than as additive votes. This is the exact
gap named in the capstone brief: *"prove liveness and timeline zero the
composite, catching the gate-as-vote bug that is the capstone's named build
failure."* Chapter 11 states the contract directly: *"No amount of fit or
sponsorship can carry a role through a gate that is closed."* This recipe
is the machine-checkable proof that the shipped code actually honors that
sentence, plus a self-test proving the proof itself has real teeth.

## Source Inventory

| Source Node | Node Type | Source URL or Path | Human Check |
|---|---|---|---|
| The scorer under test | file | `scripts/score/role-scorer.mjs` | Confirm this is still the live, maintained scorer before trusting the harness's result. |
| Book chapter | file | `chapters/11-the-bayesian-role-scorer.md` | Confirm the gate-vs-vote contract quoted above hasn't been revised since this harness was written. |
| Reference fixture | file | `data/examples/ch11-roles.json` | The `ghost-posting` role (liveness=0) already existing in this fixture is used as-is, not invented for this test. |

## Inputs
| Input | Type | Source | Required? |
|---|---|---|---|
| `ghost-posting` role | record | existing fixture, `data/examples/ch11-roles.json` | Yes |
| Synthetic timeline-gate role | constructed test fixture, clearly labeled | `data/examples/gate-harness-timeline-test.json` | Yes |
| The deliberately-broken scorer | test-only code, clearly labeled, never used for real scoring | `scripts/score/BROKEN-scorer-for-harness-selftest.mjs` | Yes (for the self-test half only) |

## Phase Gates
1. **Export gate:** `scoreRole`, `applyProfile`, `CONFIG` must be importable from `role-scorer.mjs`. Test: `node -e "import('./scripts/score/role-scorer.mjs').then(m=>console.log(typeof m.scoreRole))"` should print `function`, not `undefined`.
2. **Regression gate:** adding those exports must not change the CLI's existing output. Test: `node scripts/score/role-scorer.mjs data/examples/ch11-roles.json --out-dir /tmp` must still print `Apply 2 · Consider 1 · Skip 2 (skip 40%)` — the exact result already on record in this repo's `logs/RUN_LOG.md`.
3. **Real-scorer gate:** the harness's 6 assertions against the real `scoreRole` must all pass. Failure path: if any fail, the real scorer has a gate-as-vote regression — stop, do not promote this recipe, file it as a defect against `role-scorer.mjs` instead.
4. **Self-test gate:** the same 3 assertions run against the deliberately-broken scorer must all fail. Failure path: if any pass, the harness itself has no detection power and must not be trusted or promoted, regardless of what it says about the real scorer.

## Steps
1. **Run the real-scorer assertions.** Labor: script only, no human gate needed (read-only, no live/external action).
   Script: `node scripts/score/gate-behavior-harness.mjs`
   Output: PASS/FAIL per assertion, printed to stdout.
2. **Run the self-test assertions against the broken scorer.** Same script, same run — both halves execute in one invocation by design, so the self-test can never be silently skipped.
3. **Report the combined verdict.** The script's own exit code (0 = harness valid, 1 = invalid) is the machine-checkable pass/fail signal for CI or `npm run verify` integration.

## Output Contract
Printed to stdout (this harness does not yet write a separate JSON/Markdown
report file — see Stop Conditions for why that's named as an open item,
not silently skipped):
- Per-assertion PASS/FAIL lines with the actual value observed
- A summary section: Part 1 pass count, Part 2 fail count
- A final verdict: `Harness self-test: VALID` or `INVALID`
- Process exit code matching that verdict

## Verification Checks
Run `node scripts/score/gate-behavior-harness.mjs` and confirm:
- Part 1: 6/6 assertions pass against the real scorer
- Part 2: 3/3 assertions correctly fail against the broken scorer
- Final line reads `VALID`, exit code 0

## Logging Rules
Every run of this harness that informs a real decision about whether to
trust `role-scorer.mjs`'s gate behavior should get a `logs/RUN_LOG.md`
entry: date, harness run, pass/fail counts, and whether any assertion's
result surprised you (a surprise is exactly what happened once during this
build — see `reports/gate-harness-honest-run.md`).

## Stop Conditions
- Stop and do not promote this recipe past DRAFT if Part 1 has any failure
  — that means the real scorer has a gate-as-vote defect, which is a
  production bug in `role-scorer.mjs`, not a harness problem.
- Stop and distrust the entire harness if Part 2 has any pass — a harness
  that can't fail on the bug it targets provides zero real assurance,
  regardless of how confidently it reports "VALID" elsewhere.
- **`[TODO: DEV]`** This harness does not yet
  write a `reports/generated/*.md` file or a `logs/*.json` agent log in the
  format the other 43 recipes use — it currently only prints to stdout.
  This is the 1 open TODO on this recipe.

## Provenance
| Source | Verification command | Notes |
|---|---|---|
| Real scorer exports | `grep -n "^export" scripts/score/role-scorer.mjs` | Confirms the 3 added exports (`CONFIG`, `applyProfile`, `scoreRole`) are present. |
| CLI regression, unaffected by the exports/guard changes | `node scripts/score/role-scorer.mjs data/examples/ch11-roles.json --out-dir /tmp` | Must match the pre-existing documented result in `logs/RUN_LOG.md` (2026-06-14 entry: "Apply 2 · Consider 1 · Skip 2"). |
| The book's stated contract | `chapters/11-the-bayesian-role-scorer.md`, section "Why liveness and timeline are multipliers, not addends" | The harness's assertions are a direct, literal test of this section's claim. |
