from pydantic import BaseModel

from legal_agents_pr.tools import Tool, ToolRegistry


class Query(BaseModel):
    citation: str


class Finding(BaseModel):
    citation: str
    verified: bool = False


class SyntheticCitationTool(Tool):
    name = "synthetic-citation-check"
    description = "Example only; it does not access legal sources."
    input_schema = Query
    output_schema = Finding

    async def execute(self, payload: BaseModel) -> BaseModel:
        return Finding(citation=payload.citation, verified=False)


registry = ToolRegistry()
registry.register(SyntheticCitationTool())
print(registry.schemas())

