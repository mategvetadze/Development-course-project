from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import asyncio
from contextlib import asynccontextmanager, suppress
import logging

from app.analytics import dispatch_pending
from app.config import get_settings
from app.routers import decide, health, publish, sets

settings = get_settings()


@asynccontextmanager
async def lifespan(app):
    async def deliver():
        while True:
            try:
                await asyncio.to_thread(dispatch_pending)
            except Exception:
                logging.getLogger(__name__).warning("Analytics worker unavailable; retrying later")
            await asyncio.sleep(15)
    worker = asyncio.create_task(deliver()) if settings.posthog_key else None
    if not worker:
        logging.getLogger(__name__).warning("POSTHOG_KEY is not configured; events remain in the database outbox")
    try:
        yield
    finally:
        if worker:
            worker.cancel()
            with suppress(asyncio.CancelledError):
                await worker

app = FastAPI(
    title="CareerCards API",
    description="Python backend for Prometheus Sprint 1 journey (publish 5 cards → apply/skip → summary).",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list or ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router)
app.include_router(sets.router)
app.include_router(publish.router)
app.include_router(decide.router)
