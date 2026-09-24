# IDECA - Modelo predictivo de violencia escolar

## Descripción

Solución desarrollada en Python con una interfaz Streamlit para apoyar el análisis de situaciones de abuso y violencia escolar. Permite cargar un archivo, explorar distribuciones de variables y obtener estimaciones de categorías de tipo de violencia y tipo de agresor mediante dos modelos previamente almacenados. Sus resultados son orientativos y apoyan la identificación de patrones; no identifican personas ni establecen que ocurrirá un hecho.

La interfaz ofrece tres secciones: carga de datos, análisis descriptivo y resultados de predicción. Utiliza pandas y NumPy para el procesamiento, Altair para gráficos y joblib para cargar los artefactos predictivos.

## Arquitectura general

```text
Archivo cargado por el usuario (CSV / Excel)
    ↓
Lectura con pandas y clasificación de Edad con NumPy
    ↓
Selección de cinco variables → estado de sesión de Streamlit
    ├── Resumen descriptivo, conteos y gráficos Altair
    └── Dos modelos .pkl cargados con joblib → predict
            ↓
        Decodificación de las salidas con codificadores .pkl, si se cargan
            ↓
        Tabla y distribuciones de predicciones en Streamlit
```

`main.py` coordina este flujo. No define ni ajusta el preprocesamiento interno de los modelos; las importaciones de `OneHotEncoder`, `ColumnTransformer` y `Pipeline` no demuestran por sí solas qué transformaciones contienen los archivos serializados.

## Componentes del proyecto

| Componente | Función observada |
| --- | --- |
| `main.py` | Interfaz, carga de archivos, preparación de variables, análisis descriptivo e inferencia. |
| `requirements.txt` | Dependencias declaradas del entorno. |
| `.streamlit/` | Contiene `config.toml`, que configura un tema oscuro y los colores de la interfaz. |
| `images/` | Contiene `logo.png`, mostrado en la barra lateral. |
| `data/` | Carpeta de datos locales y documentación; no se lee automáticamente desde `main.py`. |
| `le_agresor.pkl` | Codificador de salida utilizado mediante `inverse_transform` para las categorías de tipo de agresor. |
| `le_violencia.pkl` | Codificador de salida utilizado mediante `inverse_transform` para las categorías de tipo de violencia. |
| `xgb_pipeline_over_agresor.pkl` | Artefacto cargado con joblib cuyo método `predict` estima la categoría de tipo de agresor. |
| `xgb_pipeline_over_violencia.pkl` | Artefacto cargado con joblib cuyo método `predict` estima la categoría de tipo de violencia. |

## Modelos

El código utiliza dos modelos preexistentes, uno por variable de salida. Sus nombres sugieren pipelines XGBoost y `requirements.txt` declara `xgboost`. Sin embargo, `main.py` no instancia estos estimadores ni expone su estructura interna: no permite confirmar su composición exacta, hiperparámetros o metodología de entrenamiento. Tampoco permite afirmar que el sufijo `over` corresponda a una técnica específica de balanceo.

El código identifica los archivos `le_*.pkl` como codificadores de etiquetas y los utiliza para decodificar las predicciones. Si falla la carga de cualquiera de ellos, desactiva ambos y conserva las salidas sin decodificar. Los dos archivos de modelos son necesarios para generar predicciones.

No se incluyen en el código inspeccionado procedimientos de entrenamiento, métricas de desempeño, probabilidades de salida ni validación de los modelos. Los artefactos no se deserializaron para elaborar esta documentación. Deben proceder de una fuente institucional confiable, ya que la carga de archivos serializados puede ejecutar código.

## Datos de entrada

El usuario debe proporcionar una fuente compatible mediante el cargador de la interfaz. Este admite extensiones `.xlsx`, `.xls` y `.csv`; la lectura se realiza con `pandas.read_excel` o `pandas.read_csv`.

Los encabezados requeridos, con su escritura exacta, son:

| Campo de entrada | Uso en el código |
| --- | --- |
| `Edad` | Valor numérico empleado para generar `Clasificacion Edad`. |
| `Género` | Variable seleccionada para análisis y predicción. |
| `Jornada` | Variable seleccionada para análisis y predicción. |
| `Localidad` | Variable seleccionada para análisis y predicción. |
| `NivelAcad` | Variable seleccionada para análisis y predicción. |

La clasificación implementada asigna `Primera infancia` a edades menores o iguales a 5; `Infancia` a las restantes menores o iguales a 11; `Adolescencia` a las restantes menores o iguales a 17; y `Adultez` en el caso restante. Estas etiquetas y umbrales provienen del código, no de registros del Excel. El código no incorpora una validación explícita de edades faltantes o fuera de rango.

Las cinco columnas seleccionadas para los modelos, en su orden inicial, son `Género`, `Jornada`, `Localidad`, `Clasificacion Edad` y `NivelAcad`. `Edad` no se envía directamente al modelo. El código no documenta el catálogo completo de categorías admitidas por los artefactos.

Las salidas se agregan como `Predicción_TipoViolencia` y `Predicción_TipoAgresor`. La interfaz muestra los primeros diez registros y gráficos de distribución; no implementa un botón de exportación.

### Papel del Excel local

`data/Abuso y violencia 2025.xlsx` **no es utilizado actualmente de forma automática por la aplicación (caso C)**. `main.py` no contiene ninguna referencia a ese archivo ni a la carpeta `data/`, y no demuestra que se haya usado para entrenamiento. No es necesario para iniciar la aplicación. Para realizar análisis y predicciones se requiere cargar manualmente una fuente compatible, sin depender de ese nombre o ubicación.

El archivo se mantiene únicamente en el entorno local y debe quedar excluido del repositorio público. La base de datos utilizada para análisis y/o entrenamiento no se distribuye a través del repositorio público. Quienes deseen ejecutar o reentrenar la solución deben proporcionar una fuente compatible con la estructura requerida; el reentrenamiento requiere además definir su metodología y variables objetivo, pues no está implementado en `main.py`.

Los datos utilizados para operar, analizar o entrenar los modelos deben gestionarse de acuerdo con las políticas institucionales de seguridad, privacidad y protección de datos.

## Instalación

Desde la raíz del repositorio, crear un entorno virtual:

```console
python -m venv .venv
```

Activarlo en Windows (CMD):

```bat
.venv\Scripts\activate
```

En PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Instalar las dependencias declaradas:

```console
pip install -r requirements.txt
```

**Limitación de reproducibilidad:** el archivo actual contiene referencias `file:///C:/...` a paquetes y ruedas del entorno de origen, entre ellos NumPy, SciPy, scikit-learn, joblib y XGBoost. El comando puede fallar en equipos donde esas rutas no existen. Algunas ruedas referenciadas corresponden a CPython 3.11 en Windows de 64 bits; esto no constituye una declaración general de compatibilidad del proyecto. Se requiere un entorno compatible con las dependencias y los artefactos serializados. `requirements.txt` se conserva sin cambios.

Se declara `openpyxl` para lectura de Excel, pero no `xlrd`; aunque la interfaz acepta `.xls`, su lectura puede requerir un motor adicional que no está declarado. No se ha validado la ejecución de la aplicación como parte de esta revisión documental.

## Ejecución

Con las dependencias disponibles y el entorno activado, ejecutar desde la raíz del repositorio para respetar las rutas relativas:

```console
streamlit run main.py
```

Mantener disponibles `images/logo.png` y los artefactos `.pkl` en sus rutas originales. Cargar una fuente autorizada en **Carga de datos**, consultar **Análisis descriptivo** y abrir **Resultados de predicción**.

## Estructura del repositorio

```text
ideca-violencia-escolar/
├── .streamlit/
│   └── config.toml
├── images/
│   └── logo.png
├── data/
│   ├── README.md
│   └── Abuso y violencia 2025.xlsx   [archivo local; excluir de publicación]
├── main.py
├── requirements.txt
├── le_agresor.pkl
├── le_violencia.pkl
├── xgb_pipeline_over_agresor.pkl
├── xgb_pipeline_over_violencia.pkl
├── README.md
├── CONTRIBUTING.md
├── LICENSE
└── .gitignore
```

`.gitignore` excluye archivos de datos locales y permite versionar `data/README.md`. **Si un archivo ya está rastreado por Git, estas reglas no lo retiran del índice ni del historial.** Antes de publicar, comprobar que el Excel no forme parte de los commits que se distribuirán.

## Consideraciones sobre los resultados

- Los resultados son herramientas de apoyo al análisis y deben interpretarse como estimaciones orientativas.
- No sustituyen la valoración profesional ni institucional.
- No deben utilizarse como única fuente para tomar decisiones sobre personas.
- El desempeño depende de los datos, su calidad y el contexto de aplicación; el código no aporta métricas que permitan cuantificarlo.
- Las categorías de tipo de agresor son salidas de clasificación y no identifican a una persona ni atribuyen responsabilidad individual.

## Privacidad y manejo de datos

El desarrollo utiliza información desidentificada. Aunque se han eliminado identificadores directos, las variables demográficas, territoriales y relacionadas con violencia escolar son sensibles: la ausencia de identificadores directos no elimina automáticamente los riesgos de reidentificación. Los datos reales deben mantenerse bajo los controles institucionales aplicables.

No deben almacenarse en el repositorio público bases con información personal, sensible o identificable. La interfaz muestra una vista previa de registros cargados; deben protegerse también el acceso a la aplicación, las capturas de pantalla y los resultados. La configuración inspeccionada de Streamlit define la apariencia y no establece controles de acceso.

La documentación puede describir esquemas y nombres de variables, pero no debe reproducir registros reales. La publicación de bases requiere validación institucional; excluir el Excel no sustituye la revisión institucional de los demás artefactos antes de su distribución.

## Contribuciones

Consultar [CONTRIBUTING.md](CONTRIBUTING.md) para el flujo de contribución y las restricciones sobre datos y secretos.

## Licencia

El archivo [LICENSE](LICENSE) contiene la licencia **Apache License 2.0**.

## Entidad

Unidad Administrativa Especial de Catastro Distrital - UAECD  
Infraestructura de Datos Espaciales para el Distrito Capital - IDECA
