---
status: RUNNABLE-SAMPLE
todos_open: 3
last_gate: "sample-run, 2026-07-05, assignments/submissions/sakshi-tapkir/worked-run.md"
attestation: null
recipe_version: 0.1.0
---

# Backend Role Authenticity

## Purpose

This mode helps international software engineers on F-1 OPT evaluate whether a job posting titled Software Engineer, Backend Engineer, Full Stack Engineer, Platform Engineer, or similar represents genuine backend engineering work before investing application or interview time.

It combines verified posting liveness, existing Cognitive Pivot role scoring, and human-reviewed engineering responsibility signals. The mode does not predict hiring success, sponsorship approval, or actual team assignment after joining.

## Source Inventory

| Source | Path / Command | Used For |
|---|---|---|
| Repository conformance | `npm run verify` | Confirms repository conformance before submission. |
| Repository doctor | `npm run doctor` | Confirms runtime, command availability, domain directories, privacy, and recipe lifecycle status. |
| ATS scan dry run | `REALLOCATION_ENGINE_PORTALS=data/ats/portals.example.yml npm run ats:scan -- --dry-run` | Runs ATS scan without writing private data. |
| Posting liveness | `npm run ats:liveness -- <job-url>` | Verifies whether a specific posting is active, expired, or uncertain. |
| Role scorer | `npm run score -- data/examples/ch11-roles.json` | Runs existing sample role-quality scoring workflow. |
| Generated role-score report | `reports/generated/backend-authenticity-score-sample.md` | Human-readable role-score sample report generated during the worked run. |
| Example role input | `data/examples/ch11-roles.json` | Sample input used for the role scorer. |
| ATS example config | `data/ats/portals.example.yml` | Example ATS scan configuration used to avoid creating private scan data. |
| BLS/O*NET layer | `data/BLS/` and `data/bls/` where present | Existing role-quality evidence layer referenced by the scorer. |

## Proposed Additions

- [TODO: DEV] Add `scripts/role-authenticity/extract-backend-signals.mjs`. This script should parse job-description text and emit backend responsibility signals such as API ownership, database design, distributed systems, testing, CI/CD, observability, infrastructure, and production service ownership.

- [TODO: DATA SOURCE] Add `data/role-authenticity/backend-signal-rubric.json`. This rubric should define positive backend engineering signals, negative implementation/support signals, and neutral signals.

- [TODO: REPORT FIELD] Add `backend_responsibility_evidence` to generated human reports. Reader: F-1 software engineer evaluating whether to continue with an application. Decision enabled: Apply, Consider, Skip, or Refuse to Score.

## Phase Gates

### Gate 1 — Posting Liveness

Command: `npm run ats:liveness -- <job-url>`

Pass condition: posting returns `active`.

Fail condition: posting returns `expired`, `uncertain`, redirects to a generic careers page, or cannot be checked.

If this gate fails, stop. Do not produce a backend-authenticity classification.

### Gate 2 — Role Family Scope

Test: role title and description must indicate Software Engineer, Backend Engineer, Full Stack Engineer, Platform Engineer, Infrastructure Engineer, or similar production engineering work.

Fail condition: role is clearly product management, data analyst, sales engineering, support, customer success, or implementation-only work.

If this gate fails, mark the posting out of scope.

### Gate 3 — Role Quality Evidence

Command: `npm run score -- data/examples/ch11-roles.json`

Pass condition: scorer runs successfully and produces role-score output.

Fail condition: no role-quality evidence is available and no TODO is documented.

If this gate fails, continue only with a warning and do not claim Cognitive Pivot support.

### Gate 4 — Backend Responsibility Evidence

Test: human reviewer checks the job description for backend engineering responsibility signals.

Positive signals include APIs, services, databases, distributed systems, concurrency, performance, reliability, testing, CI/CD, cloud infrastructure, observability, and production ownership.

Negative signals include customer onboarding, configuration, support tickets, vendor integrations, demos, presales, documentation-only work, or implementation without ownership.

If evidence is insufficient, classify as `Refuse to Score` or `Consider with manual verification`.

### Gate 5 — Human Adequacy Review

A named human must review the verified outputs and decide whether the evidence is adequate. Model output may summarize evidence but cannot clear this gate.

## What This Mode Can Verify

This mode can verify:

- Whether repository conformance completed.
- Whether repository doctor completed.
- Whether ATS scan runs in dry-run mode using the example config.
- Whether a public job posting is active, expired, or uncertain according to `ats:liveness`.
- Whether the existing role scorer runs against sample role data.
- Whether the job description contains explicit backend engineering responsibility language.

## What This Mode Cannot Verify

This mode cannot verify:

- Whether the hiring team has active headcount.
- Whether the company will sponsor a specific candidate.
- Whether the day-to-day work after joining will match the posting.
- Whether a recruiter’s verbal description is accurate.
- Whether a live posting is actively reviewed.
- Whether backend-authenticity classification is correct without human review.

## Output Contract

### Agent Log JSON

```json
{
  "recipe": "case-backend-role-authenticity",
  "recipe_version": "0.1.0",
  "run_date": "YYYY-MM-DD",
  "mode": "sample",
  "input": {
    "job_url": "<public-job-url>",
    "company": "<company>",
    "role_title": "<role-title>"
  },
  "commands_run": [
    "npm run verify",
    "npm run doctor",
    "REALLOCATION_ENGINE_PORTALS=data/ats/portals.example.yml npm run ats:scan -- --dry-run",
    "npm run score -- data/examples/ch11-roles.json",
    "npm run ats:liveness -- <job-url>"
  ],
  "gates": {
    "posting_liveness": {
      "status": "pass|fail|unknown",
      "evidence": "<terminal-output-reference>"
    },
    "role_family_scope": {
      "status": "pass|fail|unknown",
      "evidence": "<title-and-description-evidence>"
    },
    "role_quality_sample": {
      "status": "pass|fail|unknown",
      "evidence": "<score-output-reference>"
    },
    "backend_responsibility_evidence": {
      "status": "pass|fail|unknown",
      "positive_signals": [],
      "negative_signals": []
    }
  },
  "classification": {
    "result": "apply|consider|skip|refuse_to_score",
    "verified_by_script": [],
    "human_judgment": [],
    "model_judgment": []
  },
  "limitations": []
}
```

### Human Report Markdown

| Field | Result |
|---|---|
| Company |  |
| Role title |  |
| Job URL |  |
| Posting liveness | Active / Expired / Uncertain |
| Role family scope | In scope / Out of scope |
| Role quality evidence | Available / Missing / Sample only |
| Backend engineering signals |  |
| Implementation/support signals |  |
| Classification | Apply / Consider / Skip / Refuse to Score |
| Verified by script |  |
| Human judgment |  |
| Cannot verify |  |
| Next action |  |

## Stop Conditions

Stop and refuse to classify when:

- Posting liveness returns expired or uncertain.
- Job URL is unavailable or redirects to a generic careers page.
- Job description text is unavailable.
- Role is outside software engineering.
- Classification would rely only on title keywords without responsibility evidence.
- The mode cannot separate verified script output from human or model judgment.
- Private candidate data would need to be committed to a tracked file.

## Log Template

```markdown
## YYYY-MM-DD — case-backend-role-authenticity v0.1.0

- **Runner:** <name>
- **Status:** RUNNABLE-SAMPLE
- **Inputs:** public job URL, role title, sample role-score input
- **Commands:** `npm run verify`; `npm run doctor`; `REALLOCATION_ENGINE_PORTALS=data/ats/portals.example.yml npm run ats:scan -- --dry-run`; `npm run score -- data/examples/ch11-roles.json`; `npm run ats:liveness -- <job-url>`
- **Outputs:** terminal output captured in worked run; role-score JSON/Markdown sample output
- **Result:** posting-liveness gate tested; sample role scorer ran; backend-authenticity classifier remains TODO and human-reviewed
- **Open issues:** implement backend signal extractor; add backend signal rubric; test across multiple SWE, implementation, and support postings
```