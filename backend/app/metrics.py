"""Database-clock timing for the approved five-minute student/set journey."""
from app.config import get_settings


def lock_session(conn, set_id, anonymous_id):
    conn.execute("select pg_advisory_xact_lock(hashtextextended(%s, 0))",
                 (f"{set_id}:{anonymous_id}",))


def ensure_session(conn, set_id, anonymous_id, *, first_view=False):
    context = get_settings().analytics_context(anonymous_id)
    # Old clients can still decide. Missing/late first-view evidence remains
    # unverified forever, rather than making a fast-looking completion at the end.
    conn.execute(
        """
        insert into student_set_sessions(set_id, anonymous_id, started_at, environment, is_internal)
        select %s, %s,
          case when %s and not exists (
            select 1 from decisions where set_id=%s and anonymous_id=%s
          ) then clock_timestamp() else null end, %s, %s
        on conflict (set_id, anonymous_id) do nothing
        """,
        (set_id, anonymous_id, first_view, set_id, anonymous_id,
         context["environment"], context["is_internal"]),
    )
    return conn.execute("select * from student_set_sessions where set_id=%s and anonymous_id=%s",
                        (set_id, anonymous_id)).fetchone()


def record_completion(conn, set_id, anonymous_id, apply_count):
    return conn.execute(
        """
        insert into card_set_completions(
          set_id, anonymous_id, started_at, completed_at, apply_count, skip_count, environment, is_internal
        )
        select set_id, anonymous_id, started_at, clock_timestamp(), %s, %s, environment, is_internal
        from student_set_sessions where set_id=%s and anonymous_id=%s
        on conflict (set_id, anonymous_id) do nothing returning *
        """,
        (apply_count, 5 - apply_count, set_id, anonymous_id),
    ).fetchone()
