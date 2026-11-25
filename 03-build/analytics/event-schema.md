
# Event Schema — Prometheus / CareerCards

**North star:** Number of students who complete apply-or-skip decisions for all five job cards within five minutes, per week

**North star event:** `student_completes_card_set`

**How the north star is computed from events:** PostHog **unique students** (distinct anonymous IDs) who fired `student_completes_card_set` with `qualifies = true`, `environment = production`, and `is_internal = false` in the calendar-week window.

The comparable independent database count is `north_star_students` from `backend/sql/reconcile.sql` using the same time window and filters.

An event total and a unique-student total are **not interchangeable**.

## Events

The `Live` column stays `pending` until a separate teammate observes that exact event, once, in PostHog Activity after a phone action on mobile data at the deployed URL.

| Step | Event (actor_verb_object) | Fired by | Properties (no personal details) | Owner | Live |
|---|---|---|---|---|---|
| Supply (precursor) | `curator_publishes_card_set` | Curator's Publish action; FastAPI after database write | `set_id`, `card_count`, `environment`, `is_internal` | MG | pending |
| Acquisition | `student_opens_card_set` | Student opening the five-card page; browser | `set_id`, `source` (`friend`, `groupchat`, `other`), `environment`, `is_internal` | AP | pending |
| Activation (precursor) | `student_views_card` | Student viewing at least 50% of a card; browser | `set_id`, `card_id`, `position`, `environment`, `is_internal` | AP | pending |
| Activation (precursor) | `student_decides_card` | Student making a newly saved choice; FastAPI records it | `set_id`, `card_id`, `position`, `decision`, `skip_reason`, `ms_on_card`, `environment`, `is_internal` | AP | pending |
| Activation (north star) | `student_completes_card_set` | Student finishing five distinct decisions; FastAPI after persistence | `set_id`, `apply_count`, `skip_count`, `ms_total`, `qualifies`, `completion_id`, `metric_version`, `environment`, `is_internal` | MG | pending |

Retention, referral and revenue are deliberately not instrumented in this five-card MVP. No fake events are added to fill AARRR categories.

## Rules we follow

- Event names are lowercase `actor_verb_object` and spelled identically in schema, application, PostHog and dashboard.
- Every event includes `set_id`.
- The PostHog `distinct_id` is a locally generated anonymous browser ID, not a real person's identity.
- A completion is counted once per `(set_id, anonymous_id)` by the database. We count **unique students per week** for the committed north-star sentence.
- The student receives the value; a server-recorded completion event represents the student's finished action, not a curator's action.
- The production event filter is `environment = production` AND `is_internal = false` AND, for the north star, `qualifies = true`.
- Never put names, email addresses, telephone numbers, CVs, job-application text or admin tokens in events.

## Reconcile plan (Lab 5)

**Event most likely to fail silently:** `student_decides_card`.

**How it would fail:** A student taps Apply and leaves for the original listing before the request is persisted; or the event is queued in `analytics_outbox` but not delivered to PostHog.

**The check that would catch it:** Compare the count of newly inserted `decisions` rows with PostHog `student_decides_card` events for the same set, window and internal-user exclusion.

Check pending events in `analytics_outbox`.

Independently compare the north-star distinct student count against `card_set_completions` using `backend/sql/reconcile.sql`.

**Who runs this in Week 7:** AP with MG (database access). This assignment is not proof that it was run.

---

## Gate reconcile (Lab 7)

**Production URL walked:** NOT VERIFIED — [Railway URL listed in README](https://development-course-project-production.up.railway.app/).

This is a candidate production URL, **not** evidence that someone completed the walk.

**Walked by:** PENDING — must be a teammate who did not build the north-star step (MG-owned).

**On phone with mobile data:** NOT VERIFIED.

**Window:** PENDING — identical start, end and timezone for both sources; half-open interval `[start, end)`.

| Source | Count | Window | Exactly how counted |
|---|---|---|---|
| PostHog | PENDING | PENDING | `student_completes_card_set`, **unique users**, filtered `qualifies = true`, `environment = production`, `is_internal = false`, same `set_id` if limiting the DB query to one set, same timestamp window |
| Neon database | PENDING | PENDING | `north_star_students` from `backend/sql/reconcile.sql` or the parameterized command below; `environment = production`, exclude internal users, same set/time window |

Run from `backend/` after configuring `DATABASE_URL` and installing `requirements.txt`:

```bash
python -m scripts.reconcile --from 2026-11-16T00:00:00+04:00 --to 2026-11-23T00:00:00+04:00 --environment production
```

The dates above are **illustrative query parameters, not claimed measurement dates**.

Replace them with the exact chosen window, and use `--set-id <actual-set-uuid>` on both sources if reconciling one set.

The command returns `completion_events`, `qualifying_completion_events` and `north_star_students`.

Only `north_star_students` matches the North Star wording.

`backend/sql/schema.sql` already persists completion start, finish, `ms_total` and `qualifies`; there is no need to invent a new table.

See `backend/sql/migrations/001_*`, `002_*`, `003_*` when upgrading an existing database instead of initializing an empty one.

**Match:** PENDING — enter `yes` only after recording equal, verified counts.

**If no, first and after fix:** NOT MEASURED — when checked, retain original numbers, explain gap, link fix commit, append corrected numbers; never overwrite a mismatch.

**Silent failure predicted in Lab 5:** Apply navigation may outpace persistence or analytics delivery.

**Did it happen?** PENDING — compare actual decision rows, outbox diagnostics and PostHog activity.

**Internal filter set in PostHog:** PENDING — use exact filters `environment = production` and `is_internal = false` for every relevant insight.

Set the team's real `cc_anon` values in the backend's `INTERNAL_ANONYMOUS_IDS` before internal tests; do not publish raw IDs in this document.

**Checked by:** PENDING — AP checks browser events with another teammate; MG verifies backend and database counts.

**Events still not Live:** All five until production phone walks and Activity evidence are captured. Assigned owners are in the Events table.

**Local diagnostic (AP, 25 Nov 2026):** `/health` succeeded, but `/health/ready` returned `Database or required migrations unavailable` and `/api/sets/latest` returned `Database unavailable; please try again`.

This does not establish any production count.

MG must verify the configured Neon connection and migrations; AP can then retry the five-card phone journey.
