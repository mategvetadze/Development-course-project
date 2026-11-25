
# Prometheus — CareerCards

**Problem:** Students in Kutaisi lose time and miss suitable internships/entry-level jobs because relevant posts are scattered and mixed with irrelevant ones.

**Team:** Mate Gvetadze (@mategvetadze) · Ani Purtskhvanidze (@ANANKE231) · Archil Sanikidze (@Archi-lee-Sun) · Saba Tabukashvili (@tabukashvilisaba)

| Link | Status |
|---|---|
| Prototype v1 | [Open clickable prototype preview](https://htmlpreview.github.io/?https://github.com/mategvetadze/Development-course-project/blob/main/02-design/prototype/index.html) · **verify it actually works on a phone**; replace with deployed `/prototype/index.html` when available |
| Live product | [Railway deployment URL](https://development-course-project-production.up.railway.app/) (student) · [Admin](https://development-course-project-production.up.railway.app/admin) — **listed in repo, but production phone test not verified** |
| Analytics dashboard (PostHog) | **PENDING** — MG: insert shareable three-insight dashboard URL, verified in a logged-out browser |
| GitHub Projects board | **PENDING** — add the actual four-column board link (next / doing / review / done) |
| 12-month model | coming Week 12 |
| Pitch deck | coming Week 13 |
| One-pager | coming Week 15 |

## Current Lab 7 gate

**Not yet verified.** The repo contains a Next.js UI in `app/` (AP frontend), a FastAPI service in `backend/` (MG backend), Neon PostgreSQL schema/migrations, and PostHog instrumentation. A source file or local test is **not** a passed production rung.

Obtain, in order:

1. Phone-accessible HTTPS URL.
2. Completed five-card journey.
3. Production PostHog north-star event.
4. Equal PostHog/Neon counts.
5. Public dashboard link.

Record the real evidence in `03-build/analytics/event-schema.md` and `03-build/sprints/sprint-2.md`. No production numbers have been fabricated.

**Local check (AP, 25 Nov 2026):** The Next.js page opened and the FastAPI `/health` returned `{"ok":true,"service":"careercards-backend"}`, but `/health/ready` and `/api/sets/latest` reported the database or required migrations unavailable.

These local tests do not verify the Railway deployment.

**North star:** Number of students who complete apply-or-skip decisions for all five job cards within five minutes, per week. Event: `student_completes_card_set` (`qualifies = true`, distinct anonymous students, production and non-internal traffic).

**Research catch-up:** At least three non-course ICP usability sessions must be logged in `02-design/user-testing/usability-findings.md`; the file currently reports **zero documented sessions**. AP reported testing took place but supplied no session timings or observations.

The five sample listings in `02-design/prototype/script.js` must be replaced with **verified real posts** before claiming they were used for the frozen research test.

## Run and deploy

Read [frontend setup](app/README.md), [backend setup](backend/README.md), [MVP architecture](03-build/architecture/architecture.md) and [Sprint 2 gate checklist](03-build/sprints/sprint-2.md).

Never commit `.env` files or real credentials. The internal admin form is `/admin`; do not send an admin token in a URL.
