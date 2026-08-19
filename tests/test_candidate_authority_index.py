from pathlib import Path

import pytest

from legal_agents_pr.core.candidate_authority_index import CandidateAuthorityIndexLoader
from legal_agents_pr.schemas.authority import VerificationStatus


def test_candidate_index_contains_only_unverified_citations() -> None:
    index = CandidateAuthorityIndexLoader().load()
    assert len(index.authorities) > 500
    assert all(
        item.verification_status == VerificationStatus.UNVERIFIED
        for item in index.authorities
    )


def test_candidate_index_searches_by_topic_and_citation() -> None:
    loader = CandidateAuthorityIndexLoader()
    civil = loader.search(topic="daños", limit=10)
    tspr = loader.search(citation="TSPR", limit=10)
    assert civil
    assert all("Daños" in item.topics for item in civil)
    assert tspr
    assert all("TSPR" in item.citation for item in tspr)


def test_candidate_index_exposes_focused_admin_and_civil_topics() -> None:
    loader = CandidateAuthorityIndexLoader()
    index = loader.load()
    administrative = loader.search(topic="administrativo", limit=100)
    civil_procedure = loader.search(topic="procedimiento civil", limit=100)
    assert sum("Administrativo" in item.topics for item in index.authorities) == 238
    assert sum("Procedimiento civil" in item.topics for item in index.authorities) == 306
    assert len(administrative) == 100
    assert len(civil_procedure) == 100
    assert all("Administrativo" in item.topics for item in administrative)
    assert all("Procedimiento civil" in item.topics for item in civil_procedure)


def test_candidate_index_rejects_preverified_records(tmp_path: Path) -> None:
    manifest = tmp_path / "candidates.yaml"
    manifest.write_text(
        """\
schema_version: '1.0'
provenance: citation-only extraction
copyright_scope: factual citation metadata only
verification_notice: verify against official sources
authorities:
  - citation: 2024 TSPR 1
    authority_type: tspr-decision
    year: 2024
    topics: [Daños]
    verification_status: VERIFIED
""",
        encoding="utf-8",
    )
    with pytest.raises(ValueError, match="must remain UNVERIFIED"):
        CandidateAuthorityIndexLoader(manifest).load()


def test_candidate_index_limit_is_bounded() -> None:
    with pytest.raises(ValueError, match="between 1 and 100"):
        CandidateAuthorityIndexLoader().search(limit=101)
