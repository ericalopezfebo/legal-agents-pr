from __future__ import annotations

from importlib.resources import files
from pathlib import Path

import yaml

from legal_agents_pr.schemas.candidate_authority import CandidateAuthority, CandidateAuthorityIndex


class CandidateAuthorityIndexLoader:
    def __init__(self, manifest: Path | None = None) -> None:
        self.manifest = manifest or Path(
            str(files("legal_agents_pr").joinpath("sources").joinpath("authority_candidates.yaml"))
        )

    def load(self) -> CandidateAuthorityIndex:
        data = yaml.safe_load(self.manifest.read_text(encoding="utf-8"))
        return CandidateAuthorityIndex.model_validate(data)

    def search(
        self,
        *,
        topic: str | None = None,
        citation: str | None = None,
        limit: int = 25,
    ) -> list[CandidateAuthority]:
        if limit < 1 or limit > 100:
            raise ValueError("limit must be between 1 and 100")
        topic_key = topic.casefold().strip() if topic else None
        citation_key = citation.casefold().strip() if citation else None
        matches: list[CandidateAuthority] = []
        for authority in self.load().authorities:
            if topic_key and not any(topic_key in item.casefold() for item in authority.topics):
                continue
            if citation_key and citation_key not in authority.citation.casefold():
                continue
            matches.append(authority)
        return matches[:limit]
