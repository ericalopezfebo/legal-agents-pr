# Source verification contract

La extracción de texto de PDF oficiales se documenta en
[official-pdf-text-verification.md](official-pdf-text-verification.md). Una coincidencia textual crea
un punto de partida auditable, pero no determina por sí sola vigencia, efecto jurídico ni valor
precedencial.

La verificación exacta de citas TSPR, DPR y leyes numeradas se documenta en
[source-identifier-verification.md](source-identifier-verification.md).

The framework separates four questions that must not be collapsed into one status:

1. **Identity:** what document was retrieved, from which URL and publisher?
2. **Textual support:** does an exact passage at a reproducible pinpoint support the proposition?
3. **Legal effect:** is the material effective, amended, repealed, superseded, proposed or unknown?
4. **Currency:** through what date were later enactments, rules or decisions checked?

`RetrievalEvidence` records the URL, timezone-aware retrieval timestamp, SHA-256 digest, publisher and whether the location is official. `SourceLocator` requires at least one section, article, page, paragraph or line pinpoint. `VerificationEvidence` records the quotation, matching result, legal-effect status, currency status and verification method.

An `Authority` may be `VERIFIED` only when it has a supported proposition and matching retrieval evidence. Text verification does not establish current law. The `current_law` quality check passes only when every verified authority is effective and checked through the requested as-of date.

## Trust boundary

Language-model output is never a trusted verification channel. `AgentRuntime` downgrades every provider-supplied authority to `UNVERIFIED` and removes provider-supplied evidence before schema validation. A future source connector must construct evidence outside model output after retrieving and hashing the actual document.

## Official source is not current-law status

`official_source=true` identifies the provenance of the retrieved document. It does not prove that a compilation includes later amendments, that a regulation is effective, or that a decision has not been limited. Those questions belong to `legal_effect`, `currency_status` and `checked_through`.

## Minimum connector behavior

A production source connector must:

- retrieve from an allowlisted source;
- preserve the final URL and retrieval time;
- hash the exact bytes used;
- extract a reproducible pinpoint and quotation;
- compare the quotation to the retrieved content;
- classify legal effect conservatively;
- state the date through which later authority was checked;
- return `UNKNOWN` or `NOT_CHECKED` rather than infer missing facts.

## Puerto Rico retrieval foundation

`PuertoRicoOfficialConnector` currently allowlists the Poder Judicial, Departamento de Estado, SUTRA and OGP hosts. It requires HTTPS, rejects credentials and nonstandard ports, refuses implicit redirects, enforces content-type and size limits, hashes the retrieved bytes and records timezone-aware retrieval evidence. Retrieval establishes document identity only; parsing, pinpoint matching, legal effect and currency remain separate steps.

## TSPR index metadata

`TsprDecisionIndexParser` extracts citation, docket number, parties, author, date, subject, document classification and document URL from annual Puerto Rico Supreme Court index material. Incomplete entries produce parse issues instead of fabricated fields. Every record is marked `metadata_only=true`: an index entry does not prove the content, precedential force or later treatment of the linked judicial document.
