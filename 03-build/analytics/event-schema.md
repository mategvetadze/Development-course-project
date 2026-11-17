# Event Schema


Every event has four parts: name (actor_verb_object), fired by, properties, owner. No personal data on any event: no names, emails, phone numbers or CV content.

| Event | Fired by | Properties | Owner | Live |
|---|---|---|---|---|
| `curator_publishes_card_set` | FastAPI after a successful publish | `set_id`, `card_count` | MG | pending verification |
| `student_opens_card_set` | Next.js browser once per set page load | `set_id`, `source` | AP | pending verification |
| `student_views_card` | Next.js browser when 50% visible | `set_id`, `card_id`, `position` | AP | pending verification |
| `student_decides_card` | FastAPI after new decision saved | `set_id`, `card_id`, `position`, `decision`, `skip_reason`, `ms_on_card` | AP | pending verification |
| `student_completes_card_set` | FastAPI after the fifth new decision | `set_id`, `apply_count`, `skip_count`, `ms_total` | MG | pending verification |

**Lab 6 mapping:** All five journey steps already have events with the required name, fired-by, properties and owner. No new schema event is needed for the five-step boundary. Owners: MG = Mate Gvetadze; AP = Ani Purtskhvanidze; AS = Archil Sanikidze; ST = Saba Tabukashvili.

**North star:** count of `student_completes_card_set` with `ms_total` ≤ 300000, per week (DECISIONS.md, Wk5). `student_opens_card_set` and `student_views_card` are tracked but rejected as success measures: they do not prove a decision.

Implementation (Week 7): browser events (student_opens_card_set, student_views_card) fire in app/components/StudentCardSet.tsx; server events (curator_publishes_card_set, student_decides_card, student_completes_card_set) fire in the FastAPI backend (backend/app/routers/) after the database write.

## Gate reconcile (Lab 7)

Only change `Live` to `yes` in the Events table above after a different teammate performs the corresponding action on a phone at the **production URL** with mobile data and another teammate sees that exact event and properties in PostHog Activity. Do not count local development events as live.

**Production URL walked:** PENDING — not supplied · **walked by:** PENDING (must not be the north-star builder MG) · **on a phone, mobile data:** PENDING

**Count window:** PENDING — write identical start/end times with timezone in both rows. Compare the same published set and exclude known internal testers from both counts.

| Source | Count | Window | Exactly how it was counted |
|---|---|---|---|
| PostHog | PENDING (do not enter 0 without checking) | PENDING same start/end, timezone | Trends: `student_completes_card_set`, total count, filter `ms_total <= 300000`, production and non-team users only; note set ID and property filters |
| Database (Neon PostgreSQL) | PENDING | PENDING same start/end, timezone | Run the SQL below after confirming the database and window; filter test `anonymous_id`s consistently, and compare qualifying users in the same set |

**Reconcile SQL (parameterize window / production set and exclusions; first view timestamp is not stored in the current decisions table):**

```sql
-- This counts completed sets; it cannot independently validate the north star
-- <= 300000ms threshold with the current schema because ms_total is not stored.
SELECT set_id, anonymous_id, COUNT(*) AS decisions,
       MAX(created_at) AS completed_at
FROM decisions
WHERE created_at >= :window_start AND created_at < :window_end
  AND set_id = :production_set_id
  -- AND anonymous_id NOT IN (:internal_test_ids)
GROUP BY set_id, anonymous_id
HAVING COUNT(*) = 5;
```

**Important reconciliation limitation:** The current database can count complete five-decision sets, but cannot independently check the north-star 5-minute threshold (`ms_total`) and cannot exactly reconstruct the fifth-decision event timestamp if historical data is incomplete. Before claiming a match for the *qualified* north star, add a persisted completion record with `ms_total`, `completed_at`, `set_id`, `anonymous_id` and a uniqueness constraint, or separately reconcile **unfiltered** completion events as an interim gate check and label that distinction. Never write “Match: yes” for mismatched definitions.

**Match:** PENDING — no numbers observed

**If no, first:** PENDING. Preserve both original counts, investigate event delivery/filter mismatches, link fix commit, then append recounts. Do not overwrite original counts.

**Silent failure we predicted in Lab 5:** A student taps Apply and leaves for the source post before the decision is saved; check that a decision row and server-side `student_decides_card` event both exist, and review missing events/failed requests. · **Did it happen?** PENDING

**Internal filter set in PostHog:** PENDING — agree an exact property-based filter and apply to every insight. The current schema does **not** tag events with `is_internal`; identify team test IDs or add a safe test flag to both browser and server events before claiming filters work. · **Our test record is:** PENDING (do not publish personal contact details)

**Checked by:** AP (assigned; actual check PENDING) · **events still not Live, with owner and by when:** all five pending — `curator_publishes_card_set` MG; `student_opens_card_set` AP; `student_views_card` AP; `student_decides_card` AP; `student_completes_card_set` MG. Each owner to set time before Lab 8.
