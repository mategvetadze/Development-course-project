from fastapi import APIRouter, HTTPException

from app.analytics import capture
from app.db import get_conn
from app.schemas import AppliedSummary, DecideRequest, DecideResponse

router = APIRouter(prefix="/api", tags=["decide"])


@router.post("/decide", response_model=DecideResponse)
def decide_card(body: DecideRequest):
    if body.decision == "skip" and not body.skip_reason:
        raise HTTPException(status_code=400, detail="skip_reason required when decision is skip")

    try:
        with get_conn() as conn:
            with conn.transaction():
                # "returning 1" tells us whether a NEW row was saved.
                # A repeat tap on the same card saves nothing, so it must fire nothing.
                inserted = conn.execute(
                    """
                    insert into decisions (
                      set_id, card_id, anonymous_id, decision, skip_reason, ms_on_card
                    ) values (%s, %s, %s, %s, %s, %s)
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
                    ),
                ).fetchone() is not None

                count_row = conn.execute(
                    """
                    select count(*)::int as n
                    from decisions
                    where set_id = %s and anonymous_id = %s
                    """,
                    (body.set_id, body.anonymous_id),
                ).fetchone()
                count = count_row["n"]

                applied_rows = []
                if count >= 5:
                    applied_rows = conn.execute(
                        """
                        select c.role, c.deadline::text as deadline, c.source_url
                        from decisions d
                        join cards c on c.id = d.card_id
                        where d.set_id = %s
                          and d.anonymous_id = %s
                          and d.decision = 'apply'
                        order by c.position
                        """,
                        (body.set_id, body.anonymous_id),
                    ).fetchall()
    except RuntimeError as e:
        raise HTTPException(status_code=503, detail=str(e)) from e

    # Events fire only after a new row is committed, so PostHog count = database count.
    if inserted:
        capture(
            distinct_id=body.anonymous_id,
            event="student_decides_card",
            properties={
                "set_id": str(body.set_id),
                "card_id": str(body.card_id),
                "position": body.position,
                "decision": body.decision,
                "skip_reason": body.skip_reason if body.decision == "skip" else None,
                "ms_on_card": body.ms_on_card,
            },
        )

    if count < 5:
        return DecideResponse(complete=False)

    summary = [AppliedSummary(**row) for row in applied_rows]

    # North star: only the request that saved the 5th row fires it, exactly once.
    if inserted and count == 5:
        capture(
            distinct_id=body.anonymous_id,
            event="student_completes_card_set",
            properties={
                "set_id": str(body.set_id),
                "apply_count": len(summary),
                "skip_count": 5 - len(summary),
                "ms_total": body.ms_total,
            },
        )
    return DecideResponse(complete=True, summary=summary)from fastapi import APIRouter, HTTPException

from app.analytics import capture
from app.db import get_conn
from app.schemas import AppliedSummary, DecideRequest, DecideResponse

router = APIRouter(prefix="/api", tags=["decide"])


@router.post("/decide", response_model=DecideResponse)
def decide_card(body: DecideRequest):
    if body.decision == "skip" and not body.skip_reason:
        raise HTTPException(status_code=400, detail="skip_reason required when decision is skip")

    try:
        with get_conn() as conn:
            with conn.transaction():
                # "returning 1" tells us whether a NEW row was saved.
                # A repeat tap on the same card saves nothing, so it must fire nothing.
                inserted = conn.execute(
                    """
                    insert into decisions (
                      set_id, card_id, anonymous_id, decision, skip_reason, ms_on_card
                    ) values (%s, %s, %s, %s, %s, %s)
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
                    ),
                ).fetchone() is not None

                count_row = conn.execute(
                    """
                    select count(*)::int as n
                    from decisions
                    where set_id = %s and anonymous_id = %s
                    """,
                    (body.set_id, body.anonymous_id),
                ).fetchone()
                count = count_row["n"]

                applied_rows = []
                if count >= 5:
                    applied_rows = conn.execute(
                        """
                        select c.role, c.deadline::text as deadline, c.source_url
                        from decisions d
                        join cards c on c.id = d.card_id
                        where d.set_id = %s
                          and d.anonymous_id = %s
                          and d.decision = 'apply'
                        order by c.position
                        """,
                        (body.set_id, body.anonymous_id),
                    ).fetchall()
    except RuntimeError as e:
        raise HTTPException(status_code=503, detail=str(e)) from e

    # Events fire only after a new row is committed, so PostHog count = database count.
    if inserted:
        capture(
            distinct_id=body.anonymous_id,
            event="student_decides_card",
            properties={
                "set_id": str(body.set_id),
                "card_id": str(body.card_id),
                "position": body.position,
                "decision": body.decision,
                "skip_reason": body.skip_reason if body.decision == "skip" else None,
                "ms_on_card": body.ms_on_card,
            },
        )

    if count < 5:
        return DecideResponse(complete=False)

    summary = [AppliedSummary(**row) for row in applied_rows]

    # North star: only the request that saved the 5th row fires it, exactly once.
    if inserted and count == 5:
        capture(
            distinct_id=body.anonymous_id,
            event="student_completes_card_set",
            properties={
                "set_id": str(body.set_id),
                "apply_count": len(summary),
                "skip_count": 5 - len(summary),
                "ms_total": body.ms_total,
            },
        )
    return DecideResponse(complete=True, summary=summary)
