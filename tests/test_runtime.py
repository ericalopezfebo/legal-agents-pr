from legal_agents_pr import LegalAgent, MockProvider
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


def test_non_json_provider_response_fails_conservatively():
    result = LegalAgent.load("civil-law", provider=MockProvider(["plain text"])).run("Pregunta")
    assert result.quality.status == QualityStatus.DRAFT
    assert result.unverified_claims

