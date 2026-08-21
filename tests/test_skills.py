from pathlib import Path

import pytest

from legal_agents_pr.core.loader import AgentLoader
from legal_agents_pr.skills import SkillLoader


def test_all_agent_skill_references_resolve() -> None:
    agents = AgentLoader()
    skills = SkillLoader()
    for agent_id in agents.list_ids():
        skills.validate_references(agents.load(agent_id).definition.skills)


def test_skill_library_contains_substantive_instructions() -> None:
    loader = SkillLoader()
    assert len(loader.list_ids()) == 86
    for skill_id in loader.list_ids():
        skill = loader.load(skill_id)
        assert len(skill.instructions.splitlines()) >= 5
        assert skill.source.endswith("SKILL.md")


def test_skill_name_must_match_directory(tmp_path: Path) -> None:
    directory = tmp_path / "expected-name"
    directory.mkdir()
    (directory / "SKILL.md").write_text(
        "---\nname: wrong-name\ndescription: A valid description.\n---\nInstructions.\n",
        encoding="utf-8",
    )
    with pytest.raises(ValueError, match="does not match"):
        SkillLoader(tmp_path).load("expected-name")


def test_unknown_skill_reference_fails_safely() -> None:
    with pytest.raises(ValueError, match="Unknown skill references"):
        SkillLoader().validate_references(["missing-skill"])
