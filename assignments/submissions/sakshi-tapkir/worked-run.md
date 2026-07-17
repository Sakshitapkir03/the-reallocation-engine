Worked Run — case-backend-opt-sponsorship-triage
Runner: Sakshi Tapkir
Date: 2026-07-17
Recipe: recipes/case-backend-opt-sponsorship-triage.md v0.1.0
## Inputs

Primary posting: Software Engineer, Enterprise AI — Scale AI
https://job-boards.greenhouse.io/scaleai/jobs/4513943005
Confirmed present on Scale AI's live Greenhouse board (184 openings) at time of check.
Break-test posting: ADP Workforce Now-hosted listing
https://workforcenow.adp.com/mascsr/default/mdf/recruitment/recruitment.html?cid=b82bdd52-2595-49e9-8433-01d3c0f96cf0&ccId=9200554775585_2&lang=en_US&jobId=611247&source=LI&jr_id=6a591dc163a8f619507c04ef
Used deliberately to test the liveness gate against a non-Greenhouse/Lever/Ashby ATS.
Candidate facts used (not committed elsewhere): OPT end date 2027-02-20; STEM OPT eligibility self-assessed by candidate, not DSO-confirmed this run; earliest realistic start date August 29, 2026; no full-time engineering experience approaching the posting's stated "4+ years post-graduation" requirement.

## Commands (verbatim)
```
npm run verify
npm run doctor
npm run ats:liveness -- https://job-boards.greenhouse.io/scaleai/jobs/4513943005
npm run ats:liveness -- "https://workforcenow.adp.com/mascsr/default/mdf/recruitment/recruitment.html?cid=b82bdd52-2595-49e9-8433-01d3c0f96cf0&ccId=9200554775585_2&lang=en_US&jobId=611247&source=LI&jr_id=6a591dc163a8f619507c04ef"
grep -i "scale ai" data/80-days-to-stay/data/SEC_DOL_H1b_data_mapped.csv
grep -i "^scale" data/80-days-to-stay/data/SEC_DOL_H1b_data_mapped.csv
npm run score -- data/examples/ch11-roles.json
grep -i "15-1252" data/bls/compact/soc_occupation_compact.csv
```
## Real terminal output
### `npm run verify`
```
conformance: 132 files (76 md · 30 py · 23 js · 1 sh · 1 yaml · 1 json)
all conform (machine half of P4). Adequacy is still the human gate.
MANIFEST CHECK — The Reallocation Engine
WARN (4):
  W1 ignore path not in .gitignore: output/
  W1 ignore path not in .gitignore: reports/generated/
  W1 ignore path not in .gitignore: archive/
  W2 private path not gitignored (PII/secret risk): private/
manifest check passed (4 warnings)
```
Note: the four warnings are pre-existing repo-wide conditions, not introduced by this recipe or this run.
### `npm run doctor`
```
RECIPE DOCTOR — The Reallocation Engine
ENVIRONMENT (required)
  node v20.20.0
  python3 Python 3.9.6
ENVIRONMENT (optional)
  pandoc pandoc 3.6.3
  libreoffice not found (PDF fallback)
  playwright installed
RUNNABLE COMMANDS: all present (18/18 targets present)
DOMAIN DIRECTORIES: all present
PRIVACY (no personal data committed)
  no private/PII paths are tracked
RECIPES (43)
  with lifecycle frontmatter: 43   missing: 0
  by status: DRAFT 43
  open TODOs: 522 declared (in frontmatter) 522 TODO markers in bodies
SUMMARY
  environment: runnable
  recipes: 43/43 carry lifecycle frontmatter — all tracked
  next: promote a recipe past DRAFT with a logged run
```
### `npm run ats:liveness -- <Scale AI URL>`
```
Checking 1 URL(s)...
active     https://job-boards.greenhouse.io/scaleai/jobs/4513943005
Results: 1 active  0 expired  0 uncertain
```
### `npm run ats:liveness -- <ADP URL>` (deliberate break attempt)
```
Checking 1 URL(s)...
expired    https://workforcenow.adp.com/mascsr/default/mdf/recruitment/recruitment.html?cid=b82bdd52-2595-49e9-8433-01d3c0f96cf0&ccId=9200554775585_2&lang=en_US&jobId=611247&source=LI&jr_id=6a591dc163a8f619507c04ef
insufficient content — likely nav/footer only
Results: 0 active  1 expired  0 uncertain
```
### `grep -i "scale ai"` / `grep -i "^scale"` against sponsorship CSV
```
(no match for "scale ai")
MINDSCALE AI INC,...
SCALE MEDICINE INC,...
SCALED INFERENCE INC,...
SCALEFACTOR INC,...
SCALEFAST INC,...
SCALEFLUX INC,...
SCALER GLOBAL INC,...
SCALEWITH INC,...
SCALEWORKS FUND I LP,...
SCALEWORKS FUND II LP,...
SCALEWORKS FUND III LP,...
SCALEWORKS VENTURE FINANCE FUND I LP,...
```
No row matches "Scale AI" (the employer behind the posting). Eleven "Scale"-prefixed companies matched, none of them this employer.
### `npm run score -- data/examples/ch11-roles.json`
```
scored 5 roles → Apply 2 · Consider 1 · Skip 2 (skip 40%)
data/examples/role-scores.json  +  data/examples/role-scores.md
```
Reproduces the book's Ch.11 worked example exactly. Ran against the sample fixture only — a real per-posting evidence envelope builder for this specific Scale AI role does not exist yet (see recipe's open development item).
### `grep -i "15-1252"` against SOC compact table
```
15-1252.00,15-1252,Software Developers,Research design and develop computer and network software,4,93,...,2024,1654440.0,144570.0,133080.0,69.5,63.98,0.7,...,3.834
```
SOC 15-1252.00, Job Zone 4, national employment 1,654,440, mean wage $144,570, cognitive_pivot_score 3.834.
## Verified vs. Inferred
Verified this run:

npm run verify and npm run doctor executed with the exact output above.
Scale AI posting liveness: active, per real Playwright-based script output.
ADP posting liveness: expired / insufficient content — likely nav/footer only, per real script output.
No row for "Scale AI" exists in SEC_DOL_H1b_data_mapped.csv — checked by direct grep, not inferred.
SOC 15-1252 (Software Developers) has a real cognitive_pivot_score of 3.834 in the BLS compact table.
The role scorer executes successfully and reproduces the book's known output on the sample fixture.

Inferred (human judgment, not machine-verified):

That an August 29, 2026 start date is realistic for this candidate (self-estimated).
That the candidate's STEM OPT eligibility, though self-assessed as eligible, has not been confirmed via official DSO documentation.
That the posting's 4+ years post-graduation requirement disqualifies the candidate on experience grounds (a direct, low-ambiguity read of the posting text against the candidate's actual history — not a machine score).
That the ADP liveness failure means the posting itself is not reachable in a way the tool can parse — not necessarily that the underlying job is gone (a real, unresolved ambiguity, logged honestly rather than resolved by assumption).

## Gate-by-Gate Result (Scale AI posting)
| Gate | Result | Evidence |
|---|---|---|
| 1. Input sufficiency and privacy | Pass | npm run doctor — no PII tracked |
| 2. Posting liveness | Pass | ats:liveness — active |
| 3. Visa timeline | Pass | Aug 29 2026 start fits inside OPT (ends 2027-02-20); STEM OPT eligibility self-assessed, not DSO-confirmed |
| 4. Sponsorship evidence | Missing | No row for Scale AI in sponsorship CSV — data gap, not a red flag |
| 5. Role/technical fit | Fail | Posting requires 4+ years post-grad experience; candidate does not have this |
| 6. Cognitive role quality | Pass | SOC 15-1252, cognitive_pivot_score 3.834 |
| 7. Output eligibility | Pass | All six gates above logged; no unknown silently upgraded |
Final classification: Skip — driven principally by Gate 5 (explicit, stated minimum-experience mismatch), independent of otherwise reasonable stack overlap.
## Deliberate Break Attempt
Command:
npm run ats:liveness -- "https://workforcenow.adp.com/mascsr/default/mdf/recruitment/recruitment.html?cid=b82bdd52-2595-49e9-8433-01d3c0f96cf0&ccId=9200554775585_2&lang=en_US&jobId=611247&source=LI&jr_id=6a591dc163a8f619507c04ef"
Result: expired / insufficient content — likely nav/footer only — confirmed independently (a manual page fetch outside the repo's tooling also returned only a browser-compatibility fallback shell, no job content, consistent with a JavaScript-rendered ADP career page that the liveness heuristics could not parse).
Did the mode stop correctly? Yes. Per Gate 2's design, a failed/uncertain liveness result halts the run before any classification is attempted — the mode did not attempt to score this posting, and this worked-run doc does not produce an Apply/Consider/Skip result for it, only a Refuse to Score by way of the liveness gate.
## Verification
Re-ran npm run ats:liveness against the Scale AI URL a second time after the initial check to confirm the result was stable, not a one-off fluke — same active result both times.
## Reflection
What worked: the liveness gate, sponsorship-CSV lookup, and SOC lookup are all genuinely useful, fast, real checks — none of them required guessing, and the sponsorship no-match case was handled correctly as a data gap rather than a false negative.
What the mode missed: there is no script yet that builds a real per-posting evidence envelope, so the role-scorer step in this run only proves the machinery works, not that it evaluated this posting — a genuine limitation, documented as an open development item in the recipe.
What surprised me: the ADP posting returning insufficient content rather than a clean expired/404 — it's a reminder that liveness as this tool defines it is really can this specific script parse this specific ATS's rendering, not a universal truth about whether the job exists.
What remains unverified: whether Scale AI would in practice ever consider a candidate close to the 4-year line if other evidence were exceptional; whether the ADP posting is genuinely dead or just unparseable by this tooling; my STEM OPT eligibility, pending actual DSO confirmation.
Concrete next steps: build the open role-envelope script so npm run score can evaluate a real posting instead of only the sample fixture; test the liveness script against at least one more ADP-hosted or Workday-hosted posting to see if the insufficient content result is a pattern with this ATS family or specific to this URL.
## Attestation

Recipe: case-backend-opt-sponsorship-triage v0.1.0
By: Sakshi Tapkir, 2026-07-17

### Tested
| Ran | Saw | Expected |
|---|---|---|
| ats:liveness (Scale AI URL) | active | Confirmation the posting is reachable |
| ats:liveness (ADP URL, deliberate break attempt) | expired, insufficient content | A liveness failure so the run stops before scoring |
| grep against sponsorship CSV | no match for Scale AI | Either a match or an honest no-row result |
| score (sample fixture) | 5 roles, Apply 2, Consider 1, Skip 2 | Reproduction of Ch.11's documented output |
| grep against SOC compact table | SOC 15-1252, score 3.834 | A real SOC-level record if one exists |
### Did not test

The real per-posting evidence-envelope builder — does not exist yet.
The visa-timeline arithmetic script — Gate 3 was done by hand this run, not by a script.
scripts/sec/entity-resolution.py against this specific company (still blocked on missing raw LCA data).
Whether the ADP liveness failure is specific to this one URL or a pattern across ADP-hosted postings generally.
A live/dialogic run with a second human reviewer clearing gates independently (this run was single-reviewer: the candidate herself).

### Broke during testing, fixed

doctor initially reported a todos_open mismatch (declared 5, body count 12) on the newly-added recipe file, caused by four TODO-tag mentions inside descriptive prose referencing the same open items a second time, rather than five genuinely distinct items. Fixed by rewording the four restated mentions to describe the gap without repeating the bracket syntax, leaving exactly five canonical markers matching the declared count. Re-ran doctor after the fix and confirmed 522 declared equals 522 body markers, no mismatch.
