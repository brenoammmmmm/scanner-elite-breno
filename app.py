import streamlit as st
import requests
import pandas as pd

# 1. CONFIGURAÇÃO VISUAL DE ELITE (DARK MODE)
st.set_page_config(page_title="APEXPITCH ELITE", layout="wide")
st.markdown("""
    <style>
    .main { background-color: #000000; }
    h1 { color: #D4AF37; }
    </style>
    """, unsafe_allow_html=True)

st.title("🏆 APEXPITCH: SCANNER PROFISSIONAL V1")

# SUA CHAVE DA API
API_KEY = "7e061e4e93msh7dda34be332134ep1038b9jsn3e9b3ef3677f"

def buscar_dados_live():
    url = "https://api-football-v1.p.rapidapi.com/v3/fixtures?live=all"
    headers = {
        "X-RapidAPI-Key": API_KEY,
        "X-RapidAPI-Host": "api-football-v1.p.rapidapi.com"
    }
    res = requests.get(url, headers=headers)
    return res.json().get('response', [])

# 2. BOTÃO DE ESCANEAMENTO
if st.button('🚀 ESCANEAR MERCADO AGORA'):
    dados = buscar_dados_live()
    
    if dados:
        jogos_processados = []
        for j in dados:
            # MÉTRICA INOVADORA: POWER SURGE (Cálculo de Pressão)
            # Soma gols, tempo e um fator de aceleração
            elapsed = j['fixture']['status']['elapsed']
            gols_total = j['goals']['home'] + j['goals']['away']
            power_surge = (gols_total + 1) * (elapsed / 45) # Exemplo de métrica viva
            
            jogos_processados.append({
                "Min": f"{elapsed}'",
                "Confronto": f"{j['teams']['home']['name']} x {j['teams']['away']['name']}",
                "Placar": f"{j['goals']['home']} - {j['goals']['away']}",
                "Power Surge ⚡": round(power_surge, 2),
                "Liga": j['league']['name']
            })
        
        # Exibe a tabela ordenada pela maior pressão
        df = pd.DataFrame(jogos_processados).sort_values(by="Power Surge ⚡", ascending=False)
        st.dataframe(df, use_container_width=True)
        st.success("Análise de tempo real concluída!")
    else:
        st.warning("Nenhum jogo ao vivo encontrado no momento.")
