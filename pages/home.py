import dash
from dash import html, dcc, callback, Input, Output

dash.register_page(__name__, path='/',
                   title='Yoana Tibaldi')

layout = html.Div(children=[
   html.H3(children='Hola! Mi nombre es Yoana Tibaldi y me encanta ser Programadora Python 🐍'),          
                html.H4(
                children='Soy Programadora Python jr con experiencia en el manejo y visualización de datos '),
                html.Br(),
                html.H4('Me gusta mucho aprender sobre este lenguaje por lo que suelo poner en práctica lo que voy aprendiendo '
                'o lo que me causa curiosidad'
                , 
        ),
    html.H4(children='Las herramientas que manejo son: Numpy, Pandas, Plotly, Dash y Jupyter Notebooks'),
    html.Br(),
    html.Footer(children=[
         html.H5(children='Contacto'),
         html.Div(children=[dcc.Link(html.Img(src='assets/css/linkedin (1).png',
                         style={'width':'32px',
                                'height':'32px'
                                }), href='https://www.linkedin.com/in/yoana-tibaldi/', target='_blank'),
                dcc.Link(html.Img(src='assets/css/cv.png',
                         style={'width':'32px',
                                'height':'32px'
                                }), href=' https://docs.google.com/document/d/1e35_Uzpe-a2S21eAAv2xyw24m48lBxAL-TBaQxFQxb8/export?format=pdf', target='_blank'),], className='icons')

    ], className='footer'),
                                

    ], className='presentacion'),
         
