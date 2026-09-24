# Datos locales

La carpeta `data/` contiene datos locales que deben permanecer fuera de GitHub público. El archivo `Abuso y violencia 2025.xlsx` se mantiene únicamente en el entorno local, en su ubicación original.

## Relación con la aplicación

`main.py` no referencia esta carpeta ni ese Excel. Por tanto, el archivo no se utiliza automáticamente en la ejecución actual y no es necesario para iniciar la interfaz. El código tampoco implementa entrenamiento ni permite confirmar un uso previo de ese archivo para entrenar modelos.

Para analizar datos o generar predicciones, el usuario debe cargar manualmente una fuente compatible en Streamlit. Los campos de entrada son `Edad`, `Género`, `Jornada`, `Localidad` y `NivelAcad`. La aplicación genera `Clasificacion Edad` a partir de `Edad`. El [README principal](../README.md) documenta el esquema y el flujo observado.

## Manejo y publicación

La solución trabaja con información desidentificada. La eliminación de identificadores directos no elimina el riesgo de reidentificación asociado a variables sensibles, demográficas o territoriales. Los datos reales no deben publicarse en GitHub y deben gestionarse bajo controles institucionales.

La base utilizada para análisis y/o entrenamiento no se distribuye mediante el repositorio público. Cualquier publicación de bases reales requiere validación institucional previa. Pueden documentarse estructuras o esquemas, pero no registros reales ni ejemplos extraídos de la base.

Las reglas de `.gitignore` excluyen `data/*.xlsx`, `data/*.xls`, `data/*.csv` y `data/*.parquet`, y permiten conservar este README. Estas reglas no excluyen archivos ya rastreados por Git. En la revisión documental se detectó `Abuso y violencia 2025.xlsx` en el índice: debe resolverse su inclusión antes de publicar, sin asumir que `.gitignore` lo retira automáticamente. Esta revisión no modificó el archivo ni su estado en Git.
