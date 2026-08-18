from datetime import date
from enum import Enum

from pydantic import BaseModel, Field, field_validator


class JudicialDocumentType(str, Enum):
    OPINION = "OPINION"
    JUDGMENT = "JUDGMENT"
    RESOLUTION = "RESOLUTION"
    UNKNOWN = "UNKNOWN"


class TsprDecisionRecord(BaseModel):
    citation: str
    docket_number: str
    parties: str
    author: str
    decision_date: date
    subject: str
    document_type: JudicialDocumentType
    index_url: str
    document_url: str | None = None
    metadata_only: bool = True

    @field_validator("citation")
    @classmethod
    def valid_tspr_citation(cls, value: str) -> str:
        parts = value.split()
        if len(parts) != 3 or not parts[0].isdigit() or parts[1] != "TSPR" or not parts[2].isdigit():
            raise ValueError("citation must use 'YYYY TSPR N' format")
        return value


class TsprParseIssue(BaseModel):
    citation: str | None = None
    reason: str


class TsprParseResult(BaseModel):
    records: list[TsprDecisionRecord] = Field(default_factory=list)
    issues: list[TsprParseIssue] = Field(default_factory=list)
