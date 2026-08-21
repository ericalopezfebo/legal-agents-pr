from legal_agents_pr.core.loader import AgentLoader
from legal_agents_pr.skills import SkillLoader


def test_drafting_skills_require_sanitization_and_attorney_review() -> None:
    skills = SkillLoader()
    motion = skills.load("motion-drafting").instructions.lower()
    pretrial = skills.load("pretrial-report-drafting").instructions.lower()
    sanitization = skills.load("legal-document-sanitization").instructions.lower()

    assert "[parte]" in motion
    assert "attorney review" in motion
    assert "no copiar identidades" in pretrial
    assert "attorney review" in pretrial
    for term in ("nombres", "direcciones", "metadatos", "reidentificación"):
        assert term in sanitization


def test_civil_procedure_prompt_blocks_model_provenance_disclosure() -> None:
    prompt = AgentLoader().load("civil-procedure").system_prompt.lower()
    assert "copia sanitizada" in prompt
    assert "nunca reveles ni conserves la procedencia" in prompt
    assert "no reutilices hechos o identidades" in prompt
