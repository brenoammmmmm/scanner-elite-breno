import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="APEXPITCH LIVE", layout="wide")
st.title("🏆 APEXPITCH: SCANNER PROFISSIONAL")

# Sua chave que aparece na imagem image_11cc83.png
API_KEY = "7e061e4e93msh7dda34be332134ep1038b9jsn3e9b3ef3677f"

def buscar_dados():
    # Endereço ajustado para a API que você assinou (Free API Live Football Data)
    url = "https://free-api-live-football-data.p.rapidapi.com/football-get-all-popular-league"
    headers = {
        "X-RapidAPI-Key": API_KEY,
        "X-RapidAPI-Host": "free-api-live-football-data.p.rapidapi.com"
    }
    return requests.get(url, headers=headers)

if st.button('🔥 INICIAR SCANNER AGORA'):
    res = buscar_dados()
    
    if res.status_code == 200:
        st.success("CONECTADO COM SUCESSO!")
        dados = res.json().get('response', {}).get('popular_league', [])
        if dados:
            st.dataframe(pd.DataFrame(dados))
        else:
            st.warning("Nenhuma liga popular com jogos agora.")
    else:
        st.error(f"Erro {res.status_code}. Verifique a inscrição na API específica.")
