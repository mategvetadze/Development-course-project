from fastapi import APIRouter, HTTPException

from app.db import get_conn
from app.schemas import CardOut, CardSetOut

router = APIRouter(prefix="/api", tags=["sets"])


@router.get("/sets/latest", response_model=CardSetOut | None)
def latest_set():
    try:
        with get_conn() as conn:
            set_row = conn.execute(
                """
                select id, published_at
                from card_sets
                order by published_at desc
                limit 1
                """
            ).fetchone()
            if not set_row:
                return None

            cards = conn.execute(
                """
                select
                  id, set_id, position, role, company, field, source, source_url,
                  students_ok, experience, hours, pay, deadline::text as deadline
                from cards
                where set_id = %s
                order by position asc
                """,
                (set_row["id"],),
            ).fetchall()
    except RuntimeError as e:
        raise HTTPException(status_code=503, detail=str(e)) from e

    return CardSetOut(
        id=set_row["id"],
        published_at=set_row["published_at"].isoformat(),
        cards=[CardOut(**card) for card in cards],
    )
