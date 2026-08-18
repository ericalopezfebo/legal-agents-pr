from datetime import date, datetime, timezone

import pytest

from legal_agents_pr.schemas.source_evidence import (
    CurrencyStatus,
    LegalEffectStatus,
    RetrievalEvidence,
    SourceLocator,
    VerificationEvidence,
)


def retrieval() -> RetrievalEvidence:
    return RetrievalEvidence(
        source_id="official-source",
        source_url="https://official.example/document.pdf",
        retrieved_at=datetime(2026, 8, 18, 9, 30, tzinfo=timezone.utc),
        document_sha256="b" * 64,
        publisher="Official publisher",
        media_type="application/pdf",
        official_source=True,
    )


def test_retrieval_requires_timezone():
    with pytest.raises(ValueError, match="timezone"):
        RetrievalEvidence(
            source_url="https://official.example/document.pdf",
            retrieved_at=datetime(2026, 8, 18, 9, 30),  # noqa: DTZ001 - intentional invalid input
            document_sha256="b" * 64,
            publisher="Official publisher",
        )


def test_locator_requires_pinpoint():
    with pytest.raises(ValueError, match="pinpoint"):
        SourceLocator()


def test_checked_through_requires_date():
    with pytest.raises(ValueError, match="requires checked_through"):
        VerificationEvidence(
            retrieval=retrieval(),
            locator=SourceLocator(article="1"),
            quotation="Supporting text.",
            content_match=True,
            legal_effect=LegalEffectStatus.EFFECTIVE,
            currency_status=CurrencyStatus.CHECKED_THROUGH,
            verification_method="test",
        )


def test_effective_source_checked_through_date_supports_current_law():
    evidence = VerificationEvidence(
        retrieval=retrieval(),
        locator=SourceLocator(article="1"),
        quotation="Supporting text.",
        content_match=True,
        legal_effect=LegalEffectStatus.EFFECTIVE,
        currency_status=CurrencyStatus.CHECKED_THROUGH,
        checked_through=date(2026, 8, 18),
        verification_method="test",
    )

    assert evidence.supports_current_law(date(2026, 8, 18))
    assert not evidence.supports_current_law(date(2026, 8, 19))
