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

## Deploy on Railway (Week 7)

The repo is a monorepo. If Railway builds from the **repo root**, Railpack fails with “could not determine how to build.” Point the service at **`backend/`**.

### Click path

1. Railway → **New Project** → **Deploy from GitHub** → pick `Development-course-project`.
2. Open the service → **Settings** → **Root Directory** → set to `backend` → Save.
3. **Variables** (same names as `.env.example`):

| Variable | Value |
|---|---|
| `DATABASE_URL` | Neon connection string (`sslmode=require`) |
| `ADMIN_TOKEN` | long random string (save it; curator URL uses it) |
| `APP_ENV` | `production` |
| `CORS_ORIGINS` | your frontend origin(s), comma-separated (e.g. `https://….vercel.app` or Netlify URL) |
| `POSTHOG_KEY` | optional for first deploy |
| `POSTHOG_HOST` | `https://eu.i.posthog.com` |

4. Neon SQL editor: run `sql/schema.sql`, then any files in `sql/migrations/` in order if the DB is new.
5. **Deploy** again. Open `https://YOUR-SERVICE.up.railway.app/health` — should return `{"ok":true,...}`.
6. Put that base URL in the team README / set frontend `NEXT_PUBLIC_API_URL` to it.

Start command (in `railpack.json` — Railpack does **not** read `Procfile`):

```bash
python -m uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

If the build still says “No start command detected”, set it manually in Railway → service → **Settings** → **Deploy** → **Custom Start Command** to that same line, then redeploy.

### Also works on Render

`render.yaml` at the repo root already sets `rootDir: backend`. Use that if Railway free tier is awkward.
