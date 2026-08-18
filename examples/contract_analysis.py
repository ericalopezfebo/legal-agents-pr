from legal_agents_pr import LegalAgent, MockProvider

agent = LegalAgent.load("contracts", provider=MockProvider())
print(agent.run("Ejemplo ficticio: identifica categorías de riesgo contractual.").narrative)

