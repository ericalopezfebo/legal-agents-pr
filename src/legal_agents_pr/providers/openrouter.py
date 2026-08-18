import os

from .http_compatible import OpenAICompatibleProvider


class OpenRouterProvider(OpenAICompatibleProvider):
    def __init__(self, api_key: str | None = None, base_url: str | None = None) -> None:
        super().__init__(
            name="openrouter",
            base_url=base_url or "https://openrouter.ai/api/v1",
            api_key=api_key or os.getenv("OPENROUTER_API_KEY"),
        )

