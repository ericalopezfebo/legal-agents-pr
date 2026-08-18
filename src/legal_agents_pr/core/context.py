from pydantic import BaseModel, Field


class MatterContext(BaseModel):
    jurisdiction: str = "pr"
    forum: str | None = None
    procedural_posture: str | None = None
    facts: dict[str, str] = Field(default_factory=dict)
    assumptions: list[str] = Field(default_factory=list)
    confidential: bool = False

