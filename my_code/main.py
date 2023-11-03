import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from datetime import datetime

st.set_page_config(
    page_title="Inicio",layout='wide', initial_sidebar_state='expanded')

st.header("General Ventas")

v_tot = pd.read_csv('../data/v_tot.csv')
v_out = pd.read_csv('../data/v_out.csv')
v_norm = pd.read_csv('../data/v_norm.csv')

#Outlier Selector
outlier = st.selectbox('Outliers',['Incluir','Excluir','Outliers'])

if outlier == 'Incluir':
    v = v_tot
elif outlier == 'Excluir':
    v = v_norm
else:
    v = v_out

v.fecha = pd.to_datetime(v.fecha)

## Timefilter General

time1, time2 = st.columns(2)
años = [2016,2017,2018,2019,2020,2021,2022,2023,2024]

with time1:

    startyear = st.selectbox('Start',años)
    
with time2:
    endyear = st.selectbox('Stop',años)




## Cols

col1, col2, col3 = st.columns(3)

with col1:

    startyear = datetime(startyear, 1, 1)
    endyear = datetime(endyear, 12, 31)
    data = v[(v['fecha'] >= startyear) & (v['fecha'] <= endyear)]
    data = data.groupby([pd.Grouper(key='fecha', freq='M')]).sum()
    data = data[~data.isna()]
    mediamensual=data.importe_de_venta.mean()
    st.metric(label="Promedio Mensual", value=round(mediamensual, 2))


with col2:
    std_mensual = data.importe_de_venta.std()
    st.metric(label="Desviación Standar Mensual", value=round(std_mensual, 2))

with col3:
    median_mensual = data.importe_de_venta.median()
    st.metric(label="Mediana Mensual", value=round(median_mensual, 2))




# Filter data on year
data = v[(v['fecha'] >= startyear) & (v['fecha'] <= endyear)]

# Calculate monthly expenses
monthly_expenses = data.groupby(pd.Grouper(key='fecha', freq='M')).sum()

# Create the timeline plot
fig1 = go.Figure(data=go.Scatter(x=monthly_expenses.index, y=monthly_expenses['importe_de_venta'],
                                mode='lines+markers', line=dict(color='red'), marker=dict(color='red')))

fig1.update_layout(xaxis_title='Fecha', yaxis_title='Ventas Mensuales', title='Linea temporal General')
st.write(fig1)

