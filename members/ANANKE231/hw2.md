# Homework 2 · Ani Purtskhvanidze (@ANANKE231) · Prometheus

## 1. Ship report

| What I shipped | Story or rung | Commit link(s), from my account | Live at the production URL? | Walked or checked by |
|---|---|---|---|---|
| North star decision line in DECISIONS.md | Lab 5, checkpoint 2 | [7573d77](https://github.com/mategvetadze/Development-course-project/commit/7573d777d29cf7e2b5e36731b341e633a7a8d9e3) | n/a (decision) | team, line cites `event-schema.md` and logs 01, 08 |
| Clickable prototype committed to `02-design/prototype/` and moved to the correct folder; a stray duplicate directory deleted | Lab 5, checkpoint 1 | [e9f2137](https://github.com/mategvetadze/Development-course-project/commit/e9f2137748eded2560f048e95ee6d08434052a04), [5a2fee0](https://github.com/mategvetadze/Development-course-project/commit/5a2fee042f9991c020fc9736aa73975d4010eafa), [45587df](https://github.com/mategvetadze/Development-course-project/commit/45587df8d520ae121d19ac6b018f02759f5de85c), [a0d5118](https://github.com/mategvetadze/Development-course-project/commit/a0d511826cfb8b15b991ac643950a59cc7883176), [e4ec774](https://github.com/mategvetadze/Development-course-project/commit/e4ec774deedc1a4211a28f3cf5126512b43266c5) | Prototype link in README (not the product) | [initials] |
| Completed `event-schema.md` (north star event, computation, Step column, Reconcile plan), fixed `mvp-boundary.md` and `sprint-1.md` (stories rewritten for Nino), added `sprint-2.md` and the Wk7 gate line | Lab 5 to 7 documents | [3771b60](https://github.com/mategvetadze/Development-course-project/commit/3771b60651f0dac2b83aad46d0876cda21698d48) | n/a (documents) | [initials] |

**The piece I am least sure works for a real person, and how I will know by Lab 8:** `student_decides_card`. Apply opens the original post in a new tab and the request can be lost before the server saves the decision (event-schema.md, Reconcile plan). I will compare the `decisions` rows in Neon with the PostHog count for the same window.

**One thing I did that was not my assigned story:** I compared our Lab 5, 6 and 7 files, which ST and MG wrote, with the lecturer's templates and committed the fixes, because the event schema had no Reconcile plan and the mvp-boundary had a wrong log count ([3771b60](https://github.com/mategvetadze/Development-course-project/commit/3771b60651f0dac2b83aad46d0876cda21698d48)).

## 2. Pattern journal, Weeks 5 to 7

### Week 5 · One metric that matters

I committed our north star line to DECISIONS.md (7573d77): students who finish all five apply-or-skip decisions within five minutes, per week. I wrote down two rejected candidates, prototype opens and card views, because neither proves a decision was made. I am also the owner of `student_opens_card_set`, `student_views_card` and `student_decides_card` in the event schema. I committed the clickable prototype to `02-design/prototype/`, then moved it and deleted the duplicate directory. I did not hack together any faster test this week; I followed the plan.

### Week 6 · The smallest complete journey

My stories in `sprint-1.md` are S2 (student sees five cards) and S3 (apply or skip), and I review S4. I checked our Lab 5, 6 and 7 files against the lecturer's templates and committed the fixes (3771b60). I made no commits in Week 6; the commits for the boundary, architecture, sprint plan and schema that week are ST's. I did not do enough in my own lane that week, and I am writing this entry late. What I did later: I checked those files against the templates (3771b60) and found the missing Reconcile plan and one wrong count.

### Week 7 · Ship to learn

I did not write this entry in its own week; I am writing it now. I ran the Next.js frontend on my computer and the student page showed "fetch failed", because the Python API is not running and nothing is deployed yet. That is why `sprint-2.md` records the gate at rung 0. I then committed the fixes to the schema, boundary and Sprint 1 files (3771b60) and wrote the Wk7 gate line.

## 3. My DECISIONS.md lines

> Wk5 · North star: Number of students who complete apply-or-skip decisions for all five job cards within five minutes, per week; rejected prototype opens (does not prove value) and job card views (does not prove decisions) · evidence: 03-build/analytics/event-schema.md, 01-discovery/interview-logs/01-student-management.md, 01-discovery/interview-logs/08-student-business.md · owner: AP

The evidence is the event schema, which names `student_completes_card_set` as the north star event, and logs 01 and 08, where students had to open post after post to learn whether they qualified.

## 4. My person this week

**The field-week person I am responsible for:** T1, 3rd-year student, job searcher (interview 07) · **how and when the link reaches them:** [how, and on which day]