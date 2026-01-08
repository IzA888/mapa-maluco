import streamlit as st
import folium
from streamlit_folium import st_folium
from folium.plugins import HeatMap
import pandas as pd

st.set_page_config(page_title="Mapa maluco", layout="centered")

st.title("Mapa")

# cdados de exemplo
pontos = pd.DataFrame({
    "nome": ["Ponto A", "Ponto B", "Ponto C"],
    "lat": [-1.4558, -1.4600, -1.4700],
    "lon": [-48.4902, -48.4800, -48.4950],
    "cor": ["red", "blue", "green"]
})

heatmap_data = pontos[["lat", "lon"]].values.tolist()

# criação de mapa
mapa = folium.Map(
    location=[-1.4558, -48.4902],
    zoom_start=13,
    zoom_control=True,
    title=None
)

# # marcador
# folium.Marker(
#     [latitude, longitude],
#     popup="📍 Belém - PA",
#     tooltip="Clique aqui"
# ).add_to(mapa)

# camadas de mapa
folium.TileLayer(
    "OpenStreetMap",
    name="🌍 OpenStreetMap"
).add_to(mapa)

folium.TileLayer(    
    tiles="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
    attr="Esri",
    name="Satélite"
    ).add_to(mapa)

# camada marcadores
layer_pontos = folium.FeatureGroup(name="📍 Pontos")

for _, row in pontos.iterrows():
    folium.Marker(
        location=[row["lat"], row["lon"]],
        popup=row["nome"],
        icon=folium.Icon(color=row["cor"], icon="icon-sign")
    ).add_to(layer_pontos)

layer_pontos.add_to(mapa)

# camada polígono
layer_area = folium.FeatureGroup(name="Área de estudo")

folium.Polygon(
    locations=[
        [-1.450, -48.500],
        [1.450, -48.480],
        [-1.470, -48.480],
        [-1.470,48.500]
        ],
    color="purple",
    fill=True,
    fill_opacity=0.3,
    popup="Área de interesse"
).add_to(layer_area)

layer_area.add_to(mapa)

# camada heatmap
layer_heat = folium.FeatureGroup(name="🔥 Heatmap")

HeatMap(
    heatmap_data,
    radius=30
).add_to(layer_heat)

layer_heat.add_to(mapa)

#controle de camadas
folium.LayerControl(collapsed=False).add_to(mapa)

# exibição no streamlit
st_folium(mapa, use_container_width=True, height=500)