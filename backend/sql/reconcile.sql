-- Executed by: python -m scripts.reconcile --from <ISO offset> --to <ISO offset>
-- Same half-open completion-time window and filters MUST be used in PostHog.
-- DECISIONS Wk5 says unique students/week; event-schema says event count.
-- Return both; never substitute completed sets for distinct students.
select
  count(*)::int as completion_events,
  count(*) filter (where qualifies)::int as qualifying_completion_events,
  count(distinct anonymous_id) filter (where qualifies)::int as north_star_students
from card_set_completions
where completed_at >= %(window_start)s::timestamptz
  and completed_at < %(window_end)s::timestamptz
  and environment = %(environment)s
  and (not is_internal or %(include_internal)s::boolean)
  and (%(set_id)s::uuid is null or set_id = %(set_id)s::uuid)
  and not (anonymous_id = any(%(excluded_ids)s::text[]));
