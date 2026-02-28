import streamlit as st
import requests
import pandas as pd

# CONFIGURAÇÃO VISUAL
st.set_page_config(page_title="APEXPITCH PRO", layout="wide")
st.title("🏆 APEXPITCH: SCANNER PROFISSIONAL")

# SUA CHAVE REAL (imagem 11cc83.png)
API_KEY = "7e061e4e93msh7dda34be332134ep1038b9jsn3e9b3ef3677f"

def buscar_dados():
    # Este é o comando que sua API aceita segundo a imagem 11c4db.png
    url = "https://free-api-live-football-data.p.rapidapi.com/football-get-all-popular-league"
    headers = {
        "X-RapidAPI-Key": API_KEY,
        "X-RapidAPI-Host": "free-api-live-football-data.p.rapidapi.com"
    }
    return requests.get(url, headers=headers)

if st.button('🔥 INICIAR SCANNER AGORA'):
    with st.spinner('Conectando ao banco de dados...'):
        res = buscar_dados()
        
        if res.status_code == 200:
            st.success("CONECTADO COM SUCESSO!")
            # A estrutura desta API é: response -> popular_league
            dados = res.json().get('response', {}).get('popular_league', [])
            if dados:
                df = pd.DataFrame(dados)
                st.dataframe(df, use_container_width=True)
            else:
                st.warning("Conectado, mas a API não retornou dados no momento.")
        else:
            st.error(f"Erro {res.status_code}. Verifique sua inscrição na API.")
