from __future__ import annotations

import re

from legal_agents_pr.core.exceptions import SourceParseError
from legal_agents_pr.schemas.source_evidence import (
    CurrencyStatus,
    LegalEffectStatus,
    SourceIdentifierStatus,
    SourceIdentifierVerification,
    VerificationEvidence,
)
from legal_agents_pr.sources.connectors.base import SourceConnector
from legal_agents_pr.sources.parsers.pdf_text import PdfTextExtractor

TSPR_PATTERN = re.compile(r"^(?P<year>\d{4})\s+T\.?S\.?P\.?R\.?\s+0*(?P<number>\d{1,3})$", re.IGNORECASE)
DPR_PATTERN = re.compile(
    r"^(?P<volume>\d{1,3})\s+D\.?P\.?R\.?\s+(?P<page>\d{1,4})"
    r"(?:\s*,\s*\d{1,4})?\s*\((?P<year>\d{4})\)$",
    re.IGNORECASE,
)
LAW_PATTERN = re.compile(
    r"^Ley(?:\s+N[uú]m\.?)?\s+(?P<number>\d{1,4})(?:\s*[-–]\s*(?P<year>\d{4}))?$",
    re.IGNORECASE,
)


def normalize_source_identifier(value: str) -> str:
    collapsed = " ".join(value.split()).strip(" ,.;")
    tspr = TSPR_PATTERN.fullmatch(collapsed)
    if tspr:
        return f"{tspr.group('year')} TSPR {int(tspr.group('number'))}"
    dpr = DPR_PATTERN.fullmatch(collapsed)
    if dpr:
        return (
            f"{int(dpr.group('volume'))} DPR {int(dpr.group('page'))} "
            f"({dpr.group('year')})"
        )
    law = LAW_PATTERN.fullmatch(collapsed)
    if law:
        suffix = f"-{law.group('year')}" if law.group("year") else ""
        return f"Ley {int(law.group('number'))}{suffix}"
    raise ValueError("unsupported or incomplete source identifier")


class OfficialPdfSourceVerifier:
    def __init__(
        self,
        connector: SourceConnector,
        *,
        extractor: PdfTextExtractor | None = None,
    ) -> None:
        self.connector = connector
        self.extractor = extractor or PdfTextExtractor()

    async def verify_identifier(
        self, url: str, identifier: str, *, max_matches: int = 20
    ) -> SourceIdentifierVerification:
        normalized = normalize_source_identifier(identifier)
        retrieved = await self.connector.fetch(url)
        if retrieved.evidence.media_type not in (None, "application/pdf"):
            raise SourceParseError("source identifier verification requires a PDF document")
        document = self.extractor.extract(retrieved.content)
        if document.ocr_required:
            return SourceIdentifierVerification(
                requested_identifier=identifier,
                normalized_identifier=normalized,
                status=SourceIdentifierStatus.OCR_REQUIRED,
                retrieval=retrieved.evidence,
                issues=document.issues,
            )
        exact_matches = self.extractor.locate_exact_text(
            document, normalized, max_matches=max_matches
        )
        if not exact_matches:
            return SourceIdentifierVerification(
                requested_identifier=identifier,
                normalized_identifier=normalized,
                status=SourceIdentifierStatus.SOURCE_FOUND_IDENTIFIER_UNCONFIRMED,
                retrieval=retrieved.evidence,
                issues=["The official PDF was retrieved, but the exact identifier was not found"],
            )
        evidence = [
            VerificationEvidence(
                retrieval=retrieved.evidence,
                locator=match.locator,
                quotation=match.quotation,
                content_match=True,
                legal_effect=LegalEffectStatus.UNKNOWN,
                currency_status=CurrencyStatus.NOT_CHECKED,
                verification_method="exact-normalized-source-identifier-match",
                notes=[
                    "Identifier match only; legal effect, currency and treatment were not checked"
                ],
            )
            for match in exact_matches
        ]
        return SourceIdentifierVerification(
            requested_identifier=identifier,
            normalized_identifier=normalized,
            status=SourceIdentifierStatus.VERIFIED_SOURCE_IDENTIFIER,
            retrieval=retrieved.evidence,
            matches=evidence,
            issues=document.issues,
        )
