from __future__ import annotations

from dataclasses import dataclass
from importlib.resources import files
from pathlib import Path

import yaml

from legal_agents_pr.core.exceptions import AgentNotFoundError
from legal_agents_pr.schemas.agent import AgentDefinition


@dataclass(frozen=True)
class LoadedAgent:
    definition: AgentDefinition
    system_prompt: str


class AgentLoader:
    def __init__(self, root: Path | None = None) -> None:
        self.root = root or Path(str(files("legal_agents_pr").joinpath("agents")))

    def list_ids(self) -> list[str]:
        ids: list[str] = []
        for path in self.root.iterdir():
            manifest = path / "agent.yaml"
            if manifest.is_file():
                data = yaml.safe_load(manifest.read_text(encoding="utf-8"))
                ids.append(AgentDefinition.model_validate(data).id)
        return sorted(ids)

    def load(self, agent_id: str) -> LoadedAgent:
        directory = self.root / agent_id.replace("-", "_")
        if not directory.is_dir():
            directory = self.root / agent_id
        manifest = directory / "agent.yaml"
        system = directory / "system.md"
        if not manifest.is_file() or not system.is_file():
            raise AgentNotFoundError(f"Unknown agent: {agent_id}")
        definition = AgentDefinition.model_validate(yaml.safe_load(manifest.read_text(encoding="utf-8")))
        shared_system = self.root / "_shared" / "system.md"
        prompt_parts: list[str] = []
        if shared_system.is_file():
            prompt_parts.append(shared_system.read_text(encoding="utf-8").strip())
        prompt_parts.append(system.read_text(encoding="utf-8").strip())
        return LoadedAgent(definition, "\n\n".join(prompt_parts))
