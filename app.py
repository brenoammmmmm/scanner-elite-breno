import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="APEXPITCH RADAR", layout="wide")
st.title("🏆 APEXPITCH: RADAR DE OPORTUNIDADES")

# SUA CHAVE VERIFICADA
API_KEY = "7e061e4e93msh7dda34be332134ep1038b9jsn3e9b3ef3677f"

def buscar_livescores():
    # Endereço EXATO para a sua API (Free API Live Football Data)
    url = "https://free-api-live-football-data.p.rapidapi.com/football-get-all-livescores"
    headers = {
        "X-RapidAPI-Key": API_KEY,
        "X-RapidAPI-Host": "free-api-live-football-data.p.rapidapi.com"
    }
    return requests.get(url, headers=headers)

if st.button('🔥 ESCANEAR MERCADO AGORA'):
    with st.spinner('Sincronizando com os estádios...'):
        res = buscar_livescores()
        
        if res.status_code == 200:
            st.success("CONEXÃO ESTABELECIDA COM SUCESSO!")
            # A estrutura desta API coloca os dados em response -> livescore
            dados = res.json().get('response', {}).get('livescore', [])
            
            if dados:
                df = pd.DataFrame(dados)
                st.dataframe(df, use_container_width=True)
            else:
                st.warning("Conectado! Mas não há jogos ao vivo no momento.")
        else:
            st.error(f"Erro {res.status_code}. Verifique a inscrição na API específica.")
