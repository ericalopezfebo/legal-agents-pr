from pathlib import Path

import pytest

from legal_agents_pr.core.loader import AgentLoader
from legal_agents_pr.core.source_catalog import SourceCatalogLoader


def test_catalog_loads_ten_unique_sources() -> None:
    catalog = SourceCatalogLoader().load()

    assert len(catalog.sources) == 10
    assert len({source.sha256 for source in catalog.sources}) == 10


def test_unattributed_citation_aid_is_not_marked_official() -> None:
    source = SourceCatalogLoader().get("pr-basic-legal-citation-reference-undated")

    assert source.revision_as_of is None
    assert source.status.value == "user-supplied-reference-copy"


def test_agent_source_references_exist() -> None:
    agent_loader = AgentLoader()
    source_loader = SourceCatalogLoader()

    for agent_id in agent_loader.list_ids():
        source_loader.validate_references(agent_loader.load(agent_id).definition.source_refs)


def test_unknown_source_reference_is_rejected() -> None:
    with pytest.raises(ValueError, match="Unknown source references"):
        SourceCatalogLoader().validate_references(["missing-source"])


def test_duplicate_hashes_are_rejected(tmp_path: Path) -> None:
    manifest = tmp_path / "registry.yaml"
    source = """\
schema_version: "1.0"
sources:
  - &source
    id: source-one
    title: Source one
    short_title: One
    source_type: statute
    publisher: Official publisher
    revision_as_of: 2025-01-01
    coverage_note: Test copy.
    filename: one.pdf
    sha256: aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
  - <<: *source
    id: source-two
    title: Source two
    short_title: Two
    filename: two.pdf
"""
    manifest.write_text(source, encoding="utf-8")

    with pytest.raises(ValueError, match="duplicate source files"):
        SourceCatalogLoader(manifest).load()
