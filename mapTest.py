from pyexpat import features
import folium
import requests, json
import urllib.parse

api_url = "https://api-adresse.data.gouv.fr/search/?q="
adr = "53, rue Etienne Marcel, 94210 Saint Maur des Fossés"
r = requests.get(api_url + urllib.parse.quote(adr))

dict_coords = json.loads(r.content.decode('unicode_escape'))

coords = (dict_coords['features'][0]['geometry']['coordinates'][1], dict_coords['features'][0]['geometry']['coordinates'][0])

map = folium.Map(location=coords, tiles='OpenStreetMap', zoom_start=15)
folium.Marker(location = coords, popup="Maison des Pipart").add_to(map)

map.save(outfile='map2.html')