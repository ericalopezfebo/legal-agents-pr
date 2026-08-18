from enum import Enum

from pydantic import BaseModel


class AuthorityLevel(str, Enum):
    PRIMARY_AUTHORITY = "PRIMARY_AUTHORITY"
    SECONDARY_AUTHORITY = "SECONDARY_AUTHORITY"
    UNVERIFIED_SOURCE = "UNVERIFIED_SOURCE"


class VerificationStatus(str, Enum):
    VERIFIED = "VERIFIED"
    PARTIALLY_VERIFIED = "PARTIALLY_VERIFIED"
    UNVERIFIED = "UNVERIFIED"


class Authority(BaseModel):
    citation: str
    proposition: str = ""
    source_url: str | None = None
    source_type: str = "unknown"
    authority_level: AuthorityLevel = AuthorityLevel.UNVERIFIED_SOURCE
    verification_status: VerificationStatus = VerificationStatus.UNVERIFIED
    quotation: str | None = None

