from datetime import datetime, timezone

import pytest

from legal_agents_pr.schemas.source_evidence import (
    RetrievalEvidence,
    SourceIdentifierStatus,
    SourceIdentifierVerification,
)
from legal_agents_pr.tools import (
    OfficialSourceIdentifierInput,
    OfficialSourceIdentifierTool,
    default_legal_tool_registry,
)


class StubVerifier:
    async def verify_identifier(self, url: str, identifier: str, *, max_matches: int = 20):
        return SourceIdentifierVerification(
            requested_identifier=identifier,
            normalized_identifier="2024 TSPR 7",
            status=SourceIdentifierStatus.SOURCE_FOUND_IDENTIFIER_UNCONFIRMED,
            retrieval=RetrievalEvidence(
                source_url=url,
                retrieved_at=datetime(2026, 8, 18, tzinfo=timezone.utc),
                document_sha256="c" * 64,
                publisher="Poder Judicial de Puerto Rico",
                media_type="application/pdf",
                official_source=True,
            ),
            issues=[f"No exact match among at most {max_matches} results"],
        )


@pytest.mark.asyncio
async def test_tool_returns_structured_unconfirmed_result() -> None:
    tool = OfficialSourceIdentifierTool(verifier=StubVerifier())
    result = await tool.execute(
        OfficialSourceIdentifierInput(
            url="https://poderjudicial.pr/opinion.pdf",
            identifier="2024 TSPR 7",
            max_matches=4,
        )
    )
    assert isinstance(result, SourceIdentifierVerification)
    assert result.status == SourceIdentifierStatus.SOURCE_FOUND_IDENTIFIER_UNCONFIRMED
    assert "4" in result.issues[0]


def test_default_registry_exposes_official_verification_schema() -> None:
    registry = default_legal_tool_registry()
    tool = registry.get("official-source-identifier")
    assert tool.output_schema is SourceIdentifierVerification
    assert registry.schemas()[0]["name"] == "official-source-identifier"
