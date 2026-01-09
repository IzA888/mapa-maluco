import streamlit as st
import folium
from streamlit_folium import st_folium
from folium.plugins import HeatMap, Draw
import pandas as pd
from geopy.geocoders import Nominatim
from datetime import date, timedelta
import requests
from shapely.geometry import shape
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

# criação de mapa (base)
# mapa = folium.Map(
#     location=[-1.4558, -48.4902],
#     zoom_start=13,
#     zoom_control=True,
#     tiles=None
# )


# escolha da base
base = st.radio("Base cartográfica", ["OpenStreetMap", "Satélite"],
                horizontal=True) 

# # marcador
# folium.Marker(
#     [latitude, longitude],
#     popup="📍 Belém - PA",
#     tooltip="Clique aqui"
# ).add_to(mapa)

# camadas de mapa condicionais
if base == "OpenStreetMap":
    mapa = folium.Map(
        location=[-1.4558, -48.4902],
        zoom_start=13,
        zoom_control=True,
        tiles="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.pn",
        attr="© OpenStreetMap contributors",
        name="OpenStreetMap"
    )

    # camada marcadores(dependentes)

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
            [-1.450, -48.480],
            [-1.470, -48.480],
            [-1.470, -48.500]
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

    # polígonos interativos
    Draw(
        draw_options={
            "polyline": False,
            "rectangle": True,
            "polygon": True,
            "circle": False,
            "marker": False
        }
    ).add_to(mapa)

# exibição no streamlit e salvar clicks
else:
    mapa = folium.Map(   
        location=[-1.4558, -48.4902],
        zoom_start=12,
        zoom_control=True, 
        tiles="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
        attr="Esri",
        name="Satélite"
        )
    
    # polígonos interativos
    Draw(
        draw_options={
            "polyline": False,
            "rectangle": True,
            "polygon": True,
            "circle": False,
            "marker": False
        }
    ).add_to(mapa)

    resultados = st_folium(mapa, use_container_width=True, height=500)

    if resultados and resultados.get("last_clicked"):
        lat = resultados["last_clicked"]["lat"]
        lon = resultados["last_clicked"]["lng"]

        st.success(f"clique registrado: {lat}, {lon}")

        # enderço do ponto
        geolocator = Nominatim(user_agent="mapa-maluco-app")
        location = geolocator.reverse((lat, lon), exactly_one=True)

        if location:
            st.write("Endereço, provável, do ponto: ", location.address)
            # mardador de endereço
            layer_pontos = folium.FeatureGroup(name="📍 Pontos")
            folium.Marker(
                [lat, lon],
                popup=f"""
                📍 {location.address}<br>
                """,
                icon=folium.Icon(color="blue", icon="cloud")
            ).add_to(layer_pontos)
        layer_pontos.add_to(mapa)

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
            f"?latitute={lat_centro}"
            f"&longitude={lon_centro}"
            f"&daily=temperature_2m_mean"
            f"&start_date={ontem}"
            f"&end_date={ontem}"
            f"&timezone=auto"
        )

        res = requests.get(url).json()

        temp = res.get("daily", {}).get("temperature_2m_mean", [None])[0]

        # área com previsão do tempo
        layer_area = folium.FeatureGroup(name="Área de estudo")

        folium.GeoJson(
            geojson[0],
            color="purple",
            fill=True,
            fill_opacity=0.3,
            popup=f"Temperatura de ontem: {temp}"
        ).add_to(layer_area)

        layer_area.add_to(mapa)

    # limites aproximados de belém
    min_lat, max_lat = -1.50, -1.42
    min_lon, max_lon = -48.55, -48.45

    # consulta API cobertura de nuvens, por ponto, na regiao de belém
    for lat in np.linspace(min_lat, max_lat, 6):
        for lon in np.linspace(min_lon, max_lon, 6):

            url = (
                "https://api.open-meteo.com/v1/forecast"
                f"?latitute={lat}" #região de belém
                f"&longitude={lon}"
                f"&daily=cloudcover_mean"
                f"&start_date={ontem}"
                f"&end_date={ontem}"
                f"&timezone=auto"
            )

            res = requests.get(url).json()

            clouds = res.get("daily", {}).get("cloudcover_mean", [None])[0]

            # mapa de calor de cobertura de nuvens
            if clouds and isinstance(clouds[0], (int, float)):
                heatmap_data.append(
                    [lat, lon, clouds / 100] #intensidade normalizada (0-1)
                )

    # camada heatmap
    layer_heat = folium.FeatureGroup(name="🔥 Heatmap")
    HeatMap(
        heatmap_data,
        radius=50,
        blur=30,
        max_zoom=13
    ).add_to(layer_heat)
    layer_heat.add_to(mapa)
    
#controle de camadas
folium.LayerControl(collapsed=False).add_to(mapa)