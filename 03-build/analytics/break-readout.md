# Field-week readout

Our state: **B — live, nobody came.** The product was live, but no real person had the link during the field week. Our field table is our data.

## 1. Is it real?

| Source | Count of student_completes_card_set from people who are not our team | Window | How it was counted |
|---|---|---|---|
| PostHog | [MG: count] | Lab 7 (17 Nov) to Lab 8 (24 Nov) | Trends insight, total count, internal-user filter on |
| Database | [AP: count] | same | `select count(*) from (select anonymous_id, set_id from decisions where created_at between '2026-11-17' and '2026-11-24' group by 1, 2 having count(*) = 5) t;` minus our own test ids |

Match: [yes/no]. Checked by AP.

Expected: 0 in both, because no link reached a real person before 24 Nov 23:57 (section 3). Any count above 0 is our own testing; ST's own production walk on 24 Nov is one of those and must be excluded.

## 2. Prediction against reality

Our prediction, pasted from sprint-2.md exactly as committed:

> By Lab 8: Target 2 student_completes_card_set events from real people (ms_total <= 300000), plus at least 3 distinct real student_opens_card_set events.
> We are wrong if: 0 of the 3 contacted non-classmate students complete five decisions.

| What we predicted | Predicted | Real |
|---|---|---|
| student_completes_card_set from real people | 2 | 0 |
| Distinct real student_opens_card_set | 3 | 0 |
| Contacted students who completed five decisions | at least 1 of 3 | 0 of 0 contacted |

Did "we are wrong if" fire? Not as written: it assumed 3 students would be contacted, and none were contacted during the week. The prediction was never tested. That is the finding.

## 3. Where people stop

Our field table as a funnel, Lab 7 to Lab 8:

| Step | Count |
|---|---|
| Named in sprint-2.md (T1, T2, T3) | 3 |
| Link sent | 0 (T3 was sent one on 24 Nov 23:57, after the window) |
| Opened | 0 |
| Finished five cards | 0 |

**Widest drop:** between "named" and "link sent": 3 named, 0 sent.

What the product did in the same week: the production URL loaded and the five-card journey finished on a phone (ST, 24 Nov: five cards, Apply or Skip on each, "Your apply list" appeared). So the drop is not in the product; it is before anyone reached it.

## 4. Who is standing at the drop

**The actor: our team.**

| Person | Link sent by | What happened | What did not happen |
|---|---|---|---|
| T1, 3rd-year CS student (interview 07) | AP | Named in sprint-2.md | Link sent |
| T2, 2nd-year business student (interview 08) | AP | Named in sprint-2.md | Link sent |
| T3, management student (interview 01) | ST | Named in sprint-2.md; link sent 24 Nov 23:57 | Link sent inside the field week |

Why: sprint-2.md tied every send to "after rung 3", and rung 3 (north star event confirmed in PostHog from production) was never marked passed. The deploy reached Railway during the week, but nobody updated the gate table, so the trigger to send never fired.

## 5. What the data refuses to say

| Question | Who we ask | Asked by, and by when |
|---|---|---|
| Do real students finish five cards at all? | T3, and T1 and T2 once sent | ST and AP, by Lab 9 |
| Is the card enough to decide without opening the post? | T3, after she uses it: "Was there a card you had to open the post for? Which field was missing?" | ST, within two days of her visit (new log 12) |
| Are the five live cards real openings? | AS | ST, 25 Nov |
| Does student_views_card fire from the live page? | PostHog Activity, after T3's visit | MG, 26 Nov |

## 6. Claims

**Direction:** The product works end to end on a phone; the field week failed on distribution: 3 people named, 0 links sent.

**Not yet:** anything about whether students decide faster with cards. We have no real-user event to support it, and we make no claim about it.

## 7. What changes

**Comes off the plan:** the rule "send links only after rung 3". A link goes out as soon as the production journey is walked on a phone.

**Goes on:** sending the link, by hand, to the people we interviewed, tracked per person with a date in the field table (Experiment 1).

Wk8 · Field-week read: state B, predicted 2 completions from real people, real 0; widest drop before the product (3 named, 0 links sent), actor: our team; links now go out as soon as a phone walk passes, Experiment 1 tests direct messages to interviewees · evidence: 03-build/analytics/break-readout.md, 03-build/sprints/sprint-2.md · owner: ST

## 8. Who is next

Our field table as a funnel: named 3 · link delivered 1 (T3, 24 Nov) · opened [ ] · finished [ ]

| Next person | Channel, and our evidence for it | Sent by | Sent in the lab? |
|---|---|---|---|
| T3, management student (interview 01) | Instagram: the channel we interviewed her on (log 01) | ST | Yes: 24 Nov 23:57 |
| T1, 3rd-year CS student (interview 07) | Messenger, the channel AP used for her interviews | AP | [yes/no] |
| T2, 2nd-year business student (interview 08) | Messenger | AP | [yes/no] |
| CS-6, 1st-year CS student (interview 10) | Messenger | MG | [yes/no] |
| CS-7, 4th-year CS student (interview 11) | Messenger | MG | [yes/no] |
| CSM-1, CS and Math student (interview 09) | Instagram, as in log 09 | ST | [yes/no] |

**The exact message we sent:** "Hi! A few weeks ago you told us about searching for internships. We made a page with 5 openings; for each one, tap Apply or Skip. It takes a few minutes. It's a student project: we count clicks and decisions, never names." followed by the production URL with `?src=instagram` or `?src=friend`.

**Target before Lab 9:** 6 links delivered, 3 people finish all five cards.
