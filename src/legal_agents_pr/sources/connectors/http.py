from __future__ import annotations

import hashlib
from collections.abc import Mapping
from datetime import datetime, timezone
from urllib.parse import urlsplit

import httpx

from legal_agents_pr.core.exceptions import SourceRetrievalError
from legal_agents_pr.schemas.source_evidence import RetrievalEvidence

from .base import RetrievedDocument, SourceConnector

DEFAULT_CONTENT_TYPES = frozenset(
    {
        "application/json",
        "application/octet-stream",
        "application/pdf",
        "application/xml",
        "text/html",
        "text/plain",
        "text/xml",
    }
)


class AllowlistedHttpSourceConnector(SourceConnector):
    def __init__(
        self,
        publishers: Mapping[str, str],
        *,
        client: httpx.AsyncClient | None = None,
        max_bytes: int = 15 * 1024 * 1024,
        allowed_content_types: frozenset[str] = DEFAULT_CONTENT_TYPES,
    ) -> None:
        if max_bytes < 1:
            raise ValueError("max_bytes must be positive")
        self.publishers = {host.lower(): publisher for host, publisher in publishers.items()}
        self.client = client
        self.max_bytes = max_bytes
        self.allowed_content_types = allowed_content_types

    def validate_url(self, url: str) -> tuple[str, str]:
        parsed = urlsplit(url)
        host = (parsed.hostname or "").lower()
        if parsed.scheme != "https":
            raise SourceRetrievalError("Official source retrieval requires HTTPS")
        if not host or host not in self.publishers:
            raise SourceRetrievalError(f"Source host is not allowlisted: {host or 'missing'}")
        if parsed.username or parsed.password:
            raise SourceRetrievalError("Source URLs cannot contain credentials")
        if parsed.port not in (None, 443):
            raise SourceRetrievalError("Source URLs cannot use a non-HTTPS port")
        return host, self.publishers[host]

    async def fetch(self, url: str) -> RetrievedDocument:
        self.validate_url(url)
        if self.client is not None:
            return await self._fetch(self.client, url)
        headers = {"User-Agent": "legal-agents-pr/0.2 source-verification"}
        async with httpx.AsyncClient(
            headers=headers, follow_redirects=False, trust_env=False
        ) as client:
            return await self._fetch(client, url)

    async def _fetch(self, client: httpx.AsyncClient, url: str) -> RetrievedDocument:
        _, publisher = self.validate_url(url)
        try:
            async with client.stream("GET", url) as response:
                if response.is_redirect:
                    raise SourceRetrievalError("Source redirects require explicit URL revalidation")
                response.raise_for_status()
                _, final_publisher = self.validate_url(str(response.url))
                if final_publisher != publisher:
                    raise SourceRetrievalError("Source publisher changed during retrieval")
                media_type = response.headers.get("content-type", "").split(";", 1)[0].lower()
                if media_type and media_type not in self.allowed_content_types:
                    raise SourceRetrievalError(f"Unsupported source content type: {media_type}")
                declared_size = response.headers.get("content-length")
                if declared_size is not None and int(declared_size) > self.max_bytes:
                    raise SourceRetrievalError("Source document exceeds the configured size limit")
                content = bytearray()
                async for chunk in response.aiter_bytes():
                    content.extend(chunk)
                    if len(content) > self.max_bytes:
                        raise SourceRetrievalError("Source document exceeds the configured size limit")
        except SourceRetrievalError:
            raise
        except (httpx.HTTPError, ValueError) as exc:
            raise SourceRetrievalError("Official source retrieval failed") from exc

        document = bytes(content)
        evidence = RetrievalEvidence(
            source_url=url,
            retrieved_at=datetime.now(timezone.utc),
            document_sha256=hashlib.sha256(document).hexdigest(),
            publisher=final_publisher,
            media_type=media_type or None,
            official_source=True,
        )
        return RetrievedDocument(content=document, evidence=evidence)
