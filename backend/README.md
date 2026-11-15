# CareerCards backend (Python / FastAPI)

Sprint 1 API for Prometheus: curator publishes 5 cards → student apply/skip → summary + PostHog events.

## Endpoints

| Method | Path | Auth | What |
|---|---|---|---|
| GET | `/health` | — | liveness |
| GET | `/api/sets/latest` | — | latest published set + 5 cards |
| POST | `/api/publish` | header `X-Admin-Token` | insert set + 5 cards; fires `curator_publishes_card_set` |
| POST | `/api/decide` | — | save apply/skip; fires `student_decides_card`; on 5th decision fires `student_completes_card_set` |

## Setup

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# fill DATABASE_URL, ADMIN_TOKEN, optional POSTHOG_*
```

Run schema in Neon: paste `sql/schema.sql` into the Neon SQL editor.

```bash
uvicorn app.main:app --reload --port 8000
```

Docs: http://127.0.0.1:8000/docs

## Frontend

Point Next.js at this API with `NEXT_PUBLIC_API_URL=http://127.0.0.1:8000` in `app/.env.local`.

## Deploy (Week 7)

Host on Railway / Render / Fly with the same env vars. Put the public API URL in the team README Live product row (or behind the Vercel frontend).
