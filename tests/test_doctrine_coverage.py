from legal_agents_pr.core.loader import AgentLoader

EXPECTED_COVERAGE = {
    "administrative-law": ("agotamiento", "subastas", "oficial examinador"),
    "contracts": ("vicios de la voluntad", "novación", "fraude de acreedores"),
    "civil-procedure": ("sentencia sumaria", "parte indispensable", "relevo de sentencia"),
    "constitutional-law": ("igual protección", "amplitud excesiva", "acción de estado"),
    "evidence": ("autenticación", "prueba de referencia", "privilegios"),
}


def test_internal_taxonomy_is_issue_spotting_only_and_not_disclosed():
    for agent_id, topics in EXPECTED_COVERAGE.items():
        prompt = AgentLoader().load(agent_id).system_prompt.lower()
        assert all(topic in prompt for topic in topics)
        assert "taxonomía interna" in prompt
        assert "no la menciones" in prompt
        assert "verific" in prompt
