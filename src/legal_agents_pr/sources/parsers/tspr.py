from __future__ import annotations

import re
from datetime import date
from html.parser import HTMLParser
from urllib.parse import urljoin

from legal_agents_pr.schemas.judicial import (
    JudicialDocumentType,
    TsprDecisionRecord,
    TsprParseIssue,
    TsprParseResult,
)

MONTHS = {
    "enero": 1,
    "febrero": 2,
    "marzo": 3,
    "abril": 4,
    "mayo": 5,
    "junio": 6,
    "julio": 7,
    "agosto": 8,
    "septiembre": 9,
    "octubre": 10,
    "noviembre": 11,
    "diciembre": 12,
}
TSPR_PATTERN = re.compile(r"(?m)^\s*(\d{4}\s+TSPR\s+\d+)\s*$")
FIELD_PATTERN = re.compile(r"(?i)(Núm\.|Partes|Ponente|Fecha|Materia)\s*\|?\s*")


class _IndexHtmlExtractor(HTMLParser):
    def __init__(self, base_url: str) -> None:
        super().__init__(convert_charrefs=True)
        self.base_url = base_url
        self.text_parts: list[str] = []
        self.links: dict[str, str] = {}
        self._href: str | None = None
        self._anchor_parts: list[str] = []
        self._ignored_depth = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag in {"script", "style", "noscript"}:
            self._ignored_depth += 1
            return
        if self._ignored_depth:
            return
        if tag == "a":
            self._href = dict(attrs).get("href")
            self._anchor_parts = []
        if tag in {"br", "div", "h1", "h2", "h3", "li", "p", "tr", "td"}:
            self.text_parts.append("\n")

    def handle_endtag(self, tag: str) -> None:
        if tag in {"script", "style", "noscript"} and self._ignored_depth:
            self._ignored_depth -= 1
            return
        if self._ignored_depth:
            return
        if tag == "a" and self._href:
            anchor_text = " ".join("".join(self._anchor_parts).split())
            match = re.search(r"\b(\d{4}\s+TSPR\s+\d+)\b", anchor_text)
            if match:
                self.links[match.group(1)] = urljoin(self.base_url, self._href)
            self._href = None
            self._anchor_parts = []
        if tag in {"div", "h1", "h2", "h3", "li", "p", "tr", "table"}:
            self.text_parts.append("\n")

    def handle_data(self, data: str) -> None:
        if self._ignored_depth:
            return
        self.text_parts.append(data)
        if self._href is not None:
            self._anchor_parts.append(data)


def extract_tspr_html(html: str, base_url: str) -> tuple[str, dict[str, str]]:
    extractor = _IndexHtmlExtractor(base_url)
    extractor.feed(html)
    lines = [" ".join(line.split()) for line in "".join(extractor.text_parts).splitlines()]
    return "\n".join(line for line in lines if line), extractor.links


class TsprDecisionIndexParser:
    def parse(
        self,
        text: str,
        *,
        index_url: str,
        document_urls: dict[str, str] | None = None,
    ) -> TsprParseResult:
        links = document_urls or {}
        matches = list(TSPR_PATTERN.finditer(text))
        records: list[TsprDecisionRecord] = []
        issues: list[TsprParseIssue] = []
        for position, match in enumerate(matches):
            citation = " ".join(match.group(1).split())
            end = matches[position + 1].start() if position + 1 < len(matches) else len(text)
            block = text[match.end():end]
            try:
                fields = self._fields(block)
                record = TsprDecisionRecord(
                    citation=citation,
                    docket_number=fields["núm."],
                    parties=fields["partes"],
                    author=fields["ponente"],
                    decision_date=self._date(fields["fecha"]),
                    subject=fields["materia"],
                    document_type=self._document_type(fields["ponente"]),
                    index_url=index_url,
                    document_url=links.get(citation),
                )
                records.append(record)
            except (KeyError, ValueError) as exc:
                issues.append(TsprParseIssue(citation=citation, reason=str(exc)))
        if not matches:
            issues.append(TsprParseIssue(reason="No TSPR records were found in the index text"))
        return TsprParseResult(records=records, issues=issues)

    @staticmethod
    def _fields(block: str) -> dict[str, str]:
        markers = list(FIELD_PATTERN.finditer(block))
        fields: dict[str, str] = {}
        for index, marker in enumerate(markers):
            end = markers[index + 1].start() if index + 1 < len(markers) else len(block)
            value = " ".join(block[marker.end():end].replace("|", " ").split())
            if value:
                fields[marker.group(1).lower()] = value
        required = {"núm.", "partes", "ponente", "fecha", "materia"}
        missing = sorted(required - fields.keys())
        if missing:
            raise ValueError(f"Missing TSPR fields: {', '.join(missing)}")
        return fields

    @staticmethod
    def _date(value: str) -> date:
        match = re.fullmatch(r"(\d{1,2})\s+de\s+([A-Za-záéíóúñ]+)\s+de\s+(\d{4})", value)
        if not match:
            raise ValueError(f"Unsupported TSPR date: {value}")
        day, month_name, year = match.groups()
        month = MONTHS.get(month_name.lower())
        if month is None:
            raise ValueError(f"Unsupported TSPR month: {month_name}")
        return date(int(year), month, int(day))

    @staticmethod
    def _document_type(author: str) -> JudicialDocumentType:
        normalized = author.lower()
        if "resolución" in normalized:
            return JudicialDocumentType.RESOLUTION
        if "sentencia" in normalized:
            return JudicialDocumentType.JUDGMENT
        if normalized == "per curiam" or normalized.startswith("hon."):
            return JudicialDocumentType.OPINION
        return JudicialDocumentType.UNKNOWN
