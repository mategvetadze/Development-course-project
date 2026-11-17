# Architecture — Prometheus / CareerCards

## The diagram

```mermaid
flowchart LR
    N[Student phone / browser] -->|opens five-card set| UI[Next.js frontend / Vercel]
    C[Curator phone / browser] -->|publishes verified cards| UI
    UI -->|latest set and browser interactions| DB[(Neon Postgres)]
    UI -->|POST /api/publish or /api/decide| API[FastAPI backend / Render]
    API -->|read and write card sets, cards, decisions| DB
    UI -->|open and view events| PH[PostHog]
    API -->|publish, decision, completion events| PH
    UI -->|Apply link| JOB[Original employer listing]
```

**Implementation note:** In the current code `app/lib/cards.ts` loads the latest set directly from Neon on the server-rendered student page; `backend/` handles curator publishing and decision saves via REST. The architecture reflects those actual paths, rather than claiming every read goes through FastAPI.

## The stack, one line per layer

| Layer | Choice | Why this is deployable by the Week 7 gate |
|---|---|---|
| Hosting (phone UI) | Vercel, root directory `app/` | Managed Next.js deployment; deploy configuration is limited to environment variables and a GitHub connection (MG/AP own build work) |
| App framework | Next.js 14 / React (TypeScript), `app/` | Existing student and curator pages in the repo can be deployed without rewriting the UI |
| API / backend hosting | FastAPI Python, `backend/`, on Render | Routes and requirements already exist; host needs Postgres, PostHog and CORS settings |
| Database | Neon Postgres | Schema already supplied at `backend/sql/schema.sql` and database access code is present |
| Analytics | PostHog | Mandatory for course; Python server-side capture is in `backend/app/analytics.py`, browser capture is called from `app/components/StudentCardSet.tsx` |
| Messages out | None | No step requires email, SMS or WhatsApp in this MVP |
| Sign-in | No student accounts; random anonymous id; curator admin token | Five anonymous decisions require no login; publishing is protected by `ADMIN_TOKEN` on the API |

**Layers deliberately excluded from Sprint 1:** scraping, student login, outbound messages, AI matching, files/CV uploads, employer accounts.

## The journey through the stack

| Step | Layer that handles it | Event fired |
|---|---|---|
| 1 | Curator form in Next.js -> FastAPI `POST /api/publish` -> Neon `card_sets` and `cards` | `curator_publishes_card_set` (server, after write) |
| 2 | Next.js home page loads latest five cards from Neon and renders them on phone | `student_opens_card_set` (browser, once per page load) |
| 3 | Next.js card components reveal requirements, pay, hours and deadline | `student_views_card` (browser, once per card in view) |
| 4 | Apply/Skip -> FastAPI `POST /api/decide` -> Neon `decisions`; Apply also opens original listing | `student_decides_card` (server, after saved new decision) |
| 5 | FastAPI detects fifth distinct saved decision and returns apply summary to UI | `student_completes_card_set` (server, with `ms_total`) |

## Secrets and data

- **Secrets live in deployment environment settings**, locally in `backend/.env` (`DATABASE_URL`, `ADMIN_TOKEN`, `POSTHOG_KEY`, `POSTHOG_HOST`, `CORS_ORIGINS`) and `app/.env.local` (`DATABASE_URL`, `NEXT_PUBLIC_API_URL`, `NEXT_PUBLIC_POSTHOG_KEY`, `NEXT_PUBLIC_POSTHOG_HOST` as applicable). `.gitignore` contains `.env`, `.env.*` and `app/.env.*`, with examples excepted; verified in this ZIP. No real tokens belong in commits, event properties, client-readable environment variables, or public screenshots.
- **Data:** Neon tables `card_sets`, `cards` (opportunity facts) and `decisions` (`anonymous_id`, decision, reason, time). No name, email, phone number or CV in the application data or event properties. Treat the pseudonymous id as linkable usage data, not as a real identity.
- **Curator access:** The URL token is not the same as a secured sign-in session. The backend checks `X-Admin-Token`; avoid sharing the URL and consider a safer admin mechanism after Sprint 1. An incorrect token should fail on **Publish**, not be claimed to make the page itself 404.
- **Deploy-day risk / first fix:** `app/components/StudentCardSet.tsx` imports `@/lib/posthog-client`, but that file is **absent from this uploaded ZIP**. The frontend will not compile as supplied until the helper exists. Next verify PostHog browser key, Vercel `DATABASE_URL`, API URL/CORS and the live five-decision path on a phone; do not mark the gate passed until observed.
