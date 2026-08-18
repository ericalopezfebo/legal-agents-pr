# Source and citation policy

Preferred order: constitutions; official legislation; official regulations; court rules; Puerto Rico Supreme Court; intermediate appellate decisions; applicable federal courts; secondary sources. Classification depends on both source type and actual verification. Unknown or unchecked material remains `UNVERIFIED_SOURCE`.

Never invent cases, statutes, sections, docket numbers, quotations or URLs. A citation graph proves citation, not positive or negative treatment.

## Versioned local references

`src/legal_agents_pr/sources/registry.yaml` records metadata and SHA-256 provenance for selected user-supplied official compilations. The catalog does not bundle the PDF files and does not certify that a compilation remains current. An agent must verify the official, currently effective text and any special or transitional law before citing or relying on it.

Two supplied copies of Act 38-2017 had the same SHA-256 digest, so the catalog represents them once. An absent `official_url` means the official location still needs independent verification; it must never be fabricated.

## Verification evidence

The catalog is discovery metadata, not verification evidence. See [source verification contract](source-verification-contract.md) for the retrieval, pinpoint, textual-support, legal-effect and currency requirements that must be satisfied before an authority can be marked `VERIFIED`.
