# Sprint 2 — Prometheus / CareerCards · Lab 7 to Lab 8

The evidence below reflects the uploaded repository snapshot, **not** an independently verified deployment or a fresh Git history. Code presence is not the definition of done.

## Sprint 1 review

**Definition of done (Sprint 1):** merged to `main`, live at README production URL, walked on a phone by another teammate, and event in PostHog Activity with schema properties.

| Story | Owner | Done by our definition? | If not: which clause is missing, and what happened |
|---|---|---|---|
| S1 — Finish 5 decisions and show apply list (north star) | MG | Not verified | Backend handler and student summary are present, but no production URL, independent phone walk or PostHog evidence was provided |
| S2 — Curator publishes 5 cards | MG | Not verified | Admin form and publish API are present; actual five published records, deployment, phone review and event unverified |
| S3 — Student opens five cards | AP | Not verified | Next.js renders cards if API returns a published set; production behavior, phone walk and `student_opens_card_set` unverified |
| S4 — Student views job details | AP | Not verified | Card component renders role, company, requirements, hours, pay and deadline; `student_views_card` and phone behavior unverified |
| S5 — Student applies or skips | AP | Not verified | Apply/Skip UI and POST `/api/decide` exist; no demonstrated production persistence or event |
| S6 — Deploy and instrument | MG | Not verified | README has no confirmed public URL or dashboard; frontend PostHog helper (`app/lib/posting-client.ts`) and backend routes exist, but were not deployed or tested live |

**Slip rule:** Actual activation is unknown; do not assert it did or did not fire. Per Sprint 1, prioritize the working five-decision journey and its `student_completes_card_set` event over admin-page polish. MG and AS must record what moves if the deploy timeline slips.

## The gate

| Rung | Reached? | Evidence: link or number | If not: owner, by when |
|---|---|---|---|
| 1 — Public production URL loads on phone/mobile data | Not verified | README Live product link pending | MG — before Lab 8, exact time to agree |
| 2 — Five-card journey finishes there | Not verified | No recorded reviewer phone walk | AP (frontend) + MG (API); ST reviews — before Lab 8 |
| 3 — North star event in PostHog Activity from production | Not verified | No Activity evidence | MG (server), AP (browser checks) — before Lab 8 |
| 4 — PostHog and database counts reconcile | Not verified | No matched window/counts | AP (check), MG (DB access) — before Lab 8 |
| 5 — Three-tile dashboard shared in README | Not verified | Dashboard link pending | MG (owner), ST (reviewer) — before Lab 8 |

## Real hours before Lab 8

| Initials | Hours free | When, specifically |
|---|---:|---|
| AP — Ani Purtskhvanidze | **5 confirmed by AP** | “5 hours today and last week” reported on Nov 17; how many are still available before Lab 8 needs confirmation |
| MG — Mate Gvetadze | TBD | MG to confirm upcoming slots |
| AS — Archil Sanikidze | TBD | AS to confirm upcoming slots |
| ST — Saba Tabukashvili | TBD | ST to confirm upcoming slots |
| **Total confirmed future capacity** | **up to 5 h, subject to AP clarifying past vs future** | Do not add unconfirmed teammates' hours |

## Stories this week — missing gate rungs first

### L7-1 · Fix the local build and client events · owner AP · reviewer ST · 2 h (planned)

**As** Nino, **I** load the five-card page on a phone **so that** I can start making decisions and the team can measure entry.

- Given a published set, when the production page opens, five cards appear without horizontal overflow and one `student_opens_card_set` event has `set_id` and `source`.
- When a card is at least 50% visible, its details appear and `student_views_card` records `set_id`, `card_id`, `position` once per card per page load.
- Verify the PostHog browser key, privacy settings and existing `app/lib/posting-client.ts` integration after deploy.
- **Demo:** ST opens a phone URL and shows two distinct events in PostHog.

### L7-2 · Apply/Skip through a real API · owner AP · reviewer MG · 2 h (planned)

**As** Nino, **I** choose Apply or Skip for each card **so that** I finish with a saved apply list.

- Given a card, when Apply is pressed, source URL opens and the server writes one `decisions` row; when Skip reason is selected, a decision saves without leaving the site.
- Given five saved decisions, when the fifth is made, an apply list or “skipped all five” appears. A double tap cannot create duplicate decisions.
- `student_decides_card` and `student_completes_card_set` show the schema properties from **production** and match DB writes (server owned by MG).
- **Demo:** MG reviews the five-card flow on mobile data and sees the stored results.

### L7-3 · Gate reconciliation / frontend review · owner AP · reviewer MG · 1 h (planned)

- PostHog and Neon counts use a precisely documented shared window, filters and definition. Store actual results in the gate block of the event schema, never fabricated zeroes.
- Check the key limitation: database has no persisted `ms_total`, so qualified 5-minute completion counts need a schema enhancement or an explicitly labeled unfiltered interim comparison.
- **Demo:** MG reviews the two queries, filters and numbers side by side.

**AP total planned: 5 h (provisional until the hours remaining are confirmed).** Other required work is not yet capacity-backed:

### L7-4 · Public deploy and server instrumentation · owner MG · reviewer ST · hours TBD

- Deploy FastAPI and PostgreSQL/Neon connection, configure server PostHog secret and CORS, and deploy Next.js with `NEXT_PUBLIC_API_URL` and browser PostHog key.
- Show `/health` on the API, public Next.js page on mobile data, five decisions saved, and north-star event fired after commit. Do not expose `.env` secrets.
- **Demo:** ST walks the deployed URL on a phone; MG shows events in Activity.

### L7-5 · Dashboard / private-user exclusion · owner MG · reviewer AS · hours TBD

- Create Trends for `student_completes_card_set`, an ordered step funnel or counts, and Retention; apply the same internal-user filter to all three; share link in README and check it in a private browser.
- **Demo:** AS opens public share link without logging in and checks the three tiles.

### L7-6 · Five verified opportunities / field-user coordination · owner AS · reviewer ST · hours TBD

- Confirm five real, accessible posts, deadline, salary/eligibility and source URLs; publish through the verified API after deployment.
- Coordinate the 3–5 prior discovery participants with ST/AP; do not imply contact occurred unless logged.
- **Demo:** ST opens the five published cards and verifies source links.

**Capacity guardrail:** Only AP's 5 hours are provisionally confirmed. The team must fill MG/AS/ST hours and reduce or divide work before calling the full Sprint 2 plan feasible; do not claim the 5 Lab 7 rungs were passed.

## Field week — who uses it

AP reports that real-person prototype testing took place and 3–5 prospects are available. The uploaded `02-design/user-testing/usability-findings.md` still records **0 logged sessions**, so their identities, actions, results, and links cannot be verified until those records are added. Select 3–5 **non-classmate** people from the prior interviews and confirm each agrees to receive a public link.

| Code name and role | Log or session they come from | How link reaches them | Sent by and by when | Opened? |
|---|---|---|---|---|
| T1 — third-year computer science student, job seeker | Interview 07 (confirm contact consent) | Direct message or in person, production link `?src=friend` | AP, after rung 3; time TBD | pending |
| T2 — second-year business student, job seeker | Interview 08 (confirm contact consent) | Direct message, production link `?src=friend` | AP, after rung 3; time TBD | pending |
| T3 — management student, job seeker | Interview 01 (confirm contact consent) | Direct message, production link `?src=groupchat` | ST, after rung 3; time TBD | Yes, 25 Nov ~02:00: finished all five, Apply on all five |

**What we tell them:** “We built a five-job-card page to help students decide which listings fit. Please choose Apply or Skip for each card using this public link; we record anonymous card views and decisions, not your name. Let us know what confused you.”

## Prediction (record before sending links; do not edit once the field week starts)

**By Lab 8:** Target **2** `student_completes_card_set` events from real people (`ms_total <= 300000`), plus at least **3** distinct real `student_opens_card_set` events.

**We are wrong if:** 0 of the 3 contacted non-classmate students complete five decisions. These are **targets, not results**.

**Mid-week look:** AP to review dashboard after the first real-user sessions (day/time TBD), then append dated event counts and any action taken; do not backfill a claimed check.

## The DECISIONS.md line

`Wk7 · Gate open at rung 0 (unverified): production URL, phone journey, PostHog Activity, counts and dashboard lack evidence; owners and remaining tasks in sprint-2.md · evidence: README.md, 03-build/analytics/event-schema.md, 03-build/sprints/sprint-2.md · owner: AP`
