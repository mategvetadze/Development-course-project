# Homework 2 · Ani Purtskhvanidze (@ANANKE231) · Prometheus

## 1. Ship report

| What I shipped | Story or rung | Commit link(s), from my account | Live at the production URL? | Walked or checked by |
|---|---|---|---|---|
| Student page: five cards with role, company, source, students OK, experience, hours, pay, deadline; "Pay: not stated" when empty | S2 | [paste commit link] | [yes / no] | MG (reviewer) |
| Apply / Skip on each card, skip reason, one decision per card | S3 | [paste commit link] | [yes / no] | AS (reviewer) |
| Events `student_opens_card_set`, `student_views_card`, `student_decides_card` as written in the schema | S2, S3 | [paste commit link] | [yes / no] | [initials] |
| Reconcile check: `decisions` rows in Neon against `student_decides_card` in PostHog | Rung 4 | [paste commit link] | [yes / no] | [initials] |

Delete any row you did not do, and add a row for anything else you built, deployed, tested or reviewed. A row with no commit from my account does not count.

**The piece I am least sure works for a real person, and how I will know by Lab 8:** [name the screen or the event, and the number or the row you will look at. Candidate: `student_decides_card`, because Apply opens the original post in a new tab and the request can be lost before the server saves the decision (event-schema.md, Reconcile plan). I will compare `decisions` rows in Neon with the PostHog count.]

**One thing I did that was not my assigned story:** [what, why it needed doing, link]

## 2. Pattern journal, Weeks 5 to 7

### Week 5 · One metric that matters

I am the owner of the Wk5 north star line in DECISIONS.md and of the events `student_opens_card_set`, `student_views_card` and `student_decides_card` in `03-build/analytics/event-schema.md`. The north star counts students who finish all five apply-or-skip decisions within five minutes, because opens and card views do not show that a decision was made; we rejected both. [One to three sentences about what you did yourself: which candidate you proposed, what was argued, what you wrote in the schema.] [Where you went beyond your lane.] [What you hacked together to test faster than the plan.]

### Week 6 · The smallest complete journey

My stories in `03-build/sprints/sprint-1.md` are S2 (student sees five cards) and S3 (student decides apply or skip), and I am the reviewer of S4. [What you did yourself this week.] [Where you went beyond your lane.] [What you hacked together to test faster than the plan.]

### Week 7 · Ship to learn

[What you built, wired or checked at the production URL.] [Where you went beyond your lane.] [What you hacked together.] If you did not write this entry in its own week, say so here.

## 3. My DECISIONS.md lines

> Wk5 · North star: Number of students who complete apply-or-skip decisions for all five job cards within five minutes, per week; rejected prototype opens (does not prove value) and job card views (does not prove decisions) · evidence: 03-build/analytics/event-schema.md, 01-discovery/interview-logs/01-student-management.md, 01-discovery/interview-logs/08-student-business.md · owner: AP

The evidence is the event schema, which names `student_completes_card_set` as the north star event, and interview logs 01 and 08, where students had to open post after post to learn whether they qualified.

## 4. My person this week

**The field-week person I am responsible for:** T1, 3rd-year student, job searcher (from interview 07) · **how and when the link reaches them:** [how, and on which day]