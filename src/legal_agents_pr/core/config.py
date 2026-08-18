from __future__ import annotations

import os
from pathlib import Path

import yaml
from pydantic import BaseModel, Field


class RuntimeConfig(BaseModel):
    provider: str = "mock"
    model: str = "mock-legal-model"
    temperature: float = Field(default=0.1, ge=0, le=2)
    max_handoff_depth: int = Field(default=2, ge=0, le=5)
    require_verified_citations: bool = True

    @classmethod
    def load(cls, path: str | Path | None = None, **overrides: object) -> RuntimeConfig:
        data: dict[str, object] = {}
        if path:
            loaded = yaml.safe_load(Path(path).read_text(encoding="utf-8")) or {}
            data.update(loaded)
        env_map = {
            "provider": "LEGAL_AGENTS_PROVIDER",
            "model": "LEGAL_AGENTS_MODEL",
            "temperature": "LEGAL_AGENTS_TEMPERATURE",
            "max_handoff_depth": "LEGAL_AGENTS_MAX_HANDOFF_DEPTH",
        }
        for field, env_name in env_map.items():
            if env_name in os.environ:
                data[field] = os.environ[env_name]
        data.update({key: value for key, value in overrides.items() if value is not None})
        return cls.model_validate(data)

