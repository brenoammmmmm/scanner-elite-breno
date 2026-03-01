import streamlit as st
import requests
import pandas as pd

# CONFIGURAÇÃO VISUAL PROFISSIONAL
st.set_page_config(page_title="APEXPITCH RADAR", layout="wide")
st.title("🏆 APEXPITCH: RADAR DE OPORTUNIDADES")

# SUA CHAVE VERIFICADA (image_11cc83.png)
API_KEY = "7e061e4e93msh7dda34be332134ep1038b9jsn3e9b3ef3677f"

def buscar_paises():
    # Este é o comando que deu Status 200 no seu painel (image_05213d.png)
    url = "https://free-api-live-football-data.p.rapidapi.com/football-get-all-countries"
    headers = {
        "X-RapidAPI-Key": API_KEY,
        "X-RapidAPI-Host": "free-api-live-football-data.p.rapidapi.com"
    }
    return requests.get(url, headers=headers)

if st.button('🌍 ESCANEAR PAÍSES DISPONÍVEIS'):
    with st.spinner('Acessando base de dados global...'):
        res = buscar_paises()
        
        if res.status_code == 200:
            st.success("CONEXÃO ESTABELECIDA COM SUCESSO!")
            # A estrutura desta API coloca os países em response -> countries
            paises = res.json().get('response', {}).get('countries', [])
            
            if paises:
                df = pd.DataFrame(paises)
                st.write("Selecione um país para monitorar ligas:")
                st.dataframe(df, use_container_width=True)
            else:
                st.warning("Conectado, mas nenhum país foi retornado agora.")
        else:
            st.error(f"Erro na conexão: {res.status_code}. Verifique os endpoints no painel.")
