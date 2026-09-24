# Guía de contribución

Las contribuciones deben describir su propósito y facilitar la revisión técnica e institucional.

1. Hacer un fork del repositorio.
2. Crear una rama para el cambio con un nombre descriptivo.
3. Realizar las modificaciones manteniendo el alcance del cambio claramente delimitado.
4. Probar la aplicación con `streamlit run main.py` en un entorno compatible y con una fuente de datos autorizada. Consultar las limitaciones de instalación documentadas en el README.
5. Crear un Pull Request hacia el repositorio de origen.
6. Describir claramente el cambio realizado, su justificación, las pruebas ejecutadas y cualquier limitación pendiente.

## Información que no debe incluirse

No incluir en Pull Requests:

- Datos personales.
- Información sensible.
- Archivos de datos institucionales no autorizados.
- Credenciales, secretos o tokens.
- Archivos `.env`.

Estas restricciones también aplican a descripciones, capturas, resultados de pruebas y archivos adjuntos. Documentar esquemas sin copiar registros reales. Las reglas de `.gitignore` no protegen archivos que ya estén rastreados: revisar el contenido del cambio antes de enviarlo.

## Cambios en modelos predictivos

Cualquier cambio sobre modelos predictivos debe documentar:

- Motivo del cambio.
- Datos o metodología utilizados, incluyendo procedencia y autorización sin adjuntar información restringida.
- Impacto esperado sobre las salidas y la compatibilidad de la solución.
- Validaciones realizadas, métricas disponibles y limitaciones identificadas.

Mantener un lenguaje prudente: los resultados apoyan el análisis y no sustituyen la valoración profesional o institucional.
