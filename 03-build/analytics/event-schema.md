# Event Schema


Every event has four parts: name (actor_verb_object), fired by, properties, owner. No personal data on any event: no names, emails, phone numbers or CV content.

| Event | Fired by | Properties | Owner |
|---|---|---|---|
| curator_publishes_card_set | Server, when the curator taps Publish on the admin page | set_id, card_count | MG |
| student_opens_card_set | Client, once per page load | set_id, source (from ?src=instagram, groupchat, friend or other) | AP |
| student_views_card | Client, when a card comes into view | set_id, card_id, position (1–5) | AP |
| student_decides_card | Server, after the decision row is saved | set_id, card_id, position, decision (apply / skip), skip_reason (not_my_field / not_eligible / hours / pay / not_interested / other), ms_on_card | AP |
| student_completes_card_set | Server, when the 5th decision is saved | set_id, apply_count, skip_count, ms_total (from first card view to 5th decision) | MG |

**Lab 6 mapping:** All five journey steps already have events with the required name, fired-by, properties and owner. No new schema event is needed for the five-step boundary. Owners: MG = Mate Gvetadze; AP = Ani Purtskhvanidze; AS = Archil Sanikidze; ST = Saba Tabukashvili.

**North star:** count of `student_completes_card_set` with `ms_total` ≤ 300000, per week (DECISIONS.md, Wk5). `student_opens_card_set` and `student_views_card` are tracked but rejected as success measures: they do not prove a decision.

Implementation (Week 7): browser events (student_opens_card_set, student_views_card) fire in app/components/StudentCardSet.tsx; server events (curator_publishes_card_set, student_decides_card, student_completes_card_set) fire in the FastAPI backend (backend/app/routers/) after the database write.

## Live column and gate reconcile

| Event | Live in production? | Seen in PostHog Activity on |
|---|---|---|
| curator_publishes_card_set | [yes/no] | [date] |
| student_opens_card_set | [yes/no] | [date] |
| student_views_card | [yes/no] | [date] |
| student_decides_card | [yes/no] | [date] |
| student_completes_card_set | [yes/no] | [date] |

Gate reconcile, [date], last 7 days:
- student_decides_card: PostHog [N] vs database [N]; record whether equal after verification (rows in the decisions table)
- student_completes_card_set: PostHog [N] vs database [N]; record whether equal after verification (students with 5 decisions in one set)

**Gate status for this ZIP:** Production URL, PostHog Activity observations and reconciliation numbers are not supplied; leave the live rows unverified until a real deployed run. Do not fill them with invented data.
