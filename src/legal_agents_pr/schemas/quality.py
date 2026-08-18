from enum import Enum

from pydantic import BaseModel, Field


class QualityStatus(str, Enum):
    DRAFT = "DRAFT"
    VALIDATED_DRAFT = "VALIDATED_DRAFT"
    ATTORNEY_REVIEW = "ATTORNEY_REVIEW"
    FINAL = "FINAL"


class CheckStatus(str, Enum):
    VERIFIED = "verified"
    PARTIALLY_VERIFIED = "partially_verified"
    UNVERIFIED = "unverified"
    NOT_APPLICABLE = "not_applicable"
    BLOCKED = "blocked"


class QualityCheck(BaseModel):
    name: str
    status: CheckStatus
    details: list[str] = Field(default_factory=list)


class QualityReport(BaseModel):
    status: QualityStatus = QualityStatus.DRAFT
    checks: list[QualityCheck] = Field(default_factory=list)
    blocking_issues: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)
    attorney_review_required: bool = True

