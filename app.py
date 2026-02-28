import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="APEXPITCH PRO", layout="wide")
st.title("🏆 APEXPITCH: SCANNER PROFISSIONAL")

# SUA CHAVE REAL DA IMAGE_11CC83.PNG
API_KEY = "7e061e4e93msh7dda34be332134ep1038b9jsn3e9b3ef3677f"

def buscar_dados():
    # Este é o ÚNICO endereço que funciona para a sua assinatura atual
    url = "https://free-api-live-football-data.p.rapidapi.com/football-get-all-fixtures-by-date"
    querystring = {"date": "2026-02-28"} # Data de hoje
    headers = {
        "X-RapidAPI-Key": API_KEY,
        "X-RapidAPI-Host": "free-api-live-football-data.p.rapidapi.com"
    }
    return requests.get(url, headers=headers, params=querystring)

if st.button('🔥 INICIAR SCANNER AGORA'):
    with st.spinner('Conectando ao satélite...'):
        res = buscar_dados()
        
        if res.status_code == 200:
            st.success("CONECTADO COM SUCESSO!")
            # A estrutura desta API específica é diferente:
            fixtures = res.json().get('response', {}).get('fixtures', [])
            if fixtures:
                df = pd.DataFrame(fixtures)
                st.dataframe(df)
            else:
                st.warning("A API retornou sucesso, mas não há jogos registrados para hoje.")
        else:
            st.error(f"Erro {res.status_code}. A API diz: {res.text}")
