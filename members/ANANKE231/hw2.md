# Homework 2 · Ani Purtskhvanidze (@ANANKE231) · Prometheus

## 1. Ship report

My main responsibility in CareerCards is frontend development. The goal of our product is to help students review five internship or entry-level job opportunities and decide whether to Apply or Skip.

I worked on our clickable prototype and contributed to the project documentation. My frontend responsibilities in Sprint 1 included displaying five opportunities, showing their important details, and implementing Apply/Skip interactions.

| What I shipped | Story or rung | Commit link(s), from my account | Live at production URL? | Walked or checked by |
|---|---|---|---|---|
| CareerCards clickable prototype | Week 5 prototype | [e9f2137](https://github.com/mategvetadze/Development-course-project/commit/e9f2137748eded2560f048e95ee6d08434052a04) | Prototype, not verified in production | No reviewer recorded |
| Prototype HTML, CSS and JavaScript improvements | Week 5 prototype | [5a2fee0](https://github.com/mategvetadze/Development-course-project/commit/5a2fee042f9991c020fc9736aa73975d4010eafa) | Prototype, not verified in production | No reviewer recorded |
| MVP boundary, event schema and sprint planning documentation | Weeks 5–7 planning | [3771b60](https://github.com/mategvetadze/Development-course-project/commit/3771b60651f0dac2b83aad46d0876cda21698d48) | Documentation contribution | GitHub commit evidence |

**The piece I am least sure works for a real person, and how I will know by Lab 8:**

I am least sure about the complete Apply/Skip journey on the deployed website. I tested the frontend locally, but the job cards could not load because the database connection or required migrations were unavailable. To confirm the journey works, a teammate needs to complete all five decisions on a phone, receive the final summary, and verify the saved decisions and PostHog events.

**One thing I did that was not my assigned story:**

Although my main responsibility is frontend development, I also contributed to the MVP boundary, analytics documentation and sprint planning. This helped me understand how our interface connects to the product's goals and how user interactions should be measured. Evidence: commit [3771b60](https://github.com/mategvetadze/Development-course-project/commit/3771b60651f0dac2b83aad46d0876cda21698d48).

## 2. Pattern journal — Weeks 5 to 7

### Week 5 · One metric that matters

During Week 5, I worked on our clickable CareerCards prototype using HTML, CSS and JavaScript. My goal was to make the internship cards simple to understand and easy to use. I learned that counting website visits does not tell us whether students actually benefit from the product. Measuring students who finish all five Apply/Skip decisions gives us more meaningful evidence of value.

### Week 6 · The smallest complete journey

During Week 6, I focused on the frontend requirements for displaying job opportunities, showing important information and supporting Apply/Skip decisions. I also contributed to the MVP and sprint documentation outside my main responsibility. I learned that an MVP is not just a collection of working screens. Students need to complete the whole journey and receive a useful result. I reconstructed this entry using our project documentation and commits.

### Week 7 · Ship to learn

During Week 7, I ran the Next.js frontend and FastAPI backend locally to examine the student experience. The frontend opened successfully, and the backend health endpoint responded correctly. However, the opportunities could not load because the database was unavailable. This showed me that a working interface does not necessarily mean the entire product works. My next step is to verify the complete five-card journey and its analytics on the deployed website.

## 3. My DECISIONS.md lines

> Wk5 · North star: Number of students who complete apply-or-skip decisions for all five job cards within five minutes, per week; rejected prototype opens (does not prove value) and job card views (does not prove decisions) · evidence: 03-build/analytics/event-schema.md, 01-discovery/interview-logs/01-student-management.md, 01-discovery/interview-logs/08-student-business.md · owner: AP

This decision focuses our success metric on completed student decisions rather than simply viewing the opportunities. The supporting evidence is recorded in our event schema and interview logs.

> Wk7 · Verification update (recorded 25 Nov): Railway URL is listed in README but a production phone walk is still unverified; AP ran the Next.js UI locally, FastAPI /health succeeded, but database readiness and latest-set endpoint failed, so none of the five gate rungs can yet be marked passed · evidence: README.md, 03-build/analytics/event-schema.md, 03-build/sprints/sprint-2.md; local GET /health, /health/ready, /api/sets/latest results · owner: AP

This decision records the local tests I performed and distinguishes them from a verified production deployment.

## 4. My person this week

**The field-week person I am responsible for:** T1 — a third-year Computer Science student looking for an internship or entry-level job, from Interview 07.

**How and when the link reaches them:** My plan is to contact T1 directly after the production website is verified and send the CareerCards link with their consent. I will record the actual sending date and whether they complete the journey in `03-build/sprints/sprint-2.md`.

The goal is to understand whether the student can complete five decisions without help and whether those decisions are recorded correctly. Outreach completion has not yet been documented.
