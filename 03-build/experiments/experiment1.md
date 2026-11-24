# Experiment 1

**The drop this is about:** between "named" and "link sent": 3 people named in sprint-2.md, 0 links sent during the field week (break-readout.md, section 3).

**Baseline, measured before any change:** 0 links delivered, 0 student_opens_card_set and 0 student_completes_card_set from real people, Lab 7 to Lab 8. Read from the field table in sprint-2.md and PostHog (internal-user filter on).

## The bet

| Part | Ours |
|---|---|
| Hypothesis | Students we interviewed will finish the five cards when the link reaches them in a personal message, on the channel we interviewed them on. |
| Change | For 7 days, each teammate sends the link by hand to the interviewees they talked to: one personal message per person, on the original channel, with the URL tagged `?src=instagram` or `?src=friend`. Each send is written in the field table with a date. No code. |
| Metric | Number of real people with a student_completes_card_set event, out of the number of links delivered. PostHog Trends, internal-user filter on, cross-checked against the decisions table (5 rows per anonymous_id). |
| Success threshold | 3 or more of 6 people finish all five cards within 7 days of their message. |
| Failure threshold | 1 or fewer of 6 finish, or fewer than 3 of 6 even open the page. |
| Decision rule | Success: keep direct messages as our channel and recruit 10 more interviewees for Lab 10. Failure with opens but no finishes: the card is the problem, so ST calls 2 people who opened and stopped, and we log why. Failure with no opens: the message is the problem; we rewrite it and try a different channel for 3 days. Fewer than 4 links delivered: run 7 more days and claim nothing. |

**Who runs it:** ST (field table and daily count) · **Starts:** 25 Nov · **Ends:** 2 Dec

**What we will not change while it runs:** the five cards on the live page, the Apply/Skip flow, and the message text above.

**What we already suspect:** these are people who already gave us half an hour for an interview, so they are friendlier than a stranger. A success here says the product works for warm contacts, not that strangers will come. Lab 10 has to test a cold channel.

## Run log

Day 0 (24 Nov): 1 link delivered (T3, Instagram, 23:57). Opened: [ ].

Day 1 (25 Nov): [links delivered today, opens, finishes]

## Result (filled in when it ends, not before)

Not yet.
