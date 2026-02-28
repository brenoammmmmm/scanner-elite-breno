import streamlit as st
import requests
import pandas as pd

# CONFIGURAÇÃO VISUAL
st.set_page_config(page_title="APEXPITCH PRO", layout="wide")
st.title("🏆 APEXPITCH: SCANNER PROFISSIONAL")

# SUA CHAVE REAL (Confirmada na imagem 11cc83.png)
API_KEY = "7e061e4e93msh7dda34be332134ep1038b9jsn3e9b3ef3677f"

def buscar_dados():
    # Este é o ÚNICO comando que sua API confirmou que aceita (imagem 11c4db.png)
    url = "https://free-api-live-football-data.p.rapidapi.com/football-players-search"
    querystring = {"search": "Cristiano"} # Teste inicial com um nome conhecido
    headers = {
        "X-RapidAPI-Key": API_KEY,
        "X-RapidAPI-Host": "free-api-live-football-data.p.rapidapi.com"
    }
    return requests.get(url, headers=headers, params=querystring)

if st.button('🔥 INICIAR SCANNER AGORA'):
    with st.spinner('Validando conexão com a API...'):
        res = buscar_dados()
        
        if res.status_code == 200:
            st.success("CONEXÃO ESTABELECIDA COM SUCESSO! (Status 200)")
            # A estrutura desta API coloca os dados em response -> suggestions
            dados = res.json().get('response', {}).get('suggestions', [])
            if dados:
                st.write("Dados recebidos da API:")
                st.dataframe(pd.DataFrame(dados), use_container_width=True)
            else:
                st.warning("Conectado, mas nenhum dado foi retornado para esta pesquisa.")
        else:
            st.error(f"Erro {res.status_code}. Detalhes técnicos: {res.text}")
