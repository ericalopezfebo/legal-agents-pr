# Tratamiento jurisprudencial

El modelo distingue `CITED`, `FOLLOWED`, `APPLIED`, `DISTINGUISHED`, `CRITICIZED`, `LIMITED`,
`OVERRULED` y `UNKNOWN_UNVERIFIED`.

Una cita, mención o coincidencia lingüística detectada automáticamente permanece como
`UNKNOWN_UNVERIFIED`. La aplicación no puede confirmar tratamiento con base
`AUTOMATED_CANDIDATE`. Para confirmar otro estado se requiere evidencia textual vinculada a una
fuente oficial y una base `HUMAN_REVIEWED_OFFICIAL_SOURCE` u `OFFICIAL_COURT_METADATA`.

El control de calidad exige tratamiento confirmado para las autoridades judiciales que ya hayan
sido verificadas como fuentes. La ausencia de esa comprobación mantiene el producto en `DRAFT`.
Esto evita concluir que una decisión fue seguida, limitada o revocada únicamente porque otra la
cita.
