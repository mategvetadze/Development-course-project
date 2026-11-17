# Homework 2 · Ani Purtskhvanidze (@ANANKE231) · Prometheus

> **Evidence status:** Draft based on the uploaded repository and AP's answers. The repository ZIP has no `.git/` history, so ownership and dates of linked commits must be checked against GitHub before submission. Do not submit the pending items as completed work. This report describes documented contributions, not proof of a production launch.

## 1. Ship report

I work on the student-facing frontend for CareerCards, where a student reviews five curated job cards and chooses Apply or Skip for each. The code in `app/components/StudentCardSet.tsx` contains the mobile card layout, eligibility, experience, hours, pay, deadlines, Skip reasons, Apply links, and the final apply list. My Sprint 1 ownership is S3–S5 (`03-build/sprints/sprint-1.md`); ownership of a story **does not by itself prove who authored every line**. I also contributed to the prototype and product documentation as recorded below.

| What I shipped or prepared | Story or rung | Commit link(s), from my account | Live at production URL? | Walked / checked by |
|---|---|---|---|---|
| Clickable prototype files and folder cleanup (`02-design/prototype/`) | Prototype / Wk5 | [e9f2137](https://github.com/mategvetadze/Development-course-project/commit/e9f2137748eded2560f048e95ee6d08434052a04), [5a2fee0](https://github.com/mategvetadze/Development-course-project/commit/5a2fee042f9991c020fc9736aa73975d4010eafa) — **verify author** | Prototype only, not production | Pending evidence |
| North-star definition and metric decision | Wk5 | [7573d77](https://github.com/mategvetadze/Development-course-project/commit/7573d777d29cf7e2b5e36731b341e633a7a8d9e3) — **verify author** | N/A documentation | `DECISIONS.md`, Wk5 |
| Lab document/event-schema review and edits, including gate record | Sprints 1–2 / Wk7 | [3771b60](https://github.com/mategvetadze/Development-course-project/commit/3771b60651f0dac2b83aad46d0876cda21698d48) — **verify author** | N/A documentation | Files in `03-build/` |
| Frontend student cards, Apply/Skip behavior and five-card summary | Sprint 1 S3–S5 | **PENDING: paste your own commit(s) only if you wrote this code** | **Not verified** | **PENDING: reviewer phone walk** |
| Lab 7 frontend PostHog import correction and backend source repair in the prepared ZIP | Lab 7 preparation | **PENDING: commit from @ANANKE231 after actually reviewing/pushing** | No, not deployed | **PENDING** |

**The piece I am least sure works for a real person, and how I will know by Lab 8:** the Apply flow that opens the external job post and posts the decision to the backend. I will have a teammate try all five choices using mobile data and compare the saved `decisions` rows with `student_decides_card` and `student_completes_card_set` events. The repository contains the UI and backend code but no confirmed live URL or event counts; the frontend's PostHog client import also needed repair. The north-star five-minute threshold cannot be independently reconciled until we store `ms_total` in the database or document an equivalent measurement.

**One thing I did that was not my assigned story:** I reviewed the event schema and sprint documentation even though my primary assignment is the frontend, because an unmeasured interface cannot show whether students finished the five decisions. The existing HW2 draft points to [3771b60](https://github.com/mategvetadze/Development-course-project/commit/3771b60651f0dac2b83aad46d0876cda21698d48); I must verify this is my commit.

## 2. Pattern journal — Weeks 5 to 7

### Week 5 · One metric that matters

I focused on an outcome rather than a page view: a student finishing Apply or Skip on all five job cards in under five minutes. `DECISIONS.md` records my initials (AP) on the north-star line. I helped move the clickable prototype into `02-design/prototype/`, and the existing draft names several commits that I will verify against GitHub. This metric is stronger than prototype opens because it shows that a student reached the decision point. I learned that every screen action needs a matching event to make this measurable.

### Week 6 · The smallest complete journey

My Sprint 1 ownership is the student-facing stages: opening a set, reading the facts and choosing Apply or Skip (S3–S5). I looked at the card components and their connection to a FastAPI endpoint; a student cannot finish the journey if any decision fails to save. I also checked Lab 5–7 documents against the required templates, as described in the earlier HW2 draft and [3771b60](https://github.com/mategvetadze/Development-course-project/commit/3771b60651f0dac2b83aad46d0876cda21698d48) (**verify commit author**). This journal entry is reconstructed after the week, not a contemporaneous entry. There is still no proof of a live phone walk.

### Week 7 · Ship to learn

I reviewed the current student-facing Next.js source and the required events `student_opens_card_set`, `student_views_card` and `student_decides_card`. I can see these actions represented in source code, but a file in a repository is not evidence that a real phone successfully used them. The uploaded snapshot includes no confirmed production URL, Activity rows, or dashboard link. The Lab 7 preparation package fixes a missing client import so the code has a better chance to build; I still need to commit and test those changes myself before calling them shipped. I reported up to five hours of work around this period and will record precisely which hours are available before Lab 8.

## 3. My DECISIONS.md lines

> Wk5 · North star: Number of students who complete apply-or-skip decisions for all five job cards within five minutes, per week; rejected prototype opens (does not prove value) and job card views (does not prove decisions) · evidence: 03-build/analytics/event-schema.md, 01-discovery/interview-logs/01-student-management.md, 01-discovery/interview-logs/08-student-business.md · owner: AP

The discovery logs describe time lost searching scattered postings, while the schema records the completion event and five-minute threshold.

> Wk7 · Gate status clarified: no public URL, production PostHog events, matched counts or dashboard were verifiable in the supplied repository snapshot; gate remains open at rung 0 until a phone walk confirms rung 1 · evidence: README.md, 03-build/analytics/event-schema.md, 03-build/sprints/sprint-2.md · owner: AP

This records what the uploaded repo can prove, not an unverified assertion that the product shipped. **After adding this line to the team repo, include the actual commit link from your GitHub account.**

## 4. My person this week

**Field-week person:** T1, a third-year CS student and job seeker from `01-discovery/interview-logs/07-student-cs.md` (confirm they are not a classmate and consent to field-week contact). **How and when the link reaches them:** I will send the real production URL in a direct message or in person only after the site works on mobile data. Date, message sent, and whether they opened it are **PENDING**, and will be added to `03-build/sprints/sprint-2.md`.
