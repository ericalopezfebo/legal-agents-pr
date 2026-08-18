from datetime import date

from legal_agents_pr.schemas.judicial import JudicialDocumentType
from legal_agents_pr.sources.parsers import TsprDecisionIndexParser, extract_tspr_html

INDEX_URL = "https://poderjudicial.pr/tribunal-supremo/decisiones-2026/"


def test_parses_opinion_judgment_and_resolution():
    text = """
2026 TSPR 73
Núm. | CC-2025-0366
Partes | Liquids and Water Transport v. AAA
Ponente | Hon. Camille Rivera Pérez
Fecha | 6 de julio de 2026
Materia | Derecho Administrativo – Revisión de tarifas.
2026 TSPR 71
Núm. | CC-2023-0270
Partes | El Pueblo v. Hernández Díaz
Ponente | Sentencia con Opiniones de Conformidad
Fecha | 30 de junio de 2026
Materia | Sentencia con Opiniones de Conformidad.
2026 TSPR 70
Núm. | AB-2025-0278
Partes | In re: Félix A. Santiago Miranda
Ponente | Resolución del Tribunal
Fecha | 26 de junio de 2026
Materia | Suspensión inmediata del ejercicio de la notaría.
"""

    result = TsprDecisionIndexParser().parse(text, index_url=INDEX_URL)

    assert not result.issues
    assert [record.document_type for record in result.records] == [
        JudicialDocumentType.OPINION,
        JudicialDocumentType.JUDGMENT,
        JudicialDocumentType.RESOLUTION,
    ]
    assert result.records[0].decision_date == date(2026, 7, 6)
    assert all(record.metadata_only for record in result.records)


def test_incomplete_record_is_reported_not_invented():
    result = TsprDecisionIndexParser().parse(
        "2026 TSPR 99\nNúm. | CC-2026-0001\nPartes | A v. B",
        index_url=INDEX_URL,
    )

    assert not result.records
    assert result.issues[0].citation == "2026 TSPR 99"
    assert "Missing TSPR fields" in result.issues[0].reason


def test_no_records_is_reported():
    result = TsprDecisionIndexParser().parse("Maintenance", index_url=INDEX_URL)
    assert result.issues[0].citation is None


def test_extracts_text_and_resolves_tspr_document_link():
    html = """
    <html><body>
      <script>2026 TSPR 999</script>
      <h3><a href="/docs/2026-tspr-73.pdf">2026 TSPR 73</a></h3>
      <table>
        <tr><td>Núm.</td><td>CC-2025-0366</td></tr>
        <tr><td>Partes</td><td>A v. B</td></tr>
        <tr><td>Ponente</td><td>Hon. Camille Rivera Pérez</td></tr>
        <tr><td>Fecha</td><td>6 de julio de 2026</td></tr>
        <tr><td>Materia</td><td>Derecho Administrativo.</td></tr>
      </table>
    </body></html>
    """

    text, links = extract_tspr_html(html, INDEX_URL)
    result = TsprDecisionIndexParser().parse(
        text,
        index_url=INDEX_URL,
        document_urls=links,
    )

    assert "2026 TSPR 999" not in text
    assert links["2026 TSPR 73"] == "https://poderjudicial.pr/docs/2026-tspr-73.pdf"
    assert result.records[0].document_url == links["2026 TSPR 73"]
