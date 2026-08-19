# Candidate authority index

The repository includes citation-only metadata extracted from user-supplied study materials.
It contains citations, visible years, authority categories and broad legal topics. It does not
contain the study materials, quotations, explanations, outlines, commentary, author analysis or
case summaries.

The focused August 2026 update processes only `Administrativo` and `Procedimiento Civil` rows from
the revised structured Markdown tables. The civil table supersedes the earlier OCR-derived list;
other subjects in the supplied materials are deliberately ignored. The index contains 1,175 unique
citation candidates, including 238 tagged `Administrativo` and 306 tagged `Procedimiento civil`.

Every record is a research lead and is permanently loaded as `UNVERIFIED`. Presence in the index
does not establish authenticity, accuracy, precedential value, legal effect, current validity or
support for any proposition. OCR may introduce errors. Before use, retrieve the operative document
from an approved official source, match the citation and pinpoint, determine legal effect and
currency, and complete attorney review.

Use the CLI to inspect a bounded set of candidates:

```bash
legal-agents-pr authorities --topic "daños" --limit 20
legal-agents-pr authorities --topic "administrativo" --limit 20
legal-agents-pr authorities --topic "procedimiento civil" --limit 20
legal-agents-pr authorities --citation "2024 TSPR"
```

The index is intentionally separate from the versioned source catalog. A citation candidate is not
a source copy and cannot satisfy the source-verification contract.

The structured lists improve transcription quality but do not establish that a reporter volume,
page, year, pin cite, title or doctrinal proposition is correct. Those questions remain for
official-source verification and attorney review.
