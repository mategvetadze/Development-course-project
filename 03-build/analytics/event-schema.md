# Event Schema

**North star:** Number of students who complete apply-or-skip decisions for all five job cards within five minutes, per week.

**North star event:** `student_completes_card_set`

**How the north star is computed from events:** count of `student_completes_card_set` with `ms_total` ≤ 300000, per calendar week.



Every event has four parts: name (actor_verb_object), fired by, properties, owner. No personal data on any event: no names, emails, phone numbers or CV content.

| Step | Event (actor_verb_object) | Fired by | Properties | Owner | Live |
|---|---|---|---|---|---|
| Supply (precursor) | `curator_publishes_card_set` | Curator, recorded by the server when Publish is tapped on the admin page | set_id, card_count | MG | no |
| Acquisition | `student_opens_card_set` | Student, recorded by the client once per page load | set_id, source (from ?src=instagram, groupchat, friend or other) | AP | no |
| Activation (precursor) | `student_views_card` | Student, recorded by the client when a card comes into view | set_id, card_id, position (1–5) | AP | no |
| Activation (precursor) | `student_decides_card` | Student, recorded by the server after the decision row is saved | set_id, card_id, position, decision (apply / skip), skip_reason (not_my_field / not_eligible / hours / pay / not_interested / other), ms_on_card | AP | no |
| Activation (north star) ★ | `student_completes_card_set` | Student, recorded by the server when the 5th decision is saved | set_id, apply_count, skip_count, ms_total (from first card view to 5th decision) | MG | no |

Retention, Referral and Revenue are empty on purpose: with one set of five cards per week there is nothing to retain, refer or pay for before Week 12.

**North star:** count of `student_completes_card_set` with `ms_total` ≤ 300000, per week (DECISIONS.md, Wk5). `student_opens_card_set` and `student_views_card` are tracked but rejected as success measures: they do not prove a decision.

## Rules we are following

- One name per event, one spelling, lowercase with underscores.
- `set_id` on every event; students are identified only by an anonymous id made by our app. Nothing that identifies a real person.
- The north star event is fired by the student, because the student receives the value and the student is who the problem statement is about.

## Reconcile plan

Before we believe the dashboard, we count the north star event a second way.

**Event most likely to fail silently:** `student_decides_card`
**How it would fail:** double fire or never fires; Apply opens the original post in a new tab and the page can lose the request before the server saves the decision and fires the event.
**The check that would catch it:** count `decisions` rows in Neon for the same week and compare to the `student_decides_card` count in PostHog; also check that the number of `student_completes_card_set` events does not exceed decisions ÷ 5.
**Who runs the check in Week 7:** AP

## Gate reconcile (Lab 7)

**Production URL walked:** not deployed yet · **walked by:** [initials of a teammate who did not build the north star step] · on a phone, mobile data: [yes or no]

| Source | Count | Window | Exactly how it was counted |
|---|---|---|---|
| PostHog | | [same start and end as the row below] | Trends insight, total count of `student_completes_card_set` |
| Database | | | [the query you ran, pasted] |

**Match:** [yes or no]

**If no, first:** [what the two numbers were, what caused the gap, what you changed (commit link), and the two numbers after the fix. Keep the wrong numbers here; do not overwrite them.]

**Silent failure we predicted in Lab 5:** `student_decides_card`: double fire or never fires; Apply opens the original post in a new tab and the page can lose the request before the server saves the decision and fires the event. · **Did it happen?** [yes or no, and how you know]

**Internal filter set in PostHog:** [the exact filter] · **our test record is:** [the id your team tests on]

**Checked by:** [initials] · **events still not Live, with owner and by when:** all five, owner MG, by [day/time]
