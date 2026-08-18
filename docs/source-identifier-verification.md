# Verificación de identificadores jurídicos

`OfficialPdfSourceVerifier` enlaza la recuperación oficial, la extracción de PDF y la localización
exacta de una cita. Actualmente reconoce identificadores TSPR, DPR y leyes numeradas. La
normalización solo uniforma abreviaturas, espacios y ceros iniciales permitidos por esos formatos.

Los resultados distinguen tres estados:

- `VERIFIED_SOURCE_IDENTIFIER`: el identificador normalizado aparece en el PDF oficial recuperado y
  existen localizadores de página y líneas.
- `SOURCE_FOUND_IDENTIFIER_UNCONFIRMED`: se recuperó el PDF, pero no apareció el identificador
  exacto.
- `OCR_REQUIRED`: el PDF no contiene una capa textual utilizable.

El primer estado confirma identidad textual en unos bytes y URL determinados. No confirma que el
documento apoye una proposición, esté vigente, sea vinculante, tenga valor precedencial o conserve
el mismo tratamiento jurídico. Por ello, la evidencia creada conserva `legal_effect=UNKNOWN` y
`currency_status=NOT_CHECKED`.
