from __future__ import annotations

import httpx

from legal_agents_pr.core.exceptions import ProviderError
from legal_agents_pr.schemas.provider import GenerationRequest, GenerationResponse

from .base import LLMProvider


class OpenAICompatibleProvider(LLMProvider):
    """Minimal adapter for OpenAI-compatible chat-completions endpoints."""

    def __init__(self, *, name: str, base_url: str, api_key: str | None = None) -> None:
        self.name = name
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key

    async def generate(self, request: GenerationRequest) -> GenerationResponse:
        headers = {"Authorization": f"Bearer {self.api_key}"} if self.api_key else {}
        payload = {
            "model": request.model,
            "messages": [m.model_dump(exclude_none=True) for m in request.messages],
            "temperature": request.temperature,
        }
        if request.max_tokens:
            payload["max_tokens"] = request.max_tokens
        try:
            async with httpx.AsyncClient(timeout=60) as client:
                response = await client.post(
                    f"{self.base_url}/chat/completions", headers=headers, json=payload
                )
                response.raise_for_status()
                data = response.json()
        except (httpx.HTTPError, KeyError, ValueError) as exc:
            raise ProviderError(f"{self.name} provider request failed") from exc
        choice = data["choices"][0]
        return GenerationResponse(
            content=choice["message"]["content"] or "",
            model=data.get("model", request.model),
            provider=self.name,
            usage=data.get("usage", {}),
            finish_reason=choice.get("finish_reason"),
        )

