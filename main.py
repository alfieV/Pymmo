from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import numpy as np
import folium
import pandas as pd

def sortdata(data):
    sorteddata = dict()

    for elem in data.itertuples(index=False):
        code = findcode(elem)
        if code in sorteddata: #17 = code postal !!!!!!!!!!!! toutes les colonnes sont décalées de 1 vers la gauche car le tableau officiel commence à 1 et python a 0
            sorteddata[code].append(elem)
        else:
            sorteddata[code] = []
            sorteddata[code].append(elem)
    
    return sorteddata

def calcdata(sorteddata):
    realdata = dict()
    for cp in sorteddata:
        city = dict()
        lignes = sorteddata[cp]

        city = calcdatachunk(city,lignes, 0)
        city = calcdatachunk(city,lignes, 1)
        city = calcdatachunk(city,lignes, 2)
        city = calcdatachunk(city,lignes, 4)

        realdata[cp] = city
    
    return realdata


def calcdatachunk(city, lignes, typebien):
    if (typebien==0):
        strend='tot'
    if (typebien==1):
        strend='mai'
    if (typebien==2):
        strend='app'
    if (typebien==4):
        strend='com'
    valeurfonciere = []
    surface = []
    prixm2 = []
    rooms = []

    if (type==0):
        for ligne in lignes:
            if (type(ligne[10]) != float):
                valeurfonciere.append(float(ligne[10].replace(',', '.'))) # 11= valeur foncière
            else:
                valeurfonciere.append(ligne[10])

            surface.append(ligne[38]) #39 = surface réelle bati
            if (type(ligne[10]) != float):
                if (ligne[38] > 0 and float(ligne[10].replace(',', '.')) > 0):
                    prixm2.append(float(ligne[10].replace(',', '.'))/ligne[38])
            else:
                if (ligne[38] > 0 and ligne[10] > 0):
                    prixm2.append(ligne[10]/ligne[38])
            rooms.append(ligne[39]) # 4° = nombre de pièces principales
    else:
        for ligne in lignes:
            if ligne[35] == 1: # code type local = maison
                if (type(ligne[10]) != float):
                    valeurfonciere.append(float(ligne[10].replace(',', '.'))) # 11= valeur foncière
                else:
                    valeurfonciere.append(ligne[10])
                surface.append(ligne[38]) #39 = surface réelle bati
                if (type(ligne[10]) != float):
                    if (ligne[38] > 0 and float(ligne[10].replace(',', '.')) > 0):
                        prixm2.append(float(ligne[10].replace(',', '.'))/ligne[38])
                else:
                    if (ligne[38] > 0 and ligne[10] > 0):
                        prixm2.append(ligne[10]/ligne[38])
                rooms.append(ligne[39]) # 4° = nombre de pièces principales
            

        if len(valeurfonciere) >0:
            city['nbtrans'+strend] = len(valeurfonciere)
            city['prixmin'+strend] = np.min(valeurfonciere)
            city['prixmax'+strend] = np.max(valeurfonciere)
            city['prixmoy'+strend] = np.mean(valeurfonciere)
            city['surfmin'+strend] = np.min(surface)
            city['surfmax'+strend] = np.max(surface)
            city['surfmoy'+strend] = np.mean(surface)
            if len(prixm2) >0:
                city['mdeumin'+strend] = np.min(prixm2)
                city['mdeumax'+strend] = np.max(prixm2)
            else: 
                city['mdeumin'+strend] = None
                city['mdeumax'+strend] = None
            city['piecmin'+strend] = np.min(rooms)
            city['piecmax'+strend] = np.max(rooms)
            city['piecmoy'+strend] = np.mean(rooms)
        else:
            city['nbtrans'+strend] = None
            city['prixmin'+strend] = None
            city['prixmax'+strend] = None
            city['prixmoy'+strend] = None
            city['surfmin'+strend] = None
            city['surfmax'+strend] = None
            city['surfmoy'+strend] = None
            city['mdeumin'+strend] = None
            city['mdeumax'+strend] = None
            city['mdeumoy'+strend] = None
            city['piecmin'+strend] = None
            city['piecmax'+strend] = None
            city['piecmoy'+strend] = None

    return city

def findcode(elem):
    regionlen=len(str(elem[18]))
    communelen=len(str(elem[19]))
    outputstr = ''
    if (regionlen==1):
        outputstr = outputstr + '0'
    outputstr = outputstr + str(elem[18])
    if (communelen==1):
        outputstr = outputstr + '00'
    if (communelen==2):
        outputstr = outputstr + '0'
    outputstr = outputstr + str(elem[19])
    #print (outputstr)
    return outputstr

def main():
    print("téléchargement des données en cours (environ 2Go)")
    url2022 = "DATA/valeursfoncieres-2022-s1.txt" #"https://www.data.gouv.fr/fr/datasets/r/87038926-fb31-4959-b2ae-7a24321c599a"
    url2021 = "https://www.data.gouv.fr/fr/datasets/r/817204ac-2202-4b4a-98e7-4184d154d98c"
    url2020 = "https://www.data.gouv.fr/fr/datasets/r/90a98de0-f562-4328-aa16-fe0dd1dca60f"
    url2019 = "https://www.data.gouv.fr/fr/datasets/r/3004168d-bec4-44d9-a781-ef16f41856a2"
    url2018 = "https://www.data.gouv.fr/fr/datasets/r/1be77ca5-dc1b-4e50-af2b-0240147e0346"
    url2017 = "https://www.data.gouv.fr/fr/datasets/r/7161c9f2-3d91-4caf-afa2-cfe535807f04"

    data2022 = pd.read_csv(url2022, delimiter="|", low_memory=False)
    #data2021 = pd.read_csv(url2021, delimiter="|", low_memory=False)
    #data2020 = pd.read_csv(url2020, delimiter="|", low_memory=False)
    #data2019 = pd.read_csv(url2019, delimiter="|", low_memory=False)
    #data2018 = pd.read_csv(url2018, delimiter="|", low_memory=False)
    #data2017 = pd.read_csv(url2017, delimiter="|", low_memory=False)

    sorteddata2022 = sortdata(data2022)
    #sorteddata2021 = sortdata(data2021)
    #sorteddata2020 = sortdata(data2020)
    #sorteddata2019 = sortdata(data2019)
    #sorteddata2018 = sortdata(data2018)
    #sorteddata2017 = sortdata(data2017)
        
    realdata2022 = pd.DataFrame.from_dict(calcdata(sorteddata2022), orient='index')
    #realdata2021 = calcdata(sorteddata2021)
    #realdata2020 = calcdata(sorteddata2020)
    #realdata2019 = calcdata(sorteddata2019)
    #realdata2018 = calcdata(sorteddata2018)
    #realdata2017 = calcdata(sorteddata2017)

    #print(realdata2022)

    app = Dash(__name__)

    coords = (46.539758, 2.430331)
    #map = folium.Map(location=coords, tiles='OpenStreetMap', zoom_start=6)
    map = px.choropleth_mapbox(sorteddata2022, geojson = "geojson/communes.geojson", locations = "cp", color = "mdeumoytot", featureidkey = "properties.code",
                               mapbox_style = "carto-positron", zoom = 4, center = {'lat': 47,'lon': 2})


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

    app.run_server(debug=True) #le dashboard s'affiche sur l'url: http://127.0.0.1:8050/

if __name__ == "__main__":
    main()
