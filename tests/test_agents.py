from legal_agents_pr.core.loader import AgentLoader

EXPECTED = {
    "administrative-law", "labor-employment-law", "constitutional-law", "notarial-law",
    "civil-law", "civil-procedure", "contracts", "evidence", "appellate-law",
}


def test_all_agent_definitions_load():
    loader = AgentLoader()
    assert set(loader.list_ids()) == EXPECTED
    for agent_id in EXPECTED:
        loaded = loader.load(agent_id)
        assert loaded.definition.id == agent_id
        assert loaded.definition.capabilities
        assert "revisión" in loaded.system_prompt.lower() or "agente" in loaded.system_prompt.lower()
