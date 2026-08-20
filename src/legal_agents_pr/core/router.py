from __future__ import annotations

import re

from pydantic import BaseModel, Field

from .loader import AgentLoader


class RouteResult(BaseModel):
    primary_agent: str
    secondary_agents: list[str] = Field(default_factory=list)
    confidence: float
    reason: str
    method: str = "deterministic"
    requires_confirmation: bool = False


ROUTING_RULES: dict[str, tuple[str, ...]] = {
    "administrative-law": ("agencia", "administrativ", "revisión judicial", "agotamiento", "lpau"),
    "labor-employment-law": ("empleo", "despido", "discriminación", "represalia", "salario", "sindicato"),
    "constitutional-law": ("constitucional", "debido proceso", "registro", "incautación", "libertad de expresión"),
    "notarial-law": ("notarial", "escritura pública", "notario", "protocolo", "comparecencia"),
    "civil-law": ("daños", "obligación", "propiedad", "prescripción", "responsabilidad civil"),
    "civil-procedure": ("demanda", "emplazamiento", "descubrimiento", "sentencia sumaria", "regla 10.2"),
    "business-organizations": ("corporación", "accionista", "junta de directores", "deber fiduciario", "acción derivativa", "compañía de responsabilidad limitada", "fusión"),
    "contracts": ("contrato", "cláusula", "incumplimiento", "indemnización", "no competencia"),
    "evidence": ("evidencia", "prueba", "hearsay", "referencia", "autenticación", "privilegio"),
    "appellate-law": ("apelación", "certiorari", "reconsideración", "error", "estándar de revisión"),
    "professional-responsibility": ("ética", "conducta profesional", "conflicto de intereses", "confidencialidad", "competencia tecnológica"),
    "criminal-law": ("delito", "penal", "acusación", "denuncia", "sentencia criminal", "ministerio público"),
}


class DomainRouter:
    def __init__(self, loader: AgentLoader | None = None) -> None:
        self.loader = loader or AgentLoader()

    def route(self, query: str) -> RouteResult:
        normalized = re.sub(r"\s+", " ", query.lower())
        scores = {agent: sum(term in normalized for term in terms) for agent, terms in ROUTING_RULES.items()}
        ranked = sorted(scores, key=lambda agent: (-scores[agent], agent))
        primary = ranked[0]
        top = scores[primary]
        if top == 0:
            return RouteResult(
                primary_agent="civil-law", confidence=0.25,
                reason="No deterministic rule was decisive; general civil-law fallback.",
                requires_confirmation=True,
            )
        secondary = [agent for agent in ranked[1:] if scores[agent] > 0][:2]
        confidence = min(0.98, 0.55 + 0.14 * top)
        return RouteResult(
            primary_agent=primary,
            secondary_agents=secondary,
            confidence=confidence,
            reason=f"Matched {top} domain indicator(s) for {primary}.",
        )
