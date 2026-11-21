# Homework 2 · Archil Sanikidze (@Archi-lee-Sun) · Team Prometheus

## 1. Ship report

I directed Codex-assisted development of our existing Next.js/FastAPI/PostgreSQL product. Codex implemented changes, ran automated checks and helped draft this report; I personally handled the external account setup. My commits were merged through [PR #1](https://github.com/mategvetadze/Development-course-project/pull/1) and [PR #2](https://github.com/mategvetadze/Development-course-project/pull/2).

| What I shipped | Story or rung | Commit link(s), from my account | Live at the production URL? | Walked or checked by |
|---|---|---|---|---|
| Card/set validation, immutable decisions and serialized concurrent completion | S1/S5 | [df71b77](https://github.com/mategvetadze/Development-course-project/commit/df71b77) | Unverified | Codex: PostgreSQL tests |
| Saved-choice restoration, retryable errors and correct summaries | S3–S5 | [2677099](https://github.com/mategvetadze/Development-course-project/commit/2677099) | Unverified | Codex: frontend/HTTP tests |
| Server-timed completions and parameterized unique-student reconciliation | S1 / rung 4 foundation | [03195ef](https://github.com/mategvetadze/Development-course-project/commit/03195ef) | Unverified | Codex: timing/concurrency tests |
| Transactional analytics outbox, retries and consistent anonymous identity | S6 / rung 3 foundation | [3ca4642](https://github.com/mategvetadze/Development-course-project/commit/3ca4642) | Unverified | Codex: local SDK receipts |
| Privacy filtering that preserves required SDK transport fields | S6 | [edb3435](https://github.com/mategvetadze/Development-course-project/commit/edb3435) | Unverified | Codex: real SDK regression |
| Deployment manifests, readiness checks, dependency locks and mobile browser tests | S6 / rungs 1–2 foundation | [52afdda](https://github.com/mategvetadze/Development-course-project/commit/52afdda) | Unverified | Codex: production build/Playwright |

**My hosting setup:** I registered with Neon, created our database, ran [schema.sql](../../backend/sql/schema.sql) in its SQL Editor and connected Render/PostHog to our project. Production journey, Activity, reconciliation and dashboard verification remain outstanding.

November 18 local results in PR #2: 36 backend tests, 14 frontend tests and four browser tests passed; one opt-in HTTP test was skipped by default, then passed separately. Build, typecheck and lint passed.

**The piece I am least sure works for a real person, and how I will know by Lab 8:** production analytics after the fifth decision. The check requires a phone walk, one `student_completes_card_set` in Activity and matching qualified [SQL counts](../../backend/sql/reconcile.sql) with identical windows/filters.

**One thing I did that was not my assigned story:** I took on persistence and instrumentation beyond my [Discovery accountability](../../00-foundation/team-contract.md), including the completion work in [03195ef](https://github.com/mategvetadze/Development-course-project/commit/03195ef).

## 2. Pattern journal, Weeks 5 to 7

Written retrospectively on November 21, 2026, applying the weekly principles to my November 17–18 commits and subsequent setup.

### Week 5 · One metric that matters

I applied the lecture's value/event/window principle to our existing [North Star](../../DECISIONS.md): students completing five decisions within five minutes, per week. With Codex, I added database-clock timing and distinct-anonymous-student counting instead of trusting client durations or equating completed sets with students. This extended my contribution into analytics; controlled fixtures checked duplicate identities and exact time boundaries without live users ([03195ef](https://github.com/mategvetadze/Development-course-project/commit/03195ef); W5 PDF pp. 5, 7, 25).

### Week 6 · The smallest complete journey

I kept the approved publish→read→decide→summary flow and existing stack, leaving accounts, scraping and search outside the implementation. My Codex-assisted work covered persistence and reload behavior across frontend and backend, beyond Discovery. A disposable PostgreSQL database and real HTTP fixture tested the complete slice without waiting for hosting ([PR #1](https://github.com/mategvetadze/Development-course-project/pull/1), [live_server.py](../../backend/tests/live_server.py); W6 PDF pp. 5, 9, 17).

### Week 7 · Ship to learn

I moved into infrastructure by creating the Neon database, running its schema and connecting Render/PostHog. Codex-assisted local SDK collectors and a 375px browser journey checked event delivery and saved decisions before production verification ([PR #2](https://github.com/mategvetadze/Development-course-project/pull/2)). These checks prepare the learning loop; a real-person session and production reconciliation remain outstanding (W7 PDF pp. 3, 15, 29).

## 3. My DECISIONS.md lines

From [DECISIONS.md](../../DECISIONS.md), my owner line since Week 5:

> Wk6 · Prototype track: B (existing clickable prototype at 02-design/prototype/index.html; under 3 sessions); run the frozen test and log 3 sessions before Week 7 · evidence: 02-design/user-testing/test-plan.md, 02-design/user-testing/usability-findings.md · owner: AS

The [plan](../../02-design/user-testing/test-plan.md) and [findings](../../02-design/user-testing/usability-findings.md) record this responsibility; I have not arranged or completed the sessions, so the line is not evidence of completed testing.

## 4. My person this week

**The field-week person I am responsible for:** not selected. **How and when the link reaches them:** not arranged. Classmates or close friends were possibilities, but no session was booked; W4 PDF p. 22 and W7 PDF p. 4 require suitable participants outside this course. This requirement remains incomplete.

Lecture references use PDF page numbers: W4 = *PDFSE-W4-LECTURE-SLIDES (1).pdf*; W5 = *PDFSE-W5-F26 (1).pdf*; W6 = *PDFSE-W6-Lecture-Slides (1).pdf*; W7 = *PDFSE-W7-F26.pdf*.
