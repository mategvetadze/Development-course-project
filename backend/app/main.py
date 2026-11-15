from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.routers import decide, health, publish, sets

settings = get_settings()

app = FastAPI(
    title="CareerCards API",
    description="Python backend for Prometheus Sprint 1 journey (publish 5 cards → apply/skip → summary).",
    version="0.1.0",
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
