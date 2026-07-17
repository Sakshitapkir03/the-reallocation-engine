---
status: DRAFT
todos_open: 5
last_gate: null
attestation: null
recipe_version: 0.1.0
---

# Backend/Full-Stack OPT Sponsorship Triage

## Purpose

This mode helps an international master's graduate on F-1 OPT (post-completion, authorization end date 2027-02-20, STEM extension eligibility currently unverified pending DSO confirmation), targeting entry-level backend, full-stack, and AI-application software engineering roles, decide — before spending application or interview time — whether a specific job posting clears the minimum evidence bar: the posting is genuinely live, the visa timeline is compatible, the employer has some sponsorship signal (or an explicit absence of one), and the role matches the candidate's backend/full-stack technical evidence.

This mode does not rank companies in bulk and does not predict hiring outcome. It evaluates one posting at a time against hard gates. A `Skip` or `Refuse to Score` result is a successful outcome, not a failure of the mode.

Note: `recipes/case-backend-swe-opt-triage.md` and `recipes/case-opt-timeline-fit-company-targeting.md` cover adjacent scope (bulk company ranking) but remain unrun `DRAFT` stubs with placeholder define-type fields and no logged run. This recipe is a distinct, single-posting evaluation, executed and logged for real (see `logs/RUN_LOG.md`).

## Source Inventory

| Source | Path / Command | Can Establish | Cannot Establish |
|---|---|---|---|
| Repo conformance | `npm run verify` | Repo files parse; machine half of P4. | Whether the recipe content is adequate — that's the human gate. |
| Repo doctor | `npm run doctor` | Environment ready, commands exist, no PII tracked, recipe lifecycle status. | Whether any individual run's data is correct. |
| Posting liveness | `npm run ats:liveness -- <job-url>` (`scripts/ats/check-liveness.mjs`, Playwright-based) | Whether a specific URL is reachable/active vs. expired/uncertain at run time. | Whether the employer is actively reviewing applicants, or whether the posting stays live tomorrow. |
| Sponsorship history | `data/80-days-to-stay/data/SEC_DOL_H1b_data_mapped.csv` + its audit `SEC_DOL_H1b_data_mapped-audit.md` | Whether a company name matches a row with historical H-1B/SEC signal. Audited: 30,369 companies, 1,557 (5.1%) with H-1B field populated, 17,752 (58.5%) with website, funding dates present for 91.8% of rows, newest funding date 2025-09-26. No ATS or SOC columns in this file. | Whether that historical sponsorship will apply to this exact role, this exact year, or this exact office. Absence of a row means data is missing, not that the company doesn't sponsor. |
| ATS scan (sample) | `REALLOCATION_ENGINE_PORTALS=data/ats/portals.example.yml npm run ats:scan -- --dry-run` | Whether the example scanner config loads, matches a provider (Greenhouse/Lever/Ashby), and runs filter/dedup logic without writing private data. | Whether the specific target company/posting is in scope — the example config only tracks Databricks (enabled) plus two disabled placeholders. |
| Role-quality / Cognitive Pivot | `data/bls/compact/soc_occupation_compact.csv` | Whether a SOC code has O*NET/OEWS-derived skill/ability levels and a `cognitive_pivot_score`. | Whether a specific employer's version of that SOC role is high-quality, or whether the score predicts durability of this specific posting. |
| Role scorer (sample) | `npm run score -- data/examples/ch11-roles.json` (`scripts/score/role-scorer.mjs`) | Whether the combiner runs and produces `Composite = (Σ vote·weight) × liveness × timeline` with per-term source labels (`record`/`model-judgment`/`your-input`), reproducing the book's worked examples (0.446 Apply / 0.178 Skip). | Real per-role evidence for *this candidate's* postings — the sample fixture is Ch.11's illustrative data, not this candidate's. Wiring real sponsorship/fit/liveness/timeline numbers per posting is the open development item  below. |
| Candidate evidence | Not committed to any tracked file — read from `private/` locally only | Which of Sakshi's claimed skills are work-proven (Humanitarians AI, MR SON Equipments), project-proven (Eventopia, Document Parser), or merely listed. | Whether a specific employer will value that evidence the way the candidate expects. |

## Proposed Additions

- `[TODO: DEV]` Add a script (working name `scripts/score/build-role-envelope.mjs`) that takes a job URL + company name + candidate evidence file (read from `private/`, never committed) and emits a single-role JSON record in the `ch11-roles.json` shape (`sponsorship`, `fit`, `liveness`, `timeline`, each with `p`/`factor` + `source`), so `npm run score` can run against a real posting instead of only the sample fixture. Expected input: job URL, company name, path to private evidence file. Expected output: one JSON object matching the existing `data/examples/ch11-roles.json` schema. Verified by: `python3 -m json.tool` on the output, then a real `npm run score` run against it.

- `[TODO: DATA SOURCE]` Confirm whether `scripts/sec/entity-resolution.py`'s FEIN/name-matching path can run end-to-end for a target company, or whether it remains blocked on missing raw LCA/DOL employer records (as `DOMAIN.md` and the SEC script notes suggest). Provenance note required once tested: date, command, and whether raw LCA data was actually present.

- `[TODO: DEFINE]` Pin the OPT/STEM-OPT visa-timeline compatibility rule as an explicit function of: OPT end date (2027-02-20), STEM eligibility (currently `uncertain` pending DSO confirmation), and a candidate-declared or posting-declared expected start date. No script computes this today — it is Gate 3 below, and it is evaluated by hand until the open development item  below closes it.

- `[TODO: DEV]` Add a small script or documented manual procedure for Gate 3 (visa timeline arithmetic), since none of `scripts/sec/`, `scripts/ats/`, or `scripts/score/` currently computes visa-timeline compatibility. Expected input: OPT end date, STEM eligibility status, candidate-declared earliest start date. Expected output: `compatible` / `incompatible` / `unknown`, with the reasoning shown. Verified by: manual arithmetic check against the stated dates in this recipe's worked run.

- `[TODO: REPORT FIELD]` Add a `sponsorship_confidence` field to the human report distinguishing "sponsorship history exists (row matched)" from "no row found (data gap, not a red flag)" from "row found, but no recent funding/approval activity." Reader: the candidate evaluating whether to continue with this application. Decision enabled: proceed, proceed with caution, or deprioritize pending more evidence.

## Phase Gates

**Gate 1 — Input sufficiency and privacy.**
Test: `npm run doctor` reports privacy check green (`no private/PII paths are tracked`) and the run's inputs (job URL, company name) are present.
Pass: doctor privacy check passes and job URL + company name are both provided.
Fail: doctor reports a tracked private path, or job URL/company name is missing.
This gate does not evaluate candidate evidence quality — only that private data stayed private and inputs exist.

**Gate 2 — Posting liveness.**
Test: `npm run ats:liveness -- <job-url>`.
Pass: script reports active.
Fail/Unknown: script reports expired, uncertain, or cannot resolve the URL.
A failed or unknown liveness gate stops the run. A high fit or sponsorship score never overrides this gate.

**Gate 3 — Work authorization and visa-timeline compatibility.**
Test: manual, per the open define/dev items  above — compare OPT end date (2027-02-20) and declared/inferred start date; STEM eligibility marked `unresolved` unless official DSO documentation is provided this run.
Pass: start date and required work-authorization window fit inside verified OPT/STEM-OPT coverage.
Fail: role requires U.S. citizenship or active security clearance (hard exclusion, unconditional), or dates plainly do not fit.
Unknown: STEM eligibility or exact timeline cannot be confirmed this run — proceed only to Gate 4 with the result logged as `unknown`, never silently upgraded to pass.

**Gate 4 — Sponsorship evidence.**
Test: look up company name in `data/80-days-to-stay/data/SEC_DOL_H1b_data_mapped.csv`.
Pass: a matching row exists with H-1B field populated.
Data-missing (not fail): no matching row — 94.9% of the dataset has no H-1B field populated, so absence is common and must be logged as `missing`, not `fail`.
This gate never equates a historical match with a guarantee that this exact role will be sponsored.

**Gate 5 — Role/SOC match and technical-fit sufficiency.**
Test: human comparison of posting responsibilities against candidate's work-proven and project-proven evidence (Java/Spring Boot, Node/Express, Python/FastAPI, REST APIs, SQL/Postgres/MongoDB/Redis, Docker/CI-CD, LangChain/FAISS/RAG where relevant), supported by a sample `npm run score` run.
Pass: posting responsibilities clearly match backend/full-stack/AI-application engineering, and candidate evidence for the required stack is at least project-proven.
Fail: posting is support/QA/implementation/sales-engineering under a generic "Software Engineer" title, or requires skills the candidate has no work- or project-proven evidence for.

**Gate 6 — Cognitive-role-quality assessment.**
Test: look up the nearest SOC code in `data/bls/compact/soc_occupation_compact.csv`; read its `cognitive_pivot_score` and OEWS/O*NET context.
Pass: SOC-level evidence available and consulted.
Unknown: no clean SOC match — logged as unknown, not treated as disqualifying by itself.
This gate never claims the score describes a specific employer or posting's durability.

**Gate 7 — Output eligibility.**
Test: all six gates above have a logged status (`pass`/`fail`/`unknown`), and no `unknown` has been silently converted to `pass`.
Pass: a final classification (`Apply`/`Consider`/`Skip`/`Refuse to Score`) can be produced with full gate provenance.
Fail: any required gate result is missing — output must be `Refuse to Score`, not a guessed classification.

## Verified vs. Inferred Boundary

**Verified (this run):** the liveness command executed and returned a specific status; the sponsorship CSV lookup executed and returned a matched row or no row; the SOC lookup executed and returned a specific `cognitive_pivot_score` or no match; `npm run score` executed and produced a composite number with labeled per-term sources.

**Inferred (always judgment, never claimed as verified):** whether the team is supportive; whether this exact employer will sponsor this exact candidate; whether the hiring manager values systems thinking; whether the candidate will get an interview; whether the employer stays financially healthy; whether a high SOC cognitive-pivot score means this specific posting is durable; whether historical H-1B activity predicts this cycle's sponsorship.

## What This Mode Can and Cannot Verify

**Can verify:** posting liveness at run time (`ats:liveness`); presence/absence of a sponsorship-history row for the named company (`SEC_DOL_H1b_data_mapped.csv`); SOC-level role-quality data presence (`soc_occupation_compact.csv`); whether the sample scanner config and role scorer run without error; whether candidate evidence for a named technology is work-proven, project-proven, or merely listed (via the candidate's own private evidence file, read locally, never committed).

**Cannot verify:** guaranteed sponsorship for this exact role; legal work-authorization eligibility without official SEVP/DSO documents; exact remaining unemployment days without official records (marked `unresolved` in this recipe, per prior assignment's finding); hiring-manager intent; interview probability; internal team quality; whether the posting stays live after this run; employment-law advice; whether resume claims are true without human attestation.

## Output Contract

### A. Agent-readable JSON log

```json
{
  "recipe": "case-backend-opt-sponsorship-triage",
  "recipe_version": "0.1.0",
  "run_id": "<uuid-or-date-sequence>",
  "timestamp": "<ISO-8601>",
  "anonymized_input_id": "<hash-or-label, never the real posting URL if privacy-sensitive>",
  "input": {
    "job_url": "<public-job-url>",
    "company": "<company>",
    "role_title": "<role-title>"
  },
  "commands_run": [
    "npm run verify",
    "npm run doctor",
    "npm run ats:liveness -- <job-url>",
    "npm run score -- data/examples/ch11-roles.json"
  ],
  "command_exit_codes": {},
  "gates": {
    "input_sufficiency_privacy": { "status": "pass|fail|unknown", "evidence": "" },
    "posting_liveness": { "status": "pass|fail|unknown", "evidence": "" },
    "visa_timeline": { "status": "pass|fail|unknown", "evidence": "" },
    "sponsorship_evidence": { "status": "pass|fail|missing", "evidence": "" },
    "role_soc_technical_fit": { "status": "pass|fail|unknown", "evidence": "" },
    "cognitive_role_quality": { "status": "pass|fail|unknown", "evidence": "" },
    "output_eligibility": { "status": "pass|fail", "evidence": "" }
  },
  "sponsorship_confidence": "history_exists|no_row_found|row_found_stale",
  "soc_code": "<code-or-null>",
  "cognitive_pivot_score": "<value-or-null>",
  "verified_facts": [],
  "inferred_judgments": [],
  "unresolved_fields": ["stem_opt_eligibility", "exact_unemployment_days"],
  "final_outcome": "Apply|Consider|Skip|Refuse to Score",
  "stop_reason": "<null-or-reason>",
  "todos_encountered": []
}
```

### B. Human-readable Markdown report

| Gate | Evidence | Status | Confidence / Unresolved | Source | Human Action Required |
|---|---|---|---|---|---|
| Input sufficiency & privacy | | | | `npm run doctor` | |
| Posting liveness | | | | `npm run ats:liveness` | |
| Visa timeline | | | STEM eligibility: unresolved | manual, per OPT end date 2027-02-20 | Confirm with DSO |
| Sponsorship evidence | | | | `SEC_DOL_H1b_data_mapped.csv` | |
| Role/SOC & technical fit | | | | manual + `npm run score` | |
| Cognitive role quality | | | | `soc_occupation_compact.csv` | |
| Output eligibility | | | | all gates above | |

## Stop Conditions

Refuse to produce an Apply/Consider/Skip classification when:
- the posting is dead or cannot be uniquely identified;
- visa-timeline information required for Gate 3 is missing and cannot be marked even `unknown` with reasoning;
- the sponsorship CSV lookup or SOC lookup fails to parse (malformed data);
- the liveness or score script exits nonzero for a reason other than expected liveness failure;
- the employer identity cannot be matched reliably between the posting and the sponsorship dataset;
- the role requires U.S. citizenship or active security clearance;
- producing a score would require fabricating any of the fields above.

In all these cases the output is `Refuse to Score` or `Unknown`, never a guessed classification.

## Log Template (for `logs/RUN_LOG.md`)

```markdown
## YYYY-MM-DD — case-backend-opt-sponsorship-triage v0.1.0

- **Recipe:** case-backend-opt-sponsorship-triage
- **Runner:** Sakshi Tapkir
- **Inputs:** <anonymized job URL/company>, `data/80-days-to-stay/data/SEC_DOL_H1b_data_mapped.csv`, `data/bls/compact/soc_occupation_compact.csv`, `data/examples/ch11-roles.json` (sample only)
- **Commands:** `npm run verify`; `npm run doctor`; `npm run ats:liveness -- <job-url>`; `npm run score -- data/examples/ch11-roles.json`
- **Outputs:** terminal output captured in `assignments/submissions/sakshi-tapkir/worked-run.md`
- **Result:** <gate-by-gate pass/fail/unknown summary>
- **Open issues:** real per-role evidence envelope builder still open (see Proposed Additions); visa-timeline script still open (see Proposed Additions); entity-resolution against raw LCA still unverified
- **Privacy check:** confirmed no private/PII paths tracked (`npm run doctor`)
```
