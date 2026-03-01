import streamlit as st
import requests
import pandas as pd

# Interface Profissional e Estável
st.set_page_config(page_title="APEXPITCH RADAR", layout="wide")
st.title("🏆 APEXPITCH: RADAR DE OPORTUNIDADES")

# Sua chave mestre validada (conforme imagem 11cc83)
API_KEY = "7e061e4e93msh7dda34be332134ep1038b9jsn3e9b3ef3677f"

def buscar_paises():
    # Único endereço que seu plano Basic aprovou com Status 200 (imagem 05213d)
    url = "https://free-api-live-football-data.p.rapidapi.com/football-get-all-countries"
    headers = {
        "X-RapidAPI-Key": API_KEY,
        "X-RapidAPI-Host": "free-api-live-football-data.p.rapidapi.com"
    }
    return requests.get(url, headers=headers)

if st.button('🌍 ESCANEAR MERCADO GLOBAL'):
    with st.spinner('Acessando dados...'):
        res = buscar_paises()
        
        if res.status_code == 200:
            st.success("CONEXÃO ESTABELECIDA COM SUCESSO!")
            # Estrutura de resposta confirmada (conforme imagem 051a16)
            paises = res.json().get('response', {}).get('countries', [])
            
            if paises:
                st.write("### Mercados Disponíveis (Plano Basic Ativo):")
                df = pd.DataFrame(paises)
                st.dataframe(df, use_container_width=True)
            else:
                st.warning("Conectado, mas sem dados. Aguarde 1 minuto.")
        else:
            st.error(f"Erro {res.status_code}. Você atingiu o limite de 100 consultas mensais do plano Basic.")
