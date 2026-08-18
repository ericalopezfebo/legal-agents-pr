from dataclasses import dataclass


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

