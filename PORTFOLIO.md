# Gate-Behavior Unit-Test Harness — Portfolio Case Study

**Sakshi Tapkir** · INFO 7375 Capstone

## A note on how I got here
My first attempt at this capstone was a different project (a remittance-
cost transparency tool) that I built to a high standard — real sourced
data, real tests, a real honest run — before realizing it didn't actually
satisfy the assignment's core requirement: closing a gap the book names.
It was a well-built answer to the wrong question. Rather than submit it
anyway with a disclosed mismatch, I rebuilt the contribution around an
actual named gap. Separately, a second review caught that my first draft
of this harness's own documentation matched the real repo's actual
convention (one combined recipe file) rather than the assignment's
literal requirement (a separate AI recipe with nine specifically-named
sections, plus a human `.card.md` with 4+ named failure modes). I rebuilt
that too, once I checked the literal wording rather than assuming the
repo's convention satisfied it. I think both corrections are worth
stating plainly here, not burying — recognizing that a finished thing
doesn't meet the real bar, and rebuilding instead of shipping it anyway,
is the same discipline this harness itself is designed to enforce in the
scorer it tests.

## The problem
The Reallocation Engine's decision core (`role-scorer.mjs`, Chapter 11)
combines four evidence signals into one Apply/Consider/Skip
recommendation per job posting. Two of those signals — whether the
posting is actually live, and whether the timeline is actually feasible —
are supposed to act as *gates*: if either is closed, no amount of
sponsorship or fit should be able to push a role to Apply. The book is
explicit about why this matters: a ghost posting at a perfect-sponsor
company is worth zero effort, no matter how good the fit score looks. If
that gate silently degraded into an ordinary weighted vote instead — the
exact failure the capstone brief names as its own build bug — a student
could burn real, scarce application effort on postings that were never
real to begin with, and never know it happened, because the tool would
still hand them a confident, well-formatted "Apply."

## What I built
A test harness that proves, mechanically, that the gates actually gate.
It runs the real scorer against a known ghost-posting case and an
impossible-timeline case and confirms both are forced to Skip regardless
of how high sponsorship and fit are. Critically, it also runs the exact
same assertions against a second, deliberately-broken version of the
scorer that reimplements the specific bug being guarded against — additive
gates instead of multiplicative ones — and confirms the harness correctly
fails on it. A harness that can't fail on the bug it targets provides no
real assurance; this one demonstrably can.

## The measurable improvement
**6/6** assertions pass against the real scorer. **3/3** of the same
assertions correctly fail against the deliberately-broken version — proof
the harness has real detection power, not just a tautology. Along the
way, the harness build itself surfaced and fixed **3 real bugs** in the
existing scorer's testability (missing exports, an unguarded CLI entry
point, and — the most interesting one — my first fix for that entry point
was itself broken, failing silently rather than loudly, caught only when
tested against a real directory path containing a space) — found by
actually trying to use and test the code, not by inspection — and caught
**1 incorrect assumption in my own test**, corrected after tracing it back
to the book's own precise wording.

## Verified vs. inferred
Every fixture is either the book's own existing worked example, reused
unmodified, or an explicitly-labeled synthetic test case built to isolate
one variable. Every harness result is deterministic script output — there
is no model judgment anywhere in this contribution's actual verdicts.

## Failure modes and the one limitation this can't verify
The harness tests the gate contract at today's single entry point with
today's two named gates. It cannot prove a future refactor, or some new
caller that doesn't exist yet, won't reintroduce the same bug in a way
these two specific fixtures don't happen to catch. Extending coverage
(both gates closed at once, a factor exactly at the threshold boundary) is
the clear next step, named explicitly rather than silently assumed done.

## Demo
- `reports/gate-harness-honest-run.md` — the real executed output, including
  the three bugs found and fixed
- `scripts/score/gate-behavior-harness.mjs` — runnable in under a second,
  no dependencies beyond Node itself
