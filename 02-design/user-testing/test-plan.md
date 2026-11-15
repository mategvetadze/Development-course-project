# Prototype Test Plan

**Prototype v1 link:** [same as README Prototype row](https://htmlpreview.github.io/?https://github.com/mategvetadze/Development-course-project/blob/main/02-design/prototype/index.html)

**Riskiest assumption under test:** A student who sees a job post's key facts (requirements, hours, salary, deadline) on one card will decide to apply or skip without asking to open the original post. (from `02-design/prototype-plan.md` section 1)

## The frozen test (copied from `02-design/prototype-plan.md`, section 5, unchanged)

**Task, read aloud word for word:** "Here are five job posts on paper cards. For each one, tell me out loud whether you would apply or skip it, and why. Use only the cards. The envelope has the full post, but you can only open it if you really need it."

**On the clickable prototype (Track B):** the five cards are on the phone screen. Saying they need the full original post, or asking the runner to show it, counts as "opening the envelope."

**Success:** A session passes only if all three are true:
- The tester says apply or skip for all five cards within 5 minutes.
- The tester opens the envelope, or asks to see the original post, for 1 card or fewer.
- The tester says out loud that they would still check the original post before deciding, for 1 card or fewer.

**Failure behaviors:**
1. The tester opens the envelope, or asks to see the original post, for 2 or more of the 5 cards.
2. The tester takes longer than 5 minutes to decide on all five.
3. The tester says out loud that they would still check the original post before deciding, for 2 or more cards.

**Decision rule (out of 5):** If 3 or more fail, the assumption is wrong. We then stop building a card that replaces opening the post, and instead test whether students can remove irrelevant and repeated posts from a long list (Pattern 1, logs 01, 04, 06, 07, 08).

**Predicted first mistake:** They will open the envelope on the card whose salary or hours are missing, because they will not trust a card that leaves out the terms (08).

## Five testers

All five from our ICP (university student looking for internship / entry-level work). None in this course. Code names only.

| # | Code name | Role (as in our ICP) | Why they fit the ICP | Session runner (asks) | Session logger (writes) | Target day | Status (messaged / booked / done) |
|---|---|---|---|---|---|---|---|
| 1 | T1 | 3rd-year student, job searcher | Interview 07 participant; junior posts + experience mismatch | AP | MG | before Week 7 lab | messaged (confirm reply) |
| 2 | T2 | 2nd-year student, job searcher | Interview 08 participant; duplicates, missing salary/hours, ignored alerts | AP | AS | before Week 7 lab | messaged (confirm reply) |
| 3 | T3 | 3rd-year management student | Interview 01 participant; skips liked posts when eligibility unclear | AS | AP | before Week 7 lab | messaged (confirm reply) |
| 4 | T4 | CS student, new (not interviewed) | Same ICP; new eyes for Track B; MG books | MG | ST | before Week 7 lab | not recruited yet — MG to message |
| 5 | T5 | CS / job-seeking student, new | Same ICP; ST books | ST | MG | before Week 7 lab | not recruited yet — ST to message |

## Session protocol (same every time)

1. The tester opens the prototype link on their own phone. Not yours.
2. The runner reads the task word for word, then says nothing.
3. The logger starts the timer on the last word of the task and writes: time to first tap, time to finishing all five decisions, every unprompted sentence verbatim, and every request to see the original post.
4. When the tester stops, or at 5 minutes, the runner asks one question only: "What were you expecting to happen?"
5. The logger writes the verdict against the rule before anyone discusses the session.
