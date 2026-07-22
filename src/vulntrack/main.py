from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
import os
from pathlib import Path

from fastapi import FastAPI

from vulntrack.repository import SQLiteFindingRepository


def create_app(database_path: str | Path | None = None) -> FastAPI:
    """Create an application with an explicit or environment-backed database."""
    configured_path = database_path or os.getenv(
        "VULNTRACK_DATABASE",
        "vulntrack.sqlite3",
    )

    @asynccontextmanager
    async def lifespan(application: FastAPI) -> AsyncIterator[None]:
        application.state.repository = SQLiteFindingRepository(configured_path)
        yield

    application = FastAPI(
        title="VulnTrack API",
        version="1.0.0",
        description="Register, triage, and report information-security findings.",
        lifespan=lifespan,
    )

    @application.get("/health", tags=["system"])
    async def health() -> dict[str, str]:
        """Return the application health status."""
        return {"status": "ok"}

    return application


app = create_app()
