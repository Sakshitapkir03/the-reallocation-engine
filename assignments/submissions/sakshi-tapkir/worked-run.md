# Worked Run

## Mode

case-backend-role-authenticity

## Lifecycle Status

RUNNABLE-SAMPLE

## Scenario

This worked run evaluates a proposed workflow for determining whether a Software Engineer job posting represents genuine backend engineering work before an international software engineer on F-1 OPT invests significant time in applications, recruiter conversations, online assessments, and technical interviews.

The workflow combines existing Reallocation Engine scripts with a proposed backend-authenticity workflow. Existing repository scripts provide verified evidence for repository integrity, ATS scanning, posting liveness, and role-quality scoring. The proposed backend-authenticity classifier remains a future enhancement and therefore stays as human-reviewed rather than verified automation.

---

# Inputs Used

| Input | Source |
|-------|--------|
| Sample role dataset | `data/examples/ch11-roles.json` |
| ATS example configuration | `data/ats/portals.example.yml` |
| Public Amazon Software Development Engineer posting | https://www.amazon.jobs/en/jobs/3175845/software-development-engineer-2026 |
| Deliberate break-test URL | https://example.com/not-a-real-job |

---

# Commands Run and Terminal Output

## 1. Repository Verification

```bash
npm run verify
```

```text
> the-reallocation-engine@1.0.0 verify
> node scripts/conformance.mjs && node scripts/manifest-check.mjs

conformance: 132 files (76 md · 30 py · 23 js · 1 sh · 1 yaml · 1 json)
✓ all conform (machine half of P4). Adequacy is still the human gate.

MANIFEST CHECK — The Reallocation Engine
==========================================

WARN (4):
  W1 ignore path not in .gitignore: output/
  W1 ignore path not in .gitignore: reports/generated/
  W1 ignore path not in .gitignore: archive/
  W2 private path not gitignored (PII/secret risk): private/

✓ manifest check passed (4 warnings)
```

---

## 2. Repository Doctor

```bash
npm run doctor
```

```text
> the-reallocation-engine@1.0.0 doctor
> node scripts/doctor.mjs

RECIPE DOCTOR — The Reallocation Engine
==========================================

ENVIRONMENT (required)
  ✓ node       v20.20.0
  ✓ python3    Python 3.9.6

ENVIRONMENT (optional — features degrade without these)
  ✓ pandoc     pandoc 3.6.3
  — libreoffice not found (PDF fallback)
  ✓ playwright installed

RUNNABLE COMMANDS (npm script → target file present?)
  ✓ verify         scripts/conformance.mjs
  ✓ manifest-check scripts/manifest-check.mjs
  ✓ eval:score     scripts/eval/score-run.mjs
  ✓ eval:report    scripts/eval/report.mjs
  ✓ doctor         scripts/doctor.mjs
  ✓ build-instructions scripts/build-instructions.mjs
  ✓ to-markdown    scripts/to-markdown.mjs
  ✓ score          scripts/score/role-scorer.mjs
  ✓ ats:dedup      scripts/ats/dedup-tracker.mjs
  ✓ ats:liveness   scripts/ats/check-liveness.mjs
  ✓ ats:merge      scripts/ats/merge-tracker.mjs
  ✓ ats:normalize  scripts/ats/normalize-statuses.mjs
  ✓ ats:scan       scripts/ats/scan.mjs
  ✓ ats:verify     scripts/ats/verify-pipeline.mjs
  ✓ resumes:pdf    scripts/resumes/generate-pdf.mjs
  ✓ svg-to-png     scripts/svg-to-png.mjs
  ✓ audit:layout   scripts/svg-layout-audit.mjs
  ✓ postsvg-to-png scripts/svg-layout-audit.mjs

DOMAIN DIRECTORIES
  ✓ data/sec
  ✓ data/bls
  ✓ data/ats
  ✓ data/80-days-to-stay
  ✓ scripts/sec
  ✓ scripts/bls
  ✓ scripts/ats
  ✓ scripts/resumes

PRIVACY (no personal data committed)
  ✓ no private/PII paths are tracked

RECIPES (43)
  with lifecycle frontmatter: 43   missing: 0
  by status: DRAFT 42 · RUNNABLE-SAMPLE 1
  open TODOs: 520 declared (in frontmatter) · 520 [TODO markers in bodies

SUMMARY
  environment: ✓ runnable
  recipes: 43/43 carry lifecycle frontmatter — all tracked
  next: continue
```

---

## 3. ATS Scan (Dry Run)

```bash
REALLOCATION_ENGINE_PORTALS=data/ats/portals.example.yml npm run ats:scan -- --dry-run
```

```text
> the-reallocation-engine@1.0.0 ats:scan
> node scripts/ats/scan.mjs --dry-run

Scanning 1 companies via providers (0 local parser; 0 skipped — no provider matched)
(dry run — no files will be written)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Portal Scan — 2026-07-05
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Companies scanned:     1
Total jobs found:      792
Filtered by title:     350 removed
Filtered by location:  391 removed
Duplicates:            1 skipped
New offers added:      50
```
```text
New offers:
  + Databricks | AI Engineer - FDE (Forward Deployed Engineer) | Remote - India
  + Databricks | Delivery Solutions Architect - Communications, Media, Entertainment & Games | United States
  + Databricks | Director, AI Forward Deployed Engineering (FDE) | United States
  + Databricks | Director, Lakebase Sales Specialists - Retail | United States
  + Databricks | Forward Deployed Engineer | Remote - India
  + Databricks | Forward Deployed Engineer - FDE (Fullstack) - Digital Native Business  | United States
  + Databricks | Lakebase Sales Specialist - Retail | United States
  + Databricks | Manager, Field Engineering - Strategic Digital Native Business | Remote - California; Remote - Colorado; Remote - Oregon; Remote - Washington
  + Databricks | Manager, Forward Deployed Engineering - CMEG | Remote - Washington D.C.
  + Databricks | Manager, Forward Deployed Engineering - Manufacturing | Remote - California
  + Databricks | Pre-sales Manager, Field Engineering - Named Accounts | Remote - Denmark
  + Databricks | Product Marketing Director, AI | United States
  + Databricks | Product Marketing Director, Lakewatch | United States
  + Databricks | RVP, Retail | United States
  + Databricks | Senior Manager, Forward Deployed Engineering (Full Stack) x 2 New roles | Remote - France
  + Databricks | Senior Solutions Engineer | Aarhus, Denmark; Remote - Denmark
  + Databricks | Senior Specialist Solutions Architect - AI & ML Engineer | Finland; Remote - Denmark; Stockholm, Sweden
  + Databricks | Solutions Architect, Retail  | Remote - Ohio
  + Databricks | Solutions Architect, Retail - CPG | Central - United States
  + Databricks | Solutions Architect - Strategic AI Natives | Remote - California; Remote - Colorado; Remote - Oregon; Remote - Washington
  + Databricks | Specialist Solutions Architect - AI/ML | United States
  + Databricks | Specialist Solutions Architect - Data Engineering & Warehousing | United States
  + Databricks | Specialist Solutions Architect - Data Warehousing (Healthcare & Life Sciences) | Northeast - United States
  + Databricks | Sr. Delivery Solutions Architect - AI Native | Remote - California; Remote - Colorado; Remote - Oregon; Remote - Washington
  + Databricks | Sr. Director, Enterprise - Retail Vertical - Strategic Accounts  | Remote - New York
  + Databricks | Sr. Director, Field Engineering (Lakebase) | United States
  + Databricks | Sr. Engagement Manager, Forward Deployed Engineering - LATAM | Remote - Mexico 
  + Databricks | Sr. Field Technical Program Manager, Forward Deployed Engineering | United States
  + Databricks | Sr Forward Deployed Engineer | Remote - India
  + Databricks | Sr. Forward Deployed Engineer - Communications, Media, Entertainment & Games | United States
  + Databricks | Sr. Forward Deployed Engineer - Financial Services | Central - United States
  + Databricks | Sr. Forward Deployed Engineer - Public Sector | Central - United States; Northeast - United States; Southeast - United States
  + Databricks | Sr. Manager, Field Engineering - Digital Native Business | Colorado; Remote - California; Remote - Oregon; Remote - Washington
  + Databricks | Sr. Manager, Field Engineering - Lakebase | Atlanta, Georgia; Chicago, Illinois; Dallas, Texas; New York City, New York; San Francisco, California; United States
  + Databricks | Sr. Manager, Field Engineering (Specialist) - HCLS | Northeast - United States
  + Databricks | Sr. Product Marketing Manager, Lakebase | United States
  + Databricks | Sr Security Engineer, Incident Response | Belgium; Finland; Remote - Denmark; Remote - France; Remote - Germany; Remote - Netherlands; Remote - Spain; Remote - Sweden; Remote - United Kingdom; Switzerland
  + Databricks | Sr. Solutions Architect - AI Natives Business | Remote - California; Remote - Oregon; Remote - Washington
  + Databricks | Sr. Solutions Architect, Retail | West Coast - United States
  + Databricks | Sr. Solutions Architect, Retail  | Northeast - United States
  + Databricks | Sr. Solutions Engineer | United States
  + Databricks | Sr. Solutions Engineer - AI Natives Business | Remote - California; Remote - Colorado; Remote - Oregon; Remote - Washington
  + Databricks | Sr. Specialist Solutions Architect - Data Engineering & Warehousing | United States
  + Databricks | Sr. Staff Product Security Engineer | United States
  + Databricks | Sr. Technical Marketing Engineer - Lakebase/Apps | United States
  + Databricks | Staff Enterprise Security Engineer | Remote - California
  + Databricks | Staff Security Assurance Engineer  | Remote - Washington D.C.; Washington, D.C.
  + Databricks | Staff Security Detection Engineer  | United States
  + Databricks | Strategic Core Account Executive - Retail  | Remote - Ohio
  + Databricks | Strategic Genie and AI Sales Specialist | Remote - New York

(dry run — run without --dry-run to save results)

Review new offers in data/ats/pipeline.md.

---

## 4. Sample Role Scoring

```bash
npm run score -- data/examples/ch11-roles.json
```

```text
> the-reallocation-engine@1.0.0 score
> node scripts/score/role-scorer.mjs data/examples/ch11-roles.json

✓ scored 5 roles → Apply 2 · Consider 1 · Skip 2 (skip 40%)
  data/examples/role-scores.json  +  data/examples/role-scores.md
```

---

## 5. Human Report Generation

```bash
npm run score -- data/examples/ch11-roles.json --out-dir reports/generated --md reports/generated/backend-authenticity-score-sample.md
```

```text
> the-reallocation-engine@1.0.0 score
> node scripts/score/role-scorer.mjs data/examples/ch11-roles.json --out-dir reports/generated --md reports/generated/backend-authenticity-score-sample.md

✓ scored 5 roles → Apply 2 · Consider 1 · Skip 2 (skip 40%)
  reports/generated/role-scores.json  +  reports/generated/backend-authenticity-score-sample.md
```

---

## 6. Posting Liveness Check (Successful Run)

```bash
npm run ats:liveness -- "https://www.amazon.jobs/en/jobs/3175845/software-development-engineer-2026"
```

```text
> the-reallocation-engine@1.0.0 ats:liveness
> node scripts/ats/check-liveness.mjs https://www.amazon.jobs/en/jobs/3175845/software-development-engineer-2026

Checking 1 URL(s)...

✅ active     https://www.amazon.jobs/en/jobs/3175845/software-development-engineer-2026

Results: 1 active  0 expired  0 uncertain
```

---

## 7. Posting Liveness Check (Deliberate Break Test)

```bash
npm run ats:liveness -- "https://example.com/not-a-real-job"
```

```text
> the-reallocation-engine@1.0.0 ats:liveness
> node scripts/ats/check-liveness.mjs https://example.com/not-a-real-job

Checking 1 URL(s)...

❌ expired    https://example.com/not-a-real-job
           HTTP 404

Results: 0 active  1 expired  0 uncertain
```

---

# Verified vs. Inferred

The Reallocation Engine requires a clear separation between evidence produced by verified scripts and judgments that require human interpretation.

## Verified by Repository Scripts

The following facts were established directly by repository commands:

| Evidence | Verification Source |
|----------|----------------------|
| Repository conforms to project standards | `npm run verify` |
| Repository environment is runnable | `npm run doctor` |
| ATS scan executed successfully using the example configuration | `npm run ats:scan -- --dry-run` |
| ATS scan found 792 postings and filtered them according to configured rules | ATS scan output |
| Sample role scorer executed successfully | `npm run score` |
| Sample role scorer classified 5 example roles as Apply (2), Consider (1), and Skip (2) | Role scorer output |
| Amazon Software Development Engineer posting was active | `npm run ats:liveness` |
| Invalid URL returned HTTP 404 and was correctly classified as expired | Deliberate break test |

---

## Human Judgment

The following decisions require human interpretation and are **not verified by existing repository scripts**:

- Whether the Software Development Engineer posting represents genuine backend engineering work.
- Whether the engineering responsibilities demonstrate production backend ownership.
- Whether backend engineering signals outweigh implementation, consulting, or customer-facing responsibilities.
- Whether the posting should ultimately be classified as **Apply**, **Consider**, **Skip**, or **Refuse to Score**.

These judgments remain outside the verified layer until the proposed backend-authenticity extractor and rubric are implemented.

---

# Verification

The workflow was verified using multiple checks.

1. Repository conformance was confirmed using `npm run verify`.

2. Repository health and runtime availability were confirmed using `npm run doctor`.

3. ATS scanning was executed in `--dry-run` mode so that no private application data or tracker files were modified.

4. The role scorer was executed twice:
   - once using the default output location;
   - once generating a human-readable report in `reports/generated/backend-authenticity-score-sample.md`.

   Both executions produced identical classification results.

5. Posting liveness was verified using a known public Amazon Software Development Engineer job posting.

6. A deliberate failure case was tested using a non-existent URL (`https://example.com/not-a-real-job`) to confirm that the liveness gate correctly detects expired postings.

---

# Reflection

The existing Reallocation Engine already provides strong evidence-first tooling for repository verification, ATS scanning, posting liveness, and role-quality scoring. These existing scripts form the verified foundation of this mode.

The primary limitation is that backend engineering authenticity cannot yet be verified automatically. Current repository scripts cannot distinguish between genuine backend engineering work and technical implementation, consulting, customer-facing engineering, or solutions engineering roles that use similar job titles.

The proposed backend-authenticity workflow addresses this gap by introducing structured responsibility analysis while maintaining the Reallocation Engine principle that human judgment clears the final gate. The next development step is implementing the proposed backend responsibility extractor together with a standardized backend-authenticity rubric so that verified repository evidence and structured responsibility signals can be combined without replacing human review.

---

# Attestation

- **Recipe:** case-backend-role-authenticity v0.1.0
- **By:** Sakshi Tapkir
- **Date:** 2026-07-05

## Tested

| Ran | Saw | Expected |
|-----|-----|----------|
| `npm run verify` | Repository passed conformance | Expected |
| `npm run doctor` | Repository environment runnable | Expected |
| `npm run ats:scan -- --dry-run` | Successfully scanned Databricks postings using example configuration | Expected |
| `npm run score -- data/examples/ch11-roles.json` | Apply 2 · Consider 1 · Skip 2 | Expected |
| `npm run ats:liveness -- "https://www.amazon.jobs/en/jobs/3175845/software-development-engineer-2026"` | Posting reported as Active | Expected |
| `npm run ats:liveness -- "https://example.com/not-a-real-job"` | HTTP 404 returned and posting classified as Expired | Expected |

---

## Did Not Test

- Backend responsibility extraction script (not yet implemented).
- Backend authenticity rubric (proposed data source).
- Classification across multiple ATS providers.
- Sponsorship history integration into backend-authenticity scoring.
- Live production workflow using private applicant tracking data.

---

## Broke During Testing, Fixed

During the first execution of the posting-liveness workflow, Playwright browsers were not installed locally and the command failed.

The issue was resolved by installing the required browsers using:

```bash
npx playwright install
```

The liveness checks were then executed again successfully, and both the valid and deliberately invalid job URLs produced the expected results.

---

# Summary

This worked run demonstrates that the proposed **Backend Role Authenticity** mode successfully integrates existing Reallocation Engine capabilities for repository verification, ATS scanning, posting liveness, and Cognitive Pivot role scoring. The mode intentionally leaves backend-authenticity classification as a human-reviewed decision until the proposed extractor and rubric are implemented, maintaining the evidence-first philosophy of the Reallocation Engine.