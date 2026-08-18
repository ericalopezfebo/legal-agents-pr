# Tools and skills

La herramienta tipada `official-source-identifier` y su comando de CLI se documentan en
[official-source-tool.md](official-source-tool.md). Confirma únicamente identidad textual en una
fuente oficial permitida; no sustituye el análisis jurídico ni la revisión profesional.

A tool is executable capability with typed input and output. A skill is a reusable legal procedure. Agents reference both by neutral identifiers. Future adapters may connect `legal-skills-pr`, `pr-law-data`, `mcp-puerto-rico-sentencias`, VELUM, native Python functions, HTTP APIs or MCP servers without making any one integration mandatory.

## Skills del repositorio

Los skills viven en `src/legal_agents_pr/skills/library/<skill>/SKILL.md`. Cada archivo contiene
frontmatter mínimo (`name` y `description`) e instrucciones procesales en español jurídico. El
runtime valida las referencias del agente y carga únicamente los skills asignados a ese agente.

La biblioteca inicial incluye investigación y citas; prescripción y términos; demandas,
contestaciones, mociones, desestimación y sentencia sumaria; práctica apelativa y preparación para
presentación; revisión y redacción contractual; instrumentos notariales; conflictos y
confidencialidad.

Los módulos especializados adicionales cubren revisión administrativa, reclamaciones
constitucionales, admisibilidad de evidencia, reclamaciones laborales, análisis de imputaciones
penales y exposición a pena.

La tercera colección añade cronologías trazables, análisis estructurado de textos normativos,
comprobación del apoyo real de cada proposición y control adversativo antes de entrega. Su diseño
surge de una [revisión documentada de colecciones externas](external-skill-review.md), sin copiar
texto o reglas sustantivas de terceros.

Un skill describe una capacidad concreta. Un workflow coordina varios skills y conserva el estado
del asunto. Añadir instrucciones a un skill no convierte sus resultados en autoridad verificada ni
permite saltar el Quality Gate.
