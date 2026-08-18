from pydantic import BaseModel, Field


class HandoffRequest(BaseModel):
    from_agent: str
    to_agent: str
    issue: str
    facts: dict[str, str] = Field(default_factory=dict)
    questions: list[str] = Field(default_factory=list)
    reason: str
    depth: int = 1
    visited_agents: list[str] = Field(default_factory=list)

