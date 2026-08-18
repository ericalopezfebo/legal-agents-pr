# Contributing

Contributions should be small, source-conscious and testable. Never include client information or facts from a nonpublic matter.

## Development

1. Create a focused branch.
2. Install `pip install -e ".[dev]"`.
3. Add or update tests.
4. Run `ruff check .`, `mypy src/legal_agents_pr`, `pytest`, and `python -m build`.
5. Explain authoritative sources, limitations and human-review requirements in the PR.

New agents require a complete `agent.yaml`, substantive `system.md`, routing consideration and tests. Do not copy legal text or third-party prompts without compatible licensing and attribution.

