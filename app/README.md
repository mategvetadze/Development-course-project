# CareerCards frontend (Next.js)

Phone UI only. **Backend is Python FastAPI** in `../backend`.

Needs **Node.js 20.9+**.

```bash
cp .env.example .env.local
# NEXT_PUBLIC_API_URL=http://127.0.0.1:8000
npm install
npm run dev
```

Start the API first (`backend/README.md`), then open:

- Student: http://localhost:3000/?src=instagram
- Curator: http://localhost:3000/admin/<ADMIN_TOKEN>
