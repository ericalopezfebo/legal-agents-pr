# Changelog

All notable changes will be documented here. This project follows semantic versioning.

## 0.2.0 - Unreleased

- Add six lawyer-craft agents that separate advocacy method from substantive legal authority: `lawyer-reasoning`, `legal-strategy`, `discovery-strategy`, `deposition-advocacy`, `witness-examination`, and `trial-advocacy`.
- Add `docs/lawyer-craft-layer.md` documenting the substantive-law versus lawyer-craft architecture and methodology-source policy.
- Add dedicated workflows for theory of the case, proof mapping, discovery sequencing, depositions, direct/cross examination, impeachment, trial/hearing architecture and record preservation.
- Expand `labor-employment-law` with intake triage, chronology, elements/burdens matrices, evidence-gap analysis, damages/remedies, public-employment and collective-labor workflows, and current-law verification safeguards.
- Strengthen the shared legal-agent policy with proactive issue spotting, granular task separation and deterministic tools for reproducible work when available.
- Treat trial-practice books, CLE materials, advocacy manuals, public practice guides and user-supplied litigation materials as methodology discovery sources only, never as legal authority or distributable doctrinal content.

- Expand the bankruptcy agent with twelve original operational skills for intake, chapter selection, estate property, claims, stay relief, dischargeability, contracts, avoidance, Chapter 11, adversary proceedings, deadlines and financing.

- Add four federal-practice agents and seventeen original skills covering civil and criminal litigation, evidence, bankruptcy, First Circuit appeals and federal-court ethics.

- Add a Puerto Rico privacy and cybersecurity specialist and twenty cross-domain operational skills for privacy, employment, contracts, litigation, government contracting and DMCA analysis.

- Expand motion drafting and add privacy-safe pretrial-report and document-sanitization workflows.

- Expand the intellectual-property specialist with three original copyright research and transaction workflows.

- Add an intellectual-property specialist and three original trademark workflows backed by a copyright-safe research gate.

- Strengthen interpretive analysis and employment-law lifecycle coverage while preserving source confidentiality.

- Add a business-organizations specialist and expand special-contract issue spotting with source-confidentiality safeguards.

- Expand administrative, contracts, civil-procedure, constitutional and evidence issue-spotting through an internal, non-citable coverage taxonomy.
- Add confidentiality safeguards and regression tests for internal doctrine coverage.
- Add an auditable legal-reasoning protocol covering operative facts, elements, burdens, counteranalysis, procedural fit and remedy.

- Add a shared legal operating policy automatically injected into every specialist agent.
- Strengthen administrative-law and civil-procedure issue spotting and source-date safeguards.
- Add legal-research and filing-readiness procedures to the civil-procedure agent.
- Keep the documented specialist-agent count synchronized with the available definitions.
- Add source retrieval, pinpoint, legal-effect and currency evidence contracts.
- Require matching evidence for verified authorities.
- Prevent model-provider output from self-certifying citation verification.
- Block current-law validation unless effective authority was checked through the requested date.
- Add allowlisted, size-limited retrieval for priority Puerto Rico official-source domains.
- Add conservative TSPR annual-index parsing and judicial-document classification.

## 0.1.0 - 2026-08-18

- Initial provider-agnostic runtime.
- Eleven Puerto Rico specialist agent definitions.
- Deterministic router and bounded handoffs.
- Source, citation and legal quality policies.
- Versioned source catalog for selected Puerto Rico statutes and court rules.
- Professional-responsibility agent based on Puerto Rico's 2025 rules.
- Runtime source-context injection and source-inspection CLI commands.
- Optional provider adapters, CLI, tests and documentation.
