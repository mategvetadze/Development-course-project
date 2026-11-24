# Homework 2 · Saba Tabukashvili (@tabukashvilisaba) · Prometheus

AI use: I used Claude to draft the Lab 6 planning files and Sprint 2, and to review and fix `StudentCardSet.tsx`. Every file was checked against our interview logs and `icp.md` before I committed it; logged in `docs/ai-usage-log.md`.

## 1. Ship report

| What I shipped | Story or rung | Commit link(s), from my account | Live at the production URL? | Walked or checked by |
|---|---|---|---|---|
| MVP boundary: 5-step journey, cut list citing logs, step-to-event map; rewrote it from CS-only to any field after checking `icp.md` v2 | Lab 6, boundary | [4978fb9](https://github.com/mategvetadze/Development-course-project/commit/4978fb94da285aeadcb5a09fff1bc4b718c43838), [9b0b0f8](https://github.com/mategvetadze/Development-course-project/commit/9b0b0f8302d009e59cf321fffc571d0259c8709e) | n/a | Not yet walked by a teammate |
| Event schema: five events, one per journey step, with properties and owners | Lab 6, schema | [5bbbb57](https://github.com/mategvetadze/Development-course-project/commit/5bbbb579671969c0e81bf3ea9366f0f2b644493c), [3158631](https://github.com/mategvetadze/Development-course-project/commit/3158631330971bbd232fc42ac3f9b76b1b289ac7) | n/a | Not yet |
| Architecture: diagram, stack, secrets, the riskiest part on deploy day | Lab 6, architecture | [6ad7028](https://github.com/mategvetadze/Development-course-project/commit/6ad7028d07e184ca5c360b9001c359c7f65364da) | n/a | Not yet |
| Sprint 1 plan: stories, acceptance criteria, slip rule | Lab 6, sprint | [c804359](https://github.com/mategvetadze/Development-course-project/commit/c804359a8610a5d789fa8bb6fe291602d97c3e07) | n/a | Not yet |
| MVP boundary and prototype-track lines in DECISIONS.md | Lab 6, decisions | [a50c966](https://github.com/mategvetadze/Development-course-project/commit/a50c966e5d421a43bad27799507264233aa1b13e) | n/a | n/a |
| PostHog started in the browser (`app/lib/posthog-client.ts`) | Sprint 2, ST1 | [532d7bc](https://github.com/mategvetadze/Development-course-project/commit/532d7bc01a9797d34657b3b2dc73e6103ec5b204) | No: merged, but production (Railway) now serves the student page from `backend/`, not from `app/` | n/a |
| Browser events `student_opens_card_set` and `student_views_card`, Apply opening on iPhone, double-tap guard, in `StudentCardSet.tsx` | Sprint 2, ST1 | [32c7c8d](https://github.com/mategvetadze/Development-course-project/commit/32c7c8d) | No: same reason, MG moved the student page into `backend/` | n/a |
| Event schema: where each event fires, plus the live column and reconcile table | Rung 4 (prepared for AP's check) | [55335e8](https://github.com/mategvetadze/Development-course-project/commit/55335e867612057fe55e32d436760704ce3b2276) | n/a | Not yet |
| README rows for Live product, dashboard and board | Rungs 1 and 5 | [83e9d25](https://github.com/mategvetadze/Development-course-project/commit/83e9d25f10a17bc97f31061704554215efc0de97) | MG later filled the Live product row with the Railway URL; dashboard row still pending | n/a |
| Walked the full journey on production as the reviewer: the Railway URL loads, five cards, Apply or Skip on each, "Your apply list" appears with five deadlines (rungs 1 and 2) | Rungs 1–3, reviewer | [LINK: your sprint-2.md gate-table commit] | Yes | Me, 24 Nov |

**The piece I am least sure works for a real person, and how I will know by Lab 8:** the browser events. The live student page is now served from `backend/`, not from the `app/` page I fixed, so I do not know whether `student_opens_card_set` and `student_views_card` fire in production. When T3 opens the link, I will check PostHog's Activity view for those two events next to her `student_decides_card` rows: decisions with no open event mean the browser side is still not wired.

**One thing I did that was not my assigned story:** I had no build story in Sprint 1. Before the deploy, I read MG's student page and found that PostHog was never started in the browser: the open event was only a `console.info`, and `student_views_card` did not exist. Two of our five schema events would never have arrived. I also found that Apply opened the job post only after the server answered, which iPhones block. I fixed all of it ([532d7bc](https://github.com/mategvetadze/Development-course-project/commit/532d7bc01a9797d34657b3b2dc73e6103ec5b204), [32c7c8d](https://github.com/mategvetadze/Development-course-project/commit/32c7c8d)).

## 2. Pattern journal, Weeks 5 to 7

I did not write these entries in their own weeks; I am writing them now, from my commits.

### Week 5 · One metric that matters

I did not own the north star; AP wrote it. My Week 5 work was the evidence underneath it: I updated the affinity map, the patterns analysis and the problem hypothesis ([347da01](https://github.com/mategvetadze/Development-course-project/commit/347da01433435e9d608d3f665a446b59a3838192), [02f1538](https://github.com/mategvetadze/Development-course-project/commit/02f153858b9004c1428f2b1fc5ced814e32480a6), [1874614](https://github.com/mategvetadze/Development-course-project/commit/1874614d6ca3b7f712d2ab2ec6c3ec23209ab231)). The strongest pattern, scattered and irrelevant posts in 10 of 11 logs, is why "decide on five cards in five minutes" makes sense as the metric: it measures a decision, not a visit. Doing the counting myself also showed me that our original prediction about too few jobs was weaker than we thought.

### Week 6 · The smallest complete journey

I wrote and committed our MVP boundary, schema, architecture and Sprint 1 plan. The cut I agree with most is scraping: a person picking five real cards tests whether clear cards help students decide, while a scraper would bring back the duplicate posts that log 08 complained about. My first draft limited the cards to Computer Science; when I checked `icp.md` v2, it said v1 had wrongly assumed CS, so I changed the journey to any field and added "not my field" as a skip reason, to measure whether a field filter matters. Beyond my lane: I set the slip rule and the event for every step, not only my own.

### Week 7 · Ship to learn

The gate did not pass on time: our README still said "coming Week 7". The lesson for me is that a plan with no build story for me let me stay outside the code, so in Sprint 2 I took my own story (ST1, the browser events) and I review MG's deploy and dashboard. Reading MG's code before deploying was my hack: a ten-minute review found two missing events that would have made our first reconcile fail. I tested the fix on a phone-sized screen before committing. What I learned afterwards: MG moved the student page into `backend/` while I was fixing `app/`, so my fix is not what production serves. Next time I tell the builder before I change his file, not after. On 24 November I walked the production journey on Railway myself: five cards, Apply or Skip on each, and the apply list appeared.

## 3. My DECISIONS.md lines

Wk6 · MVP boundary: 5-step journey (curator publishes 5 cards to student finishes apply-or-skip on all five); cut scraping, sign-in, deadline reminders, field picker, courses and hackathons · evidence: 03-build/mvp-boundary.md, logs 01, 06, 07, 08, 10, 11 · owner: ST

I committed this line ([a50c966](https://github.com/mategvetadze/Development-course-project/commit/a50c966e5d421a43bad27799507264233aa1b13e)); the evidence is the cut list in `03-build/mvp-boundary.md`, where every cut cites an interview log or the value hypothesis.

## 4. My person this week

The field-week person I am responsible for: T3, 3rd-year management student (interview 01) · how and when the link reaches them: an Instagram message with the production URL ending in `?src=instagram`, after I confirm with AS that the five cards on the live page are real openings, not test data, so she never taps Apply on a job that does not exist.
