from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
import os
from pathlib import Path
from uuid import UUID

from fastapi import FastAPI, HTTPException, Request, Response, status

from vulntrack.repository import SQLiteFindingRepository
from vulntrack.schemas import FindingCreate, FindingRead, FindingUpdate


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

    @application.post(
        "/findings",
        response_model=FindingRead,
        status_code=status.HTTP_201_CREATED,
        tags=["findings"],
    )
    async def create_finding(
        payload: FindingCreate,
        request: Request,
    ) -> FindingRead:
        """Register one validated security finding."""
        return request.app.state.repository.create(payload)

    @application.get(
        "/findings",
        response_model=list[FindingRead],
        tags=["findings"],
    )
    async def list_findings(request: Request) -> list[FindingRead]:
        """Return every registered finding."""
        return request.app.state.repository.list()

    @application.get(
        "/findings/{finding_id}",
        response_model=FindingRead,
        tags=["findings"],
    )
    async def get_finding(finding_id: UUID, request: Request) -> FindingRead:
        """Return a finding by UUID."""
        finding = request.app.state.repository.get(finding_id)
        if finding is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="finding not found",
            )
        return finding

    @application.put(
        "/findings/{finding_id}",
        response_model=FindingRead,
        tags=["findings"],
    )
    async def update_finding(
        finding_id: UUID,
        payload: FindingUpdate,
        request: Request,
    ) -> FindingRead:
        """Apply a validated partial update to a finding."""
        finding = request.app.state.repository.update(finding_id, payload)
        if finding is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="finding not found",
            )
        return finding

    @application.delete(
        "/findings/{finding_id}",
        status_code=status.HTTP_204_NO_CONTENT,
        tags=["findings"],
    )
    async def delete_finding(finding_id: UUID, request: Request) -> Response:
        """Remove one finding."""
        if not request.app.state.repository.delete(finding_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="finding not found",
            )
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    return application


app = create_app()
