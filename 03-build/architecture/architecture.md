Architecture

Save this file as: 03-build/architecture/architecture.md · Filled-in example: Lab-6/examples/architecture.md (Sakhli)

One diagram, one line of why per layer. The question each line answers is not "is this the best technology" but "can this team deploy it at a public URL by the Week 7 lab."

The diagram


<img width="632" height="183" alt="image" src="https://github.com/user-attachments/assets/33b768ae-db07-4e98-abc7-bea5972ae4e8" />

One public page for students, one private page for the curator. The curator page is reachable only through a long random token in the URL. No accounts in Sprint 1.

The stack, one line per layer
Layer	Choice	Why we can deploy it by Week 7
Hosting	Vercel	Free tier; HTTPS and a public URL straight from the GitHub repo; step-by-step in Lab-6/setup/vercel-and-github.md. [Write who on the team has deployed on Vercel before, if anyone]
App framework	Next.js (App Router)	Pages and server routes in one project, so there is no separate backend to host; the course setup is written for it. [Write who knows React]
Database	Postgres on Neon	Hosted, free tier, nothing to run; three small tables (card_sets, cards, decisions); Lab-6/setup/neon-and-data.md
Analytics	PostHog (wired from Lab-6/setup/SHIP-STACK-SETUP.md)	fixed for the course
Messages out	None	No step sends a message; reminders are cut (mvp-boundary.md)
Sign-in	None	Students stay anonymous (PostHog anonymous id); the curator uses a private tokenized link

Layers we deliberately do not have in Sprint 1: login, scraping or background jobs, email/SMS/Telegram messages, file storage (cards are text only), AI matching.

The journey through the stack
Step	Layer that handles it	Event fired
1	Next.js page /admin/[token]: form for five cards; Publish inserts a card_sets row and five cards rows	curator_publishes_card_set (server)
2	Next.js page / reads the latest published set from Postgres and renders five cards	student_opens_card_set (client, source from the query string)
3	Same page; each card shows role, company, field, source, students OK, experience, hours, pay, deadline	student_views_card (client, when the card comes into view)
4	Apply or Skip posts to a server route that inserts a decisions row; Apply then opens source_url in a new tab	student_decides_card (server, after the row is saved)
5	The same route sees the 5th decision for this anonymous id and set, returns the summary of applied cards with deadlines	student_completes_card_set (server, with ms_total)
Secrets and data

Secrets live in: .env (DATABASE_URL, ADMIN_TOKEN, NEXT_PUBLIC_POSTHOG_KEY, NEXT_PUBLIC_POSTHOG_HOST); .gitignore lists .env, checked by MG before the first push of app/.

Personal data we store, and where: none about students. The decisions table holds the PostHog anonymous id, card_id, decision and skip reason only. Cards hold public job-post information. Skip reasons are fixed choices, never free text, so no student can type personal data into them.

The one thing in this design most likely to break on deploy day: tapping Apply opens another site, and the event can be lost if the page navigates away first. That is why student_decides_card fires from the server after the row is saved, and the original post opens in a new tab. First test in the Week 7 lab: tap Apply on all five cards on a phone, then check that five decisions rows and one student_completes_card_set event exist.
