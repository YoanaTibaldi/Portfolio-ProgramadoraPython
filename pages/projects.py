import pandas as pd
import numpy as np
import dash
from dash import Dash, html, dcc, callback, Input, Output
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
import plotly.express as px
from process_data import *


#llamando a la f(x)
fig_food = type_food()
fig_rd = random_data()
fig_earth = dino_map()
opt_ddown = data_dropdown()
fig_teco = cotizacion_teco()


data = (
    fig_rd,
    fig_food,
)

dash.register_page(__name__,
                    title='Mis Proyectos',
                    name='Proyectos') #si no aclaro el path como en home, toma el nombre completo del archivo

layout = html.Div(children=[
    #html.H1(children='Estos son mis proyectos'),
    html.Div(children=[
    html.Hr(),
    html.H3(children='Promedio mensual de cotización de la empresa Telecom'),
    html.Div([      
        dcc.Graph(figure=fig_teco),
        html.H5(children=["Se utilizaron herramientas como yfinance para la obtención de los datos de cotización de la empresa pero solo desde el año 2018 hasta la actual. "
                "Para la obtención de los promedios por mes se usó Pandas. " 
                "Finalmente se graficó a través de Plotly donde en el eje x se visualizan los años con una frecuencia de un mes "
                "y en el eje y se muestra el promedio de cotizaciones por mes. "], className='text-teco')
       
    ], className='section-teco')], className='all-sect-teco'),
    html.Hr(),
    html.Br(),
    html.H3(children='Dino Data'),
    html.H5(children=["Para este proyecto, descargué una pequeña base de datos de dinos y los datos de las ubicaciones de ciudades y paises. "]),
    html.H5(children=["Esta última se utilizó para poder ubicarlos en el país donde vivieron. "]),
    html.H5(children=["Luego se creó el componente dropdown que filtraría por el período en el que vivieron. "]),
    html.H5(children=["A raíz de ese filtro se puede observar en el mapa los paises en los que vivieron en ese período y un gráfico de torta donde se visualiza el porcentaje de su dieta. "]),
    html.H5(children=["Debajo, de estos gráficos se creará una tabla mostrando los resultados con la siguiente información: "]),
    html.H5(children=["nombre, país, tipo de dieta, período y años en los que vivieron. "]),
    html.Br(),
    html.Div([ dcc.Dropdown(
        id='dropdown',
        options=[{'label': option, 'value': option} for option in opt_ddown if pd.notnull(option)],
        value=None,
        className="dropdown",
        placeholder='Selecciona un periodo',
    )]),
    html.Br(),
    html.Div(children=[
        html.Div(id='analytics-output'),
        html.Div(id='diet')], className='graphs-dino'),
    html.Div(id='dinosaurs-info'),
], className='sect-projetc')



# Callback to update the map and dinosaurs info based on the selected period
@callback(
    [Output('analytics-output', 'children'),
     Output('dinosaurs-info', 'children')],
    Input('dropdown', 'value')
)
def update_map_and_info(valor_seleccionado):
    df_otro = freq_period()
    df_posicion = dino_position()

    if valor_seleccionado is None:
        # Return the initial map and empty dinosaurs info if no value is selected
        return dcc.Graph(figure=fig_earth), None

    df_filtrado = df_otro[df_otro['nombre_periodo'] == valor_seleccionado]
    df_merged = pd.merge(df_filtrado, df_posicion, on='lived_in').drop_duplicates()

    fig = px.scatter_geo(df_merged, lat='lat', lon='lng',
                hover_name='lived_in', color='country',
                projection="natural earth", width=700, height=500,
                title='Localización de dinosaurios')
   


    rows = [
        html.Tr([
            html.Td(f"{name.capitalize()}"),
            html.Td(f"{country}"),
            html.Td(f"{diet.capitalize()}"),
            html.Td(f"{period}"),
            html.Td(f"{year}")
        ])
        for name, country, diet, period, year in zip(
            df_merged['name'],
            df_merged['country'],
            df_merged['diet'],
            df_merged['nombre_periodo'],
            df_merged['rango_anios']
        )
    ]

    # Create the table header
    table_header = [html.Thead(html.Tr([
        html.Th("Dinosaurio"),
        html.Th("País"),
        html.Th("Dieta"),
        html.Th("Período"),
        html.Th("Año")
    ]))]

    # Create the table body
    table_body = [html.Tbody(rows)]
    dinosaurs_info = dbc.Table(table_header + table_body, bordered=True, hover=True, responsive=True, striped=True)

    return dcc.Graph(figure=fig), dinosaurs_info


@callback(
        Output('diet', 'children'),
        Input('dropdown', 'value')
)
def update_map_diet(valor_seleccionado):
    df_otro = freq_period()
    df_posicion = dino_position()

    if valor_seleccionado is None:
        # Return the initial map and empty dinosaurs info if no value is selected
        return dcc.Graph(figure=fig_food) 

    df_filtrado = df_otro[df_otro['nombre_periodo'] == valor_seleccionado]
    df_merged = pd.merge(df_filtrado, df_posicion, on='lived_in').drop_duplicates()

    diet = df_merged['diet']

    carnivoros = []
    herbivoros = []
    omnivoros = []

    for i in diet:
        if i == 'carnivorous':
            carnivoros.append(i)
        elif i == 'herbivorous':
            herbivoros.append(i)
        else:
            omnivoros.append(i)

    all_diet = {'Carnivoros': len(carnivoros), 
                'Herbivoros': len(herbivoros), 
                'Omnivoros': len(omnivoros)}

    #Separando las claves de los valores
    labels = list(all_diet.keys())
    values = list(all_diet.values())

    fig = go.Figure(data=[go.Pie(labels=labels, values=values)])
    fig.update_layout(title='Tipo de Dieta', title_x=0.5, width=500, height=500)

    return dcc.Graph(figure=fig)
    
def update_city_selected(click_data):
    if click_data is not None:
        return f'You selected: {click_data}'
    else:
        return ''
