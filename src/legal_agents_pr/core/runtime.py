from __future__ import annotations

import json

from legal_agents_pr.providers.base import LLMProvider
from legal_agents_pr.schemas.authority import VerificationStatus
from legal_agents_pr.schemas.legal_output import LegalAnalysis
from legal_agents_pr.schemas.provider import GenerationRequest, Message

from .config import RuntimeConfig
from .loader import LoadedAgent
from .quality_gate import LegalQualityGate
from .source_catalog import SourceCatalogLoader

OUTPUT_INSTRUCTION = """
Return one JSON object with these keys: agent, issues, rules, analysis, authorities,
risks, assumptions, unverified_claims, recommended_next_steps, narrative. Do not include
markdown fences. Every authority must include verification_status. Use UNVERIFIED when
the source was not actually checked. Provider output cannot self-certify verification;
only trusted source-tool evidence can support VERIFIED. Never claim the work product is final.
""".strip()


class AgentRuntime:
    def __init__(
        self,
        provider: LLMProvider,
        config: RuntimeConfig | None = None,
        source_catalog: SourceCatalogLoader | None = None,
    ) -> None:
        self.provider = provider
        self.config = config or RuntimeConfig(provider=provider.name)
        self.quality_gate = LegalQualityGate()
        self.source_catalog = source_catalog or SourceCatalogLoader()

    def source_context(self, agent: LoadedAgent) -> str:
        if not agent.definition.source_refs:
            return "No versioned local source metadata is assigned to this agent."
        self.source_catalog.validate_references(agent.definition.source_refs)
        lines = [
            "Versioned source metadata (metadata only; the source text was not checked by this step):"
        ]
        for source_id in agent.definition.source_refs:
            source = self.source_catalog.get(source_id)
            revision = source.revision_as_of.isoformat() if source.revision_as_of else "unknown"
            lines.append(
                f"- {source.id}: {source.title}; type={source.source_type}; "
                f"revision_as_of={revision}; status={source.status.value}; "
                f"official_url={source.official_url or 'unverified'}; caution={source.coverage_note}"
            )
        lines.append(
            "Do not mark an authority VERIFIED merely because it appears in this metadata. "
            "Verification requires checking the operative source text and its official location."
        )
        return "\n".join(lines)

    async def run(self, agent: LoadedAgent, query: str) -> LegalAnalysis:
        request = GenerationRequest(
            model=self.config.model,
            temperature=self.config.temperature,
            messages=[
                Message(
                    role="system",
                    content=(
                        f"{agent.system_prompt}\n\n{self.source_context(agent)}\n\n"
                        f"{OUTPUT_INSTRUCTION}"
                    ),
                ),
                Message(role="user", content=query),
            ],
            metadata={
                "agent": agent.definition.id,
                "jurisdiction": "pr",
                "source_refs": agent.definition.source_refs,
            },
        )
        response = await self.provider.generate(request)
        try:
            payload = json.loads(response.content)
            payload.setdefault("agent", agent.definition.id)
            for authority_payload in payload.get("authorities", []):
                if isinstance(authority_payload, dict):
                    authority_payload["verification_status"] = VerificationStatus.UNVERIFIED.value
                    authority_payload.pop("evidence", None)
                    if "treatment" in authority_payload:
                        authority_payload["treatment"] = {
                            "status": "UNKNOWN_UNVERIFIED",
                            "confirmed": False,
                            "basis": "AUTOMATED_CANDIDATE",
                            "notes": [
                                "Provider-supplied treatment cannot self-certify legal history"
                            ],
                        }
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
