[hw2.md](https://github.com/user-attachments/files/34980749/hw2.md)
# Homework 2 · Saba Tabukashvili (@tabukashvilisaba) · Prometheus

Save this file as: members/tabukashvilisaba/hw2.md, committed from your own account.

Individual, 5 points, due before Lab 8. 400 to 700 words. Every claim points at a commit, a file, or a DECISIONS.md line.

AI use: I used Claude to draft the Lab 6 planning files and Sprint 2, and to review and fix StudentCardSet.tsx; logged in docs/ai-usage-log.md ([commit link]).

## 1. Ship report

| What I shipped | Story or rung | Commit link(s), from my account | Live at the production URL? | Walked or checked by |
|---|---|---|---|---|
| MVP boundary: 5-step journey, cut list with log citations, step-to-event map | Lab 6, boundary | [link to "Update MVP boundary documentation"] | n/a | [teammate] |
| Event schema rows for all five journey events | Lab 6, schema | [link to "Update event-schema.md"] | n/a | [teammate] |
| Architecture: diagram, stack, secrets | Lab 6, architecture | [link to "Create architecture.md"] | n/a | [teammate] |
| Sprint 1 plan with stories, criteria and slip rule | Lab 6, sprint | [link to "Create sprint-1.md"] | n/a | [teammate] |
| Sprint 2 plan, honest gate table | Lab 7, sprint | [link] | n/a | [teammate] |
| Wired PostHog in the browser (student_opens_card_set, student_views_card), fixed Apply on iPhone and double taps in StudentCardSet.tsx | R2 | [link to the "Wire PostHog client events" commit] | [Yes/No] | [teammate who walked it] |
| [Deploy: Render + Vercel setup with MG] | R1 | [link] | [Yes/No] | MG |
| [Reconcile and dashboard, if you do it] | R4+R5 | [link] | [Yes/No] | AP |

**The piece I am least sure works for a real person, and how I will know by Lab 8:** [e.g. the Skip reason picker on a small phone; I will compare student_views_card for position 5 against student_completes_card_set: views with no completion means people stop before the end]

**One thing I did that was not my assigned story:** I reviewed MG's student page before the deploy and found that PostHog was never started in the browser, so two of our five schema events would never have arrived; I fixed it ([commit link]). [Rewrite in your own words.]

## 2. Pattern journal, Weeks 5 to 7

Write these in your own words. I did not write my Week 5–7 entries in their own weeks; I am writing them now.

### Week 5 · One metric that matters

[What did YOU do for the north star "students who complete apply-or-skip on all five cards within five minutes"? Did you argue for another metric? Where did you go beyond your lane? What did you hack to test faster? 3–5 sentences.]

### Week 6 · The smallest complete journey

[Facts you can use: you committed the boundary, schema, architecture and sprint-1 files; the journey was changed from CS-only to any field after checking icp.md v2, because the logs showed students in many fields; scraping was cut in favour of hand-picked cards. Say which cut YOU agreed or disagreed with, and why. 3–5 sentences.]

### Week 7 · Ship to learn

[What did you learn from the gate not passing on time? What did you change (e.g. taking the deploy)? What did you hack together? 3–5 sentences.]

## 3. My DECISIONS.md lines

Every line since Week 5 where I am the owner or drove the evidence. Paste each exactly as it is in DECISIONS.md.

[Wk6 · MVP boundary: ... · owner: ??]  ← paste exactly; if it says MG, see note below

[one sentence: the evidence was the cut list in 03-build/mvp-boundary.md, citing logs 01, 06, 07, 08, 10, 11]

Wk7 · Gate open at rung 1: missing production URL, journey on production, north star event, reconcile and dashboard; owners and times in sprint-2.md · evidence: 03-build/sprints/sprint-2.md · owner: ST

[one sentence: the evidence is the gate table in 03-build/sprints/sprint-2.md and the README's Live product row]

## 4. My person this week

The field-week person I am responsible for: Mgmt-1, 3rd-year Management student (log 01) · how and when the link reaches them: Instagram DM with the production URL ending ?src=instagram, the day after rung 3 passes.
