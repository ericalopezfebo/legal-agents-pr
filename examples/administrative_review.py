from legal_agents_pr import LegalAgent, MockProvider

provider = MockProvider([{"agent": "administrative-law", "issues": ["finality"], "narrative": "Synthetic example only."}])
result = LegalAgent.load("administrative-law", provider=provider).run(
    "Ejemplo ficticio: identifica qué datos faltan para analizar revisión judicial."
)
print(result.model_dump_json(indent=2))

