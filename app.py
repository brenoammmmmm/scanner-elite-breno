import streamlit as st
import requests
import pandas as pd

# 1. ESTILO DO SCANNER
st.set_page_config(page_title="APEXPITCH RADAR", layout="wide")
st.title("🏆 APEXPITCH: RADAR DE OPORTUNIDADES")

# SUA CHAVE QUE FUNCIONOU (image_11cc83.png)
API_KEY = "7e061e4e93msh7dda34be332134ep1038b9jsn3e9b3ef3677f"

def buscar_mercado_ao_vivo():
    # Usando o endpoint de Ligas Populares que sua API aceita
    url = "https://free-api-live-football-data.p.rapidapi.com/football-get-all-popular-league"
    headers = {
        "X-RapidAPI-Key": API_KEY,
        "X-RapidAPI-Host": "free-api-live-football-data.p.rapidapi.com"
    }
    return requests.get(url, headers=headers)

# 2. BOTÃO DE VARREDURA
if st.button('🔥 ESCANEAR MERCADO AGORA'):
    with st.spinner('Rastreando oportunidades mundiais...'):
        res = buscar_mercado_ao_vivo()
        
        if res.status_code == 200:
            st.success("DADOS RECEBIDOS COM SUCESSO!")
            # A estrutura da sua API para ligas populares:
            ligas = res.json().get('response', {}).get('popular_league', [])
            
            if ligas:
                st.write("### 🏟️ Jogos e Ligas em Monitoramento")
                df = pd.DataFrame(ligas)
                # Exibe a tabela completa com as informações
                st.dataframe(df, use_container_width=True)
            else:
                st.warning("Conectado! Mas nenhuma liga com jogos ativos no momento.")
        else:
            st.error(f"Erro {res.status_code}. Verifique sua inscrição no painel.")
