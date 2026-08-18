from __future__ import annotations

import httpx

from .http import AllowlistedHttpSourceConnector

PUERTO_RICO_OFFICIAL_PUBLISHERS = {
    "poderjudicial.pr": "Poder Judicial de Puerto Rico",
    "www.poderjudicial.pr": "Poder Judicial de Puerto Rico",
    "estado.pr.gov": "Departamento de Estado de Puerto Rico",
    "www.estado.pr.gov": "Departamento de Estado de Puerto Rico",
    "sutra.oslpr.org": "Oficina de Servicios Legislativos de Puerto Rico",
    "ogp.pr.gov": "Oficina de Gerencia y Presupuesto de Puerto Rico",
    "www.ogp.pr.gov": "Oficina de Gerencia y Presupuesto de Puerto Rico",
}


class PuertoRicoOfficialConnector(AllowlistedHttpSourceConnector):
    def __init__(
        self,
        *,
        client: httpx.AsyncClient | None = None,
        max_bytes: int = 15 * 1024 * 1024,
    ) -> None:
        super().__init__(PUERTO_RICO_OFFICIAL_PUBLISHERS, client=client, max_bytes=max_bytes)
