from datetime import datetime
from typing import Annotated
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from vulntrack.domain import FindingStatus, Severity


class FindingCreate(BaseModel):
    """Validated input used to register a vulnerability finding."""

    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    title: Annotated[str, Field(min_length=3, max_length=200)]
    affected_asset: Annotated[str, Field(min_length=1, max_length=255)]
    description: Annotated[str, Field(min_length=1, max_length=4000)]
    severity: Severity
    cvss_score: Annotated[
        float,
        Field(ge=0.0, le=10.0, allow_inf_nan=False),
    ]


class FindingRead(FindingCreate):
    """Validated representation returned to API clients."""

    model_config = ConfigDict(
        str_strip_whitespace=True,
        extra="forbid",
        from_attributes=True,
    )

    id: UUID
    status: FindingStatus
    created_at: datetime
    updated_at: datetime
