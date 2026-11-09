# MVP Boundary



The smallest complete user journey that tests whether the product creates value. Complete: the person gets the value, start to finish. Smallest: nothing that is not on that path is in Sprint 1.

**Value hypothesis under test:** A university student who gets five relevant openings in one place, each card already showing who can apply, the experience, hours, pay and deadline, will decide apply or skip on all five in under five minutes, instead of opening post after post across several sites to find out whether they qualify (problem statement, sentences 1–3; logs 01, 04, 06, 07, 08, 10).

**The one person walking this journey:** Nino, a third-year student at a Georgian university, not working, looking for her first internship or entry-level job in her field; she opens post after post across several sites to check whether she qualifies, and skips some she likes when she cannot tell (00-foundation/icp.md v2; logs 01, 02, 09).

## The journey

1. A teammate (the curator) picks this week's five internship or entry-level openings that accept students from LinkedIn, jobs.ge, hr.ge, company pages, Facebook and Telegram groups, removes duplicates, fills in each card's field and eligibility details, and publishes the set.
2. Nino opens the link (from an Instagram story, a university group chat or a friend) and sees five job cards.
3. Nino reads a card: role, company, field, source, whether students can apply, experience required, hours, pay, and deadline, without opening the original post.
4. Nino taps **Apply** (the original post opens) or **Skip** (with a one-tap reason) on that card.
5. Nino finishes all five cards and sees a summary: the cards she chose to apply to, each with its deadline and link.

**Why this is complete:** After step 5 the student has made a real apply-or-skip decision on every opening, knows the deadlines of the ones they want, and never had to open a post just to find out whether they qualify — the thing 01 said she had to do for "many job posts" (logs 01, 06, 08, 10).

**Why this is smallest:** We considered removing step 1 and showing cards scraped automatically. But without a person removing duplicates and filling in eligibility, hours and pay, the cards repeat exactly what fails today: duplicated posts (08) and "junior" posts that hide the experience required (06, 07, 10, 11). The value does not land without step 1.

## Cut list

| Feature | Reason (cite the log, session, or hypothesis) | Comes back when |
|---|---|---|
| Automatic scraping of job sites and Telegram | The hypothesis tests whether clear cards speed up decisions, not how cards are collected; hand-curating 5 cards a week tests it with no scraper. Scraped posts would carry the duplicates 08 complained about | When the curator cannot keep up with 5 cards a week, or after Week 12 if decisions per set hold up |
| Field picker and a separate set per field | The ICP is any field (icp.md v2: v1 wrongly assumed CS); one mixed set of 5 keeps curation to 5 cards, and the skip reason "not my field" measures whether this matters | When "not my field" is the most common skip reason in PostHog |
| Student accounts and sign-in | The decision on 5 cards needs no identity; PostHog's anonymous id links a student's decisions | Sprint 3, if students ask to save cards across weeks |
| Deadline reminders and notifications | Missed deadlines are Pattern 3 (8 logs), but the hypothesis is about deciding. The card shows the deadline; alerts were ignored or turned off in 08 and 10 | Sprint 2, if the summary's deadlines are not enough (sessions will show) |
| Search and filters | Five curated cards replace searching; filtering is the very work 07 found hard | When sets grow past ~10 cards |
| Courses, hackathons, clinics | Pattern 5 has only 3 logs (03, 04, 06) and 10 and 11 did not raise it | When a new log adds a 4th, or a session asks for them |
| Applying inside our app / CV builder | Students apply on the original site; "CV felt too empty" is only log 10 (not yet a pattern) | Never for in-app applying; CV help only if it becomes a pattern |
| Salary fairness rating | The original pay/scarcity prediction was weakened (DECISIONS.md); the card shows the pay as a fact, students judge it | Never, unless later logs bring it back |
| Opportunities abroad | Only log 02 | When 2+ logs raise it |
| AI matching to the student's profile | 5 hand-picked cards need no matching; 02 is the only log using AI | After real decision data shows which cards get skipped and why |
| Employer side (companies posting directly) | No employer interviews yet; tests nothing about the student's decision | After student-side value is shown |

## Step to event

Event names are copied from 03-build/analytics/event-schema.md.

| Step | Event (actor_verb_object) | In the schema? |
|---|---|---|
| 1 | curator_publishes_card_set | added today |
| 2 | student_opens_card_set | added today |
| 3 | student_views_card | added today |
| 4 | student_decides_card | added today |
| 5 | student_completes_card_set | added today |

**North star step:** 5 — `student_completes_card_set` with `ms_total` ≤ 300 000 (five minutes) is the north star from DECISIONS.md (Wk5).

## The DECISIONS.md line

Wk6 · MVP boundary: 5-step journey (curator publishes 5 cards to student finishes apply-or-skip on all five); cut scraping, sign-in, deadline reminders, field picker, courses and hackathons · evidence: 03-build/mvp-boundary.md, logs 01, 06, 07, 08, 10, 11 · owner: MG
