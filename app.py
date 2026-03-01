import streamlit as st
import requests
import pandas as pd

# Interface de Alta Performance
st.set_page_config(page_title="APEXPITCH PRO", layout="wide")
st.markdown("""
    <style>
    .stMetric { background-color: #0e1117; border: 1px solid #ff4b4b; padding: 10px; border-radius: 5px; }
    .stAlert { background-color: #ff4b4b; color: white; }
    </style>
    """, unsafe_allow_html=True)

st.title("🏆 APEXPITCH: RADAR DE PRESSÃO V3")

API_KEY = "7e061e4e93msh7dda34be332134ep1038b9jsn3e9b3ef3677f"
HOST = "free-api-live-football-data.p.rapidapi.com"

def request_api(endpoint, params=None):
    url = f"https://{HOST}/{endpoint}"
    headers = {"X-RapidAPI-Key": API_KEY, "X-RapidAPI-Host": HOST}
    return requests.get(url, headers=headers, params=params)

# 1. BARRA LATERAL - GESTÃO DE DADOS
with st.sidebar:
    st.header("🎯 Central de Comando")
    res_p = request_api("football-get-all-countries")
    if res_p.status_code == 200:
        paises_dict = {p['name']: p['ccode'] for p in res_p.json()['response']['countries']}
        pais_nome = st.selectbox("Selecione o País:", ["Selecione..."] + list(paises_dict.keys()))
    else:
        st.error("Erro de conexão. Verifique o limite de 100 requisições.")

# 2. LÓGICA DE ESCANEAMENTO
if pais_nome != "Selecione...":
    ccode = paises_dict[pais_nome]
    res_l = request_api("football-get-all-leagues-by-country", params={"ccode": ccode})
    
    if res_l.status_code == 200:
        ligas = res_l.json()['response']['leagues']
        liga_escolhida = st.selectbox("Ligas Ativas:", [f"{l['name']} (ID: {l['id']})" for l in ligas])
        liga_id = liga_escolhida.split("ID: ")[1].replace(")", "")

        if st.button('🔥 INICIAR VARREDURA DE PRESSÃO'):
            res_live = request_api("football-get-all-livescores-by-league", params={"league_id": liga_id})
            
            if res_live.status_code == 200:
                jogos = res_live.json()['response'].get('livescore', [])
                if jogos:
                    for jogo in jogos:
                        # ANÁLISE DE PRESSÃO (POWER SURGE)
                        # Calculamos o risco com base no tempo (minutos finais = maior pressão)
                        tempo = int(jogo.get('time', 0))
                        placar_apertado = abs(int(jogo['home_score']) - int(jogo['away_score'])) <= 1
                        pressao = "BAIXA"
                        
                        if tempo > 75 and placar_apertado:
                            pressao = "MÁXIMA - GOL IMINENTE!"
                            st.balloons() # Efeito visual de oportunidade
                            # ALERTA SONORO (O segredo do Nível 3)
                            st.components.v1.html("""<audio autoplay><source src="https://www.soundjay.com/buttons/beep-01a.mp3" type="audio/mpeg"></audio>""", height=0)
                        
                        # EXIBIÇÃO PRO
                        with st.expander(f"⚽ {jogo['home_name']} {jogo['home_score']} x {jogo['away_score']} {jogo['away_name']} | {tempo}'", expanded=True):
                            c1, c2, c3 = st.columns(3)
                            c1.metric("Status de Pressão", pressao)
                            c2.metric("Tempo", f"{tempo}'")
                            c3.metric("Oportunidade", "OVER 0.5" if tempo > 70 else "Aguardar")
                else:
                    st.warning("Sem jogos ao vivo nesta liga.")
            else:
                st.error("Não foi possível acessar os livescores agora.")
else:
    st.info("💡 Escolha um país na lateral para ativar o radar.")
