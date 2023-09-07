#Imports

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime


st.set_page_config(page_title="Clientes", layout='wide',initial_sidebar_state='collapsed')
#Dataset


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

st.header('Clientes')




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

v.cliente = v.cliente.astype(str)
v['fecha'] = pd.to_datetime(v['fecha'])


## Timefilter General

time1, time2 = st.columns(2)
años = [2016,2017,2018,2019,2020,2021,2022,2023,2024]

with time1:

    startyear1 = st.selectbox('Start',años)
    
with time2:
    endyear1 = st.selectbox('Stop',años)

# filter data on year

startyear1 = datetime(startyear1, 1, 1)
endyear1 = datetime(endyear1, 12, 31)

data = v[(v['fecha'] >= startyear1) & (v['fecha'] <= endyear1)]




### First Row of Charts.
## Selectors

sel1, sel2 = st.columns(2)


#Range
with sel1:
    rangcliente = st.slider('Rango de clientes',0, len(data.cliente.unique()), (0, len(data.cliente.unique())))
    st.write('Rango:', rangcliente)

# Client Selector
with sel2:
    option = st.selectbox(
        'Cliente',
        (sorted(list(v.cliente.unique()))))













## Charts

fig_col1, fig_col2 = st.columns(2)
    
with fig_col1:
    clientes = data.groupby('cliente')['importe_de_venta'].sum().reset_index().sort_values('importe_de_venta', ascending=False)
    #Filter on Range
    start, stop = rangcliente
    clientes_to_plot = clientes.iloc[start:stop]

    #figure
    fig1 = go.Figure(data=go.Bar(x=clientes_to_plot['cliente'], y=clientes_to_plot['importe_de_venta'], marker_color='green'))
    fig1.update_layout(xaxis_title='Id Cliente', yaxis_title='Ventas', title='Importe de Venta por Cliente')
    st.write(fig1)
        
with fig_col2:
    #Second Plot
    
    # Retrieve the sales data from your dataset
    prod_lst = list(v.tipo.unique())
    client_lst = str(option)
    data2 = v.loc[v.tipo.isin(prod_lst)]
    data2 = data2.loc[data2.cliente == client_lst]
    serv_cliente = data2.pivot_table(values='importe_de_venta', columns='tipo', index='cliente', aggfunc='sum')

    # Initialize the figure
    fig2 = go.Figure()

    # Loop through each tipo and add a bar trace to the figure
    for tipo in serv_cliente.columns:
        tipo_data = serv_cliente[tipo]
        trace = go.Bar(x=[tipo], y=[tipo_data.values[0]], hovertext=[tipo_data.values[0]], marker_color=tipo_colors.get(tipo, 'gray'), name=tipo)
        fig2.add_trace(trace)

    # Update the layout and display the figure
    fig2.update_layout(
        title="{}".format(client_lst),
        xaxis_title="Servicio",
        yaxis_title="Ventas",
        showlegend=False  # Display the legend
    )
    st.write(fig2)

















### Second row of charts.

## Selectors:

servicios = sorted(list(v['tipo'].unique()))
servicios_select1 = st.multiselect('Servicios', servicios)
















## Charts

fig_col3, fig_col4 = st.columns(2)
    
with fig_col3:

    client_id = option
    client_data = v[v['cliente'] == client_id]

    # filter data on year
    client_data = client_data[(client_data['fecha'] >= startyear1) & (client_data['fecha'] <= endyear1)]

    # Group sales data by month and calculate monthly expenses
    monthly_expenses = client_data.groupby(pd.Grouper(key='fecha', freq='M')).sum()

    # Create the timeline plot
    fig3 = go.Figure(data=go.Scatter(x=monthly_expenses.index, y=monthly_expenses['importe_de_venta'],
                                mode='lines+markers',line=dict(color='red'), marker=dict(color='red')))

    fig3.update_layout(xaxis_title='Fecha', yaxis_title='Ventas Mensuales', title=f'Linea Temporal de Ventas {option}')
    st.write(fig3)
        
with fig_col4:
    # Filter data for a specific client
    client_id = option
    client_data = v[v['cliente'] == client_id]

    # Convert transaction dates to datetime if not already in datetime format
    client_data['fecha'] = pd.to_datetime(client_data['fecha'])

    # filter data on year
    client_data = client_data[(client_data['fecha'] >= startyear1) & (client_data['fecha'] <= endyear1)]

    # Filter the data for the selected services
    filtered_data = client_data[client_data['tipo'].isin(servicios_select1)]

    # Group filtered data by service and month
    grouped_data = filtered_data.groupby(['tipo', pd.Grouper(key='fecha', freq='M')]).sum().reset_index()

    # Create the figure
    fig4 = go.Figure()

    # Add a line trace for each service
    for service in grouped_data['tipo'].unique():
        service_data = grouped_data[grouped_data['tipo'] == service]
        color = tipo_colors[service]  # Get the color from the dictionary
        fig4.add_trace(go.Scatter(x=service_data['fecha'], y=service_data['importe_de_venta'],
                                mode='lines+markers', name=service, marker=dict(color=color)))

    fig4.update_layout(xaxis_title='Fecha', yaxis_title='Gastos Mensuales',
                    title=f'Linea Temporal de Ventas por Servicio {option}')
    st.write(fig4)

