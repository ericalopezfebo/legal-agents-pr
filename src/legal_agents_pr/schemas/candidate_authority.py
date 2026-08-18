from __future__ import annotations

from enum import Enum

from pydantic import BaseModel, Field, field_validator

from .authority import VerificationStatus


class CandidateAuthorityType(str, Enum):
    STATUTE = "statute"
    CODE = "code"
    SPECIAL_LAW = "special-law"
    REGULATION = "regulation"
    TSPR_DECISION = "tspr-decision"
    FEDERAL_DECISION = "federal-decision"
    ADMINISTRATIVE_RESOLUTION = "administrative-resolution"


class CandidateAuthority(BaseModel):
    citation: str
    authority_type: CandidateAuthorityType
    year: int | None = None
    topics: list[str] = Field(min_length=1)
    verification_status: VerificationStatus = VerificationStatus.UNVERIFIED

    @field_validator("verification_status")
    @classmethod
    def candidates_cannot_be_preverified(
        cls, value: VerificationStatus
    ) -> VerificationStatus:
        if value != VerificationStatus.UNVERIFIED:
            raise ValueError("candidate authorities must remain UNVERIFIED")
        return value


class CandidateAuthorityIndex(BaseModel):
    schema_version: str = "1.0"
    provenance: str
    copyright_scope: str
    verification_notice: str
    authorities: list[CandidateAuthority]

    @field_validator("authorities")
    @classmethod
    def unique_citations(cls, value: list[CandidateAuthority]) -> list[CandidateAuthority]:
        citations = [item.citation.casefold() for item in value]
        if len(citations) != len(set(citations)):
            raise ValueError("candidate authority citations must be unique")
        return value
