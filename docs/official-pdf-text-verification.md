# Verificación textual de PDF oficiales

`PdfTextExtractor` procesa en memoria los bytes recuperados por un conector aprobado y conserva la
separación por página. La búsqueda de texto produce localizadores de página y líneas para sustentar
una comparación textual reproducible.

El componente no decide vigencia, efecto jurídico, valor precedencial ni tratamiento posterior. Una
coincidencia textual tampoco demuestra que el pasaje sostenga una proposición jurídica. Esas
determinaciones permanecen separadas en el contrato de evidencia y requieren revisión profesional.

## Salvaguardas

- Rechaza PDF vacíos, cifrados, inválidos o que excedan los límites configurados.
- Limita páginas, caracteres extraídos y coincidencias devueltas.
- No ejecuta OCR automáticamente.
- Si no existe capa de texto, devuelve `ocr_required=true` y no permite inferir verificación.
- Conserva páginas y líneas numeradas desde uno para crear puntos de referencia auditables.
- Normaliza espacios únicamente para localizar texto; no corrige ni completa el contenido jurídico.

El hash y URL del documento proceden de `RetrievalEvidence`. Para crear `VerificationEvidence`, la
aplicación debe vincular el localizador y la cita textual con esa evidencia de recuperación. La
vigencia y el efecto jurídico continúan inicialmente como `UNKNOWN` y `NOT_CHECKED`.
