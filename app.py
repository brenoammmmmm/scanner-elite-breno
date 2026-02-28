import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="APEXPITCH LIVE", layout="wide")
st.title("🏆 APEXPITCH: SCANNER PROFISSIONAL")

# Sua chave verificada
API_KEY = "7e061e4e93msh7dda34be332134ep1038b9jsn3e9b3ef3677f"

def buscar_jogos():
    # Novo endereço corrigido para listar jogos (fixtures)
    url = "https://free-api-live-football-data.p.rapidapi.com/football-get-all-fixtures"
    headers = {
        "X-RapidAPI-Key": API_KEY,
        "X-RapidAPI-Host": "free-api-live-football-data.p.rapidapi.com"
    }
    return requests.get(url, headers=headers)

if st.button('🔥 INICIAR SCANNER AGORA'):
    res = buscar_jogos()
    
    if res.status_code == 200:
        st.success("CONECTADO COM SUCESSO!")
        # Extrai a lista de jogos da resposta da API
        dados = res.json().get('response', {}).get('fixtures', [])
        if dados:
            st.dataframe(pd.DataFrame(dados))
        else:
            st.warning("Nenhum jogo encontrado para hoje.")
    else:
        st.error(f"Erro {res.status_code}. Verifique a URL ou a chave no painel RapidAPI.")
