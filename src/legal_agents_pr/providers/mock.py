from __future__ import annotations

import json
from typing import Any

from legal_agents_pr.schemas.provider import GenerationRequest, GenerationResponse

from .base import LLMProvider


class MockProvider(LLMProvider):
    """Deterministic offline provider for tests, demos, and integration development."""

    name = "mock"

    def __init__(self, responses: list[str | dict[str, Any]] | None = None) -> None:
        self.responses = list(responses or ["Respuesta simulada para revisión humana."])
        self.requests: list[GenerationRequest] = []

    async def generate(self, request: GenerationRequest) -> GenerationResponse:
        self.requests.append(request)
        value = self.responses.pop(0) if self.responses else "Respuesta simulada."
        content = json.dumps(value, ensure_ascii=False) if isinstance(value, dict) else value
        return GenerationResponse(content=content, model=request.model, provider=self.name)

