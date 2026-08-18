from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, Field


class Message(BaseModel):
    role: Literal["system", "user", "assistant", "tool"]
    content: str
    name: str | None = None


class GenerationRequest(BaseModel):
    messages: list[Message]
    model: str
    temperature: float = Field(default=0.1, ge=0, le=2)
    max_tokens: int | None = Field(default=None, gt=0)
    metadata: dict[str, Any] = Field(default_factory=dict)


class GenerationResponse(BaseModel):
    content: str
    model: str
    provider: str
    usage: dict[str, int] = Field(default_factory=dict)
    finish_reason: str | None = None


class ProviderStatus(BaseModel):
    provider: str
    available: bool
    detail: str = ""

