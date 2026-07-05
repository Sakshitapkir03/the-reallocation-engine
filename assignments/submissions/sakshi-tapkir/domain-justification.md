---

## Phase 3 — Fill `domain-justification.md`

Paste this:

```markdown
# Domain Justification: Backend Role Authenticity

## User and Situation

This mode is for international software engineers on F-1 OPT who are applying to Software Engineer, Backend Engineer, Full Stack Engineer, and Platform Engineer roles in the United States. The specific situation is a candidate with limited OPT time and limited interview capacity deciding whether a posting is worth pursuing before investing application time, recruiter time, and technical interview preparation.

The mode is intentionally narrower than a general job-search triage workflow. It does not primarily ask whether the company is attractive or whether the candidate can get hired. It asks whether the posting contains enough evidence that the work is genuine backend engineering rather than implementation, support, consulting, or customer-facing technical work under a software engineering title.

## Information Asymmetry

The hidden information is that job titles do not reliably describe day-to-day engineering work. Many postings use titles such as Software Engineer, AI Engineer, Full Stack Engineer, or Solutions Engineer while the responsibilities may be closer to customer implementation, vendor configuration, support escalation, documentation, demos, or presales. This is difficult for early-career international candidates to catch because they often rely heavily on title keywords and may not discover the mismatch until after recruiter calls or technical rounds.

For an F-1 OPT candidate, that mismatch is expensive. Application and interview time is scarce, and spending several rounds on a role that does not build the intended backend engineering career path is a real opportunity cost.

## Engine Layer Connection

This mode connects to Job-Ops through ATS scan and posting-liveness checks. Liveness is treated as a gate, not a vote: if the posting is expired, the mode refuses to classify the role.

It connects to the Cognitive Pivot through the existing role scorer and BLS/O*NET role-quality layer. The scorer provides sample-mode role-quality evidence, while the backend-authenticity step asks a more specific question: whether the posting text shows production engineering responsibilities such as API design, databases, distributed systems, testing, deployment, reliability, and service ownership.

It can connect to 80 Days to Stay as supporting context when sponsorship history matters, but sponsorship is not the primary score in this mode. The central question is role authenticity, not visa sponsorship ranking.

## Failure Modes

One failure mode is a false positive. A posting may mention APIs, cloud, databases, or AI tools, but the actual role may be mostly implementation, customer onboarding, support, or solutions engineering. This is hardest for early-career F-1 students to catch because keyword presence can look like evidence of backend ownership even when the responsibilities are not product engineering responsibilities.

A second failure mode is a false negative. A genuinely strong backend engineering role may have a short or generic job description that does not list detailed system design, infrastructure, or ownership language. This is hardest for candidates evaluating startups or smaller teams, where job descriptions are often less formal even when the actual work is deeply technical.

This mode handles both risks by separating verified script output from human judgment and by allowing `Refuse to Score` when evidence is insufficient.