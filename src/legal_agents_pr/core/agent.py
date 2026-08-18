from __future__ import annotations

import asyncio
from pathlib import Path

from legal_agents_pr.providers.base import LLMProvider
from legal_agents_pr.providers.registry import default_registry
from legal_agents_pr.schemas.legal_output import LegalAnalysis

from .config import RuntimeConfig
from .loader import AgentLoader, LoadedAgent
from .runtime import AgentRuntime


class LegalAgent:
    def __init__(
        self,
        loaded: LoadedAgent,
        provider: LLMProvider,
        config: RuntimeConfig,
    ) -> None:
        self.loaded = loaded
        self.provider = provider
        self.config = config
        self.runtime = AgentRuntime(provider, config)

    @classmethod
    def load(
        cls,
        agent_id: str,
        *,
        provider: str | LLMProvider | None = None,
        model: str | None = None,
        config_path: str | Path | None = None,
    ) -> LegalAgent:
        overrides = {"provider": provider if isinstance(provider, str) else None, "model": model}
        config = RuntimeConfig.load(config_path, **overrides)
        provider_instance = provider if isinstance(provider, LLMProvider) else default_registry().create(config.provider)
        return cls(AgentLoader().load(agent_id), provider_instance, config)

    async def arun(self, query: str) -> LegalAnalysis:
        return await self.runtime.run(self.loaded, query)

    def run(self, query: str) -> LegalAnalysis:
        try:
            asyncio.get_running_loop()
        except RuntimeError:
            return asyncio.run(self.arun(query))
        raise RuntimeError("LegalAgent.run() cannot be used inside an active event loop; use arun()")

