from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import AsyncIterator
from typing import Any

from pydantic import BaseModel

from legal_agents_pr.schemas.provider import GenerationRequest, GenerationResponse, ProviderStatus


class LLMProvider(ABC):
    name: str

    @abstractmethod
    async def generate(self, request: GenerationRequest) -> GenerationResponse:
        raise NotImplementedError

    async def generate_structured(
        self, request: GenerationRequest, output_schema: type[BaseModel]
    ) -> BaseModel:
        response = await self.generate(request)
        return output_schema.model_validate_json(response.content)

    async def stream(self, request: GenerationRequest) -> AsyncIterator[str]:
        response = await self.generate(request)
        yield response.content

    async def health_check(self) -> ProviderStatus:
        return ProviderStatus(provider=self.name, available=True)

    def capabilities(self) -> dict[str, Any]:
        return {"structured_output": True, "streaming": True}

