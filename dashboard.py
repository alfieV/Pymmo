from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import numpy as np
import folium


app = Dash(__name__)

coords = (46.539758, 2.430331)
map = folium.Map(location=coords, tiles='OpenStreetMap', zoom_start=6)

app.layout = html.Div([
    html.H1(children=f'L\'immobilier en France',
                                        style={'textAlign': 'center', 'color': '#000000'}),
    html.Label('Selectionner l\'année désirée'),
    dcc.Dropdown(
                #id="year-dropdown",
                options=[
                    {'label': '2022', 'value': 2022},
                    {'label': '2021', 'value': 2021},
                    {'label': '2020', 'value': 2020},
                    {'label': '2019', 'value': 2019},
                    {'label': '2018', 'value': 2018},
                    {'label': '2017', 'value': 2017},
                ],
                value=2022,
            ),
    html.H3('Histogramme'),
    dcc.Graph(id="graph"),

    
    html.P("Moyenne:"),
    dcc.Slider(id="moyenne", min=-3, max=3, value=0, 
               marks={-3: '-3', 3: '3'}),
    html.P("Écart-type:"),
    dcc.Slider(id="std", min=1, max=3, value=1, 
               marks={1: '1', 3: '3'}),
    
    html.H3('Histogramme du prix au mètre carré en Seine-Saint-Denis et en Seine-et-Marne'),
    dcc.Graph(
        figure={
            'data': [
                {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'bar', 'name': 'Seine-Saint-Denis'},
                {'x': [1, 2, 3], 'y': [2, 4, 5], 'type': 'bar', 'name': 'Seine-et-Marne'},
            ],
            'layout': {
                'title': 'Prix au mètre carré'
            }
        }
    ),

    html.H3('Quantité de vente'),
    html.Iframe(
        id = "map",
        srcDoc = open('map.html', 'r').read(),
        width = "100%",
        height = "700",

    ),

    html.H3('Prix au mètre carré'),
    html.Iframe(
        id = "map",
        srcDoc = open('map.html', 'r').read(),
        width = "100%",
        height = "700",

    ),

    html.H3('Prix moyen d\'une maison'),
    html.Iframe(
        id = "map2",
        srcDoc = open('map2.html', 'r').read(),
        width = "100%",
        height = "700",

    )
])


@app.callback(
    Output("graph", "figure"), 
    Input("moyenne", "value"), 
    Input("std", "value"))
def display_color(moyenne, std):
    data = np.random.normal(moyenne, std, size=500) # replace with your own data source
    fig = px.histogram(data, range_x=[-10, 10])
    return fig

app.run_server(debug=True)

