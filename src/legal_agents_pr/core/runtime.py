from __future__ import annotations

import json

from legal_agents_pr.providers.base import LLMProvider
from legal_agents_pr.schemas.legal_output import LegalAnalysis
from legal_agents_pr.schemas.provider import GenerationRequest, Message

from .config import RuntimeConfig
from .loader import LoadedAgent
from .quality_gate import LegalQualityGate

OUTPUT_INSTRUCTION = """
Return one JSON object with these keys: agent, issues, rules, analysis, authorities,
risks, assumptions, unverified_claims, recommended_next_steps, narrative. Do not include
markdown fences. Every authority must include verification_status. Use UNVERIFIED when
the source was not actually checked. Never claim the work product is final.
""".strip()


class AgentRuntime:
    def __init__(self, provider: LLMProvider, config: RuntimeConfig | None = None) -> None:
        self.provider = provider
        self.config = config or RuntimeConfig(provider=provider.name)
        self.quality_gate = LegalQualityGate()

    async def run(self, agent: LoadedAgent, query: str) -> LegalAnalysis:
        request = GenerationRequest(
            model=self.config.model,
            temperature=self.config.temperature,
            messages=[
                Message(role="system", content=f"{agent.system_prompt}\n\n{OUTPUT_INSTRUCTION}"),
                Message(role="user", content=query),
            ],
            metadata={"agent": agent.definition.id, "jurisdiction": "pr"},
        )
        response = await self.provider.generate(request)
        try:
            payload = json.loads(response.content)
            payload.setdefault("agent", agent.definition.id)
            output = LegalAnalysis.model_validate(payload)
        except (json.JSONDecodeError, ValueError):
            output = LegalAnalysis(
                agent=agent.definition.id,
                narrative=response.content,
                unverified_claims=["Provider response was not returned in the structured legal schema."],
            )
        output.quality = self.quality_gate.evaluate(
            output,
            require_verified_citations=(
                self.config.require_verified_citations
                and agent.definition.quality_gates.require_verified_citations
            ),
        )
        return output

