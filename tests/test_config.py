from legal_agents_pr.core.config import RuntimeConfig


def test_environment_and_explicit_precedence(monkeypatch):
    monkeypatch.setenv("LEGAL_AGENTS_PROVIDER", "ollama")
    monkeypatch.setenv("LEGAL_AGENTS_MODEL", "local-model")
    config = RuntimeConfig.load(provider="mock")
    assert config.provider == "mock"
    assert config.model == "local-model"

