from legal_agents_pr import LegalAgent, MockProvider
from legal_agents_pr.schemas.authority import VerificationStatus
from legal_agents_pr.schemas.quality import QualityStatus


def test_runtime_with_structured_mock():
    provider = MockProvider([{
        "agent": "administrative-law", "issues": ["Finality"], "rules": [],
        "analysis": ["Additional facts are needed."], "authorities": [],
        "risks": [], "assumptions": [], "unverified_claims": [],
        "recommended_next_steps": ["Obtain the agency order"], "narrative": "Borrador.",
    }])
    result = LegalAgent.load("administrative-law", provider=provider).run("Pregunta ficticia")
    assert result.agent == "administrative-law"
    assert result.quality.status == QualityStatus.VALIDATED_DRAFT
    assert provider.requests
    request = provider.requests[0]
    assert request.metadata["source_refs"] == ["pr-lpau-38-2017-2025-05-16"]
    assert "metadata only; the source text was not checked" in request.messages[0].content
    assert "Do not mark an authority VERIFIED" in request.messages[0].content
    assert "## Skill: legal-research" in request.messages[0].content
    assert "## Skill: citation-check" in request.messages[0].content


def test_non_json_provider_response_fails_conservatively():
    result = LegalAgent.load("civil-law", provider=MockProvider(["plain text"])).run("Pregunta")
    assert result.quality.status == QualityStatus.DRAFT
    assert result.unverified_claims


def test_provider_cannot_self_verify_authority():
    provider = MockProvider([{
        "agent": "civil-law",
        "authorities": [{
            "citation": "Fabricated verification",
            "proposition": "A proposition.",
            "verification_status": "VERIFIED",
        }],
        "narrative": "Borrador.",
    }])

    result = LegalAgent.load("civil-law", provider=provider).run("Pregunta ficticia")

    assert result.quality.status == QualityStatus.DRAFT
    assert result.authorities
    assert all(
        authority.verification_status == VerificationStatus.UNVERIFIED
        for authority in result.authorities
    )


def test_provider_cannot_self_certify_judicial_treatment():
    provider = MockProvider([{
        "agent": "appellate-law",
        "authorities": [{
            "citation": "2024 TSPR 7",
            "source_type": "judicial-decision",
            "treatment": {
                "status": "OVERRULED",
                "confirmed": True,
                "basis": "OFFICIAL_COURT_METADATA",
            },
        }],
        "narrative": "Borrador.",
    }])
    result = LegalAgent.load("appellate-law", provider=provider).run("Pregunta ficticia")
    treatment = result.authorities[0].treatment
    assert treatment is not None
    assert not treatment.confirmed
    assert treatment.status.value == "UNKNOWN_UNVERIFIED"
