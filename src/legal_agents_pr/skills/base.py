from dataclasses import dataclass
from importlib.resources import files
from pathlib import Path

import yaml


@dataclass(frozen=True)
class Skill:
    name: str
    instructions: str
    source: str = "local"


class SkillRegistry:
    def __init__(self) -> None:
        self._skills: dict[str, Skill] = {}

    def register(self, skill: Skill) -> None:
        self._skills[skill.name] = skill

    def get(self, name: str) -> Skill:
        return self._skills[name]


class SkillLoader:
    def __init__(self, root: Path | None = None) -> None:
        self.root = root or Path(str(files("legal_agents_pr").joinpath("skills/library")))

    def list_ids(self) -> list[str]:
        return sorted(path.name for path in self.root.iterdir() if (path / "SKILL.md").is_file())

    def load(self, name: str) -> Skill:
        path = self.root / name / "SKILL.md"
        if not path.is_file():
            raise ValueError(f"Unknown skill: {name}")
        content = path.read_text(encoding="utf-8")
        if not content.startswith("---\n") or "\n---\n" not in content[4:]:
            raise ValueError(f"Invalid skill frontmatter: {name}")
        frontmatter_text, instructions = content[4:].split("\n---\n", 1)
        metadata = yaml.safe_load(frontmatter_text)
        if not isinstance(metadata, dict) or metadata.get("name") != name:
            raise ValueError(f"Skill name does not match directory: {name}")
        if not isinstance(metadata.get("description"), str) or not metadata["description"].strip():
            raise ValueError(f"Skill description is required: {name}")
        if not instructions.strip():
            raise ValueError(f"Skill instructions are required: {name}")
        return Skill(name=name, instructions=instructions.strip(), source=str(path))

    def validate_references(self, names: list[str]) -> None:
        available = set(self.list_ids())
        unknown = sorted(set(names) - available)
        if unknown:
            raise ValueError(f"Unknown skill references: {', '.join(unknown)}")
