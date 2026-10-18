# Homework 1 · Ani Purtskhvanidze (@ANANKE231) · Team Prometheus

## 1. My interview log

| Log file (link) | My role (asked / logged / both) | What this interview changed, in one sentence |
|---|---|---|
| [07-student-cs.md](../../01-discovery/interview-logs/07-student-cs.md) | both | A student contacted employers because posts said "junior level" and was then told experience was needed, so the problem is not only the number of openings but also posts that don't show whether you qualify. |
| [08-student-business.md](../../01-discovery/interview-logs/08-student-business.md) | both | The student's last search took about an hour instead of ten minutes, and they described duplicate posts, missing salary and hours, and alerts they turned off as irrelevant, so the problem is also the quality of listings, not only their number. |

**The quote I heard myself that mattered most, with its log number:**

> "The posts said junior level, so I contacted them" (Interview 07, Q9)

This mattered because the student acted on the word "junior" and was then told they needed experience. It pointed us toward how clear and reliable posts are, not just how many exist.

**One moment I broke the Mom Test, and what I asked instead next time (Interview 08):**

I asked: "Have you ever tried using any tool or platform to make your job search easier?" That question steers toward solutions and invites a yes, a no, or a wish instead of a real story. The student happened to answer with a real event: they had turned on LinkedIn job alerts and turned them off because too many of the emails were irrelevant (logged under Workaround in log 08).

Next time I would ask about a specific past moment: "Tell me about the last job alert you received. What did it say, and what did you do next?" This asks for actual behavior and suggests no solution.

## 2. Pattern journal, Weeks 1 to 4

### Week 1 · Act like an owner, not a role

In our team contract my primary accountability is Build (fullstack development and deployment). I signed it on September 28 and named a real first outreach target, Lado Sitchinava, which is a discovery task, not a build task. The contract's one pre-written rule says no member may answer a question about the product with "that is not my role." I took that literally: discovery was my job too, and in Week 3 I acted on it by running two interviews.

Evidence: [Team contract](../../00-foundation/team-contract.md)

### Week 2 · Evidence over opinion

I added three entries to our problem pool, covering two problems. Two entries were about parking in the city center (my friends Giorgi and Nika each circled the same three streets for 20 minutes and arrived 15 minutes late). The third was about a KIU student who kept deadlines in different chats and notes, missed an assignment date, and lost 10 points. Each entry names a real person, what I saw, and a cost I could name, not an app idea. The team then chose to investigate Saba's job-search problem.

Evidence:
- [Problem pool](../../00-foundation/problem-pool.md)
- [DECISIONS.md](../../DECISIONS.md) (Wk2 line)

### Week 3 · Kill your favorite idea

My contract accountability is Build, but I personally asked the questions in two discovery interviews, 07 and 08, and wrote both logs. In interview 07, a third-year Computer Science student contacted employers because posts said "junior level" and was told experience was needed. In interview 08, a second-year Business Administration student described duplicate posts, missing salary and hours, and job alerts irrelevant enough to turn off. Our prediction said we were wrong if students did not raise too few jobs or unfair pay on their own. Neither of my two students raised either, and DECISIONS.md records that prediction as killed with both logs listed as evidence. Both logs are committed in the team repo, and what these students actually said is part of why we dropped our first explanation.

Evidence:
- [Interview 07 — Computer Science student](../../01-discovery/interview-logs/07-student-cs.md)
- [Interview 08 — Business Administration student](../../01-discovery/interview-logs/08-student-business.md)
- [DECISIONS.md](../../DECISIONS.md) (Wk3 line)

### Week 4 · The prototype is the conversation

My logs 07 and 08 are cited in our patterns analysis (07 in Patterns 1 to 3, 08 in Patterns 1 to 4), including Pattern 1, the strongest pattern, which our Wk4 problem statement in DECISIONS.md restates. Both logs point to the same gap: students cannot tell from a post whether they qualify, and duplicate posts and irrelevant alerts add noise. That feeds our prototype plan's riskiest assumption: that a student who sees a post's key facts (requirements, hours, salary, deadline) on one card can decide to apply or skip without opening the original post. The test can fail: a tester fails if they open or request the original post for 2 or more of the five cards, say they would still check the original for 2 or more cards, or take over 5 minutes. The assumption is rejected if 3 or more of 5 testers fail. I also recorded the follow-ups from my two logs in DECISIONS.md: get the text of the "junior" post that required experience, and an example of a duplicated post and what it was missing.

The prototype is planned, not yet built or tested. The Lab 4 schedule calls for building it in Lab 5; I will document the results once testing happens.

Evidence:
- [Interview 07 — Computer Science student](../../01-discovery/interview-logs/07-student-cs.md)
- [Interview 08 — Business Administration student](../../01-discovery/interview-logs/08-student-business.md)
- [Patterns analysis](../../01-discovery/synthesis/patterns-analysis.md)
- [DECISIONS.md](../../DECISIONS.md) (Wk4 follow-up line, owner AP)
- [Prototype plan](../../02-design/prototype-plan.md)

## 3. My DECISIONS.md citations

Source: [DECISIONS.md](../../DECISIONS.md)

| The line, copied | What I did for it |
|---|---|
| Wk3 · Prediction "We are wrong if students describing their job search do not raise on their own, before we mention it, either that there are too few jobs in their field or that the pay and requirements offered are unfair." verdict: killed · evidence: 01-discovery/interview-logs/01-student-management.md, 01-discovery/interview-logs/02-student-cs.md, 01-discovery/interview-logs/03-student-cs.md, 01-discovery/interview-logs/04-student-cs.md, 01-discovery/interview-logs/05-student-cs.md, 01-discovery/interview-logs/06-student-law.md, 01-discovery/interview-logs/07-student-cs.md, 01-discovery/interview-logs/08-student-business.md · owner: AS | I supplied evidence: I personally conducted and logged interviews [07](../../01-discovery/interview-logs/07-student-cs.md) and [08](../../01-discovery/interview-logs/08-student-business.md), two of the eight logs it cites. Neither student said there were too few jobs or that pay was unfair. The owner of the line is AS. |
| Wk4 · Follow-up from interviews 07 and 08: ask for the text of the "junior" posting that required experience, and an example of a duplicated post and what information was missing · evidence: 01-discovery/interview-logs/07-student-cs.md, 01-discovery/interview-logs/08-student-business.md · owner: AP | I recorded the follow-up questions arising from my interviews 07 and 08, including requesting the original junior-level posting and an example of a duplicate listing. This line is attributed to AP in the team decision log. |