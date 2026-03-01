import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="APEXPITCH ELITE", layout="wide")

# CSS para Estilo Hacker/Profissional
st.markdown("""
    <style>
    .stMetric { background-color: #1e2130; padding: 15px; border-radius: 10px; border-left: 5px solid #ff4b4b; }
    .stDataFrame { border: 1px solid #ff4b4b; }
    </style>
    """, unsafe_allow_html=True)

st.title("🏆 APEXPITCH: SCANNER DE ELITE V2")

API_KEY = "7e061e4e93msh7dda34be332134ep1038b9jsn3e9b3ef3677f"
HOST = "free-api-live-football-data.p.rapidapi.com"

def request_api(endpoint, params=None):
    url = f"https://{HOST}/{endpoint}"
    headers = {"X-RapidAPI-Key": API_KEY, "X-RapidAPI-Host": HOST}
    return requests.get(url, headers=headers, params=params)

# 1. BARRA LATERAL (Filtro por País)
with st.sidebar:
    st.header("🎯 Radar de Precisão")
    res_p = request_api("football-get-all-countries")
    if res_p.status_code == 200:
        paises_dict = {p['name']: p['ccode'] for p in res_p.json()['response']['countries']}
        pais_nome = st.selectbox("Escolha o Mercado:", ["Selecione..."] + list(paises_dict.keys()))
    else:
        st.error("Limite da API atingido no painel.")

# 2. SELEÇÃO DE LIGA E JOGOS AO VIVO
if pais_nome != "Selecione...":
    ccode = paises_dict[pais_nome]
    res_l = request_api("football-get-all-leagues-by-country", params={"ccode": ccode})
    
    if res_l.status_code == 200:
        ligas = res_l.json()['response']['leagues']
        liga_escolhida = st.selectbox("Selecione a Liga Ativa:", [f"{l['name']} (ID: {l['id']})" for l in ligas])
        liga_id = liga_escolhida.split("ID: ")[1].replace(")", "")

        if st.button('📡 ESCANEAR PRESSÃO AO VIVO'):
            # BUSCANDO JOGOS EM TEMPO REAL DA LIGA SELECIONADA
            res_live = request_api("football-get-all-livescores-by-league", params={"league_id": liga_id})
            
            if res_live.status_code == 200:
                jogos = res_live.json()['response'].get('livescore', [])
                if jogos:
                    for jogo in jogos:
                        with st.container():
                            col1, col2, col3 = st.columns([2,1,2])
                            col1.subheader(jogo['home_name'])
                            col2.title(f"{jogo['home_score']} - {jogo['away_score']}")
                            col3.subheader(jogo['away_name'])
                            
                            # CÁLCULO DE PRESSÃO (POWER SURGE)
                            # Nota: Se a API não entregar ataques perigosos no Basic, 
                            # usamos o volume de jogo e tempo.
                            st.progress(min(int(jogo.get('time', 0)) * 1, 100), text=f"Tempo de Jogo: {jogo['time']}'")
                            st.divider()
                else:
                    st.warning("Nenhum jogo acontecendo nesta liga agora.")
            else:
                st.error("Esta liga não possui jogos ao vivo no momento.")

else:
    st.info("💡 Selecione um país na barra lateral para começar a análise de mercado.")
