# Sprint 2: the field week

Sprint 2 runs from Lab 7 to Lab 8. Real people use the product this week, and Lab 8 opens by reading what they did.

## Sprint 1 review

Our definition of done: merged to main, deployed at the public URL, walked on a phone by a teammate who did not build it, events in PostHog's Activity view.

| Story | Owner | Done by our definition? | If not: which clause is missing, and what happened |
|---|---|---|---|
| S1 Curator publishes five cards | MG | No | Code is merged (backend/, app/), but "deployed at the public URL", "walked on a phone" and "events in PostHog" are missing: README Live product row still says "coming Week 7" |
| S2 Student opens the link and sees five cards | AP | No | Same three clauses missing. ST's code walk also found that student_opens_card_set was only a console.info and student_views_card did not exist; fixed in ST1 below |
| S3 Student decides apply or skip | AP | No | Same three clauses missing. ST's code walk found Apply opened the post only after the server answered, which iPhones block; fixed in ST1 below |
| S4 Student finishes the set (north star) | MG | No | Same three clauses missing |
| S5 Deploy and instrument | MG | No | No public URL, no events in PostHog Activity, reconcile check not written |

**Slip rule:** did not fire yet; nothing has moved. If S1 (admin page) is still not deployed by the evening before Lab 8, the admin page moves to Sprint 3 and AS's five cards go in through a seed script that also fires curator_publishes_card_set; S4 and student_completes_card_set stay.

## The gate

| Rung | Reached? | Evidence: a link or a number | If not: owner, and by when |
|---|---|---|---|
| 1 Production URL loads on a phone | No | | MG (S5), Sat 21 Nov, 22:00 |
| 2 Journey completes there | No | | MG, Sat 21 Nov, 22:00 |
| 3 North star event in Activity, from production | No | | MG, Sat 21 Nov, 22:00 |
| 4 Counts reconcile | No | | AP runs the check, Sun 22 Nov, 22:00 |
| 5 Dashboard, linked in README | No | | MG, Sun 22 Nov, 22:00 |

## Real hours before Lab 8

| Initials | Hours free | When, specifically |
|---|---|---|
| MG | [ ] | [days and times] |
| AP | [ ] | [days and times] |
| AS | [ ] | [days and times] |
| ST | [ ] | [days and times] |
| **Total** | [ ] | |

Stories below sum to 8 h (1 h already done). If the total above is smaller, shrink the dashboard to the north star tile only.

## Stories this week

In this order: missing rungs, then anything that slipped from Sprint 1, then at most one new story, and only if a walk or a test session asked for it. The sum of hours must not exceed the total above.

### ST1 · Browser events and Apply on iPhone · owner ST · reviewer MG · 1 h · done in code, not yet deployed

Slipped from S2/S3: a code walk before the deploy found two schema events would never reach PostHog.

Acceptance criteria:

- Given the production URL on a phone, when it loads, then student_opens_card_set fires once with set_id and source, and student_views_card fires once per card with card_id and position
- And tapping Apply opens the original post on an iPhone; a double tap saves one decision, not two
- And ms_on_card is the time since that card came into view, not since the page loaded

Evidence: [532d7bc](https://github.com/mategvetadze/Development-course-project/commit/532d7bc01a9797d34657b3b2dc73e6103ec5b204) (app/lib/posthog-client.ts), [32c7c8d](https://github.com/mategvetadze/Development-course-project/commit/32c7c8d) (app/components/StudentCardSet.tsx).

### Rungs 1 to 3 · Deploy, walk the journey, see the north star event in Activity · owner MG · reviewer ST · 4 h

As Nino, I open the production URL on my phone on mobile data and finish all five cards so that I decide apply or skip without opening the posts.

Acceptance criteria:

- Given the production URL (README's Live product row) on a phone with Wi-Fi off, when it loads, then I see five cards
- And a teammate who did not build S4 finishes all five decisions and sees the summary
- And PostHog Activity shows curator_publishes_card_set, student_opens_card_set, student_views_card, student_decides_card and student_completes_card_set, each with its schema properties, fired once, from production

Two parts to deploy: backend/ (FastAPI) on Render, app/ (Next.js) on Vercel with NEXT_PUBLIC_API_URL pointing at the Render URL. On Render, CORS_ORIGINS must include the Vercel URL. Known risk: Render's free plan sleeps after 15 minutes idle, so the first visit can take up to a minute; we open the site ourselves before sending any link.

Smallest demo that proves it: open the production URL on a phone, decide five cards, read each row aloud in PostHog Activity.

### Rung 4 · Reconcile the counts · owner AP · reviewer MG · 1 h

As the team, we count student_completes_card_set two ways so that we believe the dashboard.

Acceptance criteria:

- Given the gate window, when PostHog's Trends insight counts student_completes_card_set and a SQL query counts the matching rows in Neon, then both numbers are written in the Gate reconcile block of 03-build/analytics/event-schema.md
- And if they differ, the cause and the fix are written there with a commit link
- And PostHog's internal-user filter is set so our own test clicks are not counted

Smallest demo that proves it: show the two numbers side by side and the filter.

### Rung 5 · Dashboard · owner MG · reviewer ST · 2 h

As the team, we open one link to see the north star so that Lab 8 can read what real people did.

Acceptance criteria:

- Given the PostHog dashboard link, when opened without logging in, then it shows Trends for student_completes_card_set, the journey steps in order, and Retention
- And the link is in the README's Analytics dashboard row

Smallest demo that proves it: open the link in a private window.

## Field week: who uses it

3 to 5 real people from our ICP. Not classmates. Code names and roles only, as in our logs. Each gets the production URL, never a preview link, and only after rung 3 passes.

| Code name and role | Log or session they come from | How the link reaches them | Sent by, and by when | Opened? (fill in during the week) |
|---|---|---|---|---|
| T1, 3rd-year student, job searcher | Interview 07 | Messenger, URL ending ?src=friend | AP, the day after rung 3 | |
| T2, 2nd-year student, job searcher | Interview 08 | Messenger, URL ending ?src=friend | AP, the day after rung 3 | |
| T3, 3rd-year management student | Interview 01 | Instagram message, URL ending ?src=instagram | ST, the day after rung 3 | |

**What we tell them:** "Hi! You told us about searching for internships. We made a page with 5 real openings; for each one, tap Apply or Skip. It takes a few minutes. It is a student project: we count clicks and decisions, never names."

## Prediction

Written in the lab, before the week starts. Never edited afterwards; Lab 8 reads it as written.

**By Lab 8:** 2 student_completes_card_set events from real people, not our team. Also: 3 of 3 people fire student_opens_card_set.

**We are wrong if:** 0 real people complete all five cards.

**Mid-week look:** AP opens the dashboard on Thursday 20 Nov and writes one line here.

## The DECISIONS.md line

Wk7 · Gate open at rung 0: missing public URL, events in PostHog, reconcile numbers and dashboard, owners and times in sprint-2.md · evidence: 03-build/sprints/sprint-2.md · owner: AP
