# Pattern Journal · Archil Sanikidze (@Archi-lee-Sun)

The entries for Weeks 1 to 4 were written retrospectively on 18 October 2026 from my interview records, repository commits, and recollection. They were not committed during the individual weeks.

## Week 1 · Act like an owner, not a role

My primary accountability in the team contract is Discovery, but I also uploaded the team contract, a team setup task outside that lane. I added two problems I had observed: my mother's difficulty with a tax declaration and my friend's difficulty finding tutoring students. I recorded the struggle and cost for each, rather than starting with a product idea. I did not run a separate quick test that week.

Evidence: [team contract](../../00-foundation/team-contract.md), [problem pool](../../00-foundation/problem-pool.md).

## Week 2 · Evidence over opinion

I took part in the lab discussion where we compared the team's problems and chose to investigate students' job search. My beginner-tutor observation was considered as the runner-up. The decision record links the choice to the team's problem pool and four-filters scorecard. I contributed the tutor observation, but I did not run an independent test of either problem that week.

Evidence: [problem pool](../../00-foundation/problem-pool.md), [four-filters scorecard](../../00-foundation/four-filters-scorecard.md), [Week 2 decision](../../DECISIONS.md).

## Week 3 · Kill your favorite idea

I prepared interview questions and shared them with my teammates. I personally asked the questions in interviews 03–06 with friends and fellow students. Two conversations were recorded as audio and two were conducted through Discord messages; I turned the responses into text and uploaded the logs. I used AI to help organize our analysis, reviewed the resulting content against our discussion, and committed the affinity map, patterns analysis, revised interview script, problem-hypothesis addendum, and Week 3 decision. My interviews supplied four of the logs cited by the decision to kill our original prediction. I also added a separate affinity-map cluster for courses and career events after noticing this theme in my interviews. Recording and transcribing the interviews, then organizing them with AI, helped us check the prediction quickly; I did not test a prototype.

Evidence: [interviews 03](../../01-discovery/interview-logs/03-student-cs.md), [04](../../01-discovery/interview-logs/04-student-cs.md), [05](../../01-discovery/interview-logs/05-student-cs.md), [06](../../01-discovery/interview-logs/06-student-law.md); [affinity map](../../01-discovery/synthesis/affinity-map.md), [patterns analysis](../../01-discovery/synthesis/patterns-analysis.md), [interview script v2](../../01-discovery/interview-script-v2.md), [problem hypothesis](../../01-discovery/problem-hypothesis.md), [Week 3 decision](../../DECISIONS.md).

## Week 4 · The prototype is the conversation

The team's Week 4 problem statement cites the patterns analysis built from our interview evidence, including my logs. I supplied that evidence, but I did not write the Week 4 decision line, review the team's prototype plan, run a prototype session, or make a quick prototype test. I cannot claim personal prototype learning yet.

Evidence: [Week 4 decision](../../DECISIONS.md), [patterns analysis](../../01-discovery/synthesis/patterns-analysis.md), [team prototype plan](../../02-design/prototype-plan.md).

**Weeks 5 to 7:** Written retrospectively on November 21, 2026, applying the weekly principles to my November 17–18 commits and subsequent setup. These entries are copied from [my HW2](hw2.md#2-pattern-journal-weeks-5-to-7).

## Week 5 · One metric that matters

I applied the lecture's value/event/window principle to our existing [North Star](../../DECISIONS.md): students completing five decisions within five minutes, per week. With Codex, I added database-clock timing and distinct-anonymous-student counting instead of trusting client durations or equating completed sets with students. This extended my contribution into analytics; controlled fixtures checked duplicate identities and exact time boundaries without live users ([03195ef](https://github.com/mategvetadze/Development-course-project/commit/03195ef); W5 PDF pp. 5, 7, 25).

## Week 6 · The smallest complete journey

I kept the approved publish→read→decide→summary flow and existing stack, leaving accounts, scraping and search outside the implementation. My Codex-assisted work covered persistence and reload behavior across frontend and backend, beyond Discovery. A disposable PostgreSQL database and real HTTP fixture tested the complete slice without waiting for hosting ([PR #1](https://github.com/mategvetadze/Development-course-project/pull/1), [live_server.py](../../backend/tests/live_server.py); W6 PDF pp. 5, 9, 17).

## Week 7 · Ship to learn

I moved into infrastructure by creating the Neon database, running its schema and connecting Render/PostHog. Codex-assisted local SDK collectors and a 375px browser journey checked event delivery and saved decisions before production verification ([PR #2](https://github.com/mategvetadze/Development-course-project/pull/2)). These checks prepare the learning loop; a real-person session and production reconciliation remain outstanding (W7 PDF pp. 3, 15, 29).

Lecture references use PDF page numbers: W5 = *PDFSE-W5-F26 (1).pdf*; W6 = *PDFSE-W6-Lecture-Slides (1).pdf*; W7 = *PDFSE-W7-F26.pdf*.
