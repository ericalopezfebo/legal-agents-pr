from __future__ import annotations

import os

from legal_agents_pr.core.exceptions import ConfigurationError, ProviderError
from legal_agents_pr.schemas.provider import GenerationRequest, GenerationResponse

from .base import LLMProvider


class OpenAIProvider(LLMProvider):
    name = "openai"

    def __init__(self, api_key: str | None = None) -> None:
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ConfigurationError("OPENAI_API_KEY is required for the OpenAI provider")

    async def generate(self, request: GenerationRequest) -> GenerationResponse:
        try:
            from openai import AsyncOpenAI
        except ImportError as exc:
            raise ConfigurationError("Install legal-agents-pr[openai]") from exc
        try:
            result = await AsyncOpenAI(api_key=self.api_key).responses.create(
                model=request.model,
                input=[m.model_dump(exclude_none=True) for m in request.messages],
                temperature=request.temperature,
            )
        except Exception as exc:
            raise ProviderError("OpenAI provider request failed") from exc
        usage_value = getattr(result, "usage", None)
        usage = usage_value.model_dump() if usage_value is not None else {}
        return GenerationResponse(
            content=result.output_text,
            model=request.model,
            provider=self.name,
            usage=usage,
        )
