# Providers

The core speaks only through `LLMProvider`. OpenAI, Anthropic and Gemini SDKs are optional extras. OpenRouter and Ollama use the compatible HTTP adapter. `MockProvider` is deterministic and requires no network.

Adapters must not modify agent instructions, silently change verification status, log secrets, or treat provider confidence as legal verification.

