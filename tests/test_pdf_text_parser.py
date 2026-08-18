from io import BytesIO

import pytest
from pypdf import PdfWriter

from legal_agents_pr.core.exceptions import SourceParseError
from legal_agents_pr.schemas.document_text import ParsedPdfText, PdfPageText
from legal_agents_pr.sources.parsers import PdfTextExtractor


def blank_pdf() -> bytes:
    output = BytesIO()
    writer = PdfWriter()
    writer.add_blank_page(width=612, height=792)
    writer.write(output)
    return output.getvalue()


def test_blank_pdf_requires_ocr_instead_of_claiming_text_verification() -> None:
    result = PdfTextExtractor().extract(blank_pdf())
    assert result.ocr_required
    assert result.extracted_characters == 0
    assert "OCR" in result.issues[0]


def test_invalid_pdf_fails_safely() -> None:
    with pytest.raises(SourceParseError, match="extraction failed"):
        PdfTextExtractor().extract(b"not a PDF")


def test_page_limit_is_enforced() -> None:
    output = BytesIO()
    writer = PdfWriter()
    writer.add_blank_page(width=612, height=792)
    writer.add_blank_page(width=612, height=792)
    writer.write(output)
    with pytest.raises(SourceParseError, match="page limit"):
        PdfTextExtractor(max_pages=1).extract(output.getvalue())


def test_locates_normalized_text_with_page_and_line_pinpoint() -> None:
    document = ParsedPdfText(
        pages=[
            PdfPageText(
                page=1,
                lines=[
                    "Texto introductorio.",
                    "La agencia deberá notificar",
                    "a todas las partes.",
                ],
            )
        ],
        total_pages=1,
        extracted_characters=70,
    )
    matches = PdfTextExtractor().locate_exact_text(
        document, "la agencia deberá notificar a todas las partes"
    )
    assert len(matches) == 1
    assert matches[0].locator.page == 1
    assert matches[0].locator.line_start == 2
    assert matches[0].locator.line_end == 3
    assert matches[0].exact_normalized_match


def test_exact_match_search_is_bounded() -> None:
    document = ParsedPdfText(
        pages=[PdfPageText(page=1, lines=["TSPR"] * 150)],
        total_pages=1,
        extracted_characters=600,
    )
    assert len(PdfTextExtractor().locate_exact_text(document, "TSPR", max_matches=3)) == 3
    with pytest.raises(ValueError, match="between 1 and 100"):
        PdfTextExtractor().locate_exact_text(document, "TSPR", max_matches=101)
