import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="APEXPITCH SCANNER", layout="wide")
st.title("🏆 APEXPITCH: RADAR DE OPORTUNIDADES")

# SUA CHAVE VERIFICADA (image_11cc83.png)
API_KEY = "7e061e4e93msh7dda34be332134ep1038b9jsn3e9b3ef3677f"

def buscar_ligas():
    # Usando o endpoint de ligas populares que é o mais estável na sua API
    url = "https://free-api-live-football-data.p.rapidapi.com/football-get-all-popular-league"
    headers = {
        "X-RapidAPI-Key": API_KEY,
        "X-RapidAPI-Host": "free-api-live-football-data.p.rapidapi.com"
    }
    return requests.get(url, headers=headers)

if st.button('🔥 ESCANEAR MERCADO AGORA'):
    with st.spinner('Acessando dados das ligas...'):
        res = buscar_ligas()
        
        if res.status_code == 200:
            st.success("CONEXÃO ESTABELECIDA!")
            # A estrutura da sua API organiza os dados em popular_league
            dados = res.json().get('response', {}).get('popular_league', [])
            
            if dados:
                df = pd.DataFrame(dados)
                st.write("Ligas em Monitoramento:")
                st.dataframe(df, use_container_width=True)
            else:
                st.warning("Conectado, mas nenhuma liga retornada no momento.")
        else:
            st.error(f"Erro na conexão: {res.status_code}. Verifique os endpoints no painel.")
