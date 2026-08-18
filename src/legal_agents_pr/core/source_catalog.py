from __future__ import annotations

from importlib.resources import files
from pathlib import Path

import yaml

from legal_agents_pr.schemas.source import LegalSource, SourceCatalog


class SourceCatalogLoader:
    def __init__(self, manifest: Path | None = None) -> None:
        self.manifest = manifest or Path(
            str(files("legal_agents_pr").joinpath("sources").joinpath("registry.yaml"))
        )

    def load(self) -> SourceCatalog:
        data = yaml.safe_load(self.manifest.read_text(encoding="utf-8"))
        return SourceCatalog.model_validate(data)

    def get(self, source_id: str) -> LegalSource:
        catalog = self.load()
        for source in catalog.sources:
            if source.id == source_id:
                return source
        raise KeyError(f"Unknown source: {source_id}")

    def validate_references(self, source_refs: list[str]) -> None:
        available = {source.id for source in self.load().sources}
        unknown = sorted(set(source_refs) - available)
        if unknown:
            raise ValueError(f"Unknown source references: {', '.join(unknown)}")
