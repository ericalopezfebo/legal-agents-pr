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


def test_routes_professional_responsibility():
    route = DomainRouter().route("Posible conflicto de intereses y confidencialidad del cliente")
    assert route.primary_agent == "professional-responsibility"


def test_routes_criminal_charge():
    route = DomainRouter().route("Analiza los elementos del delito en esta acusación penal")
    assert route.primary_agent == "criminal-law"


def test_routes_business_organizations():
    route = DomainRouter().route("¿Qué deber fiduciario tiene la junta de directores de esta corporación?")
    assert route.primary_agent == "business-organizations"


def test_routes_trademark_dispute():
    route = DomainRouter().route("Evalúa el riesgo de confusión y dilución de esta marca")
    assert route.primary_agent == "intellectual-property-law"
