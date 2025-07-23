import streamlit as st
import pandas as pd
import plotly.express as px

# Título de la aplicación
st.set_page_config(page_title="Análisis de Vehículos", layout="wide")
st.title("Panel de Control: Análisis de Ventas de Vehículos")

# Carga del dataset
@st.cache_data
def load_data():
    df = pd.read_csv("/Users/elias/Downloads/Proyectos Tripleten/Actividad-Sprint7/Tarea-Sprint7/Tarea-Sprint7/vehicles_us.csv")  
    # Extraer la marca desde la columna 'model'
    df['brand'] = df['model'].str.split().str[0]
    return df

df = load_data()


# Vista previa de los datos
with st.expander("🔍 Mostrar datos"):
    st.dataframe(df.head())

# Gráfico 1: Histograma de precios con filtro de marca
st.subheader("Gráfico 1: Distribución de Precios por Marca")
marca_sel1 = st.selectbox("Selecciona una marca:", sorted(df['brand'].unique()), key="grafico1")
df_filtrado1 = df[df['brand'] == marca_sel1]
fig1 = px.histogram(df_filtrado1, x="price", nbins=50, title=f"Distribución de Precios - {marca_sel1}")
st.plotly_chart(fig1, use_container_width=True)

# Gráfico 2: Pie Chart por tipo de carrocería con filtro de marca
st.subheader("Gráfico 2: Distribución por Tipo de Carrocería")
marca_sel2 = st.selectbox("Selecciona una marca:", sorted(df['brand'].unique()), key="grafico2")
df_filtrado2 = df[df['brand'] == marca_sel2]
fig2 = px.pie(df_filtrado2, names="type", title=f"Distribución por Tipo - {marca_sel2}")
st.plotly_chart(fig2, use_container_width=True)

# Gráfico 3: Precio promedio por tipo de combustible
st.subheader("Gráfico 3: Precio Promedio por Tipo de Combustible")
precio_combustible = df.groupby("fuel")["price"].mean().reset_index()
fig3 = px.bar(precio_combustible, x="fuel", y="price", title="Precio Promedio por Combustible")
st.plotly_chart(fig3, use_container_width=True)

# Gráfico 4: Precio promedio por condición con filtro de odómetro
st.subheader("Gráfico 4: Precio Promedio por Condición del Vehículo")
odometro_max = int(df['odometer'].max())
odometro_filtrado = st.slider("Selecciona el rango máximo de kilometraje:", 0, odometro_max, odometro_max, key="grafico4")
df_filtrado4 = df[df['odometer'] <= odometro_filtrado]
precio_condicion = df_filtrado4.groupby("condition")["price"].mean().reset_index()
fig4 = px.bar(precio_condicion, x="condition", y="price", title=f"Precio Promedio por Condición (hasta {odometro_filtrado} km)")
st.plotly_chart(fig4, use_container_width=True)

# Gráfico 5: Línea - evolución del precio por modelo y año para una marca
st.subheader("Gráfico 5: Evolución del Precio Promedio por Modelo y Año")
marca_sel5 = st.selectbox("Selecciona una marca:", sorted(df['brand'].unique()), key="grafico5")
df_filtrado5 = df[df['brand'] == marca_sel5]
precio_anio_modelo = df_filtrado5.groupby(["model_year", "model"])["price"].mean().reset_index()
fig5 = px.line(precio_anio_modelo, x="model_year", y="price", color="model", title=f"Evolución de Precio - {marca_sel5}")
st.plotly_chart(fig5, use_container_width=True)

# Gráfico 6: Distribución de precios por tipo de vehículo
st.subheader("Gráfico 6: Distribución de Precios por Tipo de Vehículo")
fig6 = px.box(df, x="type", y="price", title="Distribución de Precios por Tipo")
st.plotly_chart(fig6, use_container_width=True)

# Gráfico 7: Comparación entre dos marcas
st.subheader("Gráfico 7: Comparación de Condición y Precios entre Dos Marcas")
col1, col2 = st.columns(2)
with col1:
    marca_1 = st.selectbox("Marca 1:", sorted(df['brand'].unique()), key="grafico7_1")
with col2:
    marca_2 = st.selectbox("Marca 2:", sorted(df['brand'].unique()), key="grafico7_2")

df_marca1 = df[df['brand'] == marca_1]
df_marca2 = df[df['brand'] == marca_2]
df_condiciones = pd.concat([
    df_marca1.assign(marca=marca_1),
    df_marca2.assign(marca=marca_2)
])

fig7 = px.histogram(df_condiciones, x="condition", color="marca", barmode="group",
                    title=f"Distribución de Condiciones: {marca_1} vs {marca_2}")
st.plotly_chart(fig7, use_container_width=True)