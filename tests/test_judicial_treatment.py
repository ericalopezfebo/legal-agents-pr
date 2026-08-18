from datetime import datetime, timezone

import pytest

from legal_agents_pr.schemas.judicial_treatment import (
    JudicialTreatmentAssessment,
    JudicialTreatmentStatus,
    TreatmentBasis,
)
from legal_agents_pr.schemas.source_evidence import (
    RetrievalEvidence,
    SourceLocator,
    VerificationEvidence,
)


def evidence() -> VerificationEvidence:
    return VerificationEvidence(
        retrieval=RetrievalEvidence(
            source_url="https://poderjudicial.pr/opinion.pdf",
            retrieved_at=datetime(2026, 8, 18, tzinfo=timezone.utc),
            document_sha256="b" * 64,
            publisher="Poder Judicial de Puerto Rico",
            media_type="application/pdf",
            official_source=True,
        ),
        locator=SourceLocator(page=12, line_start=4, line_end=7),
        quotation="El Tribunal distingue expresamente la decisión anterior.",
        content_match=True,
        verification_method="human-reviewed-official-source",
    )


def test_confirmed_treatment_requires_trusted_textual_evidence() -> None:
    assessment = JudicialTreatmentAssessment(
        status=JudicialTreatmentStatus.DISTINGUISHED,
        confirmed=True,
        basis=TreatmentBasis.HUMAN_REVIEWED_OFFICIAL_SOURCE,
        evidence=evidence(),
    )
    assert assessment.confirmed


def test_automated_candidate_cannot_confirm_treatment() -> None:
    with pytest.raises(ValueError, match="automated candidates cannot confirm"):
        JudicialTreatmentAssessment(
            status=JudicialTreatmentStatus.OVERRULED,
            confirmed=True,
            basis=TreatmentBasis.AUTOMATED_CANDIDATE,
            evidence=evidence(),
        )


def test_unconfirmed_treatment_cannot_assert_status_or_evidence() -> None:
    with pytest.raises(ValueError, match="must remain UNKNOWN_UNVERIFIED"):
        JudicialTreatmentAssessment(status=JudicialTreatmentStatus.FOLLOWED)
    with pytest.raises(ValueError, match="cannot contain verification evidence"):
        JudicialTreatmentAssessment(evidence=evidence())
