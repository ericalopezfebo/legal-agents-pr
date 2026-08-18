from pydantic import BaseModel, Field

from .authority import Authority
from .quality import QualityReport


class LegalAnalysis(BaseModel):
    agent: str
    issues: list[str] = Field(default_factory=list)
    rules: list[str] = Field(default_factory=list)
    analysis: list[str] = Field(default_factory=list)
    authorities: list[Authority] = Field(default_factory=list)
    risks: list[str] = Field(default_factory=list)
    assumptions: list[str] = Field(default_factory=list)
    unverified_claims: list[str] = Field(default_factory=list)
    recommended_next_steps: list[str] = Field(default_factory=list)
    narrative: str = ""
    quality: QualityReport = Field(default_factory=QualityReport)

