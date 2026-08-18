from enum import Enum

from pydantic import BaseModel, model_validator

from .source_evidence import VerificationEvidence


class AuthorityLevel(str, Enum):
    PRIMARY_AUTHORITY = "PRIMARY_AUTHORITY"
    SECONDARY_AUTHORITY = "SECONDARY_AUTHORITY"
    UNVERIFIED_SOURCE = "UNVERIFIED_SOURCE"


class VerificationStatus(str, Enum):
    VERIFIED = "VERIFIED"
    PARTIALLY_VERIFIED = "PARTIALLY_VERIFIED"
    UNVERIFIED = "UNVERIFIED"


class Authority(BaseModel):
    citation: str
    proposition: str = ""
    source_url: str | None = None
    source_type: str = "unknown"
    authority_level: AuthorityLevel = AuthorityLevel.UNVERIFIED_SOURCE
    verification_status: VerificationStatus = VerificationStatus.UNVERIFIED
    quotation: str | None = None
    evidence: VerificationEvidence | None = None

    @model_validator(mode="after")
    def verified_requires_evidence(self) -> "Authority":
        if self.verification_status == VerificationStatus.VERIFIED:
            if self.evidence is None or not self.evidence.supports_text_verification():
                raise ValueError("VERIFIED authority requires matching retrieval evidence")
            if not self.proposition.strip():
                raise ValueError("VERIFIED authority requires a supported proposition")
            if self.source_url is not None and self.source_url != self.evidence.retrieval.source_url:
                raise ValueError("authority source_url must match retrieval evidence")
            if self.quotation is not None and self.quotation != self.evidence.quotation:
                raise ValueError("authority quotation must match verification evidence")
        return self
