import streamlit as st
import requests
import pandas as pd

# CONFIGURAÇÃO DE INTERFACE TRADER PRO
st.set_page_config(page_title="APEXPITCH RADAR PRO", layout="wide")
st.markdown("""
    <style>
    .stMetric { background-color: #111; border: 1px solid #ff4b4b; padding: 10px; border-radius: 8px; }
    .status-alert { padding: 20px; border-radius: 10px; background-color: #ff4b4b; color: white; text-align: center; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

st.title("🏆 APEXPITCH: RADAR DE PRESSÃO ABSOLUTA")

API_KEY = "7e061e4e93msh7dda34be332134ep1038b9jsn3e9b3ef3677f"
HOST = "free-api-live-football-data.p.rapidapi.com"

def request_api(endpoint, params=None):
    url = f"https://{HOST}/{endpoint}"
    headers = {"X-RapidAPI-Key": API_KEY, "X-RapidAPI-Host": HOST}
    return requests.get(url, headers=headers, params=params)

# 1. CENTRAL DE FILTROS (SIDEBAR)
with st.sidebar:
    st.header("🎯 Filtros de Elite")
    res_p = request_api("football-get-all-countries")
    if res_p.status_code == 200:
        paises = {p['name']: p['ccode'] for p in res_p.json()['response']['countries']}
        escolha_pais = st.selectbox("Escolha o País:", ["Selecione..."] + list(paises.keys()))
    else:
        st.error("Erro ao conectar. Verifique seus créditos no painel.")

# 2. LÓGICA DE ANÁLISE EM TEMPO REAL
if escolha_pais != "Selecione...":
    ccode = paises[escolha_pais]
    res_l = request_api("football-get-all-leagues-by-country", params={"ccode": ccode})
    
    if res_l.status_code == 200:
        ligas = res_l.json()['response']['leagues']
        liga_txt = st.selectbox("Selecione a Liga:", [f"{l['name']} (ID: {l['id']})" for l in ligas])
        liga_id = liga_txt.split("ID: ")[1].replace(")", "")

        if st.button('🔥 ESCANEAR JOGOS E PRESSÃO'):
            res_live = request_api("football-get-all-livescores-by-league", params={"league_id": liga_id})
            
            if res_live.status_code == 200:
                jogos = res_live.json()['response'].get('livescore', [])
                if jogos:
                    for jogo in jogos:
                        with st.container():
                            # DADOS BÁSICOS
                            home = jogo['home_name']
                            away = jogo['away_name']
                            score = f"{jogo['home_score']} - {jogo['away_score']}"
                            tempo = int(jogo.get('time', 0))
                            
                            # CÁLCULO DE PRESSÃO ESTIMADA
                            # (Se a API liberar ataques, calculamos APM. Se não, usamos tendência de tempo)
                            st.subheader(f"🏟️ {home} {score} {away}")
                            
                            col1, col2, col3 = st.columns(3)
                            col1.metric("Minuto", f"{tempo}'")
                            
                            # ALERTA DE GOL IMINENTE
                            if tempo > 70 and abs(int(jogo['home_score']) - int(jogo['away_score'])) <= 1:
                                col2.markdown('<div class="status-alert">🔥 ZONA DE GOL!</div>', unsafe_allow_html=True)
                                # Alerta Sonoro
                                st.components.v1.html("""<audio autoplay><source src="https://www.soundjay.com/buttons/beep-01a.mp3" type="audio/mpeg"></audio>""", height=0)
                            else:
                                col2.metric("Status", "Monitorando")
                            
                            col3.metric("Sugestão", "Over 0.5 FT" if tempo > 75 else "Analisando")
                            st.progress(min(tempo, 100) / 100)
                            st.divider()
                else:
                    st.warning("Nenhum jogo ao vivo nesta liga no momento.")
else:
    st.info("💡 Use a barra lateral para selecionar o mercado e ativar o Scanner.")
