from __future__ import annotations

from io import BytesIO

from pypdf import PdfReader
from pypdf.errors import PdfReadError

from legal_agents_pr.core.exceptions import SourceParseError
from legal_agents_pr.schemas.document_text import ExactTextMatch, ParsedPdfText, PdfPageText
from legal_agents_pr.schemas.source_evidence import SourceLocator


def _normalize(value: str) -> str:
    return " ".join(value.split())


class PdfTextExtractor:
    def __init__(self, *, max_pages: int = 500, max_characters: int = 5_000_000) -> None:
        if max_pages < 1 or max_characters < 1:
            raise ValueError("PDF extraction limits must be positive")
        self.max_pages = max_pages
        self.max_characters = max_characters

    def extract(self, content: bytes) -> ParsedPdfText:
        if not content:
            raise SourceParseError("PDF content is empty")
        try:
            reader = PdfReader(BytesIO(content), strict=False)
            if reader.is_encrypted:
                raise SourceParseError("Encrypted PDFs are not supported")
            if not reader.pages:
                raise SourceParseError("PDF does not contain pages")
            if len(reader.pages) > self.max_pages:
                raise SourceParseError("PDF exceeds the configured page limit")

            pages: list[PdfPageText] = []
            extracted_characters = 0
            issues: list[str] = []
            for page_number, page in enumerate(reader.pages, start=1):
                try:
                    extracted = page.extract_text() or ""
                except (KeyError, TypeError, ValueError) as exc:
                    extracted = ""
                    issues.append(f"Page {page_number} text extraction failed: {type(exc).__name__}")
                lines = [_normalize(line) for line in extracted.splitlines() if _normalize(line)]
                extracted_characters += sum(len(line) for line in lines)
                if extracted_characters > self.max_characters:
                    raise SourceParseError("PDF exceeds the configured extracted-text limit")
                pages.append(PdfPageText(page=page_number, lines=lines))
        except SourceParseError:
            raise
        except (PdfReadError, OSError, TypeError, ValueError) as exc:
            raise SourceParseError("Official PDF text extraction failed") from exc

        ocr_required = extracted_characters == 0
        if ocr_required:
            issues.append("No text layer was found; OCR and independent review are required")
        return ParsedPdfText(
            pages=pages,
            total_pages=len(pages),
            extracted_characters=extracted_characters,
            ocr_required=ocr_required,
            issues=issues,
        )

    def locate_exact_text(
        self, document: ParsedPdfText, query: str, *, max_matches: int = 20
    ) -> list[ExactTextMatch]:
        normalized_query = _normalize(query)
        if not normalized_query:
            raise ValueError("query cannot be empty")
        if max_matches < 1 or max_matches > 100:
            raise ValueError("max_matches must be between 1 and 100")

        matches: list[ExactTextMatch] = []
        for page in document.pages:
            for line_start in range(len(page.lines)):
                candidate_parts: list[str] = []
                for line_end in range(line_start, len(page.lines)):
                    candidate_parts.append(page.lines[line_end])
                    candidate = _normalize(" ".join(candidate_parts))
                    position = candidate.casefold().find(normalized_query.casefold())
                    if 0 <= position < len(page.lines[line_start]):
                        matches.append(
                            ExactTextMatch(
                                locator=SourceLocator(
                                    page=page.page,
                                    line_start=line_start + 1,
                                    line_end=line_end + 1,
                                ),
                                quotation=candidate[position : position + len(normalized_query)],
                                normalized_query=normalized_query,
                            )
                        )
                        break
                    if len(candidate) > len(normalized_query) * 4 + 500:
                        break
                if len(matches) >= max_matches:
                    return matches
        return matches
