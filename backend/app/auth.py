from secrets import compare_digest

from fastapi import Header, HTTPException

from app.config import get_settings


def require_admin(x_admin_token: str | None = Header(default=None)):
    expected = get_settings().admin_token
    if not expected or not compare_digest(expected.encode(), (x_admin_token or "").encode()):
        raise HTTPException(status_code=404, detail="Not found")
