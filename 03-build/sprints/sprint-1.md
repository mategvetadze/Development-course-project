# Sprint 1 — Prometheus / CareerCards

**Goal:** Deploy one complete five-card decision journey to a public phone-accessible URL, with `student_completes_card_set` visible in PostHog. This plan records the Week 6-to-Week 7 sprint; actual completion must be demonstrated, not assumed.

## Definition of done

A story is **done** only when code in this team's repository is merged into `main`, running at the README public URL, independently walked on a phone by its named reviewer, and its specified event is visible with the correct properties in PostHog Activity.

## Real hours before the Week 7 lab

The repository documents MG's and ST's availability, but AP's and AS's available hours are not confirmed. **AP is the frontend owner** for steps 2–4 (S3–S5). AP's 4 hours below are a proposed workload estimate, **not** a claim of confirmed free time. Confirm AP's actual hours and schedule before committing this sprint plan. This plan covers remaining fixes/integration rather than writing the whole system from scratch.

| Initials | Hours free counted | When, specifically |
|---|---:|---|
| MG (Mate Gvetadze) | 6 | Tue 20:00–22:00; Thu 20:00–22:00; Sun 18:00–20:00 (from original sprint file) |
| AP (Ani Purtskhvanidze) | TBD; 4 h planned for frontend | **AP to confirm actual free hours and dates before committing** |
| AS (Archil Sanikidze) | 0 (not confirmed) | AS must enter actual available hours before team commits the sprint |
| ST (Saba Tabukashvili) | 4 | Original file: Friday 22:00–02:00 (four hours); second Saturday window mentioned but not counted until confirmed |
| **Total confirmed free** | **10 h (MG 6 + ST 4)** | **10 h stories planned: MG 6 + AP 4; AP needs to confirm availability (ST has 4 h available for review/backup)** |

**Team initials:** MG = Mate Gvetadze; AP = Ani Purtskhvanidze; AS = Archil Sanikidze; ST = Saba Tabukashvili (`00-foundation/team-contract.md`). AS curates the five verified openings; **AP develops the student-facing frontend (S3, S4, S5)**; ST supports review/QA. Owner and reviewer are different for every story.

## The board

Use **GitHub Projects** linked from the repository's README (link **not yet supplied**). Columns: **next → doing → review → done**. Make one card per story; merge to `main` every day work is done. The README currently contains a placeholder for the project-board URL, so the team must insert the real URL.

## Stories

**Priority order:** North-star story is listed first. **Execution order:** Do the deploy skeleton immediately on the first work session, then land the highest-value journey step; the deploy story is listed last as required by the sprint template. Because most code already exists, estimates below cover fixes, integration, testing and review rather than greenfield development.

### S1 · Step 5: student completes five decisions (north star) · owner MG · reviewer AP · 1 h

**As** Nino, **I** finish five decisions and see the jobs I want to pursue with deadlines, **so that** I can choose next actions without re-reading five listings.

**Acceptance criteria:**
- Given four distinct saved choices, when I make the fifth choice on my phone, then the apply list appears with original links and deadlines (or states that I skipped all five).
- And Neon contains exactly five decision rows for the same `set_id` and `anonymous_id`, not more.
- And `student_completes_card_set` appears once in PostHog with `set_id`, `apply_count`, `skip_count`, `ms_total` (the north star qualifies only when `ms_total <= 300000`).

**Smallest demo:** Decide all five cards within five minutes; show the summary, the five database rows and one completion event.

### S2 · Step 1: curator publishes five verified cards · owner MG · reviewer AS · 2 h

**As** the team curator, **I** publish five complete opportunity cards, **so that** Nino can assess eligibility from one place.

**Acceptance criteria:**
- Given five real, de-duplicated openings, when the curator fills role, company, field, source, URL, students OK, experience, hours, pay and deadline and taps Publish, then the page shows `Published: 5 cards`.
- And Neon has one new `card_sets` row and five matching `cards` rows. A wrong `X-Admin-Token` **rejects Publish**; the admin page itself may still load.
- And `curator_publishes_card_set` appears in PostHog with `set_id`, `card_count=5`.

**Smallest demo:** Publish one set from a phone; confirm its five records and the server event.

### S3 · Step 2: student opens the set · owner AP · reviewer ST · 2 h

**As** Nino, **I** open the shared link and see five curated jobs on my phone, **so that** I avoid hunting across several sources.

**Acceptance criteria:**
- Given the public URL ending `?src=instagram` and a published set, when opened on a phone, then five cards are visible/scrollable with readable labels and no horizontal overflow.
- And the page retrieves only the latest published set from Neon without requiring login.
- And `student_opens_card_set` fires once per page load with `set_id` and `source=instagram` in PostHog.

**Smallest demo:** Open the URL in a new phone tab and show five cards plus the open event.

### S4 · Step 3: student reads the important facts · owner AP · reviewer AS · 1 h

**As** Nino, **I** see the eligibility, requirements, hours, pay and deadline on each card, **so that** I can decide without opening the original post for missing facts.

**Acceptance criteria:**
- Given any card, when it enters at least half the phone viewport, then its role, company, source, field, eligibility, experience, hours, pay and deadline are on that card; missing pay is explicitly `not stated`.
- And the card can be viewed without a login or opening its employer link.
- And `student_views_card` fires once per card per page view with `set_id`, `card_id`, `position` (1–5).

**Smallest demo:** Scroll through the five cards and show five distinct view events.

### S5 · Step 4: student chooses Apply or Skip · owner AP · reviewer MG · 1 h

**As** Nino, **I** choose Apply or Skip and a skip reason for each opening, **so that** I can keep only opportunities worth pursuing.

**Acceptance criteria:**
- Given an undecided card, when I tap Apply, then its original listing opens and the card is marked Applying; when I tap Skip and select a reason, it is marked Skipped.
- And Neon has one decision row per `(set_id, card_id, anonymous_id)` even after a double tap; Apply opening a new tab must not stop the save.
- And `student_decides_card` fires only on a newly saved row with `set_id`, `card_id`, `position`, `decision`, `skip_reason`, `ms_on_card`.

**Smallest demo:** Apply once, skip once with reason, retry a decided card, and show only two rows/events.

### S6 · Deploy and instrument · owner MG · reviewer ST · 3 h

**Do the deployment setup first**, using `Lab-6/setup/SHIP-STACK-SETUP.md` if available, then complete the gate as the final story. Host Next.js on Vercel, FastAPI on Render, Neon Postgres and PostHog. Fix missing `app/lib/posthog-client.ts` (referenced by StudentCardSet in the ZIP) before a frontend build.

**Acceptance criteria:**
- Given a phone on mobile data, when the README Live product URL is opened, then five published cards load and the fifth choice produces a summary.
- And the URL is inserted into README; a different teammate walks every step on a phone.
- And all five schema events are visible in PostHog Activity with properties, with the north-star event triggered from production.
- And the gate reconciliation is written in `03-build/analytics/event-schema.md`: PostHog `student_decides_card` count vs Neon decision rows, and PostHog `student_completes_card_set` vs students with five decisions (same date range and environment). Record numbers, not an unsupported claim that they match.

**Smallest demo:** On a real phone, open the live URL, finish five decisions, show PostHog Activity and the recorded reconciliation numbers.

**Total story hours:** S1 1 + S2 2 + S3 2 + S4 1 + S5 1 + S6 3 = **10 h**. **Owner allocation:** MG 6 h; **AP 4 h (frontend, availability not yet confirmed)**. ST has 4 h of documented availability for review and integration support; AS handles curation/review subject to confirmation. **Capacity check is pending until AP confirms at least 4 h before Week 7**; if not, reassign or re-scope the frontend stories rather than claiming the plan fits.

## Slip rule

If the curator admin UI (S2) cannot publish by the **evening before the Week 7 lab**, move the **admin form UI only** to Sprint 2 and publish AS's five verified cards using a temporary controlled seed script that produces `curator_publishes_card_set`. **Keep** the five-card public view, Apply/Skip decisions, completion summary, PostHog `student_completes_card_set`, and production deployment: without them, Nino receives no measurable value. If publishing cannot be done safely or verified, report the gate blocked instead of claiming completion.

## The DECISIONS.md lines

**Boundary:** copy the exact Wk6 boundary line from `03-build/mvp-boundary.md`.

**Prototype track:** **B**, because `02-design/prototype/index.html` exists but `02-design/user-testing/usability-findings.md` documents **0 completed sessions**. Schedule and log **three real** frozen-test sessions before the Week 7 lab; the present ZIP contains no evidence of those completed sessions.

`Wk6 · Prototype track: B (existing clickable prototype at 02-design/prototype/index.html; under 3 sessions); run the frozen test and log 3 sessions before Week 7 · evidence: 02-design/user-testing/test-plan.md, 02-design/user-testing/usability-findings.md · owner: AS`
