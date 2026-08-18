from datetime import datetime, timezone

import pytest

from legal_agents_pr.core.source_verifier import (
    OfficialPdfSourceVerifier,
    normalize_source_identifier,
)
from legal_agents_pr.schemas.document_text import ParsedPdfText, PdfPageText
from legal_agents_pr.schemas.source_evidence import (
    CurrencyStatus,
    LegalEffectStatus,
    RetrievalEvidence,
    SourceIdentifierStatus,
)
from legal_agents_pr.sources.connectors.base import RetrievedDocument, SourceConnector


class FakeConnector(SourceConnector):
    async def fetch(self, url: str) -> RetrievedDocument:
        return RetrievedDocument(
            content=b"pdf bytes",
            evidence=RetrievalEvidence(
                source_url=url,
                retrieved_at=datetime(2026, 8, 18, tzinfo=timezone.utc),
                document_sha256="a" * 64,
                publisher="Poder Judicial de Puerto Rico",
                media_type="application/pdf",
                official_source=True,
            ),
        )


class FakeExtractor:
    def __init__(self, document: ParsedPdfText) -> None:
        self.document = document

    def extract(self, content: bytes) -> ParsedPdfText:
        return self.document

    def locate_exact_text(self, document, query, *, max_matches=20):
        from legal_agents_pr.sources.parsers.pdf_text import PdfTextExtractor

        return PdfTextExtractor().locate_exact_text(document, query, max_matches=max_matches)


def document(*lines: str, ocr_required: bool = False) -> ParsedPdfText:
    return ParsedPdfText(
        pages=[PdfPageText(page=1, lines=list(lines))],
        total_pages=1,
        extracted_characters=sum(len(line) for line in lines),
        ocr_required=ocr_required,
        issues=["OCR required"] if ocr_required else [],
    )


@pytest.mark.parametrize(
    ("raw", "normalized"),
    [
        ("2024 T.S.P.R. 007", "2024 TSPR 7"),
        ("214 D.P.R. 123 (2024)", "214 DPR 123 (2024)"),
        ("Ley Núm. 55-2020", "Ley 55-2020"),
    ],
)
def test_normalizes_supported_source_identifiers(raw: str, normalized: str) -> None:
    assert normalize_source_identifier(raw) == normalized


def test_rejects_incomplete_identifier() -> None:
    with pytest.raises(ValueError, match="unsupported or incomplete"):
        normalize_source_identifier("un caso importante")


@pytest.mark.asyncio
async def test_exact_identifier_match_builds_textual_evidence_only() -> None:
    verifier = OfficialPdfSourceVerifier(
        FakeConnector(), extractor=FakeExtractor(document("Véase 2024 TSPR 7 para el resultado."))
    )
    result = await verifier.verify_identifier("https://poderjudicial.pr/opinion.pdf", "2024 TSPR 7")
    assert result.status == SourceIdentifierStatus.VERIFIED_SOURCE_IDENTIFIER
    assert result.matches[0].content_match
    assert result.matches[0].legal_effect == LegalEffectStatus.UNKNOWN
    assert result.matches[0].currency_status == CurrencyStatus.NOT_CHECKED
    assert result.matches[0].locator.page == 1


@pytest.mark.asyncio
async def test_missing_exact_identifier_remains_unconfirmed() -> None:
    verifier = OfficialPdfSourceVerifier(
        FakeConnector(), extractor=FakeExtractor(document("Véase 2024 TSPR 70."))
    )
    result = await verifier.verify_identifier("https://poderjudicial.pr/opinion.pdf", "2024 TSPR 7")
    assert result.status == SourceIdentifierStatus.SOURCE_FOUND_IDENTIFIER_UNCONFIRMED
    assert not result.matches


@pytest.mark.asyncio
async def test_scan_requires_ocr_and_cannot_create_match() -> None:
    verifier = OfficialPdfSourceVerifier(
        FakeConnector(), extractor=FakeExtractor(document(ocr_required=True))
    )
    result = await verifier.verify_identifier("https://poderjudicial.pr/opinion.pdf", "Ley 55-2020")
    assert result.status == SourceIdentifierStatus.OCR_REQUIRED
    assert not result.matches
