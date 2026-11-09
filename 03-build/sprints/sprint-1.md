# Sprint 1



## Definition of done

A story is done when it is merged to main, deployed at the public URL, walked on a phone by a teammate who did not build it, and its events show in PostHog's Activity view.

## Real hours before the Week 7 lab

Each teammate fills in their own row honestly. The story hours below (17 h) must not exceed the total; if they do, use the slip rule or cut.

| Initials | Hours free | When, specifically |
|---|---|---|
| MG | [ ] | [days and times] |
| AP | [ ] | [days and times] |
| AS | [ ] | [days and times] |
| ST | [ 4 ] | friday 22:00-12:00 and saturday the same time |
| **Total** | [ ] | |

## The board

GitHub Projects on the team repo, linked from the README. Columns: next, doing, review, done. One card per story. Merge to main every day anyone works.

Curation is not a story but it has an owner: AS picks this week's five real internship or entry-level openings that accept students and fills in every field before S1 is reviewed.

## Stories

### S5 first · Deploy and instrument · owner MG · reviewer ST · 2 h

Do this on the first evening, with Lab-6/setup/SHIP-STACK-SETUP.md, so every later story deploys the day it merges. Public URL in the README's Live product row, all five schema events visible in PostHog's Activity view, reconcile check written (decisions rows in Neon = student_decides_card events in PostHog). The Week 7 lab adds the dashboard.

### S1 · Curator publishes this week's five cards · owner MG · reviewer AS · 4 h

As the curator, I enter five openings with their eligibility, hours, pay and deadline and publish them so that students never have to open a post to find out whether they qualify.

Acceptance criteria:
- Given /admin/TOKEN on a phone, when I fill five cards (role, company, field, source, source_url, students OK yes/no, experience required, hours, pay, deadline) and tap Publish, then I see "Published: 5 cards"
- And a card_sets row and five cards rows exist; the same page with a wrong token shows "Not found"
- And curator_publishes_card_set fires with set_id, card_count 5

Smallest demo that proves it: publish five cards on a phone, show the rows, show the event.

### S2 · Student opens the link and sees five cards · owner AP · reviewer MG · 4 h

As a CS student, I open one link on my phone and see five openings so that I do not have to check five places.

Acceptance criteria:
- Given the public URL with ?src=instagram on a phone browser, when it loads, then I see five cards with no pinch-zoom needed, each showing role, company, source, students/first-years OK, experience, hours, pay and deadline
- And a card with an empty pay field shows "Pay: not stated" instead of nothing
- And student_opens_card_set fires once per load with set_id and source; student_views_card fires once per card with card_id and position

Smallest demo that proves it: open the link with ?src=instagram, scroll the five cards, show the events.

### S3 · Student decides apply or skip · owner AP · reviewer AS · 4 h

As a CS student, I tap Apply or Skip on each card so that I decide in seconds instead of reading the whole post.

Acceptance criteria:
- Given the five cards, when I tap Apply, then the original post opens in a new tab and the card shows "Applying"; when I tap Skip and choose a reason, the card shows "Skipped"
- And one decisions row exists per card with the anonymous id, decision and skip_reason; a second tap on the same card does not add a second row
- And student_decides_card fires with set_id, card_id, position, decision, skip_reason, ms_on_card

Smallest demo that proves it: apply to one card, skip one as "not eligible", show the two rows and two events.

### S4 · Student finishes the set (north star) · owner MG · reviewer AP · 3 h

As a CS student, I finish all five cards and see the ones I chose with their deadlines so that I do not miss them.

Acceptance criteria:
- Given four cards decided, when I decide the fifth, then I see a summary listing the cards I chose to apply to, each with its deadline and a link to the original post
- And the summary appears only once per student per set
- And student_completes_card_set fires once with set_id, apply_count, skip_count, ms_total

Smallest demo that proves it: decide all five cards on a phone in under five minutes, show the summary, show the event with ms_total below 300000.

## Slip rule

If S1 (the curator admin page) is not done by the Wednesday evening before the Week 7 lab, the admin page moves to Sprint 2 and AS's five cards go in through a seed script that also fires curator_publishes_card_set. S4 and its student_completes_card_set event stay no matter what, because without them the north star cannot be measured.

## The DECISIONS.md lines

The boundary line is in 03-build/mvp-boundary.md. Our prototype exists (02-design/prototype/) but has no logged test sessions, so we are on Track B:

Wk6 · Prototype track: B, existing prototype in 02-design/prototype/; frozen test runs on it, 3 sessions logged in 02-design/user-testing/usability-findings.md before the Week 7 lab · evidence: 02-design/prototype-plan.md · owner: [saba tabukashvili]
