from datetime import date, datetime
from enum import Enum

from pydantic import BaseModel, Field, field_validator, model_validator


class LegalEffectStatus(str, Enum):
    EFFECTIVE = "EFFECTIVE"
    AMENDED = "AMENDED"
    REPEALED = "REPEALED"
    SUPERSEDED = "SUPERSEDED"
    PROPOSED = "PROPOSED"
    UNKNOWN = "UNKNOWN"


class CurrencyStatus(str, Enum):
    CHECKED_THROUGH = "CHECKED_THROUGH"
    HISTORICAL_ONLY = "HISTORICAL_ONLY"
    NOT_CHECKED = "NOT_CHECKED"


class SourceIdentifierStatus(str, Enum):
    VERIFIED_SOURCE_IDENTIFIER = "VERIFIED_SOURCE_IDENTIFIER"
    SOURCE_FOUND_IDENTIFIER_UNCONFIRMED = "SOURCE_FOUND_IDENTIFIER_UNCONFIRMED"
    OCR_REQUIRED = "OCR_REQUIRED"


class SourceLocator(BaseModel):
    section: str | None = None
    article: str | None = None
    page: int | None = Field(default=None, ge=1)
    paragraph: str | None = None
    line_start: int | None = Field(default=None, ge=1)
    line_end: int | None = Field(default=None, ge=1)

    @model_validator(mode="after")
    def has_pinpoint(self) -> "SourceLocator":
        if not any((self.section, self.article, self.page, self.paragraph, self.line_start)):
            raise ValueError("a source locator requires at least one pinpoint")
        line_start = self.line_start
        if self.line_end is not None and line_start is None:
            raise ValueError("line_end requires line_start")
        if self.line_end is not None and line_start is not None and self.line_end < line_start:
            raise ValueError("line_end cannot precede line_start")
        return self


class RetrievalEvidence(BaseModel):
    source_id: str | None = None
    source_url: str
    retrieved_at: datetime
    document_sha256: str = Field(min_length=64, max_length=64)
    publisher: str
    media_type: str | None = None
    official_source: bool = False

    @field_validator("retrieved_at")
    @classmethod
    def timezone_required(cls, value: datetime) -> datetime:
        if value.tzinfo is None or value.utcoffset() is None:
            raise ValueError("retrieved_at must include a timezone")
        return value

    @field_validator("document_sha256")
    @classmethod
    def valid_sha256(cls, value: str) -> str:
        if any(ch not in "0123456789abcdef" for ch in value):
            raise ValueError("document_sha256 must be lowercase hexadecimal")
        return value


class VerificationEvidence(BaseModel):
    retrieval: RetrievalEvidence
    locator: SourceLocator
    quotation: str = Field(min_length=1)
    content_match: bool = False
    legal_effect: LegalEffectStatus = LegalEffectStatus.UNKNOWN
    currency_status: CurrencyStatus = CurrencyStatus.NOT_CHECKED
    checked_through: date | None = None
    verification_method: str
    notes: list[str] = Field(default_factory=list)

    @model_validator(mode="after")
    def consistent_currency(self) -> "VerificationEvidence":
        if self.currency_status == CurrencyStatus.CHECKED_THROUGH and self.checked_through is None:
            raise ValueError("CHECKED_THROUGH requires checked_through")
        if self.currency_status != CurrencyStatus.CHECKED_THROUGH and self.checked_through is not None:
            raise ValueError("checked_through requires CHECKED_THROUGH currency status")
        return self

    def supports_text_verification(self) -> bool:
        return self.content_match and bool(self.quotation.strip())

    def supports_current_law(self, as_of: date) -> bool:
        return (
            self.supports_text_verification()
            and self.currency_status == CurrencyStatus.CHECKED_THROUGH
            and self.checked_through is not None
            and self.checked_through >= as_of
            and self.legal_effect == LegalEffectStatus.EFFECTIVE
        )


class SourceIdentifierVerification(BaseModel):
    requested_identifier: str
    normalized_identifier: str
    status: SourceIdentifierStatus
    retrieval: RetrievalEvidence
    matches: list[VerificationEvidence] = Field(default_factory=list)
    issues: list[str] = Field(default_factory=list)

    @model_validator(mode="after")
    def verified_identifier_requires_match(self) -> "SourceIdentifierVerification":
        if self.status == SourceIdentifierStatus.VERIFIED_SOURCE_IDENTIFIER and not self.matches:
            raise ValueError("VERIFIED_SOURCE_IDENTIFIER requires at least one exact match")
        if self.status != SourceIdentifierStatus.VERIFIED_SOURCE_IDENTIFIER and self.matches:
            raise ValueError("unconfirmed source identifiers cannot contain verification matches")
        return self
