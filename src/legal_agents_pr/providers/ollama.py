from .http_compatible import OpenAICompatibleProvider


class OllamaProvider(OpenAICompatibleProvider):
    def __init__(self, base_url: str = "http://localhost:11434/v1") -> None:
        super().__init__(name="ollama", base_url=base_url)

