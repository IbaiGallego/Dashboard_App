import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime


st.set_page_config(page_title="Servicios", layout='wide',initial_sidebar_state='collapsed')

# Color Dict

tipo_colors = {'Mantenimiento SW': '#1f77b4',
                'Venta accesorios': '#ff7f0e',
                'Licencia SW': '#2ca02c',
                'Venta de equipos':'#dbdb8d',
                'RMM': '#d62728',
                'Desarrollo SW': '#9467bd',
                'Horas sueltas': '#8c564b',
                'SMI': '#e377c2',
                'Consultoria': '#7f7f7f',
                'Copia de seguridad': '#bcbd22',
                'nesicCLOUD': '#17becf',
                'HW/SW Seguridad': '#aec7e8',
                'Kit Digital': '#ffbb78',
                'Venta servidores': '#98df8a',
                'Gastos corrientes': '#ff9896',
                'Licencia MS': '#c5b0d5',
                'Mantenimiento APPS': '#c49c94',
                'Desarrollo APPS': '#f7b6d2',
                'Gastos bancarios devol': '#c7c7c7',
                'Abonos por errores':'#9edae5'}

#Page configuration

st.header('Servicios')

#Dataset

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

v['fecha'] = pd.to_datetime(v['fecha'])


### First Row of Charts.

## Timefilter General

time1, time2 = st.columns(2)
años = [2016,2017,2018,2019,2020,2021,2022,2023,2024]

with time1:

    startyear2 = st.selectbox('Start',años)
    
with time2:
    endyear2 = st.selectbox('Stop',años)



## Charts

col1, col2 = st.columns(2)

with col1:
    startyear2 = datetime(startyear2, 1, 1)
    endyear2 = datetime(endyear2, 12, 31)
    # filter data on year
    data = v[(v['fecha'] >= startyear2) & (v['fecha'] <= endyear2)]
    # Group the data by 'tipo' and calculate sum of ventas
    servicios = data.groupby('tipo').sum().sort_values('importe_de_venta', ascending=False)
    servicios = servicios[['importe_de_venta']]
    servicios = servicios.reset_index()

    # Create a list of colors based on the order of 'tipo' from the DataFrame servicios
    colors = [tipo_colors[tipo] for tipo in servicios['tipo']]

    fig1 = go.Figure(data=go.Bar(x=servicios['tipo'], y=servicios['importe_de_venta'], marker_color=colors))
    fig1.update_layout(xaxis_title='Servicio', yaxis_title='Ventas', title='Importe de Venta por Servicio')

    # Show the plot
    st.write(fig1)


with col2:
    v2 = v[v.importe_de_venta >= 0]
    # filter data on year
    data = v2[(v2['fecha'] >= startyear2) & (v2['fecha'] <= endyear2)]
    # Group the data by 'tipo' and calculate the sum of 'importe_de_venta' and count of rows
    grouped_df = data.groupby('tipo').agg({'importe_de_venta': 'sum', 'fecha': 'count'}).reset_index()
    grouped_df = grouped_df.rename(columns={'fecha':'numero_compras'})
    grouped_df['importex10']=grouped_df.importe_de_venta.apply(lambda x: x*100)
    # Create a scatter plot
    fig2 = px.scatter(grouped_df, x='numero_compras', y='importe_de_venta', size='importex10', color='tipo',
                 hover_name='tipo', color_discrete_map=tipo_colors)

    # Add title and axis labels
    fig2.update_layout(title='Number of Times Bought vs Importe de Venta',
                    xaxis_title='Numero de Ventas',
                    yaxis_title='Importe de Venta')

    # Show the plot
    st.write(fig2)


# Selector Servicios

servicios = sorted(list(v['tipo'].unique()))
servicios_select2 = st.multiselect('Servicios', servicios)

## Timelinne servicios

# Filter data for a specific services
service_data = v[v['tipo'].isin(servicios_select2)]

# Filter data on year
service_data = service_data[(service_data['fecha'] >= startyear2) & (service_data['fecha'] <= endyear2)]

# Group filtered data by service and month
grouped_data = service_data.groupby(['tipo', pd.Grouper(key='fecha', freq='M')]).sum().reset_index()

# Create the figure
fig3 = go.Figure()

# Add a line trace for each service
for service in grouped_data['tipo'].unique():
    service_data = grouped_data[grouped_data['tipo'] == service]
    color = tipo_colors[service]  # Get the color from the dictionary
    fig3.add_trace(go.Scatter(x=service_data['fecha'], y=service_data['importe_de_venta'],
                            mode='lines+markers', name=service, marker=dict(color=color)))

fig3.update_layout(xaxis_title='Fecha', yaxis_title='Ventas Mensuales',
                title='Line Temporal de Servicios')
st.write(fig3)