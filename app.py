import streamlit as st
import requests
import pandas as pd

# CONFIGURAÇÃO VISUAL DARK/GOLD - SUPERIOR AO CORNERPRO
st.set_page_config(page_title="APEXPITCH REVOLUTION", layout="wide")
st.markdown("<style>body {background-color: #000; color: #D4AF37;}</style>", unsafe_allow_html=True)

st.title("🏆 APEXPITCH: O RADAR REVOLUCIONÁRIO")

API_KEY = "7e061e4e93msh7dda34be332134ep1038b9jsn3e9b3ef3677f"

def get_data():
    url = "https://api-football-v1.p.rapidapi.com/v3/fixtures?live=all"
    headers = {"X-RapidAPI-Key": API_KEY, "X-RapidAPI-Host": "api-football-v1.p.rapidapi.com"}
    return requests.get(url, headers=headers).json()

if st.button('🔥 SINCRONIZAR MILHARES DE JOGOS'):
    res = get_data()
    if res and 'response' in res and len(res['response']) > 0:
        jogos = res['response']
        db = []
        for j in jogos:
            tempo = j['fixture']['status']['elapsed']
            casa = j['teams']['home']['name']
            fora = j['teams']['away']['name']
            gols = f"{j['goals']['home']}x{j['goals']['away']}"
            
            # --- LÓGICA DE ESPECIALISTA (O DIFERENCIAL) ---
            # Cálculo de probabilidade de vitória baseado no momentum (exemplo inovador)
            momentum = (tempo / 90) * (j['goals']['home'] + j['goals']['away'] + 1)
            analise = "🔥 FAVORITO PRESSIONANDO" if momentum > 1.5 else "⚖️ JOGO EQUILIBRADO"
            if tempo > 80 and j['goals']['home'] == j['goals']['away']:
                analise = "💎 GOLDEN GOAL (ZOIÃO)"

            db.append({
                "Min": f"{tempo}'",
                "Confronto": f"{casa} x {fora}",
                "Placar": gols,
                "Índice IA": round(momentum, 2),
                "Oportunidade": analise,
                "Liga": j['league']['name']
            })
        
        df = pd.DataFrame(db).sort_values(by="Índice IA", ascending=False)
        st.success(f"Radar ativo! {len(jogos)} jogos rastreados no planeta.")
        st.dataframe(df.style.highlight_max(axis=0, subset=['Índice IA']), use_container_width=True)
    else:
        st.error("Erro: A API não enviou dados. Verifique se clicou em 'Subscribe' no plano Basic da RapidAPI.")
