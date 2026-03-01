import streamlit as st
import requests
import pandas as pd

# Configuração de interface profissional
st.set_page_config(page_title="APEXPITCH RADAR", layout="wide")
st.title("🏆 APEXPITCH: RADAR DE OPORTUNIDADES")

# Sua chave mestre validada (conforme imagem 11cc83)
API_KEY = "7e061e4e93msh7dda34be332134ep1038b9jsn3e9b3ef3677f"

def buscar_paises():
    # Este é o ÚNICO endereço que seu painel aprovou com Status 200 (imagem 05213d)
    url = "https://free-api-live-football-data.p.rapidapi.com/football-get-all-countries"
    headers = {
        "X-RapidAPI-Key": API_KEY,
        "X-RapidAPI-Host": "free-api-live-football-data.p.rapidapi.com"
    }
    return requests.get(url, headers=headers)

if st.button('🌍 ESCANEAR MERCADO GLOBAL'):
    with st.spinner('Acessando satélites da API...'):
        res = buscar_paises()
        
        if res.status_code == 200:
            st.success("CONEXÃO ESTABELECIDA!")
            # Estrutura exata da resposta desta API (conforme imagem 051a16)
            paises = res.json().get('response', {}).get('countries', [])
            
            if paises:
                df = pd.DataFrame(paises)
                st.write("### Selecione um país para abrir as ligas:")
                st.dataframe(df, use_container_width=True)
            else:
                st.warning("Conectado, mas nenhum país foi retornado no momento.")
        else:
            st.error(f"Erro {res.status_code}. Verifique a aba Authorizations no painel.")
