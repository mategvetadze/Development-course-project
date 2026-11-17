# AI usage log

One line per AI-assisted piece of work.
Format: Wk\<N> · who · tool · what it produced · what you checked or changed

Wk5 · MG · Cursor / AI prototyping · clickable five-card prototype (HTML/CSS/JS) under 02-design/prototype/ · checked against prototype-plan.md screens; kept Apply/Skip only; sample jobs still need swapping for five real posts before sessions
Wk6 · MG · Cursor · mvp-boundary / architecture / sprint-1 drafting support · MG checked cut list against logs 01, 06, 07, 08, 10, 11 and event names against event-schema.md
Wk6 · MG · Cursor · README, test-plan.md, usability-findings scaffold, ai-usage-log · filled from Lab-5/Lab-6 templates and team DECISIONS.md; no invented test sessions
Wk6 · MG · Cursor · app/ Next.js skeleton (pages, admin token route, publish/decide APIs, Neon schema) · needs Node 20+, Neon, PostHog, Vercel before Live product URL; not deployed yet
Wk6 · MG · Cursor · backend/ FastAPI (publish, sets/latest, decide + PostHog) · Next.js API routes removed; frontend calls NEXT_PUBLIC_API_URL; architecture + DECISIONS updated
Wk7 · AP · Claude · fixes to event-schema.md, mvp-boundary.md, sprint-1.md, sprint-2.md against the Lab 5-7 templates · AP checked every change against the lecturer's templates and our logs; hours, predictions and field-week people left empty for the team to fill



Wk7 · ST used Claude to review MG's StudentCardSet.tsx and to write the fix: PostHog client init (app/lib/posthog-client.ts), student_opens_card_set and student_views_card events, Apply on iPhone, double-tap guard. Tested by ST on a phone-sized screen before committing.
Wk6–7 · ST used Claude to draft 03-build/mvp-boundary.md, architecture.md, sprint-1.md, sprint-2.md, the event schema rows and the hw2 outline; facts checked against our interview logs and icp.md.
