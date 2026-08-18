from legal_agents_pr import LegalAgent, MockProvider

# Replace MockProvider with any LLMProvider implementation.
provider = MockProvider(["Custom provider response"])
agent = LegalAgent.load("evidence", provider=provider)
print(agent.run("Ejemplo ficticio de integración.").narrative)

