from legal_agents_pr.core.loader import AgentLoader

EXPECTED_COVERAGE = {
    "administrative-law": ("agotamiento", "subastas", "oficial examinador"),
    "contracts": ("vicios de la voluntad", "novación", "fraude de acreedores"),
    "business-organizations": ("deberes de cuidado", "acciones directas y derivativas", "descorrer el velo"),
    "labor-employment-law": ("contratista independiente", "periodo probatorio", "justa causa"),
    "intellectual-property-law": ("riesgo de confusión", "presentación comercial", "control de calidad"),
    "civil-procedure": ("sentencia sumaria", "parte indispensable", "relevo"),
    "constitutional-law": ("igual protección", "amplitud excesiva", "acción estatal"),
    "evidence": ("autenticación", "prueba de referencia", "privilegios"),
}


def test_internal_taxonomy_is_issue_spotting_only_and_not_disclosed():
    for agent_id, topics in EXPECTED_COVERAGE.items():
        prompt = AgentLoader().load(agent_id).system_prompt.lower()
        assert all(topic in prompt for topic in topics)
        assert "taxonomía interna" in prompt
        assert "no la menciones" in prompt
        assert "verific" in prompt


def test_every_agent_receives_auditable_legal_reasoning_protocol():
    for agent_id in EXPECTED_COVERAGE:
        prompt = AgentLoader().load(agent_id).system_prompt.lower()
        assert "protocolo común de razonamiento jurídico" in prompt
        assert "hechos jurídicamente operativos" in prompt
        assert "cargas" in prompt
        assert "mejor teoría contraria" in prompt
        assert "vehículo procesal" in prompt
        assert "texto operativo" in prompt
        assert "límites institucionales" in prompt
        assert "razón decisoria" in prompt
        assert "fuente de descubrimiento" in prompt
        assert "prueba anti-sustitución" in prompt
