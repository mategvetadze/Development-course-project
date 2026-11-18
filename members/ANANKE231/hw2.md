# Homework 2 · Ani Purtskhvanidze (@ANANKE231) · Prometheus

**Evidence status:** Production and reviewer evidence remains unverified; only GitHub-confirmed commits are credited below.

## 1. Ship report

I contributed to CareerCards, helping students review five opportunities and choose Apply or Skip. My assigned Sprint 1 work was the student frontend (S3–S5), but I only claim code authorship supported by commits.

| What I shipped or contributed | Story or rung | Confirmed commit from @ANANKE231 | Live at production URL? | Walked / checked by |
|---|---|---|---|---|
| Initial Lab 5 clickable prototype code | Week 5 prototype | [e9f2137](https://github.com/mategvetadze/Development-course-project/commit/e9f2137748eded2560f048e95ee6d08434052a04) | Prototype only; production not confirmed | No recorded phone review |
| Prototype HTML/CSS/JS improvements | Week 5 prototype | [5a2fee0](https://github.com/mategvetadze/Development-course-project/commit/5a2fee042f9991c020fc9736aa73975d4010eafa) | Prototype only; production not confirmed | No recorded phone review |
| Event schema, MVP boundary, Sprint 1 and Sprint 2 documentation edits | Weeks 5–7 planning and gate | [3771b60](https://github.com/mategvetadze/Development-course-project/commit/3771b60651f0dac2b83aad46d0876cda21698d48) | Documentation; not a deployed feature | Changes visible in commit |
| Student frontend integration / live review | Sprint 1 S3–S5 / Lab 7 | **PENDING** — add only if my own GitHub commit proves it | **Unverified** | **PENDING** |

**Least-certain part:** Apply opens an employer link before its database request completes. I need a production-phone review of five saved decisions, the apply list, and one `student_completes_card_set` with `qualifies = true`.

**One thing beyond my assigned lane:** I reviewed analytics, MVP and sprint documentation in [3771b60](https://github.com/mategvetadze/Development-course-project/commit/3771b60651f0dac2b83aad46d0876cda21698d48), beyond my student UI assignment, to align measurable student actions with the course's required files.

## 2. Pattern journal — Weeks 5 to 7

### Week 5 · One metric that matters

I contributed to the clickable prototype in `e9f2137` and `5a2fee0`. I focused on finished Apply/Skip decisions rather than page views. I learned that the success rule must be frozen before research sessions.

### Week 6 · The smallest complete journey

My assigned work was the frontend journey, and I edited MVP/sprint documents in `3771b60`. The smallest complete journey needs stored decisions and a completion event, not only attractive cards. This entry is reconstructed after Week 6.

### Week 7 · Ship to learn

I reviewed the Apply/Skip and analytics path against the Lab 7 gate. Source code cannot prove production usage or reconciled counts. I must add a real phone walk, reviewer evidence and any verified personal frontend commits before claiming deployment.

## 3. My DECISIONS.md lines

> Wk5 · North star: Number of students who complete apply-or-skip decisions for all five job cards within five minutes, per week; rejected prototype opens (does not prove value) and job card views (does not prove decisions) · evidence: 03-build/analytics/event-schema.md, 01-discovery/interview-logs/01-student-management.md, 01-discovery/interview-logs/08-student-business.md · owner: AP

The decision is visible in the repository's `DECISIONS.md`, with its evidence and event definition in the cited files. My commit `7573d77` **deleted** older versions of `DECISIONS.md` and `README.md`; it must not be presented as proof that this north-star line was added.

> Wk7 · Gate status clarified: no public URL, production PostHog events, matched counts or dashboard were verifiable in the supplied repository snapshot; gate remains open at rung 0 until a phone walk confirms rung 1 · evidence: README.md, 03-build/analytics/event-schema.md, 03-build/sprints/sprint-2.md · owner: AP

This documents the open gate without claiming it passed.

## 4. My person this week

**Field-week person:** T1 — third-year CS student and job seeker (interview log 07). After the URL is tested, request consent, send it directly and log the real date/open status in Sprint 2. No sending or testing is claimed yet.
