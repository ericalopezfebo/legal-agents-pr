from __future__ import annotations

import os

from legal_agents_pr.core.exceptions import ConfigurationError, ProviderError
from legal_agents_pr.schemas.provider import GenerationRequest, GenerationResponse

from .base import LLMProvider


class GeminiProvider(LLMProvider):
    name = "gemini"

    def __init__(self, api_key: str | None = None) -> None:
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ConfigurationError("GEMINI_API_KEY is required for the Gemini provider")

    async def generate(self, request: GenerationRequest) -> GenerationResponse:
        try:
            from google import genai
        except ImportError as exc:
            raise ConfigurationError("Install legal-agents-pr[gemini]") from exc
        prompt = "\n\n".join(f"[{m.role}] {m.content}" for m in request.messages)
        try:
            result = await genai.Client(api_key=self.api_key).aio.models.generate_content(
                model=request.model, contents=prompt
            )
        except Exception as exc:
            raise ProviderError("Gemini provider request failed") from exc
        return GenerationResponse(content=result.text or "", model=request.model, provider=self.name)

