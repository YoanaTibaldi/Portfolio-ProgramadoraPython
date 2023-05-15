import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from ipywidgets import interact, interactive, fixed, interact_manual
import ipywidgets as widgets
import yfinance as yf
from datetime import datetime


data_dir = 'data/data.csv'
data_dir_cities = 'data/worldcities.csv'

#Creacion de dataframe
def data_frame():
    dt = pd.read_csv(data_dir)
    df = pd.DataFrame(dt)
    select_cols = df.loc[:, :'species']
    return select_cols

def data_cities():
    df = pd.read_csv(data_dir_cities)
    df_cities = pd.DataFrame(df)
    select_cols = df_cities.loc[:, 'lat':'country'].sort_values(by='country').drop_duplicates(subset='country', keep='first')
    df_countries =  select_cols.reset_index(drop=True)
    return df_countries

# df_dt = [data_frame(), data_cities()]
# df_maps = pd.concat(df_dt)

def dino_position():
    dino_data = data_frame()
    country_data = data_cities()

    com_data = pd.merge(dino_data['lived_in'], country_data, how="right", left_on=dino_data['lived_in'], right_on=country_data['country'])
    df_data = pd.DataFrame(com_data)
    df_data = df_data[df_data['lived_in'].notna()]
    return df_data


def cotizacion_teco():
    teco= yf.Ticker("TECO2.BA")
    df = pd.DataFrame(teco.history(start='2018-01-01', end=datetime.now())) 
    df_avg = df.groupby(pd.Grouper(freq='M', level='Date')).mean()

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df_avg.index, y=df_avg['Close'], mode='lines+markers'))
    fig.update_layout(title='Cotización mensual de Telecom', 
                      title_x=0.5, 
                      xaxis_title="Dates",
                      yaxis_title="Values",
                      width=700, 
                      height=600)
    return fig




def random_data():
    #for random data
    x_data = np.array([2, 4, 6, 8, 10, 12])
    y_data = np.array([1, 2, 3, 4, 5, 6])
    xx_data = np.array([13, 15, 17, 19, 21])
    yy_data = np.array([7, 8, 9, 10, 11, 12])

    fig_rd = go.Figure()
    fig_rd.add_trace(go.Scatter( x=x_data, y=y_data, mode='lines+markers'))
    fig_rd.add_trace(go.Scatter(x=np.concatenate((x_data[-1:], xx_data)), y=np.concatenate((y_data[-1:], yy_data)), mode='lines+markers'))
    fig_rd.update_layout(width=600, height=500, title="Random Data")
    return fig_rd


#Tipo de alimentacion
def type_food():
    df = data_frame()
    #Filtrando por tipo de alimentacion
    diet = df['diet']

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
    return fig



#Separa nombre del período de los años
def freq_period():
    df = data_frame()
    periodo = df['period']

    patron = r'(?P<nombre>.+)\s(?P<rango>\d+-\d+\s.+ ago)'
    df[['nombre_periodo', 'rango_anios']] = periodo.str.extract(patron)

    # Imprimir DataFrame resultante
    sep_periodos = df
    return sep_periodos
   
def data_dropdown():
    df = freq_period()
    df_options = df['nombre_periodo'].unique()
    return df_options



def dino_map():
    df = dino_position()

    #Periodo en el que vivio
    fig = px.scatter_geo(df, lat=df['lat'], lon=df['lng'],
                    hover_name=df['lived_in'], color=df['country'],
                    projection="natural earth", width=700, height=500,
                    title='Localización de dinosaurios')
    return fig


    
     
    
    

