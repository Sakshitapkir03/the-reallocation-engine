# Domain Justification: Backend/Full-Stack OPT Sponsorship Triage

## User and Exact Situation

The user is an international master's graduate on F-1 post-completion OPT
(authorization end date 2027-02-20), self-assessed as eligible for the STEM
OPT extension but not yet DSO-confirmed. She is targeting entry-level
backend, full-stack, and AI-application software engineering roles in the
United States and will require future employer sponsorship. Her situation
is not generic "job seeker" triage: she needs to decide, for one posting at
a time, whether the posting clears a minimum evidence bar before she spends
scarce application and interview effort on it, given a fixed OPT clock and
an early-career technical profile (work-proven evidence at Humanitarians AI
and MR SON Equipments; project-proven evidence in Eventopia and a Document
Parser RAG system; no evidence approaching several years of full-time
engineering experience).

## Information Asymmetry

The candidate cannot easily see, from a job posting alone: whether the
posting is still genuinely live or has gone stale while remaining
reachable; whether the employer has any sponsorship history at all, and
whether that history is current or years old; whether a stated experience
requirement is a hard filter or a soft preference; whether the SOC-level
occupation behind the title is durable, cognitively demanding work or
lower-value implementation work; and whether applying is rational given her
specific OPT end date and unresolved STEM eligibility, as opposed to a
generic assumption that "more applications is always better." Each of these
facts is knowable in principle, from a public data source or a repeatable
script, but not visible to the candidate without deliberately checking.

## Engine Layer Connection

Job-Ops contributes the posting-liveness check. In this recipe, liveness is
tested with the repository's real `ats:liveness` script (Playwright-based),
not assumed. A posting that returns active is treated differently from one
that returns expired or "insufficient content" -- the recipe never lets a
strong sponsorship or technical-fit signal override a failed liveness gate.

80 Days to Stay contributes the sponsorship-evidence layer, via the mapped
SEC/H-1B dataset (`SEC_DOL_H1b_data_mapped.csv`). This recipe treats a
missing row as a data gap, not as evidence the employer will not sponsor --
94.9% of that dataset's rows have no H-1B field populated, so absence is the
common case, not a red flag by itself.

Cognitive Pivot contributes SOC-level role-quality context via the BLS/O*NET
compact table (`soc_occupation_compact.csv`), including a `cognitive_pivot_score`
for the matched occupation. This recipe uses that score only to describe the
occupation in general, never to describe the quality of the specific
employer or posting.

## Domain-Specific Failure Modes

1. Employer-name collision or subsidiary mismatch. A sponsorship record for
a similarly named or parent company can be incorrectly attributed to the
employer named in a posting. This is hardest for an international candidate
to catch because a recognizable brand name creates a false sense that
sponsorship is proven, when in fact the dataset row belongs to an unrelated
company. In this recipe's own worked run, eleven companies whose names
begin with "Scale" appeared in the sponsorship CSV, and none of them were
the employer behind the posting being evaluated -- a candidate skimming
quickly could easily have mis-attributed one of those rows to the real
employer. The candidate is the one harmed: a false positive here leads her
to over-trust a sponsorship signal that does not actually apply to the role
she is considering.

2. Technical-title mismatch against a stated experience floor. A posting
titled "Software Engineer" can carry a hard, explicit minimum-experience
requirement (for example, several years of full-time engineering work
post-graduation) that is easy to miss if a candidate is scanning for
keyword overlap in the required stack rather than reading the experience
requirement itself. This is difficult for an early-career candidate to
catch because the technology stack can look like a strong match even when
the seniority bar quietly disqualifies the candidate. The candidate is the
one harmed here too: time spent tailoring an application or preparing for
an interview against a role she was never eligible for, at the direct cost
of OPT-clock time she cannot get back.

3. HTTP-live but operationally unclear postings across ATS platforms. A
posting can return a fully rendered, working application form when fetched
directly, while not being confirmed present through the employer's own
current listings, or while a generic liveness heuristic misclassifies the
page as "insufficient content" because the platform renders content
client-side. This recipe's own break-test, run against an ADP
Workforce-Now-hosted posting, produced exactly this ambiguity: the
liveness script correctly refused to classify the posting rather than
guessing, but it could not distinguish "this job is genuinely gone" from
"this specific tool cannot parse this specific ATS's rendering." The
candidate is again the one harmed if this ambiguity gets silently resolved
in either direction -- treating an unparseable-but-real posting as dead
wastes a real opportunity, while treating a genuinely dead posting as live
wastes application effort on a role that no longer exists.
