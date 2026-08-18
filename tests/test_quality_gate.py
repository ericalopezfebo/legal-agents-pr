from datetime import date, datetime, timezone

import pytest

from legal_agents_pr.core.quality_gate import LegalQualityGate
from legal_agents_pr.schemas.authority import Authority, VerificationStatus
from legal_agents_pr.schemas.legal_output import LegalAnalysis
from legal_agents_pr.schemas.quality import CheckStatus, QualityStatus
from legal_agents_pr.schemas.source_evidence import (
    CurrencyStatus,
    LegalEffectStatus,
    RetrievalEvidence,
    SourceLocator,
    VerificationEvidence,
)


def evidence(*, checked_through: date | None = None) -> VerificationEvidence:
    return VerificationEvidence(
        retrieval=RetrievalEvidence(
            source_url="https://official.example/source.pdf",
            retrieved_at=datetime(2026, 8, 18, 12, tzinfo=timezone.utc),
            document_sha256="a" * 64,
            publisher="Official publisher",
            official_source=True,
        ),
        locator=SourceLocator(section="1"),
        quotation="Exact supporting text.",
        content_match=True,
        legal_effect=LegalEffectStatus.EFFECTIVE,
        currency_status=(
            CurrencyStatus.CHECKED_THROUGH
            if checked_through is not None
            else CurrencyStatus.NOT_CHECKED
        ),
        checked_through=checked_through,
        verification_method="test-fixture",
    )


def test_unverified_authority_blocks_validation():
    output = LegalAnalysis(
        agent="civil-law", rules=["A legal proposition"],
        authorities=[Authority(citation="Unverified placeholder")],
    )
    report = LegalQualityGate().evaluate(output)
    assert report.status == QualityStatus.DRAFT
    assert report.blocking_issues


def test_verified_authority_allows_validated_draft():
    authority = Authority(
        citation="Verified source placeholder",
        proposition="The source supports this proposition.",
        source_url="https://official.example/source.pdf",
        verification_status=VerificationStatus.VERIFIED,
        evidence=evidence(checked_through=date(2026, 8, 18)),
    )
    report = LegalQualityGate().evaluate(
        LegalAnalysis(agent="civil-law", authorities=[authority]),
        as_of_date=date(2026, 8, 18),
    )
    assert report.status == QualityStatus.VALIDATED_DRAFT
    assert report.attorney_review_required


def test_text_verified_but_currency_unchecked_remains_draft():
    authority = Authority(
        citation="Text-verified source",
        proposition="The source supports this proposition.",
        verification_status=VerificationStatus.VERIFIED,
        evidence=evidence(),
    )

    report = LegalQualityGate().evaluate(
        LegalAnalysis(agent="civil-law", authorities=[authority]),
        as_of_date=date(2026, 8, 18),
    )

    assert report.status == QualityStatus.DRAFT
    assert any("Current-law status" in issue for issue in report.blocking_issues)


def test_verified_authority_requires_matching_evidence():
    with pytest.raises(ValueError, match="matching retrieval evidence"):
        Authority(
            citation="Unsupported verified claim",
            proposition="Unsupported proposition.",
            verification_status=VerificationStatus.VERIFIED,
        )


def test_final_requires_human_confirmation():
    gate = LegalQualityGate()
    report = gate.evaluate(LegalAnalysis(agent="civil-law"))
    with pytest.raises(ValueError):
        gate.human_finalize(report, confirmed_by_attorney=False)


def test_jurisdiction_is_not_automatically_verified():
    report = LegalQualityGate().evaluate(LegalAnalysis(agent="administrative-law"))
    jurisdiction = next(check for check in report.checks if check.name == "jurisdiction")
    assert jurisdiction.status == CheckStatus.PARTIALLY_VERIFIED
