from enum import StrEnum


class Severity(StrEnum):
    """Supported vulnerability severity levels."""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class FindingStatus(StrEnum):
    """Supported states in the finding triage workflow."""

    NEW = "new"
    CONFIRMED = "confirmed"
    IN_PROGRESS = "in_progress"
    RESOLVED = "resolved"
