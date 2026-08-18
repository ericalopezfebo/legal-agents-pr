from __future__ import annotations

from pydantic import BaseModel, Field, model_validator

from .source_evidence import SourceLocator


class PdfPageText(BaseModel):
    page: int = Field(ge=1)
    lines: list[str]


class ParsedPdfText(BaseModel):
    pages: list[PdfPageText]
    total_pages: int = Field(ge=1)
    extracted_characters: int = Field(ge=0)
    ocr_required: bool = False
    issues: list[str] = Field(default_factory=list)

    @model_validator(mode="after")
    def page_count_matches(self) -> ParsedPdfText:
        if len(self.pages) != self.total_pages:
            raise ValueError("parsed page count must match total_pages")
        return self


class ExactTextMatch(BaseModel):
    locator: SourceLocator
    quotation: str = Field(min_length=1)
    normalized_query: str = Field(min_length=1)
    exact_normalized_match: bool = True
