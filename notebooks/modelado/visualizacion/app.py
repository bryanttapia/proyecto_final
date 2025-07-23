import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

df=pd.read_csv("../../../data/final/datos_finales.csv", sep=";")

st.set_page_config(
    page_title="Herramienta de visualizacion de datos",
    page_icon="",
    layout="wide"
)

st.title("herramienta de visualizacion de datos")
st.write("esta aplicacion permite explorar y visualizar los datos del proyecto en curso")
st.write("desarrollado por: bryant tapia muro")

st.header("Graficos")
st.subheader("caracterizacion de los creditos otorgados")

# Cantidad de créditos por objetivo del mismo

creditos_x_objetivo = px.histogram(df, x='objetivo_credito', 
                                  title='Conteo de créditos por objetivo')
creditos_x_objetivo.update_layout(xaxis_title='Objetivo del crédito', yaxis_title='Cantidad')

st.plotly_chart(creditos_x_objetivo, use_container_width=True)
#-----
# Histograma de los importes de créditos otorgados

histograma_importes = px.histogram(df, x='importe_solicitado', nbins=10, title='Importes solicitados en créditos')
histograma_importes.update_layout(xaxis_title='Importe solicitado', yaxis_title='Cantidad')
st.plotly_chart(histograma_importes, use_container_width=True)
#---
# Conteo de ocurrencias por estado
estado_credito_counts = df['estado_credito_N'].value_counts()

# Gráfico de torta de estos valores
fig = go.Figure(data=[go.Pie(labels=estado_credito_counts.index, values=estado_credito_counts)])
fig.update_layout(title_text='Distribución de créditos por estado registrado')

st.plotly_chart(fig, use_container_width=True)
#---
# Conteo de ocurrencias por caso
falta_pago_counts = df['falta_pago'].value_counts()

# Create a Pie chart
fig = go.Figure(data=[go.Pie(labels=falta_pago_counts.index, values=falta_pago_counts)])
fig.update_layout(title_text='Distribución de créditos en función de registro de mora')
fig.show()

#---
# Gráfico de barras apiladas: Comparar la distribución de créditos por estado y objetivo
barras_apiladas = px.histogram(df, x='objetivo_credito', color='estado_credito_N', 
                               title='Distribución de créditos por estado y objetivo',
                               barmode='stack')
barras_apiladas.update_layout(xaxis_title='Objetivo del crédito', yaxis_title='Cantidad')

st.plotly_chart(barras_apiladas, use_container_width=True)
#---

# Definir el orden personalizado
orden_antiguedad = ['menor_2y', '2y_a_4y', 'mayor_4y']

# Ordenar los datos según el orden personalizado
df_ordenado = df.groupby('antiguedad_cliente')['importe_solicitado'].mean().reset_index()
df_ordenado['antiguedad_cliente'] = pd.Categorical(df_ordenado['antiguedad_cliente'], categories=orden_antiguedad, ordered=True)
df_ordenado = df_ordenado.sort_values('antiguedad_cliente')

# Crear el gráfico de líneas
lineas_importes_antiguedad = px.line(df_ordenado, x='antiguedad_cliente', y='importe_solicitado',
                                     title='Evolución de los importes solicitados por antigüedad del cliente')
lineas_importes_antiguedad.update_layout(xaxis_title='Antigüedad del cliente', yaxis_title='Importe solicitado promedio')

st.plotly_chart(lineas_importes_antiguedad, use_container_width=True)
#---

# 1. Distribución de importes por objetivo del crédito
cajas_importe_objetivo = px.box(df, 
                                x='objetivo_credito', 
                                y='importe_solicitado',
                                title='Distribución de Importes Solicitados por Objetivo del Crédito',
                                labels={'objetivo_credito': 'Objetivo del Crédito', 'importe_solicitado': 'Importe Solicitado'}
                               )
cajas_importe_objetivo.show()
st.plotly_chart(cajas_importe_objetivo, use_container_width=True)
#---

# 2. Relación entre importe y duración, coloreado por estado del crédito
dispersion_importe_duracion = px.scatter(df, 
                                         x='duracion_credito', 
                                         y='importe_solicitado',
                                         color='estado_credito_N',
                                         title='Importe vs. Duración del Crédito por Estado',
                                         labels={'duracion_credito': 'Duración del Crédito (meses)', 
                                                 'importe_solicitado': 'Importe Solicitado',
                                                 'estado_credito_N': 'Estado del Crédito'}
                                        )

st.plotly_chart(dispersion_importe_duracion, use_container_width=True)
#---

# 3. Mapa de calor de correlaciones
columnas_correlacion = ['importe_solicitado', 'duracion_credito', 'personas_a_cargo']
matriz_correlacion = df[columnas_correlacion].corr()

mapa_calor_correlacion = px.imshow(matriz_correlacion,
                                   text_auto=True,
                                   title='Mapa de Calor de Correlación',
                                   labels=dict(color='Coeficiente de Correlación')
                                  )
st.plotly_chart(mapa_calor_correlacion, use_container_width=True)