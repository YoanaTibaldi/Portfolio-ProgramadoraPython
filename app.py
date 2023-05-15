from flask import Flask
import pandas as pd
import numpy as np
from dash import Dash, html, dcc 
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
import plotly.express as px
from process_data import *
import dash

   
app = Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.BOOTSTRAP])


# Se crea un parent Div, que busca dentro de html el tag Div
app.layout = html.Div(
    children=
        html.Div(
                children=[       
                html.Img(src='assets/css/Logo-Programming.png',
                         style={'width':'250px',
                                'height':'250px'
                                }),
                  
         html.Div(
        [
            html.Div(
                dbc.NavItem(dcc.Link(
                    f"{page['name']}", href=page["relative_path"], className='letra'
                ))
            )
            for page in dash.page_registry.values()
        ], className="buttons" 
    ),
    
	dash.page_container
       
    ])
)


if __name__ == "__main__":
    app.run_server(debug=True)
