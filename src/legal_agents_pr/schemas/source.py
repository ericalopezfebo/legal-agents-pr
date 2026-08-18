from datetime import date
from enum import Enum

from pydantic import BaseModel, Field, field_validator


class SourceStatus(str, Enum):
    USER_SUPPLIED_OFFICIAL_COPY = "user-supplied-official-copy"


class LegalSource(BaseModel):
    id: str
    title: str
    short_title: str
    jurisdiction: str = "pr"
    source_type: str
    publisher: str
    revision_as_of: date
    coverage_note: str
    filename: str
    sha256: str = Field(min_length=64, max_length=64)
    status: SourceStatus = SourceStatus.USER_SUPPLIED_OFFICIAL_COPY
    official_url: str | None = None

    @field_validator("id")
    @classmethod
    def valid_id(cls, value: str) -> str:
        if not value or any(ch not in "abcdefghijklmnopqrstuvwxyz0123456789-" for ch in value):
            raise ValueError("source id must use lowercase letters, digits, and hyphens")
        return value

    @field_validator("sha256")
    @classmethod
    def valid_sha256(cls, value: str) -> str:
        if any(ch not in "0123456789abcdef" for ch in value):
            raise ValueError("sha256 must be lowercase hexadecimal")
        return value


class SourceCatalog(BaseModel):
    schema_version: str = "1.0"
    sources: list[LegalSource]

    @field_validator("sources")
    @classmethod
    def unique_sources(cls, value: list[LegalSource]) -> list[LegalSource]:
        ids = [source.id for source in value]
        hashes = [source.sha256 for source in value]
        if len(ids) != len(set(ids)):
            raise ValueError("source ids must be unique")
        if len(hashes) != len(set(hashes)):
            raise ValueError("duplicate source files must be represented once")
        return value
