from __future__ import annotations

from enum import Enum

from pydantic import BaseModel, Field, model_validator

from .source_evidence import VerificationEvidence


class JudicialTreatmentStatus(str, Enum):
    CITED = "CITED"
    FOLLOWED = "FOLLOWED"
    APPLIED = "APPLIED"
    DISTINGUISHED = "DISTINGUISHED"
    CRITICIZED = "CRITICIZED"
    LIMITED = "LIMITED"
    OVERRULED = "OVERRULED"
    UNKNOWN_UNVERIFIED = "UNKNOWN_UNVERIFIED"


class TreatmentBasis(str, Enum):
    HUMAN_REVIEWED_OFFICIAL_SOURCE = "HUMAN_REVIEWED_OFFICIAL_SOURCE"
    OFFICIAL_COURT_METADATA = "OFFICIAL_COURT_METADATA"
    AUTOMATED_CANDIDATE = "AUTOMATED_CANDIDATE"


class JudicialTreatmentAssessment(BaseModel):
    status: JudicialTreatmentStatus = JudicialTreatmentStatus.UNKNOWN_UNVERIFIED
    confirmed: bool = False
    basis: TreatmentBasis = TreatmentBasis.AUTOMATED_CANDIDATE
    evidence: VerificationEvidence | None = None
    notes: list[str] = Field(default_factory=list)

    @model_validator(mode="after")
    def confirmed_treatment_requires_trusted_evidence(self) -> JudicialTreatmentAssessment:
        if not self.confirmed:
            if self.status != JudicialTreatmentStatus.UNKNOWN_UNVERIFIED:
                raise ValueError("unconfirmed treatment must remain UNKNOWN_UNVERIFIED")
            if self.evidence is not None:
                raise ValueError("unconfirmed treatment cannot contain verification evidence")
            return self
        if self.status == JudicialTreatmentStatus.UNKNOWN_UNVERIFIED:
            raise ValueError("confirmed treatment requires an explicit status")
        if self.basis == TreatmentBasis.AUTOMATED_CANDIDATE:
            raise ValueError("automated candidates cannot confirm judicial treatment")
        if self.evidence is None or not self.evidence.supports_text_verification():
            raise ValueError("confirmed treatment requires matching textual evidence")
        return self
