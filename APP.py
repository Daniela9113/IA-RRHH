import streamlit as st
import pandas as pd
import plotly.express as px
import pickle

# Título principal
st.title("Evaluación de Candidatos - Probabilidad de Contratación")

# Sidebar para subir el modelo
st.sidebar.header("Subir Modelo Entrenado")
uploaded_model = st.sidebar.file_uploader("Sube tu archivo .pkl", type="pkl")

# Sidebar para subir el dataset de candidatos (CSV)
st.sidebar.header("Subir Datos de Candidatos")
uploaded_data = st.sidebar.file_uploader("Sube tu archivo .csv", type="csv")

# Si ambos archivos fueron cargados
if uploaded_model is not None and uploaded_data is not None:
    # Cargar modelo
    modelo = pickle.load(uploaded_model)
    st.success("✅ Modelo cargado correctamente")
    
    # Cargar datos de candidatos
    df_candidatos = pd.read_csv(uploaded_data)
    st.success("✅ Datos de candidatos cargados correctamente")

    st.write("### Vista previa de los datos:")
    st.dataframe(df_candidatos.head())

    # Dropdown para elegir vacante
    vacantes = df_candidatos['vacante_id'].unique()
    vacante_seleccionada = st.selectbox("Selecciona la Vacante", vacantes)

    # Filtrar por vacante seleccionada
    df_filtrado = df_candidatos[df_candidatos['vacante_id'] == vacante_seleccionada]
    ranking = df_filtrado.sort_values(by='probabilidad_contratacion', ascending=False)

    # Gráfico interactivo de ranking
    fig = px.bar(
        ranking, 
        x='probabilidad_contratacion', 
        y=ranking.index, 
        color='educacion',
        orientation='h',
        hover_data=['experiencia_anios', 'puntaje_test', 'puntaje_entrevista', 'nivel_ingles'],
        title=f'Ranking de Candidatos para {vacante_seleccionada}',
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    fig.update_layout(yaxis_title='ID Candidato', xaxis_title='Probabilidad de Contratación')
    st.plotly_chart(fig)

    st.info("🔎 **Este gráfico muestra un ranking horizontal de los candidatos ordenados por su probabilidad de contratación para la vacante seleccionada. Puedes visualizar su educación, experiencia, puntajes y nivel de inglés al pasar el mouse.**")

else:
    st.warning("🔴 Sube el archivo del modelo (.pkl) y los datos (.csv) para continuar.")

