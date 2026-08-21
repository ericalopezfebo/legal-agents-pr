---
name: bankruptcy-deadline-matrix
description: Construye términos auditables de quiebra sin producir fechas definitivas con datos incompletos.
---

# Matriz de términos de quiebra

## Workflow

1. Inventariar petition, order for relief, notices, meeting, bar dates, hearings y orders.
2. Para cada término, identificar regla, evento activador, método de cómputo y zona horaria.
3. Distinguir statutory, rules-based, court-set, claims-processing y jurisdictional questions.
4. Verificar service, electronic notice, extensions, tolling y emergency rules.
5. Mostrar fecha calculada, inputs, fuente, confianza y revisión humana requerida.
6. Bloquear calendaring definitivo si falta cualquier input material.

## Salida

Entrega un borrador estructurado, hechos faltantes, cálculos reproducibles, autoridades verificadas, incertidumbres y próximos pasos.

## Fuentes y gate

Verifica Title 11, Federal Rules of Bankruptcy Procedure, formularios oficiales, reglas locales, órdenes generales y órdenes del caso en versiones vigentes. Marca autoridades pendientes como `UNVERIFIED`, minimiza datos personales y exige revisión independiente por abogado.
