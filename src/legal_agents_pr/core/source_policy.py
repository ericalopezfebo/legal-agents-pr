from legal_agents_pr.schemas.authority import Authority, AuthorityLevel, VerificationStatus

PRIMARY_SOURCE_TYPES = {
    "constitution", "statute", "regulation", "court_rule", "supreme_court_case",
    "federal_case",
}
SECONDARY_SOURCE_TYPES = {"treatise", "law_review", "official_guidance"}


def classify_authority(source_type: str, verified: bool) -> AuthorityLevel:
    if not verified:
        return AuthorityLevel.UNVERIFIED_SOURCE
    if source_type in PRIMARY_SOURCE_TYPES:
        return AuthorityLevel.PRIMARY_AUTHORITY
    if source_type in SECONDARY_SOURCE_TYPES:
        return AuthorityLevel.SECONDARY_AUTHORITY
    return AuthorityLevel.UNVERIFIED_SOURCE


def normalize_authority(authority: Authority) -> Authority:
    verified = authority.verification_status == VerificationStatus.VERIFIED
    authority.authority_level = classify_authority(authority.source_type, verified)
    return authority

