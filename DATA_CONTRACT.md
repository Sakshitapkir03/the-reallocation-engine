# Data Contract

This document defines which files are source material, maintained system code,
generated outputs, book content, and private/user-specific work for The
Reallocation Engine.

## Maintained System Layer

These files are part of the repo's maintained data-processing system.

| Path | Purpose |
|---|---|
| `scripts/` | Canonical scripts for SEC, ATS, audit, and enrichment workflows. |
| `scripts/sec/` | Maintained SEC Form D pipeline. |
| `scripts/ats/` | Maintained ATS detection, provider, scanner, and liveness pipeline. |
| `package.json` | Node runtime dependencies for book/script utilities. |

Rule: prefer adding new automation here, not as loose one-off scripts in `data/`.

## Source Data Layer

These files are source or upstream reference data. Treat them as provenance.

| Path | Purpose |
|---|---|
| `data/80-days-to-stay/` | Upstream 80 Days to Stay data and scripts. |
| `data/bls/` | BLS source/reference data. |
| `data/sec/form-d/raw/` | Downloaded SEC quarter ZIP files. |
| `data/sec/form-d/extracted/` | Extracted SEC quarter TSV files. |

Rule: do not casually rewrite upstream source data. Copy/adapt useful code into
`scripts/` and document the provenance.

## Generated Data Layer

These files are produced by maintained scripts and can be regenerated.

| Path | Purpose |
|---|---|
| `data/sec/form-d/processed/` | Processed SEC quarterly JSON and audits. |
| `data/ats/` | ATS scanner inputs/outputs, scan history, and job pipeline files. |
| `*-audit.md` | Markdown audit reports written next to the data they inspect. |

Rule: large generated files should be split, compressed, moved out of git, or
kept under GitHub size limits before committing.

## Book Content Layer

These files are editorial material for the book/repo.

| Path | Purpose |
|---|---|
| `book.md` | Main manuscript entry point. |
| `chapters/` | Chapter files. |
| `outline.md`, `vision.md`, `risks.md`, `architecture.md` | Planning and architecture notes. |
| `images/`, `d3/`, `styles/` | Book visuals and presentation assets. |
| `pantry/` | Research pantry for curated material before it becomes manuscript text. |

Rule: scripts should support the book, but generated data should not be mixed
into manuscript folders.

## Private/User-Specific Layer

These files should not be assumed safe to publish.

| Path | Purpose |
|---|---|
| `.env*` | API keys, credentials, deployment config. |
| `data/ats/applications.md` | Personal application tracker if created. |
| `data/ats/pipeline.md` | Job pipeline output that may contain user-specific targets. |
| `data/ats/scan-history.tsv` | Scan history that may reveal target companies or job search activity. |

Rule: check privacy and size before committing generated ATS/job-search files.

## Operating Rules

- Put maintained automation in `scripts/`.
- Put audit reports next to the data they audit, using `-audit.md`.
- Keep upstream source folders intact for provenance.
- Do not rebuild source datasets from scratch when a mapped or processed asset
  already exists.
- Avoid committing files over GitHub's practical size limits; split or move
  large files before publishing.

---

## TrueRate Remittance Cost Audit — addition (2026-08-11)

*Appended by the `truerate-remittance-cost-audit` contribution. Domain
note: this is a personal-finance transparency tool, not a job-search/
visa-evidence component — see `PR_DESCRIPTION.md` for the full disclosure
of that mismatch. The table below follows this file's existing
verified-vs-inferred convention.*

| Field | Label | Detail |
|---|---|---|
| Mid-market USD/INR rate (snapshot) | record | 6-source corroborated median, fetched via web research 2026-08-09. One conflicting source found and excluded — see `reports/generated/truerate-plausibility-audit.md`. |
| Mid-market USD/INR rate (live) | external-source | Calls `api.frankfurter.dev`; written but unexecuted end-to-end in the build sandbox (no network to install `httpx`). |
| Wise fee structure (0.66% + $1.70) | record | Secondary source (feeprobe.com) citing Wise's own published pricing, dated 2026-05-22. |
| Remitly fee/markup range (0.4%–1.4%) | model-inference bounded by record | Sourced from a competitor's (Wise's) published analysis of Remitly — a real conflict-of-interest caveat, named explicitly in `scripts/tools/truerate_logic.py`. |
| Historical 14-day USD/INR sample | script-output derived from record | Derived from real ECB/Frankfurter cross-rates fetched during this build; small sample, explicitly not a full-history claim. |
| Timing analysis statistics | script-output | Deterministic computation over the record above; no forecasting. |
| Wise volume-discount tiers | missing | Known to exist, not modeled — see the recipe's "Cannot Verify Without More Work" section. |
| Rate staleness auto-block | missing | Currently only raises a flag (Step 4); does not block the run. Named as an open TODO on the recipe. |

**Ethics gate for this addition:** No personal transfer data, account
numbers, or names are stored anywhere in this contribution. Run
`python3 scripts/tools/truerate-verify-provenance.py` to re-check source
presence before trusting any number this recipe reports.
