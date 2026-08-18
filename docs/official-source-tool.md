# Herramienta de verificación oficial

La herramienta `official-source-identifier` acepta una URL oficial permitida, un identificador TSPR,
DPR o de ley numerada y un máximo de coincidencias. Devuelve `SourceIdentifierVerification` con la
evidencia de recuperación, el estado de la cita y los localizadores disponibles.

También está disponible desde la CLI:

```bash
legal-agents-pr verify-source \
  "https://poderjudicial.pr/documento.pdf" \
  "2024 TSPR 7"
```

La URL debe pasar las reglas HTTPS, host, puerto, redirección, tipo de contenido y tamaño del
conector oficial. La herramienta no acepta una fuente secundaria como sustituto silencioso, no hace
OCR automáticamente y no determina vigencia, efecto jurídico ni tratamiento posterior.
