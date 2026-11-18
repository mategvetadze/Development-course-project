from fastapi import APIRouter, Header, HTTPException

from app.analytics import enqueue
from app.config import get_settings
from app.db import get_conn
from app.schemas import PublishRequest, PublishResponse

router = APIRouter(prefix="/api", tags=["publish"])


@router.post("/publish", response_model=PublishResponse)
def publish_cards(
    body: PublishRequest,
    x_admin_token: str | None = Header(default=None),
):
    settings = get_settings()
    if not settings.admin_token or x_admin_token != settings.admin_token:
        raise HTTPException(status_code=404, detail="Not found")

    try:
        with get_conn() as conn:
            with conn.transaction():
                set_row = conn.execute(
                    "insert into card_sets default values returning id"
                ).fetchone()
                set_id = set_row["id"]

                for i, card in enumerate(body.cards, start=1):
                    pay = card.pay.strip() if card.pay and card.pay.strip() else "Pay: not stated"
                    conn.execute(
                        """
                        insert into cards (
                          set_id, position, role, company, field, source, source_url,
                          students_ok, experience, hours, pay, deadline
                        ) values (
                          %s, %s, %s, %s, %s, %s, %s,
                          %s, %s, %s, %s, %s::date
                        )
                        """,
                        (
                            set_id,
                            i,
                            card.role,
                            card.company,
                            card.field,
                            card.source,
                            card.source_url,
                            card.students_ok,
                            card.experience,
                            card.hours,
                            pay,
                            card.deadline,
                        ),
                    )
                enqueue(conn, distinct_id="curator", event="curator_publishes_card_set",
                        properties={"set_id": str(set_id), "card_count": 5,
                                    **settings.analytics_context("curator")})
    except RuntimeError as e:
        raise HTTPException(status_code=503, detail=str(e)) from e

    return PublishResponse(set_id=set_id, card_count=5)
