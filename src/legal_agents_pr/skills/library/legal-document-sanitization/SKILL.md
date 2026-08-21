---
name: legal-document-sanitization
description: Crear una copia de trabajo desidentificada de escritos jurídicos antes de analizarlos, convertirlos en ejemplos o extraer patrones de tono y formato. Usar con mociones, informes previos a juicio, cartas, órdenes y expedientes que contengan datos de personas o asuntos reales.
---
# Sanitización de documentos jurídicos

1. Trabajar sobre una copia y conservar el original fuera de cualquier carpeta distribuible.
2. Sustituir nombres de partes, testigos, abogados, jueces, empleados y terceros por roles consistentes como `[PARTE DEMANDANTE]` o `[TESTIGO 1]`.
3. Sustituir direcciones, teléfonos, correos, identificadores, números de caso, cuentas, licencias, placas y fechas individualizantes por marcadores tipados.
4. Generalizar hechos que permitan reidentificación cuando no sean necesarios para estudiar estructura; conservar solo la función retórica del pasaje.
5. Revisar tablas, encabezados, pies, notas, campos, cuadros de texto, hipervínculos, comentarios, cambios controlados, propiedades y contenido oculto.
6. Eliminar firmas manuscritas o digitales, iniciales, sellos, códigos de barras, imágenes y metadatos que identifiquen personas o expedientes.
7. Mantener un mapa temporal de sustituciones solo durante la tarea y destruirlo al terminar. No incorporarlo al repositorio ni a la skill.
8. Buscar residuos mediante patrones y revisión visual. Tratar cualquier coincidencia dudosa como un bloqueo.
9. Extraer únicamente rasgos abstractos: jerarquía, orden de secciones, alineación, espaciado, longitud, numeración, tono y función de cada bloque.
10. Aplicar una prueba de reidentificación: si un lector razonable puede reconocer el asunto, reducir o eliminar más contenido.
11. Aplicar una prueba de sustitución: no distribuir una reconstrucción que permita recuperar sustancialmente el documento de referencia.
12. Informar solo el resultado del control y los patrones abstractos; nunca revelar qué documento, persona o expediente originó el patrón.
