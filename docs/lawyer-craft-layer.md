# Lawyer Craft Layer

`legal-agents-pr` separates two different kinds of legal intelligence.

## 1. Substantive law layer — what law governs

These agents answer questions such as:

- What statute, regulation, rule or precedent controls?
- What are the elements, definitions, exceptions and burdens?
- What forum, term, standard of review or remedy applies?
- What authority is binding, persuasive, current or still `UNVERIFIED`?

Examples: `administrative-law`, `labor-employment-law`, `civil-procedure`, `evidence`, `contracts`, `constitutional-law` and the federal-practice agents.

This layer must be grounded in verified legal sources. Treatises, blogs, advocacy books and training manuals never become substantive authority merely because an agent has learned a useful technique from them.

## 2. Lawyer craft layer — how to think and act on the case

These agents consume the substantive output and the record, then decide how to investigate, test, organize and present the case:

- `lawyer-reasoning` — issue framing, element/fact mapping, alternative hypotheses, burdens, proof gaps, counteranalysis and decision logic.
- `legal-strategy` — theory of the case, chronology, witness/document maps, leverage, risk, pre-mortem and litigation sequencing.
- `discovery-strategy` — information-gap analysis, discovery objectives, sequencing, preservation, requests, admissions, subpoenas and follow-up.
- `deposition-advocacy` — deposition goals, witness/document preparation, topic architecture, questioning, lock-ins, exhibits, evasions and transcript exploitation.
- `witness-examination` — direct, cross, impeachment, contradiction analysis, witness preparation and record preservation.
- `trial-advocacy` — hearing/trial architecture, proof order, openings, witness/exhibit sequence, objections, preservation and closing.

## Operating rule

The substantive layer determines **what must be proved and under what legal rule**. The craft layer determines **how to investigate, prove, attack, preserve and present it**.

Neither layer may silently perform the other's job. A craft agent may flag that a rule must be researched, but it must hand the legal question to the proper substantive agent. A substantive agent may identify an evidentiary or strategic problem, but it should hand the tactical design to the appropriate craft agent.

## Methodology sources

Trial-practice books, CLE materials, advocacy manuals, public training guides and user-supplied litigation materials may be used as **methodology discovery sources**. They may inform original workflows, issue-spotting prompts, checklists and quality controls. They must not be treated as legal authority, cited for propositions of law, copied, or reproduced through substantial paraphrase.

When methodology conflicts with governing procedural, evidentiary, ethical or substantive law, the verified legal source controls.

## Example workflow

```text
User record
   ↓
labor-employment-law
   ↓
verified elements / defenses / forum / remedies
   ↓
lawyer-reasoning
   ↓
legal-strategy
   ├── discovery-strategy
   │      └── deposition-advocacy
   └── witness-examination
          └── trial-advocacy
   ↓
attorney review
```

This architecture is intended to make the system behave less like one general-purpose legal chatbot and more like a coordinated legal team with distinct research and advocacy roles.
