# Prototype Plan

## 1. The riskiest assumption

We assume that a student who sees a job post's key facts (requirements, hours, salary, deadline) on one card will decide to apply or skip without asking to open the original post.

Why this one is riskiest: 01 says "I have to open many job posts to find out whether I'm actually eligible," and 08 messaged people to ask the salary and the hours, but no log shows whether a student would trust a short card instead of reading the original post. That is why we test it.

## 2. The one action

A third-year university student who is looking for an internship can decide, for each of five job cards, to apply or skip, using only the card.

## 3. Fidelity

| Choice (paper / clickable / coded) | Why it is the cheapest thing that can kill the assumption in section 1 | Tool | Time we will spend |
|---|---|---|---|
| Paper | The assumption is about whether a student trusts a card, not about software. Five real posts rewritten as paper cards test it. The full original post sits in a sealed envelope; opening it counts against the card. | Pen, paper, printed real posts | 1 hour |

## 4. Screens, each traced to evidence

| Screen | What the tester does on it | The log or problem-statement sentence that earns it |
|---|---|---|
| 1. Five cards laid out together | Reads the five cards and picks apply or skip for each one | Problem statement, sentence 2: students open post after post across several sources (01, 04, 06, 07, 08) |
| 2. Each card shows requirements, hours, salary and deadline | Checks whether they qualify, whether the schedule fits, and whether the deadline is still open | 01 skipped liked positions because they were unsure they qualified; 06 found 3 years of experience asked for a "junior" role; 08 asked for salary and hours; 01, 04, 06 and 08 missed a deadline, course or internship |

Will not appear, even if a tool generates it: login, notifications, search or filters, a ranking or score, CV upload, chat, user profiles, a "recommended for you" list.

## 5. The test that can fail

Write this before the first session, and do not edit it after.

**Task, read aloud to the tester, word for word:** "Here are five job posts on paper cards. For each one, tell me out loud whether you would apply or skip it, and why. Use only the cards. The envelope has the full post, but you can only open it if you really need it."

**A session passes only if all three are true:**
- The tester says apply or skip for all five cards within 5 minutes.
- The tester opens the envelope, or asks to see the original post, for 1 card or fewer.
- The tester says out loud that they would still check the original post before deciding, for 1 card or fewer.

**A session fails if any one of these happens:**
- The tester opens the envelope, or asks to see the original post, for 2 or more of the 5 cards.
- The tester takes longer than 5 minutes to decide on all five.
- The tester says out loud that they would still check the original post before deciding, for 2 or more cards.

**Decision rule:** Out of 5 testers, if 3 or more fail, the assumption is wrong. We then stop building a card that replaces opening the post, and instead test whether students can remove irrelevant and repeated posts from a long list (Pattern 1, logs 01, 04, 06, 07, 08).

**Our prediction of the first thing a tester gets wrong:** They will open the envelope on the card whose salary or hours are missing, because they will not trust a card that leaves out the terms (08).

## 6. Five testers (recruitment plan, not confirmed bookings)

People from our ICP who are not in this course. Code names only. At least 2 who have not been interviewed before.

| Code name | From log, or new | Who on the team books them |
|---|---|---|
| T1 | Interview 07 participant — invitation not confirmed | AP (proposed; confirm) |
| T2 | Interview 08 participant — invitation not confirmed | AP (proposed; confirm) |
| T3 | Interview 01 participant — invitation not confirmed | AS (proposed; confirm) |
| T4 | New participant — not recruited | MG (proposed; confirm) |
| T5 | New participant — not recruited | ST (proposed; confirm) |

**Planning status:** These are proposed recruiting assignments, not confirmed bookings or participant consent. Confirm availability and ownership with the team before testing.

## Self-check before committing

- Section 1 is about behavior, not technology: yes.
- Section 5 has failure behaviors we can see with our own eyes: yes.
- Every screen in section 4 cites a log or a problem-statement sentence: yes.
