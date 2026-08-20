# Architecture

`AgentDefinition` describes legal scope and operating policy. `AgentLoader` prepends `agents/_shared/system.md` to every specialist prompt so jurisdiction, factual discipline, source hierarchy, deadline analysis, privacy and attorney-review safeguards remain uniform without duplicating them in twelve files. Specialist `system.md` files contain only domain-specific instructions.

`AgentRuntime` combines the loaded definition with an interchangeable `LLMProvider` and resolves its `source_refs` through `SourceCatalogLoader`. Only source metadata and cautions enter the prompt; this does not verify the underlying text. Tools and skills are registries, not dependencies of the core. `DomainRouter` uses deterministic rules before any optional model classification. `HandoffManager` enforces depth, count and cycle limits. `LegalQualityGate` evaluates the structured result after generation.

The initial release deliberately avoids general-purpose agent frameworks. This keeps provider translation at the edge and makes the execution path inspectable.
