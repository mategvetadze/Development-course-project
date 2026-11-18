
from uuid import UUID

from fastapi import APIRouter, HTTPException, Query

from app.analytics import capture
from app.config import get_settings
from app.db import get_conn
from app.metrics import ensure_session, lock_session, record_completion
from app.schemas import AppliedSummary, DecideRequest, DecideResponse, DecisionState, SessionRequest, SessionResponse

router = APIRouter(prefix="/api", tags=["decide"])


def decision_state(conn, set_id: UUID, anonymous_id: str) -> DecisionState:
    rows = conn.execute(
        """
        select c.id, d.decision, c.role, c.deadline::text as deadline, c.source_url
        from decisions d join cards c on c.id = d.card_id and c.set_id = d.set_id
        where d.set_id = %s and d.anonymous_id = %s
        order by c.position
        """,
        (set_id, anonymous_id),
    ).fetchall()
    complete = len(rows) == 5
    session = conn.execute("select * from student_set_sessions where set_id=%s and anonymous_id=%s",
                           (set_id, anonymous_id)).fetchone()
    context = ({"environment": session["environment"], "is_internal": session["is_internal"]}
               if session else get_settings().analytics_context(anonymous_id))
    return DecisionState(
        choices={str(row["id"]): row["decision"] for row in rows},
        complete=complete,
        summary=[AppliedSummary(**row) for row in rows if row["decision"] == "apply"] if complete else None,
        analytics=context, started_at=session["started_at"] if session else None,
        session_exists=session is not None,
    )


@router.get("/sets/{set_id}/decisions", response_model=DecisionState)
def get_decisions(set_id: UUID, anonymous_id: str = Query(min_length=1, max_length=128)):
    try:
        with get_conn() as conn:
            if not conn.execute("select 1 from card_sets where id = %s", (set_id,)).fetchone():
                raise HTTPException(status_code=404, detail="Set not found")
            return decision_state(conn, set_id, anonymous_id)
    except RuntimeError as e:
        raise HTTPException(status_code=503, detail=str(e)) from e


@router.post("/sets/{set_id}/start", response_model=SessionResponse)
def start_set(set_id: UUID, body: SessionRequest):
    try:
        with get_conn() as conn:
            with conn.transaction():
                lock_session(conn, set_id, body.anonymous_id)
                if not conn.execute("select 1 from card_sets where id=%s", (set_id,)).fetchone():
                    raise HTTPException(status_code=404, detail="Set not found")
                session = ensure_session(conn, set_id, body.anonymous_id, first_view=True)
        return SessionResponse(started_at=session["started_at"], analytics={
            "environment": session["environment"], "is_internal": session["is_internal"]})
    except RuntimeError as e:
        raise HTTPException(status_code=503, detail=str(e)) from e


@router.post("/decide", response_model=DecideResponse)
def decide_card(body: DecideRequest):
    if body.decision == "skip" and not body.skip_reason:
        raise HTTPException(status_code=400, detail="skip_reason required when decision is skip")

    try:
        with get_conn() as conn:
            with conn.transaction():
                # Serialize one student's set, including different cards/tabs.
                # The lock is released by PostgreSQL on commit or rollback.
                lock_session(conn, body.set_id, body.anonymous_id)
                card = conn.execute("select position from cards where id = %s and set_id = %s",
                                    (body.card_id, body.set_id)).fetchone()
                if card is None:
                    raise HTTPException(status_code=404, detail="Card not found in this set")
                if card["position"] != body.position:
                    raise HTTPException(status_code=400, detail="Incorrect card position")
                ensure_session(conn, body.set_id, body.anonymous_id)
                # "returning 1" tells us whether a NEW row was saved.
                # A repeat tap on the same card saves nothing, so it must fire nothing.
                inserted = conn.execute(
                    """
                    insert into decisions (
                      set_id, card_id, anonymous_id, decision, skip_reason, ms_on_card, ms_total
                    ) values (%s, %s, %s, %s, %s, %s, %s)
                    on conflict (set_id, card_id, anonymous_id) do nothing
                    returning 1
                    """,
                    (
                        body.set_id,
                        body.card_id,
                        body.anonymous_id,
                        body.decision,
                        body.skip_reason if body.decision == "skip" else None,
                        body.ms_on_card,
                        body.ms_total,
                    ),
                ).fetchone() is not None

                state = decision_state(conn, body.set_id, body.anonymous_id)
                completion = (record_completion(conn, body.set_id, body.anonymous_id, len(state.summary))
                              if inserted and state.complete else None)
    except RuntimeError as e:
        raise HTTPException(status_code=503, detail=str(e)) from e

    # Only newly committed decisions attempt analytics; retries keep the first choice.
    if inserted:
        capture(
            distinct_id=body.anonymous_id,
            event="student_decides_card",
            properties={
                "set_id": str(body.set_id),
                "card_id": str(body.card_id),
                "position": card["position"],
                "decision": body.decision,
                "skip_reason": body.skip_reason if body.decision == "skip" else None,
                "ms_on_card": body.ms_on_card,
                **state.analytics,
            },
        )

    # The per-student lock makes exactly one request observe the fifth new row.
    if completion:
        capture(
            distinct_id=body.anonymous_id,
            event="student_completes_card_set",
            properties={
                "set_id": str(body.set_id),
                "apply_count": len(state.summary),
                "skip_count": 5 - len(state.summary),
                "ms_total": completion["ms_total"],
                "completion_id": str(completion["id"]),
                "qualifies": completion["qualifies"],
                "metric_version": "server_v1",
                **state.analytics,
            },
        )
    return DecideResponse(complete=state.complete, summary=state.summary,
                          decision=state.choices[str(body.card_id)])
