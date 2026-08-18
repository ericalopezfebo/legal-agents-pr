from __future__ import annotations

from pydantic import BaseModel, Field

from legal_agents_pr.core.source_verifier import OfficialPdfSourceVerifier
from legal_agents_pr.schemas.source_evidence import SourceIdentifierVerification
from legal_agents_pr.sources.connectors import PuertoRicoOfficialConnector

from .base import Tool


class OfficialSourceIdentifierInput(BaseModel):
    url: str
    identifier: str
    max_matches: int = Field(default=20, ge=1, le=100)


class OfficialSourceIdentifierTool(Tool):
    name = "official-source-identifier"
    description = (
        "Verifica la aparición exacta de una cita TSPR, DPR o ley numerada en un PDF "
        "recuperado desde una fuente oficial permitida. No determina vigencia ni tratamiento."
    )
    input_schema = OfficialSourceIdentifierInput
    output_schema = SourceIdentifierVerification

    def __init__(self, verifier: OfficialPdfSourceVerifier | None = None) -> None:
        self.verifier = verifier or OfficialPdfSourceVerifier(PuertoRicoOfficialConnector())

    async def execute(self, payload: BaseModel) -> BaseModel:
        request = OfficialSourceIdentifierInput.model_validate(payload.model_dump())
        return await self.verifier.verify_identifier(
            request.url,
            request.identifier,
            max_matches=request.max_matches,
        )


def default_legal_tool_registry():
    from .base import ToolRegistry

    registry = ToolRegistry()
    registry.register(OfficialSourceIdentifierTool())
    return registry
