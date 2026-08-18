# Revisión de colecciones externas de skills

Fecha de revisión: 18 de agosto de 2026.

Esta revisión identifica patrones y brechas funcionales. No incorpora texto, datasets, reglas de
otra jurisdicción ni supuestos benchmarks de mercado. Los skills añadidos a este repositorio fueron
redactados originalmente para su arquitectura, política de fuentes y contexto de Puerto Rico.

| Fuente | Licencia observada | Uso permitido en este proyecto |
|---|---|---|
| [zh-xx/legal-assistant-skills](https://github.com/zh-xx/legal-assistant-skills) | Apache-2.0 | Inventario y patrones generales; no se importó texto. |
| [LegalQuants/lq-skills](https://github.com/LegalQuants/lq-skills) | Apache-2.0 en el repositorio; algunos módulos además incluyen licencia propia | Detección de brechas como cronologías, comprobación de proposiciones y QC; implementación original. |
| [evolsb/claude-legal-skill](https://github.com/evolsb/claude-legal-skill) | MIT | Se evaluó su checklist contractual; no se importó ni se adoptaron benchmarks no verificados. |
| [HAQQ Legal AI Skills](https://www.haqq.ai/best-legal-skills) | Directorio de múltiples autores y procedencias | Solo descubrimiento. Cada skill requeriría verificar autor, fuente y licencia antes de reutilizarlo. |

## Decisiones

- Añadir `build-chronology`, `check-proposition-support`, `analyze-statute` y
  `adversarial-legal-qc` como capacidades generales y auditables.
- Exigir fuentes accesibles, pin cites, estados de incertidumbre y revisión profesional.
- No incorporar reglas sustantivas extranjeras, texto de terceros, datasets ni métricas de mercado.
- Evaluar futuras incorporaciones individualmente; la presencia en un directorio no acredita
  licencia, actualidad, autoridad jurídica ni idoneidad para Puerto Rico.
