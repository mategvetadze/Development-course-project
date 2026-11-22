"""Railpack entrypoint: exposes the FastAPI app at the service root."""

from app.main import app

__all__ = ["app"]
