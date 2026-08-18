from legal_agents_pr.core.source_policy import classify_authority
from legal_agents_pr.schemas.authority import AuthorityLevel


def test_verified_court_rule_is_primary_authority():
    assert classify_authority("court-rule", verified=True) == AuthorityLevel.PRIMARY_AUTHORITY


def test_source_type_alias_is_normalized():
    assert classify_authority("law_review", verified=True) == AuthorityLevel.SECONDARY_AUTHORITY


def test_unverified_source_never_receives_authority_level():
    assert classify_authority("statute", verified=False) == AuthorityLevel.UNVERIFIED_SOURCE
