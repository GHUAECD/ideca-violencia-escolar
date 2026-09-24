import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import joblib
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline


# --- Configuración general ---
st.set_page_config(page_title="Informe de Modelamiento", page_icon="📊", layout="wide")

# --- Menú lateral ---
# Cargar el logo
st.sidebar.image("images/logo.png", use_container_width=True)

st.sidebar.title("📋 Navegación")
page = st.sidebar.radio(
    "Selecciona una sección:",
    ["1️⃣ Carga de datos", "2️⃣ Análisis descriptivo", "3️⃣ Resultados de predicción"]
)

# --- 1. CARGA DE DATOS ---
if page == "1️⃣ Carga de datos":
    #st.image("D:/Documentos/Catastro/Proyecto_Niñez/logo.png", width=1000)
    st.title("Modelo Abuso y Violencia")
    st.write("Este modelo permite determinar cuál es el tipo de violencia y el tipo de agresor más probable que puede afectar a un niño.")


    # Title and description
    st.title("📂 Carga de datos")
    uploaded_file = st.file_uploader("Sube tu archivo Excel", type=["xlsx", "xls", "csv"])
    
    if uploaded_file is not None:
        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
        
        
        st.success("Archivo cargado correctamente ✅")
        df['Clasificacion Edad'] = np.where(df['Edad'] <= 5, "Primera infancia",
                     np.where(df['Edad'] <= 11, "Infancia",
                              np.where(df['Edad'] <= 17, "Adolescencia", "Adultez")))
    

        variables = ['Género', 'Jornada', 'Localidad', 'Clasificacion Edad', 
             'NivelAcad']
       
        df = df[variables]
        st.write(f"Has cargado un archivo con **{df.shape[0]:.0f}** registros. A continuación, encontrarás una vista previa de la base de datos (10 registros) y las variables requeridas para el modelo.")
        st.session_state["data"] = df  # Guardamos los datos para otras páginas
        st.dataframe(df.head(10))
        
    # 💡 Si ya había datos cargados, mostrarlos de nuevo
    elif "data" in st.session_state:
        st.info("Ya hay un archivo cargado previamente ✅")
        st.write(f"Has cargado un archivo con **{st.session_state['data'].shape[0]:.0f}** registros. A continuación, encontrarás una vista previa de la base de datos (10 registros) y las variables requeridas para el modelo.")
        st.dataframe(st.session_state["data"].head(10))
    else:
        st.info("Por favor, carga un archivo para continuar.")

# --- 2. ANÁLISIS DESCRIPTIVO ---
elif page == "2️⃣ Análisis descriptivo":
    st.title("📊 Análisis descriptivo")

    if "data" in st.session_state:
        df = st.session_state["data"]
        st.write("Se puede observar, para cada variable, la cantidad de clases, la clase con mayor número de registros y la cantidad de registros correspondiente a dicha clase.")

        # Guardar describe
        if "df_describe" not in st.session_state:
            Describe = df.describe().iloc[1:].rename(mapper={'count' : '', 'unique' : 'Cantidad de clases', 'top':'Clase mayoritaria', 'freq':' Registros clase mayoritaria'})
            st.session_state["df_describe"] = Describe

        st.dataframe(st.session_state["df_describe"])

        categoricas = ['Género', 'Jornada', 'Localidad', 'NivelAcad', 'Clasificacion Edad']
        st.subheader("📊 Distribución de variables categóricas")

        # Permitir elegir variable
        var = st.selectbox("Selecciona una variable para graficar:", categoricas)

        data_ = df[var].fillna("Sin datos")

        # Calcular conteos
        df_counts = data_.value_counts().reset_index()
        df_counts.columns = [var, "Cantidad"]

        # Gráfico Altair
        chart = (
            alt.Chart(df_counts)
            .mark_bar(color="#4C72B0")
            .encode(
                x=alt.X(var, sort='-y', title=var),
                y=alt.Y("Cantidad", title="Cantidad"),
                tooltip=[var, "Cantidad"]
            )
            .properties(
                width=700,
                height=400,
                title=f"Distribución de: {var}"
            )
        )

        # Mostrar el gráfico
        st.altair_chart(chart, use_container_width=True)

        with st.expander("Ver tabla de conteos"):
            st.dataframe(df_counts)

    else:
        st.warning("⚠️ Aún no has cargado un archivo. Ve a la página 'Carga de datos' primero.")

# --- 3. RESULTADOS DE PREDICCIÓN ---
elif page == "3️⃣ Resultados de predicción":
    st.title("📊 Resultados de predicción")

    if "data" in st.session_state:
        df = st.session_state["data"]

        # Cargar modelos
        xgb_pipeline_over_violencia = joblib.load("xgb_pipeline_over_violencia.pkl")
        xgb_pipeline_over_agresor = joblib.load("xgb_pipeline_over_agresor.pkl")

        #  Cargar LabelEncoders 
        try:
            le_violencia = joblib.load("le_violencia.pkl")
            le_agresor = joblib.load("le_agresor.pkl")
        except:
            le_violencia = None
            le_agresor = None

        # Generar predicciones
        y_pred_violencia = xgb_pipeline_over_violencia.predict(df)
        y_pred_agresor = xgb_pipeline_over_agresor.predict(df)

        # Decodificar
        if le_violencia is not None:
            y_pred_violencia = le_violencia.inverse_transform(y_pred_violencia)
        if le_agresor is not None:
            y_pred_agresor = le_agresor.inverse_transform(y_pred_agresor)

        # Agregar resultados al DataFrame
        df["Predicción_TipoViolencia"] = y_pred_violencia
        df["Predicción_TipoAgresor"] = y_pred_agresor

        # Mostrar resultados
        #st.subheader("📊 Resultados de las predicciones")
        st.dataframe(df.head(10))

        st.success("✅ Predicciones generadas correctamente")

        st.subheader("📊 Distribución predicciones")
        # Permitir elegir variable
        categoricas = ["Predicción_TipoViolencia", "Predicción_TipoAgresor"]
        var = st.selectbox("Selecciona una variable para graficar:", categoricas)

        data_ = df[var].fillna("Sin datos")

        # Calcular conteos
        df_counts = data_.value_counts().reset_index()
        df_counts.columns = [var, "Cantidad"]

        # Gráfico Altair
        chart = (
            alt.Chart(df_counts)
            .mark_bar(color="#4C72B0")
            .encode(
                x=alt.X(var, sort='-y', title=var),
                y=alt.Y("Cantidad", title="Cantidad"),
                tooltip=[var, "Cantidad"]
            )
            .properties(
                width=700,
                height=400,
                title=f"Distribución de: {var}"
            )
        )

        # Mostrar el gráfico
        
        st.altair_chart(chart, use_container_width=True)
    else:
        st.warning("⚠️ Primero carga un archivo antes de generar predicciones.")



# Calculate BMI
# if height > 0:
#     bmi = weight / (height ** 2)
#     st.write(f"Your BMI is: **{bmi:.2f}**")

#     # Interpret result
#     if bmi < 18.5:
#         st.warning("You are underweight.")
#     elif 18.5 <= bmi < 25:
#         st.success("You are in the normal weight range. Great job!")
#     elif 25 <= bmi < 30:
#         st.warning("You are overweight.")
#     else:
#         st.error("You are in the obese range. Consider consulting a healthcare professional.")
# else:
#     st.info("Please enter your height to calculate BMI.")


