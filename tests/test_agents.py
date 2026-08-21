from legal_agents_pr.core.loader import AgentLoader

EXPECTED = {
    "administrative-law", "labor-employment-law", "constitutional-law", "notarial-law",
    "civil-law", "civil-procedure", "contracts", "business-organizations", "evidence", "appellate-law",
    "professional-responsibility", "intellectual-property-law",
    "criminal-law",
    "privacy-cybersecurity-law",
    "federal-civil-litigation-pr",
    "federal-criminal-litigation-pr",
    "bankruptcy-pr",
    "federal-appellate-pr",
}


def test_all_agent_definitions_load():
    loader = AgentLoader()
    assert set(loader.list_ids()) == EXPECTED
    for agent_id in EXPECTED:
        loaded = loader.load(agent_id)
        assert loaded.definition.id == agent_id
        assert loaded.definition.capabilities
        assert "revisión" in loaded.system_prompt.lower() or "agente" in loaded.system_prompt.lower()


def test_shared_legal_policy_is_injected_into_every_agent():
    loader = AgentLoader()
    for agent_id in EXPECTED:
        prompt = loader.load(agent_id).system_prompt
        assert "Política común de operación jurídica" in prompt
        assert "UNVERIFIED" in prompt
        assert "evento activador" in prompt


def test_civil_procedure_has_research_and_filing_readiness_skills():
    skills = AgentLoader().load("civil-procedure").definition.skills
    assert "legal-research" in skills
    assert "filing-readiness" in skills
