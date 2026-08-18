from abc import ABC, abstractmethod
from dataclasses import dataclass

from legal_agents_pr.schemas.source_evidence import RetrievalEvidence


@dataclass(frozen=True)
class RetrievedDocument:
    content: bytes
    evidence: RetrievalEvidence


class SourceConnector(ABC):
    @abstractmethod
    async def fetch(self, url: str) -> RetrievedDocument:
        raise NotImplementedError
