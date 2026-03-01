import streamlit as st
import requests
import pandas as pd
import plotly.express as px # Esta é a linha que estava dando erro

st.set_page_config(page_title="APEXPITCH QUANT", layout="wide")

# Estilo Dark Trader
st.markdown("""
    <style>
    .main { background-color: #050505; }
    .stMetric { background: #111; border: 1px solid #ff4b4b; padding: 15px; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

st.title("🏆 APEXPITCH: QUANTITATIVE RADAR")

API_KEY = "7e061e4e93msh7dda34be332134ep1038b9jsn3e9b3ef3677f"
HOST = "free-api-live-football-data.p.rapidapi.com"

# Função de busca segura
def fetch(endpoint, params=None):
    url = f"https://{HOST}/{endpoint}"
    headers = {"X-RapidAPI-Key": API_KEY, "X-RapidAPI-Host": HOST}
    r = requests.get(url, headers=headers, params=params)
    return r.json() if r.status_code == 200 else None

# Sidebar de Elite (imagem 043503)
with st.sidebar:
    st.header("🎯 Filtros de Elite")
    data_p = fetch("football-get-all-countries")
    if data_p:
        paises = {p['name']: p['ccode'] for p in data_p['response']['countries']}
        escolha = st.selectbox("Selecione o País:", ["Selecione..."] + list(paises.keys()))

if escolha != "Selecione...":
    # Aqui o sistema continua a lógica de buscar ligas e mostrar gráficos
    st.success(f"Radar ativado para {escolha}!")
    # O gráfico de pressão usará o plotly.express (px) que acabamos de instalar
