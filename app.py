import streamlit as st
import requests
import pandas as pd

# Interface Blindada
st.set_page_config(page_title="APEXPITCH RADAR", layout="wide")
st.title("🏆 APEXPITCH: RADAR DE OPORTUNIDADES")

# Sua chave mestre validada (conforme imagem 11cc83)
API_KEY = "7e061e4e93msh7dda34be332134ep1038b9jsn3e9b3ef3677f"

def buscar_base():
    # Este é o ÚNICO endereço que seu painel aprovou com Status 200 (imagem 05213d)
    url = "https://free-api-live-football-data.p.rapidapi.com/football-get-all-countries"
    headers = {
        "X-RapidAPI-Key": API_KEY,
        "X-RapidAPI-Host": "free-api-live-football-data.p.rapidapi.com"
    }
    return requests.get(url, headers=headers)

if st.button('🔥 ESCANEAR MERCADO GLOBAL'):
    with st.spinner('Acessando dados...'):
        res = buscar_base()
        
        if res.status_code == 200:
            st.success("CONEXÃO ESTABELECIDA!")
            # Estrutura exata da resposta (conforme imagem 051a16)
            paises = res.json().get('response', {}).get('countries', [])
            
            if paises:
                st.write("### Selecione o mercado para operar:")
                st.dataframe(pd.DataFrame(paises), use_container_width=True)
            else:
                st.warning("Conectado, mas nenhum dado retornado. Tente novamente em 1 minuto.")
        else:
            st.error(f"Erro {res.status_code}. A API rejeitou o comando.")
