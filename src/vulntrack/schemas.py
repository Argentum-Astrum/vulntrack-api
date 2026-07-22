from datetime import datetime
from typing import Annotated
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, model_validator

from vulntrack.domain import FindingStatus, Severity


class FindingCreate(BaseModel):
    """Validated input used to register a vulnerability finding."""

    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    title: Annotated[str, Field(min_length=3, max_length=200)]
    affected_asset: Annotated[str, Field(min_length=1, max_length=255)]
    description: Annotated[str, Field(min_length=1, max_length=4000)]
    source: Annotated[str, Field(min_length=1, max_length=100)]
    severity: Severity
    cvss_score: Annotated[
        float,
        Field(ge=0.0, le=10.0, allow_inf_nan=False),
    ]


class FindingUpdate(BaseModel):
    """Validated fields that may be changed after registration."""

    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    title: Annotated[str, Field(min_length=3, max_length=200)] | None = None
    affected_asset: Annotated[str, Field(min_length=1, max_length=255)] | None = None
    description: Annotated[str, Field(min_length=1, max_length=4000)] | None = None
    source: Annotated[str, Field(min_length=1, max_length=100)] | None = None
    severity: Severity | None = None
    status: FindingStatus | None = None
    cvss_score: (
        Annotated[
            float,
            Field(ge=0.0, le=10.0, allow_inf_nan=False),
        ]
        | None
    ) = None

    @model_validator(mode="after")
    def require_a_change(self) -> "FindingUpdate":
        """Reject empty updates and explicit null field values."""
        changes = self.model_dump(exclude_unset=True)
        if not changes or any(value is None for value in changes.values()):
            raise ValueError("at least one non-null field is required")
        return self


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
