import pytest

from legal_agents_pr.core.quality_gate import LegalQualityGate
from legal_agents_pr.schemas.authority import Authority, VerificationStatus
from legal_agents_pr.schemas.legal_output import LegalAnalysis
from legal_agents_pr.schemas.quality import CheckStatus, QualityStatus


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
        citation="Verified source placeholder", source_url="https://example.invalid",
        verification_status=VerificationStatus.VERIFIED,
    )
    report = LegalQualityGate().evaluate(LegalAnalysis(agent="civil-law", authorities=[authority]))
    assert report.status == QualityStatus.VALIDATED_DRAFT
    assert report.attorney_review_required


def test_final_requires_human_confirmation():
    gate = LegalQualityGate()
    report = gate.evaluate(LegalAnalysis(agent="civil-law"))
    with pytest.raises(ValueError):
        gate.human_finalize(report, confirmed_by_attorney=False)


def test_jurisdiction_is_not_automatically_verified():
    report = LegalQualityGate().evaluate(LegalAnalysis(agent="administrative-law"))
    jurisdiction = next(check for check in report.checks if check.name == "jurisdiction")
    assert jurisdiction.status == CheckStatus.PARTIALLY_VERIFIED
