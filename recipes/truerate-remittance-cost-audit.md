---
status: DRAFT
todos_open: 2
last_gate: null
attestation: null
recipe_version: 0.1.0
---

# TrueRate Remittance Cost Audit

## Purpose

Compares the real mid-market USD/INR exchange rate against what named
remittance providers (Wise, Remitly) would likely deliver after fees, for
a given transfer amount, and reports a backward-looking analysis of
whether waiting has historically helped. Built for international students
sending money between the US and India who want to see the real cost of
a transfer stated as a number, not buried inside an advertised rate.

**Domain note, read before anything else:** unlike this repo's other
recipes, this one does not evaluate a job, a sponsor, or an application —
it is a personal-finance transparency tool, unrelated to the engine's
job-search/visa-evidence purpose. It follows this repo's recipe contract
and folder conventions as closely as honestly possible, but does not
close a gap named in *The Reallocation Engine* book or its chapters. See
`PR_DESCRIPTION.md` for the full disclosure.

## Source Inventory

| Source Node | Node Type | Source URL or Path | Human Check |
|---|---|---|---|
| Mid-market rate corroboration | file | `reports/generated/truerate-plausibility-audit.md` | Confirm the 6-source median is still reasonably current before trusting a comparison. |
| Wise fee schedule | inline citation | `scripts/tools/truerate_logic.py::PROVIDER_FEE_STRUCTURES["Wise"]` | Confirm Wise's published pricing hasn't changed since `verified_date` (2026-05-22). |
| Remitly fee/markup range | inline citation | `scripts/tools/truerate_logic.py::PROVIDER_FEE_STRUCTURES["Remitly_Economy"]` | Confirm this is a competitor-sourced estimate, not Remitly's own disclosure — real conflict-of-interest caveat. |
| Historical USD/INR sample | inline data | `scripts/tools/truerate_logic.py::HISTORICAL_USD_INR_SAMPLE` | Confirm this is a 14-day real sample, not a full-history claim, before trusting the timing percentage. |

## Inputs

| Input | Type | Source | Required? |
|---|---|---|---|
| amount_usd | number | Run envelope (`data/raw/truerate-remittance-cost-audit/run-envelope.json`) | Yes |
| providers | list of strings | Run envelope; must match keys in `PROVIDER_FEE_STRUCTURES` | Yes |
| horizon_days | integer | Run envelope; must be less than the historical sample length (14) | Yes |

## Phase Gates

1. **Source gate:** All cited sources in Source Inventory exist and parse. Test: `python3 scripts/tools/truerate-verify-provenance.py`. Human capacity: confirm sources are still accurate, not just present.
2. **Scope gate:** The run declares `sample_mode: true` or an approved live mode before ingest begins. Test: `python3 -m json.tool data/raw/truerate-remittance-cost-audit/run-envelope.json`.
3. **Data-shape gate:** The ingested record has required fields, correct types, sane ranges. Test: `python3 scripts/gigo/truerate-validate-data-shape.py`.
4. **Quality-check gate:** Every requested provider is a known, sourced provider; staleness is flagged. Test: `python3 scripts/gigo/truerate-transform-quality-check.py`.
5. **Approval gate:** N/A for this recipe in its current form — no live network calls, external writes, credentials, or sensitive data are involved; everything is a pure computation over local, already-sourced data. If the live rate path (`get_mid_market_rate_live`) is ever wired in, this gate becomes required and is not yet implemented — see Stop Conditions.
6. **Report gate:** Agent log and human report are written with the required fields and sections. Test: `test -f logs/truerate-remittance-cost-audit-[DATE].json && test -f reports/generated/truerate-remittance-cost-audit-[DATE].md`.

## Steps

1. **Verify provenance.** Labor: script, no human gate needed (read-only check).
   Script: `scripts/tools/truerate-verify-provenance.py`
   Input: none (checks inline-cited sources in `truerate_logic.py`)
   Output: source_paths, exists, parsed_ok, checked_at, checks (per-fact detail)
   Where output goes: `logs/truerate-remittance-cost-audit-verify-provenance.json`

2. **Ingest declared inputs.** Labor: script, no human gate needed.
   Script: `scripts/ingest/truerate-ingest-inputs.py <run-envelope.json>`
   Input: a run envelope JSON with `amount_usd`, `providers`, `horizon_days`, `sample_mode`
   Output: records, source_name, source_type, fetched_at, sample_mode, rejects
   Where output goes: `data/raw/truerate-remittance-cost-audit/`

3. **Validate data shape.** Labor: script, no human gate needed.
   Script: `scripts/gigo/truerate-validate-data-shape.py`
   Input: Step 2's output
   Output: record_count, required_fields_present, missing_fields, parse_errors, schema_version
   Where output goes: `data/verified/truerate-remittance-cost-audit/`

4. **Transform and quality check.** Labor: script, no human gate needed.
   Script: `scripts/gigo/truerate-transform-quality-check.py`
   Input: Step 2's output
   Output: verified_records, record_count, duplicates, rejects, flags, quality_notes
   Where output goes: `data/verified/truerate-remittance-cost-audit/`

5. **Run approved tools.** Labor: script, no human gate needed (pure computation, no external action).
   Script: `scripts/tools/truerate-run-approved-tools.py`
   Input: Step 4's output
   Output: mid_market, comparisons (per-provider), timing, computed_at
   Where output goes: `data/verified/truerate-remittance-cost-audit/comparison-result.json`

6. **Produce human report.** Labor: script; human reads before acting on the result.
   Script: `scripts/tools/truerate-produce-human-report.py`
   Input: Step 5's output + Step 1 and Step 4's outputs
   Output: summary, sources_checked, gate_results, findings, todo_items, decision recommendation
   Where output goes: `reports/generated/` (Markdown) and `logs/` (JSON)

## Output Contract

### Agent output
File: `logs/truerate-remittance-cost-audit-[DATE].json`
Fields: workflow, run_id, mode, steps_completed, records_seen, rejects, duplicates, flags, stop_conditions, todo_items, source_files, gate_decisions, generated_at, raw_output_paths, verified_output_paths, report_path.

### Human report
File: `reports/generated/truerate-remittance-cost-audit-[DATE].md`
Reader: the student (or a reviewer) deciding whether to act on this comparison.
Decision enabled: which provider looks cheaper for this amount, given published fee schedules; whether the timing sample says anything trustworthy about waiting.
Sections: run summary, purpose, source inventory, phase-gate results, records seen/rejects/flags, verified findings, inferred findings, decision recommendation.

## Stop Conditions

- Stop if a cited source in Source Inventory cannot be found (Step 1 gate fails) — do not proceed with a comparison built on an unverifiable fact.
- Stop if an unknown provider is requested (not in `PROVIDER_FEE_STRUCTURES`) — never guess a fee structure.
- Stop if `horizon_days` >= the historical sample length (14 days) — the timing analysis will return a labeled error rather than a fabricated statistic.
- - `[TODO: DEV]` Not yet implemented: an automatic block when the mid-market snapshot is more than 24 hours stale. Currently this only raises a `flag` in Step 4's output; a human reading the report must notice it.
- Stop before presenting the timing percentage as advice ("so I should wait") — the recipe's own `honest_framing` field exists specifically so this never gets stripped out before reaching a reader.

## Snickerdoodle

**Honest disclosure, found during this build:** `snickerdoodle` is not an
installed or runnable CLI in this repo (`which snickerdoodle` → not
found; `npx snickerdoodle --help` → cannot resolve). The reference recipe
`case-h1b-sponsorship-audit.md` includes a full "Snickerdoodle Run
Commands" section for this same non-existent tool. This is a real,
pre-existing gap in the repo's own documentation, not something
introduced by this recipe — named here rather than silently repeated. The
section below documents the intended convention for consistency with the
other 43 recipes, but every command in it is aspirational, matching the
the "TODO: DEV" placeholder pattern used elsewhere in this repo for not-yet-implemented tooling.

### Run Commands (aspirational — snickerdoodle does not exist yet; run the real scripts below instead)
```
snickerdoodle run truerate-remittance-cost-audit --mode sample
```
**Actually runnable today:**
```bash
python3 scripts/tools/truerate-verify-provenance.py
python3 scripts/ingest/truerate-ingest-inputs.py data/raw/truerate-remittance-cost-audit/run-envelope.json
python3 scripts/gigo/truerate-validate-data-shape.py
python3 scripts/gigo/truerate-transform-quality-check.py
python3 scripts/tools/truerate-run-approved-tools.py
python3 scripts/tools/truerate-produce-human-report.py
```

### Script Locations

| Step | Script Path | Layer |
|---|---|---|
| Verify provenance | `scripts/tools/truerate-verify-provenance.py` | tools |
| Ingest declared inputs | `scripts/ingest/truerate-ingest-inputs.py` | ingest |
| Validate data shape | `scripts/gigo/truerate-validate-data-shape.py` | gigo |
| Transform and quality check | `scripts/gigo/truerate-transform-quality-check.py` | gigo |
| Run approved tools | `scripts/tools/truerate-run-approved-tools.py` | tools |
| Produce human report | `scripts/tools/truerate-produce-human-report.py` | tools |

### Output Locations

| Output | Path | Format |
|---|---|---|
| Raw ingest | `data/raw/truerate-remittance-cost-audit/` | JSON |
| Verified data | `data/verified/truerate-remittance-cost-audit/` | JSON |
| Agent log | `logs/truerate-remittance-cost-audit-[DATE].json` | JSON |
| Human report | `reports/generated/truerate-remittance-cost-audit-[DATE].md` | Markdown |

## Provenance

| Source | Verification command | Notes |
|---|---|---|
| Mid-market rate corroboration | `cat reports/generated/truerate-plausibility-audit.md` | 6-source median; one conflicting source found and excluded during this build. |
| Wise fee schedule | `grep -A3 '"Wise"' scripts/tools/truerate_logic.py` | Published, dated 2026-05-22. |
| Remitly fee/markup range | `grep -A5 'Remitly_Economy' scripts/tools/truerate_logic.py` | Competitor-sourced range, not Remitly's own disclosure. |
| Historical USD/INR sample | `grep -A20 'HISTORICAL_USD_INR_SAMPLE' scripts/tools/truerate_logic.py` | Real 14-day sample derived from api.frankfurter.dev during this build. |

## Existing Recipe Notes Preserved For Implementation

### Known Evidence From This Build
- Mid-market rate: 95.20 INR/USD, corroborated across 6 sources, as_of 2026-08-09.
- Wise hidden cost on $1,000: 0.83%. Remitly: 0.4%–1.4% (range).
- 14-day real historical sample; 85.7% of 7-day waits helped in that window (not generalizable).

### Cannot Verify Without More Work
- Whether a live authenticated quote from either provider matches these estimates today.
- Whether a longer (multi-year) historical sample changes the timing conclusion.
- Whether the FastAPI HTTP wrapper (if built) behaves correctly when actually started — unverified in the build sandbox (no network to install FastAPI).

### Proposed Or Missing Tools
- `scripts/tools/truerate-check-staleness.py` — would implement the automatic staleness block named as a Stop Condition but not yet built.
- - `[TODO: DEV]` `scripts/tools/truerate-fetch-live-rate.py` — would call `api.frankfurter.dev` for a real live rate; written in `truerate_logic.py::get_mid_market_rate_live` but never executed end-to-end.
