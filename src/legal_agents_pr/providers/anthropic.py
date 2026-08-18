from __future__ import annotations

import os

from legal_agents_pr.core.exceptions import ConfigurationError, ProviderError
from legal_agents_pr.schemas.provider import GenerationRequest, GenerationResponse

from .base import LLMProvider


class AnthropicProvider(LLMProvider):
    name = "anthropic"

    def __init__(self, api_key: str | None = None) -> None:
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ConfigurationError("ANTHROPIC_API_KEY is required for the Anthropic provider")

    async def generate(self, request: GenerationRequest) -> GenerationResponse:
        try:
            from anthropic import AsyncAnthropic
        except ImportError as exc:
            raise ConfigurationError("Install legal-agents-pr[anthropic]") from exc
        system = "\n\n".join(m.content for m in request.messages if m.role == "system")
        messages = [m.model_dump(include={"role", "content"}) for m in request.messages if m.role != "system"]
        try:
            result = await AsyncAnthropic(api_key=self.api_key).messages.create(
                model=request.model,
                system=system,
                messages=messages,
                max_tokens=request.max_tokens or 4096,
                temperature=request.temperature,
            )
        except Exception as exc:
            raise ProviderError("Anthropic provider request failed") from exc
        text = "".join(block.text for block in result.content if getattr(block, "type", "") == "text")
        return GenerationResponse(content=text, model=request.model, provider=self.name)

