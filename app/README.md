# CareerCards frontend (Next.js 15)

The student-facing application uses the **FastAPI backend** in `../backend` for card retrieval, session start, decisions and publication; it does **not** connect to Neon directly.

Requires Node.js 20.9+. Start the Python API first using `../backend/README.md`.

```bash
cd app
cp .env.example .env.local
# Configure NEXT_PUBLIC_API_URL=http://127.0.0.1:8000 and the browser PostHog key.
npm ci
npm run dev
```

Open `http://localhost:3000/?src=friend` for the student or `http://localhost:3000/admin` for the curator. The curator enters the admin token privately into the password-style form; **do not put the admin token in a URL**.

Verification:

```bash
npm test
npm run lint
npm run typecheck
npm run build
npm run test:e2e
```

Playwright requires its Chromium browser and the local test database/API server setup described in `playwright.config.ts` and the GitHub workflow. Do not call the tests passed without actually running them.

For Vercel, use repository root directory `app/`, set `APP_ENV=production`, `NEXT_PUBLIC_API_URL` to the hosted **HTTPS FastAPI origin**, plus `NEXT_PUBLIC_POSTHOG_KEY`, `NEXT_PUBLIC_POSTHOG_HOST=/ingest`, and matching region. Test the **deployed** URL on a phone with mobile data, not just `localhost`.
