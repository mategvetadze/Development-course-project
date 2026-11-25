# Homework 2 · Ani Purtskhvanidze (@ANANKE231) · Prometheus

## 1. Ship report

My main responsibility in CareerCards is frontend development. Our product helps students review five internship or entry-level opportunities and decide whether to Apply or Skip. I contributed to the clickable prototype and product documentation, while my assigned Sprint 1 stories covered the student-facing interface, job details and Apply/Skip interactions.

| What I shipped | Story or rung | Commit link(s), from my account | Live at the production URL? | Walked or checked by |
|---|---|---|---|---|
| Clickable CareerCards prototype | Week 5 prototype | [e9f2137](https://github.com/mategvetadze/Development-course-project/commit/e9f2137748eded2560f048e95ee6d08434052a04) | Prototype, not production | No reviewer recorded |
| HTML, CSS and JavaScript prototype improvements | Week 5 prototype | [5a2fee0](https://github.com/mategvetadze/Development-course-project/commit/5a2fee042f9991c020fc9736aa73975d4010eafa) | Prototype, not production | No reviewer recorded |
| MVP, event schema and sprint planning documentation | Weeks 5–7 planning | [3771b60](https://github.com/mategvetadze/Development-course-project/commit/3771b60651f0dac2b83aad46d0876cda21698d48) | Documentation | GitHub commit |

**The piece I am least sure works for a real person, and how I will know by Lab 8:**

My biggest concern is frontend analytics. According to Saba's HW2, he successfully completed the five-card journey on the Railway website on November 24. However, the production student page is served through `backend/`, while some browser analytics improvements were made in the separate Next.js `app/`. I need to verify that `student_opens_card_set` and `student_views_card` are actually recorded in PostHog when someone uses the production website.

**One thing I did that was not my assigned story:**

Besides my frontend responsibilities, I contributed to the MVP boundary, event schema and sprint planning. This helped connect the interface to measurable user actions and the team's north star metric. Evidence: [3771b60](https://github.com/mategvetadze/Development-course-project/commit/3771b60651f0dac2b83aad46d0876cda21698d48).

## 2. Pattern journal — Weeks 5 to 7

These entries were reconstructed from project commits, documentation and my local testing.

### Week 5 · One metric that matters

During Week 5, I contributed to our clickable CareerCards prototype using HTML, CSS and JavaScript. Building a quick prototype let us explore the student journey without waiting for the backend. I learned that counting page visits does not tell us whether students actually benefit from our product. A better metric is how many students finish all five Apply/Skip decisions within five minutes.

### Week 6 · The smallest complete journey

During Week 6, my assigned frontend responsibilities included displaying five opportunities, showing their important details and supporting Apply/Skip interactions. I also contributed to planning and documentation beyond my assigned development work. I learned that an MVP must provide a complete experience, not just attractive screens. The student should finish the journey with a useful list of opportunities.

### Week 7 · Ship to learn

During Week 7, I ran the Next.js frontend and FastAPI backend locally to test their integration. Both applications started, but the opportunities could not load because my local database connection or required migrations were unavailable. Saba's report confirms that he subsequently walked the five-card journey on the Railway production website, which showed that the deployed version could complete the main interaction. However, I learned that working frontend functionality and verified analytics are different things. Our team still needs evidence that browser events reach PostHog from the version actually served in production.

## 3. My DECISIONS.md lines

> Wk5 · North star: Number of students who complete apply-or-skip decisions for all five job cards within five minutes, per week; rejected prototype opens (does not prove value) and job card views (does not prove decisions) · evidence: 03-build/analytics/event-schema.md, 01-discovery/interview-logs/01-student-management.md, 01-discovery/interview-logs/08-student-business.md · owner: AP

This decision focuses our measurement on completed student decisions rather than page views. The supporting evidence is in the event schema and interview logs.

> Wk7 · Verification update (recorded 25 Nov): Railway URL is listed in README but a production phone walk is still unverified; AP ran the Next.js UI locally, FastAPI /health succeeded, but database readiness and latest-set endpoint failed, so none of the five gate rungs can yet be marked passed · evidence: README.md, 03-build/analytics/event-schema.md, 03-build/sprints/sprint-2.md; local GET /health, /health/ready, /api/sets/latest results · owner: AP

This decision records what I personally verified locally at that point. Saba's separate November 24 production walkthrough provides additional team evidence, but it does not establish that all five gate requirements passed.

## 4. My person this week

**The field-week person I am responsible for:** T1, a third-year Computer Science student looking for an internship or entry-level job, from Interview 07.

**How and when the link reaches them:** I plan to send T1 the production CareerCards URL directly after confirming that the published opportunities are real and the student journey is accessible. I will document the sending date and whether the student completes the five decisions in `03-build/sprints/sprint-2.md`.

My goal is to understand whether a student can complete the journey without assistance and whether their interactions are recorded correctly. Outreach completion is not yet documented.