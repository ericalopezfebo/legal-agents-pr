from legal_agents_pr.core.router import DomainRouter


def test_routes_administrative_review():
    route = DomainRouter().route("¿Cuándo procede revisión judicial de una agencia?")
    assert route.primary_agent == "administrative-law"
    assert route.confidence > 0.5


def test_routes_contract_question_with_secondary():
    route = DomainRouter().route("¿Es válida esta cláusula de no competencia en el contrato de empleo?")
    assert route.primary_agent in {"contracts", "labor-employment-law"}
    assert route.secondary_agents


def test_uncertain_route_requires_confirmation():
    assert DomainRouter().route("Necesito orientación").requires_confirmation

