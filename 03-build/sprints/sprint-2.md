# Sprint 2 — Prometheus / CareerCards

**Period:** Lab 7 to Lab 8

**Goal:** Deploy the complete five-card student journey, verify analytics, reconcile database and PostHog counts, and prepare for real-user field testing.

## Sprint 1 review

**Definition of done:** Code merged to `main`, working at the public production URL, checked on a phone by another teammate, with the corresponding event visible in PostHog Activity.

| Story | Owner | Done by our definition? | Missing requirement |
|---|---|---|---|
| S1 — Complete five decisions and show apply list | MG | Not verified | Backend implementation exists, but production completion and event verification are missing |
| S2 — Curator publishes five cards | MG | Not verified | Publishing functionality exists; successful production publishing and review are not confirmed |
| S3 — Display five opportunities | AP | Not verified | Frontend implementation exists; production API data and mobile review need verification |
| S4 — Display job details | AP | Not verified | Frontend displays requirements, company, pay, hours and deadline; production review is pending |
| S5 — Apply and Skip interactions | AP | Not verified | Interface and API integration exist; persistence and completion need production testing |
| S6 — Deploy and instrument | MG | Not verified | Railway URL is listed, but phone accessibility, database readiness and PostHog events are unverified |

**Slip rule:** Keep the five-card decision journey, saved decisions and north star completion event as priorities. Move nonessential interface improvements to a later sprint if deployment or integration takes longer than planned.

## The gate

| Rung | Reached? | Evidence | If not: owner and deadline |
|---|---|---|---|
| 1 — Production URL loads on a phone | Not verified | Railway URL listed in `README.md`; mobile-data test pending | MG — before Lab 8 |
| 2 — Complete journey works in production | Not verified | Local frontend runs, but local database readiness failed | AP + MG — before Lab 8 |
| 3 — North star event appears in PostHog | Not verified | Production Activity evidence pending | MG + AP — before Lab 8 |
| 4 — PostHog and database counts match | Not verified | Actual counts and shared time window pending | MG + AP — before Lab 8 |
| 5 — Dashboard is linked in README | Not verified | Public three-insight dashboard link pending | MG — before Lab 8 |

## Real hours before Lab 8

| Initials | Hours free | When, specifically |
|---|---|---|
| AP — Ani Purtskhvanidze | 5 hours reported; remaining availability to confirm | Frontend integration and testing; exact remaining slots TBD |
| MG — Mate Gvetadze | TBD | Confirm with MG |
| AS — Archil Sanikidze | TBD | Confirm with AS |
| ST — Saba Tabukashvili | TBD | Confirm with ST |
| **Total confirmed future capacity** | **TBD** | Confirm remaining AP hours and teammates' availability |

## Stories this week

### L7-1 — Frontend and browser analytics

**Owner:** AP  
**Reviewer:** ST  
**Estimated hours:** 2

**As** a student looking for an internship, **I want** to open five relevant job cards on my phone **so that** I can quickly review available opportunities.

**Acceptance criteria:**

- Given a published set, the frontend displays exactly five cards.
- Each card displays its company, role, eligibility, requirements, pay, hours and deadline.
- The interface works on a phone without horizontal scrolling.
- `student_opens_card_set` fires once with the required schema properties.
- `student_views_card` fires when each card becomes at least 50% visible.
- Another teammate verifies the events in production PostHog Activity.

**Smallest demo:** Open the production website on a phone, show the five cards, and verify the browser events.

### L7-2 — Apply/Skip frontend integration

**Owner:** AP  
**Reviewer:** MG  
**Estimated hours:** 2

**As** a student, **I want** to choose Apply or Skip for each job **so that** I can finish with a list of opportunities I want to pursue.

**Acceptance criteria:**

- Apply opens the original job listing and attempts to save the decision.
- Skip allows the student to select a reason.
- The backend successfully stores each decision.
- A repeated tap does not create duplicate records.
- After five saved decisions, the apply list or skipped-all message appears.
- The server fires `student_decides_card` and `student_completes_card_set` with the required properties.

**Smallest demo:** Complete five Apply/Skip decisions and show the saved summary.

### L7-3 — Analytics and frontend review

**Owner:** AP  
**Reviewer:** MG  
**Estimated hours:** 1

**Acceptance criteria:**

- Verify the student journey on a phone using mobile data.
- Verify browser events in PostHog Activity.
- Compare the qualifying north star event count with the database count using the same time window and filters.
- Check `ms_total` and `qualifies` in the existing completion records.
- Document actual results in `03-build/analytics/event-schema.md`.

**Smallest demo:** Show production frontend actions and their corresponding PostHog records.

**AP planned work: 5 hours.** These estimates must fit AP's confirmed remaining availability.

### L7-4 — Production deployment

**Owner:** MG  
**Reviewer:** ST  
**Estimated hours:** TBD

**Acceptance criteria:**

- The public website loads on mobile data.
- FastAPI connects to the configured PostgreSQL database.
- The database contains the required tables and migrations.
- All five decisions can be saved in production.
- The completion event reaches PostHog.
- The public URL is linked in README.

### L7-5 — Analytics dashboard

**Owner:** MG  
**Reviewer:** AS  
**Estimated hours:** TBD

**Acceptance criteria:**

- Create a Trends insight for `student_completes_card_set`.
- Create a journey Funnel or step-count insight.
- Create a Retention insight.
- Apply consistent production and internal-user filters.
- Share the dashboard using a link that opens without a login.
- Add the link to README.

### L7-6 — Five verified opportunities and field-user coordination

**Owner:** AS  
**Reviewer:** ST  
**Estimated hours:** TBD

**Acceptance criteria:**

- Verify five real opportunity listings and their source URLs.
- Confirm the requirements and deadlines.
- Publish the five cards through the application.
- Coordinate the real-user field test with the other team members.

**Capacity rule:** Confirm MG, AS and ST availability before treating the complete story plan as feasible.

## Field week — who uses it

The team plans to contact 3–5 students matching the ICP. Participants must be real potential users rather than classmates, with identities represented by code names.

| Code name and role | Previous source | How the link reaches them | Sent by and by when | Opened? |
|---|---|---|---|---|
| T1 — Third-year CS student, job seeker | Interview 07 | Direct message with production URL, after consent | AP — after production verification | Pending |
| T2 — Second-year business student, job seeker | Interview 08 | Direct message with production URL, after consent | AP — after production verification | Pending |
| T3 — Management student, job seeker | Interview 01 | Direct message with production URL, after consent | ST — confirm date | Completion reported in earlier draft; supporting evidence pending |

**What we tell them:**

"We built a small website that shows five job opportunities. Please review them and choose Apply or Skip for each one. We record anonymous interactions to understand whether the experience helps students make decisions. Let us know if anything is confusing."

## Prediction

**By Lab 8:** We predict at least **2** qualifying `student_completes_card_set` events from real people, and at least **3** distinct real-user `student_opens_card_set` events.

**We are wrong if:** None of the three contacted students completes all five decisions.

This is the original prediction target, not a claim about the actual result. Do not edit the prediction after the field week starts.

**Mid-week look:** AP will review the dashboard after real-user testing. Record the actual date, counts and resulting action when this check occurs.

## The DECISIONS.md line

`Wk7 · Gate open at rung 0 (unverified): production phone access, completed journey, PostHog Activity, reconciliation and dashboard still require evidence; owners and remaining work in sprint-2.md · evidence: README.md, 03-build/analytics/event-schema.md, 03-build/sprints/sprint-2.md · owner: AP`
