from __future__ import annotations

from collections.abc import Callable

from legal_agents_pr.core.exceptions import ConfigurationError

from .base import LLMProvider

ProviderFactory = Callable[[], LLMProvider]


class ProviderRegistry:
    def __init__(self) -> None:
        self._factories: dict[str, ProviderFactory] = {}

    def register(self, name: str, factory: ProviderFactory) -> None:
        self._factories[name] = factory

    def create(self, name: str) -> LLMProvider:
        try:
            return self._factories[name]()
        except KeyError as exc:
            raise ConfigurationError(f"Unknown provider: {name}") from exc

    def names(self) -> list[str]:
        return sorted(self._factories)


def default_registry() -> ProviderRegistry:
    from .anthropic import AnthropicProvider
    from .gemini import GeminiProvider
    from .mock import MockProvider
    from .ollama import OllamaProvider
    from .openai import OpenAIProvider
    from .openrouter import OpenRouterProvider

    registry = ProviderRegistry()
    registry.register("mock", MockProvider)
    registry.register("openai", OpenAIProvider)
    registry.register("anthropic", AnthropicProvider)
    registry.register("gemini", GeminiProvider)
    registry.register("openrouter", OpenRouterProvider)
    registry.register("ollama", OllamaProvider)
    return registry

