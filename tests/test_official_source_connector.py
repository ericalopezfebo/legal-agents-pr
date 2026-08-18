import hashlib

import httpx
import pytest

from legal_agents_pr.core.exceptions import SourceRetrievalError
from legal_agents_pr.sources.connectors import PuertoRicoOfficialConnector


@pytest.mark.asyncio
async def test_fetches_and_hashes_official_document():
    content = b"official legal document"

    async def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, content=content, headers={"content-type": "application/pdf"})

    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as client:
        result = await PuertoRicoOfficialConnector(client=client).fetch(
            "https://poderjudicial.pr/document.pdf"
        )

    assert result.content == content
    assert result.evidence.document_sha256 == hashlib.sha256(content).hexdigest()
    assert result.evidence.official_source
    assert result.evidence.publisher == "Poder Judicial de Puerto Rico"


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "url",
    [
        "http://poderjudicial.pr/document.pdf",
        "https://example.com/document.pdf",
        "https://user:password@poderjudicial.pr/document.pdf",
        "https://poderjudicial.pr:8443/document.pdf",
    ],
)
async def test_rejects_non_allowlisted_or_unsafe_url(url: str):
    with pytest.raises(SourceRetrievalError):
        await PuertoRicoOfficialConnector().fetch(url)


@pytest.mark.asyncio
async def test_rejects_redirect_without_implicit_trust():
    async def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(302, headers={"location": "https://example.com/document.pdf"})

    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as client:
        with pytest.raises(SourceRetrievalError, match="redirects require explicit"):
            await PuertoRicoOfficialConnector(client=client).fetch(
                "https://www.estado.pr.gov/document.pdf"
            )


@pytest.mark.asyncio
async def test_rejects_document_over_size_limit():
    async def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, content=b"12345", headers={"content-type": "text/plain"})

    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as client:
        with pytest.raises(SourceRetrievalError, match="size limit"):
            await PuertoRicoOfficialConnector(client=client, max_bytes=4).fetch(
                "https://sutra.oslpr.org/document.txt"
            )


@pytest.mark.asyncio
async def test_rejects_unsupported_content_type():
    async def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, content=b"archive", headers={"content-type": "application/zip"})

    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as client:
        with pytest.raises(SourceRetrievalError, match="content type"):
            await PuertoRicoOfficialConnector(client=client).fetch(
                "https://www.ogp.pr.gov/archive.zip"
            )
