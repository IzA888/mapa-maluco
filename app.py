import asyncio
import aiohttp
import streamlit as st
import folium
from streamlit_folium import st_folium
from folium.plugins import HeatMap, Draw
import pandas as pd
from geopy.geocoders import Nominatim
from datetime import date, timedelta
import requests
from shapely.geometry import shape, Polygon, MultiPolygon, GeometryCollection
import numpy as np

st.set_page_config(page_title="Mapa maluco", layout="centered")

st.title("Mapa")

# dados de exemplo
pontos = pd.DataFrame({
"nome": ["Ponto A", "Ponto B", "Ponto C"],
"lat": [-1.4558, -1.4600, -1.4700],
"lon": [-48.4902, -48.4800, -48.4950],
"cor": ["red", "blue", "green"]
})

heatmap_data = pontos[["lat", "lon"]].values.tolist()

@st.cache_data(ttl=3600)
def consulta_clima(url):
    try:
        res = requests.get(url, timeout=100)
        res.raise_for_status()
        return res.json()
    except requests.exceptions.RequestException as e:
        st.warning("Não foi posível acessar dados climáticos.")
        st.caption(str(e))
        return None
    
async def consulta_clima_async(url):
    try:
        async with aiohttp.ClientSession().get(url, timeout=10) as resp:
            if resp.status != 200:
                return None
            data = await resp.json()
            return data.get("daily", {}).get("cloudcover_mean", [None])[0]
    except Exception:
        return None


def extrair_poligonos(geom):
    if isinstance(geom, Polygon):
        return [geom]

    if isinstance(geom, MultiPolygon):
        return list(geom.geoms)

    if isinstance(geom, GeometryCollection):
        return [g for g in geom.geoms if isinstance(g, Polygon)]

    return []


#criação de mapa (base)
mapa = folium.Map(
location=[-1.4558, -48.4902],
zoom_start=13,
zoom_control=True,
tiles=None
)

# # marcador
# folium.Marker(
#     [latitude, longitude],
#     popup="📍 Belém - PA",
#     tooltip="Clique aqui"
# ).add_to(mapa)


# camadas de mapa
folium.TileLayer(
    tiles="OpenStreetMap",
    attr="© OpenStreetMap contributors",
    name="OpenStreetMap"
).add_to(mapa)

folium.TileLayer(   
    tiles="EsriWorldImagery",
    attr="Esri World Imagery",
    name="Satélite"
).add_to(mapa)

# polígonos interativos
Draw(
    draw_options={
        "polyline": False,
        "rectangle": True,
        "polygon": True,
        "circle": True,
        "marker": True
    }
).add_to(mapa)

# camadas de dados
layer_pontos = folium.FeatureGroup(name="📍 Pontos", overlay=True, control=True)
layer_area = folium.FeatureGroup(name="Área de estudo", overlay=True, control=True)
layer_heat = folium.FeatureGroup(name="🔥 Heatmap", overlay=True, control=True)


layer_pontos.add_to(mapa)
layer_area.add_to(mapa)
layer_heat.add_to(mapa)

#controle de camadas
folium.LayerControl(collapsed=False).add_to(mapa)


# exibição no streamlit e salvar clicks
resultados = st_folium(mapa, use_container_width=True, height=500)

if resultados and resultados.get("last_clicked"):
    lat = resultados["last_clicked"]["lat"]
    lon = resultados["last_clicked"]["lng"]


    # enderço do ponto
    geolocator = Nominatim(user_agent="mapa-maluco-app", timeout=10)
    local = geolocator.reverse((lat, lon), exactly_one=True)

    if local:
        st.success(f"Endereço, provável, do ponto: {local.address}")

    # mardador de endereço
    folium.Marker(
        location=[lat, lon],
        popup=f"📍 {local.address}<br>",
        icon=folium.Icon(color="red", icon="cloud")
    ).add_to(layer_pontos)


# exibir clima do dia anterior
ontem = date.today() - timedelta(days=1)

# capturar polígonos desenhados
if resultados and resultados.get("all_drawings"):
    geojson = resultados["all_drawings"]
    # st.json(geojson) #coodenadas do polígono
    if isinstance(geojson, list) and len(geojson) > 0:
        poligono = shape(geojson[0]["geometry"])
    else:
        poligono = None

    centroide = poligono.centroid.representative_point()
    lat_centro = centroide.y
    lon_centro = centroide.x
    # #garantir ponto dentro do polígono
    # ponto_interno = poligono.representative_point()

    # lat_interno = ponto_interno.y
    # lon_interno = ponto_interno.x

    # consulta API previsão do tempo
    url = (
        "https://api.open-meteo.com/v1/forecast"
        f"?latitude={lat_centro}"
        f"&longitude={lon_centro}"
        f"&daily=temperature_2m_mean"
        f"&start_date={ontem}"
        f"&end_date={ontem}"
        f"&timezone=auto"
    )

    res = consulta_clima(url)

    temp = (
        res.get("daily", {})
            .get("temperature_2m_mean", [None])[0]
        if res else None
        )

    # área com previsão do tempo

    poligonos = extrair_poligonos(poligono)
    #converter polígono - () - em coordenadas para o folium - [] -
    for pol in poligonos:
        coords = list(pol.exterior.coords)
        
        coords_folium = [[lat,lon] for lon, lat in coords]

        folium.Polygon(
            locations=coords_folium,
            weight=4,
            color="purple",
            fill=True,
            fill_opacity=0.4,
            popup=f"Temperatura de ontem: {temp}"
        ).add_to(layer_area)

# limites aproximados de belém
min_lat, max_lat = -1.50, -1.42
min_lon, max_lon = -48.55, -48.45

# consulta API cobertura de nuvens, por ponto, na regiao de belém
for lat in np.linspace(min_lat, max_lat, 6):
    for lon in np.linspace(min_lon, max_lon, 6):

        url = (
            "https://api.open-meteo.com/v1/forecast"
            f"?latitude={lat}" #região de belém
            f"&longitude={lon}"
            f"&daily=cloudcover_mean"
            f"&start_date={ontem}"
            f"&end_date={ontem}"
            f"&timezone=auto"
        )

        clouds = asyncio.run(consulta_clima_async(url))

        # mapa de calor de cobertura de nuvens
        if clouds is None:
            continue
        if not isinstance(clouds, (int, float)):
            continue
        intensidade = clouds / 100 #intensidade normalizada (0-1)
        heatmap_data.append(
                [lat, lon, intensidade] 
            )
    
    heatmap_data_safe = [
        item for item in heatmap_data if isinstance(item, (list, tuple)) and len(item) == 3
    ]

    # camada heatmap
    HeatMap(
        heatmap_data_safe,
        radius=50,
        blur=20,
        max_zoom=13,
        min_opacity=0.5
    ).add_to(layer_heat)