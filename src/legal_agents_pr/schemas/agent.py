from pydantic import BaseModel, Field, field_validator


class JurisdictionConfig(BaseModel):
    primary: str = "pr"
    secondary: list[str] = Field(default_factory=list)


class QualityGateConfig(BaseModel):
    required: bool = True
    require_verified_citations: bool = True


class AgentDefinition(BaseModel):
    schema_version: str = "1.0"
    id: str
    name: str
    jurisdiction: JurisdictionConfig
    description: str
    specialties: list[str]
    capabilities: list[str]
    preferred_sources: list[str]
    source_refs: list[str] = Field(default_factory=list)
    allowed_tools: list[str] = Field(default_factory=list)
    skills: list[str] = Field(default_factory=list)
    handoffs: list[str] = Field(default_factory=list)
    output_schema: str = "legal-analysis"
    quality_gates: QualityGateConfig = Field(default_factory=QualityGateConfig)

    @field_validator("id")
    @classmethod
    def valid_id(cls, value: str) -> str:
        if not value or any(ch not in "abcdefghijklmnopqrstuvwxyz0123456789-" for ch in value):
            raise ValueError("agent id must use lowercase letters, digits, and hyphens")
        return value
