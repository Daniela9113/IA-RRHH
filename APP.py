import streamlit as st
import pandas as pd
import plotly.express as px
import pickle

# ------------------- Funciones ------------------- #

@st.cache_resource
def cargar_modelo():
    with open('modelo_entrenado.pkl', 'rb') as file:
        modelo = pickle.load(file)
    return modelo

@st.cache_data
def cargar_datos():
    df = pd.read_csv('datos_candidatos.csv')
    return df

def grafico_ranking(df, vacante_seleccionada):
    df_vacante = df[df['vacante_id'] == vacante_seleccionada]
    df_vacante['candidato_id'] = df_vacante.index.astype(str)

    fig = px.bar(
        df_vacante,
        x='probabilidad_contratacion',
        y='candidato_id',
        color='vacante_id',
        color_discrete_sequence=px.colors.qualitative.Pastel1,
        orientation='h',
        hover_data=['educacion', 'experiencia_anios', 'puntaje_test', 'puntaje_entrevista', 'nivel_ingles'],
        title=f'Ranking de Candidatos - {vacante_seleccionada}'
    )

    fig.update_layout(
        xaxis_title='Probabilidad de Contratación',
        yaxis_title='Candidato',
        height=600
    )
    return fig

def grafico_contratados(df, vacante_seleccionada):
    df_vacante = df[(df['vacante_id'] == vacante_seleccionada) & (df['contratado'] == 1)]
    if df_vacante.empty:
        return None

    fig = px.pie(
        df_vacante,
        names='educacion',
        values='probabilidad_contratacion',
        color_discrete_sequence=px.colors.qualitative.Pastel,
        title=f'Distribución de Educación - Candidatos Contratados en {vacante_seleccionada}'
    )

    return fig

# ------------------- Streamlit App ------------------- #

st.set_page_config(page_title="Evaluación de Candidatos", layout="wide")

st.title("📊 Evaluación de Candidatos - Probabilidad de Contratación")

# Cargar datos y modelo
modelo = cargar_modelo()
df_candidatos = cargar_datos()

# Filtro de Vacante
vacantes = df_candidatos['vacante_id'].unique()
vacante_seleccionada = st.selectbox('Selecciona una Vacante', vacantes)

st.markdown("---")

# ------------------- Gráfico 1: Ranking ------------------- #
st.subheader(f"🔹 Ranking de Candidatos - {vacante_seleccionada}")
st.write("Este gráfico muestra a todos los candidatos de la vacante seleccionada ordenados por su **probabilidad de contratación**. "
         "Puedes ver detalles como su nivel educativo, años de experiencia y puntajes obtenidos en las evaluaciones.")

fig_ranking = grafico_ranking(df_candidatos, vacante_seleccionada)
st.plotly_chart(fig_ranking, use_container_width=True)

st.markdown("---")

# ------------------- Gráfico 2: Distribución Educación (Contratados) ------------------- #
st.subheader(f"🔹 Distribución de Educación en Candidatos Contratados - {vacante_seleccionada}")
st.write("Este gráfico de pastel muestra la **distribución del nivel educativo** entre los candidatos que fueron contratados para la vacante seleccionada. "
         "Permite identificar el perfil educativo predominante entre los seleccionados.")

fig_contratados = grafico_contratados(df_candidatos, vacante_seleccionada)
if fig_contratados:
    st.plotly_chart(fig_contratados, use_container_width=True)
else:
    st.info("No hay candidatos contratados en esta vacante.")

st.markdown("---")

# ------------------- Tabla de Datos ------------------- #
st.subheader(f"📄 Detalle de Candidatos - {vacante_seleccionada}")
st.write("En esta tabla se muestran los datos completos de los candidatos de la vacante seleccionada, incluyendo su puntaje en pruebas y entrevistas.")

st.dataframe(df_candidatos[df_candidatos['vacante_id'] == vacante_seleccionada])
