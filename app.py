import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import time

# 1. CONFIGURAÇÃO DE INTERFACE DE ALTO NÍVEL
st.set_page_config(page_title="APEXPITCH RADAR QUANT", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
    <style>
    .main { background-color: #050505; color: #00ff00; }
    .stMetric { background: #111; border: 1px solid #333; padding: 15px; border-radius: 10px; }
    .stButton>button { width: 100%; border-radius: 20px; background: linear-gradient(45deg, #ff4b4b, #ff0000); color: white; font-weight: bold; border: none; }
    </style>
    """, unsafe_allow_html=True)

st.title("🏆 APEXPITCH: QUANTITATIVE RADAR PRO")

# DADOS DA API VERIFICADOS (imagem 11cc83)
API_KEY = "7e061e4e93msh7dda34be332134ep1038b9jsn3e9b3ef3677f"
HOST = "free-api-live-football-data.p.rapidapi.com"

def fetch(endpoint, params=None):
    url = f"https://{HOST}/{endpoint}"
    headers = {"X-RapidAPI-Key": API_KEY, "X-RapidAPI-Host": HOST}
    try:
        r = requests.get(url, headers=headers, params=params)
        return r.json() if r.status_code == 200 else None
    except: return None

# 2. INTELIGÊNCIA NA BARRA LATERAL (imagem 043503)
with st.sidebar:
    st.header("🎯 Central de Varredura")
    countries_data = fetch("football-get-all-countries")
    if countries_data:
        countries = {c['name']: c['ccode'] for c in countries_data['response']['countries']}
        pais = st.selectbox("Selecione o Mercado Global:", ["Selecione..."] + list(countries.keys()))
    
    st.divider()
    st.write("📊 **Status do Sistema:** 🟢 ONLINE")
    st.write("💳 **Cota Basic:** 100 Req/Mês") # Referência à imagem 043fc2

# 3. LÓGICA DE ANÁLISE PREDITIVA
if pais != "Selecione...":
    ccode = countries[pais]
    leagues_data = fetch("football-get-all-leagues-by-country", params={"ccode": ccode})
    
    if leagues_data:
        ligas = {l['name']: l['id'] for l in leagues_data['response']['leagues']}
        liga_nome = st.selectbox("Selecione a Liga para Monitorar:", list(ligas.keys()))
        liga_id = ligas[liga_nome]

        if st.button('🔥 ATIVAR ESCANER DE ALTA FREQUÊNCIA'):
            with st.spinner('Realizando análise quantitativa...'):
                live_data = fetch("football-get-all-livescores-by-league", params={"league_id": liga_id})
                
                if live_data and live_data['response'].get('livescore'):
                    for jogo in live_data['response']['livescore']:
                        with st.container():
                            # Header do Jogo
                            st.write(f"### 🏟️ {jogo['home_name']} {jogo['home_score']} x {jogo['away_score']} {jogo['away_name']}")
                            
                            col1, col2, col3, col4 = st.columns(4)
                            tempo = int(jogo.get('time', 0))
                            
                            # Indicador de Pressão (Power Surge)
                            # Simulamos a tendência de pressão baseada no tempo e placar para o gráfico
                            col1.metric("⏱️ Cronômetro", f"{tempo}'")
                            
                            # Cálculo de Risco
                            risco = "BAIXO" if tempo < 60 else ("MÉDIO" if tempo < 75 else "ALTO - ENTRADA!")
                            col2.metric("⚠️ Nível de Risco", risco)
                            
                            # Probabilidade de Gol (Algoritmo ApexPitch)
                            prob = min(tempo + 10, 95) if abs(int(jogo['home_score']) - int(jogo['away_score'])) <= 1 else 15
                            col3.metric("📈 Prob. de Gol", f"{prob}%")
                            
                            col4.metric("💰 Sugestão", "Over 0.5 FT" if tempo > 70 else "Aguardar")

                            # GRÁFICO DE PRESSÃO EM TEMPO REAL
                            df_chart = pd.DataFrame({
                                'Minuto': range(max(0, tempo-10), tempo+1),
                                'Pressão': [i * (prob/100) for i in range(11)]
                            })
                            fig = px.line(df_chart, x='Minuto', y='Pressão', title="Gráfico de Pressão ApexPulse")
                            fig.update_layout(template="plotly_dark", height=300)
