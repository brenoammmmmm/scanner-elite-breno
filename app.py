import streamlit as st
import requests
import pandas as pd
import time

# DESIGN DARK PRO
st.set_page_config(page_title="APEXPITCH REVOLUTION", layout="wide")
st.markdown("<style>body {background-color: #000; color: #D4AF37;}</style>", unsafe_allow_html=True)

st.title("🏆 APEXPITCH: INTELLIGENCE & ODDS RADAR")

# Sua chave verificada
API_KEY = "7e061e4e93msh7dda34be332134ep1038b9jsn3e9b3ef3677f"

def get_live_data():
    url = "https://api-football-v1.p.rapidapi.com/v3/fixtures"
    querystring = {"live": "all"}
    headers = {"X-RapidAPI-Key": API_KEY, "X-RapidAPI-Host": "api-football-v1.p.rapidapi.com"}
    
    # Tenta 3 vezes caso a API esteja lenta
    for _ in range(3):
        res = requests.get(url, headers=headers, params=querystring)
        if res.status_code == 200:
            return res.json()
        time.sleep(1)
    return None

st.sidebar.header("🎯 FILTROS DE ELITE")
sensibilidade = st.sidebar.slider("Sensibilidade do Alerta (Power Surge)", 5, 50, 15)

if st.button('🔥 ESCANEAR MERCADO MUNDIAL AGORA'):
    with st.spinner('Acessando satélites e estádios...'):
        res = get_live_data()
        
        if res and 'response' in res and len(res['response']) > 0:
            jogos = res['response']
            analise_final = []
            
            for j in jogos:
                tempo = j['fixture']['status']['elapsed']
                casa = j['teams']['home']['name']
                fora = j['teams']['away']['name']
                
                # Cálculo Power Surge
                momentum = (j['goals']['home'] + j['goals']['away'] + 1) * (tempo / 30)
                
                alerta = "⚖️ Estável"
                if tempo > 80 and j['goals']['home'] == j['goals']['away']:
                    alerta = "💎 GOLDEN GOAL"
                elif momentum > sensibilidade:
                    alerta = "⚡ PRESSÃO MÁXIMA"
                
                analise_final.append({
                    "Min": f"{tempo}'",
                    "Confronto": f"{casa} x {fora}",
                    "Placar": f"{j['goals']['home']}-{j['goals']['away']}",
                    "Power Surge ⚡": round(momentum, 2),
                    "Oportunidade": alerta
                })
            
            df = pd.DataFrame(analise_final).sort_values(by="Power Surge ⚡", ascending=False)
            st.success(f"Radar Ativo: {len(jogos)} jogos monitorados!")
            st.dataframe(df, use_container_width=True)
        else:
            st.warning("🔄 A API ainda está processando sua assinatura. Clique novamente em 15 segundos.")
