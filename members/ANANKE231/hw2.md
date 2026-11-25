# Homework 2 · Ani Purtskhvanidze (@ANANKE231) · Prometheus

## 1. Ship report

I worked on CareerCards, a project that helps students review internship and entry-level job opportunities and decide whether to Apply or Skip. My assigned responsibilities in Sprint 1 were the student-facing frontend stories S3, S4 and S5.

The repository contains the five-card interface, job details, Apply/Skip interactions and the apply-list summary. I also contributed to the clickable prototype and project documentation. Below are the contributions supported by my existing GitHub commit references.

| What I shipped | Story or rung | Commit link(s) from my account | Live at production URL? | Walked or checked by |
|---|---|---|---|---|
| Initial clickable prototype | Week 5 prototype | [e9f2137](https://github.com/mategvetadze/Development-course-project/commit/e9f2137748eded2560f048e95ee6d08434052a04) | Prototype only; production not verified | No recorded phone review |
| Prototype HTML, CSS and JavaScript improvements | Week 5 prototype | [5a2fee0](https://github.com/mategvetadze/Development-course-project/commit/5a2fee042f9991c020fc9736aa73975d4010eafa) | Prototype only; production not verified | No recorded phone review |
| Event schema, MVP boundary and sprint documentation contributions | Weeks 5–7 planning | [3771b60](https://github.com/mategvetadze/Development-course-project/commit/3771b60651f0dac2b83aad46d0876cda21698d48) | Documentation, not a deployed feature | Changes documented in commit |

**The piece I am least sure works for a real person, and how I will know by Lab 8:**

I am least sure about the complete Apply/Skip interaction on the production website. The frontend displays the interface locally, but successfully saving decisions depends on the backend and database. I will know it works when another teammate completes five decisions on a phone, sees the final apply list, and verifies the corresponding completion event in PostHog.

**One thing I did that was not my assigned story:**

Although my main responsibility was frontend development, I also worked on the MVP boundary, sprint planning and analytics documentation. These tasks helped connect the student interface to the project requirements and event tracking. My documentation contributions are included in commit [3771b60](https://github.com/mategvetadze/Development-course-project/commit/3771b60651f0dac2b83aad46d0876cda21698d48).

## 2. Pattern journal — Weeks 5 to 7

### Week 5 · One metric that matters

During Week 5, I contributed to the clickable CareerCards prototype using HTML, CSS and JavaScript. I focused on making the five-card experience understandable for students who want to review opportunities quickly. I also learned why counting completed Apply/Skip decisions gives us more useful information than simply counting page visits. The prototype contributions are recorded in my GitHub commits.

### Week 6 · The smallest complete journey

During Week 6, my assigned responsibilities were the student-facing frontend stories, including displaying opportunities, presenting their details, and supporting Apply/Skip actions. I also contributed to the MVP and sprint documentation. I learned that the smallest complete product is not just a set of attractive cards: the student must finish the journey and receive a useful result. This journal entry was reconstructed after Week 6 using the project documents and commits.

### Week 7 · Ship to learn

During Week 7, I ran the CareerCards frontend and backend locally to check the student experience. The Next.js frontend opened, and the FastAPI health endpoint returned a successful response. However, the opportunities could not load because the database connection or required migrations were unavailable. This helped me understand that frontend implementation alone does not prove the product works for real users. My next step is to verify the five-card journey, database persistence, and PostHog events on the production website.

## 3. My DECISIONS.md lines

> Wk5 · North star: Number of students who complete apply-or-skip decisions for all five job cards within five minutes, per week; rejected prototype opens (does not prove value) and job card views (does not prove decisions) · evidence: 03-build/analytics/event-schema.md, 01-discovery/interview-logs/01-student-management.md, 01-discovery/interview-logs/08-student-business.md · owner: AP

This decision focuses our measurement on completed student decisions instead of page views. The event definition and supporting evidence are documented in the event schema and interview logs.

> Wk7 · Gate status clarified: no public URL, production PostHog events, matched counts or dashboard were verifiable in the supplied repository snapshot; gate remains open at rung 0 until a phone walk confirms rung 1 · evidence: README.md, 03-build/analytics/event-schema.md, 03-build/sprints/sprint-2.md · owner: AP

This entry documented the lack of verified deployment evidence at the time of the decision. Although the README now lists a Railway URL, the full production journey and analytics gate still need confirmation.

## 4. My person this week

**The field-week person I am responsible for:** T1 — third-year Computer Science student and job seeker, from Interview 07.

**How and when the link reaches them:** After verifying that the production website works on a phone, I will ask for consent and send the link directly. I will record when it was sent and whether the person opened and used the application in `03-build/sprints/sprint-2.md`.

My goal is to observe whether a real student can complete the five Apply/Skip decisions without help and whether that action is correctly recorded.
