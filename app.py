import streamlit as st
import requests
import pandas as pd

# 1. ESTILO DO SCANNER
st.set_page_config(page_title="APEXPITCH RADAR", layout="wide")
st.title("🏆 APEXPITCH: RADAR DE OPORTUNIDADES")

# SUA CHAVE QUE FUNCIONOU (image_11cc83.png)
API_KEY = "7e061e4e93msh7dda34be332134ep1038b9jsn3e9b3ef3677f"

def buscar_jogos_importantes():
    # Usando o endpoint de Ligas Populares (onde ficam os jogos principais)
    url = "https://free-api-live-football-data.p.rapidapi.com/football-get-all-popular-league"
    headers = {
        "X-RapidAPI-Key": API_KEY,
        "X-RapidAPI-Host": "free-api-live-football-data.p.rapidapi.com"
    }
    return requests.get(url, headers=headers)

# 2. BOTÃO DE VARREDURA
if st.button('🔥 ESCANEAR JOGOS AO VIVO AGORA'):
    with st.spinner('Rastreando ligas mundiais...'):
        res = buscar_jogos_importantes()
        
        if res.status_code == 200:
            st.success("CONEXÃO ESTABELECIDA COM SUCESSO!")
            # A estrutura da sua API para ligas populares:
            ligas = res.json().get('response', {}).get('popular_league', [])
            
            if ligas:
                st.write("### 🏟️ Ligas e Jogos em Destaque")
                df = pd.DataFrame(ligas)
                # Mostra a tabela com as informações da liga
                st.dataframe(df, use_container_width=True)
            else:
                st.warning("Conectado! Mas não há jogos em destaque no momento.")
        else:
            st.error(f"Erro {res.status_code}. Verifique a aba 'Endpoints' no painel da RapidAPI.")
