import streamlit as st
import requests
import pandas as pd

# 1. ESTILO DO SCANNER
st.set_page_config(page_title="APEXPITCH RADAR", layout="wide")
st.title("🏆 APEXPITCH: RADAR DE OPORTUNIDADES")

# SUA CHAVE QUE FUNCIONOU (image_11cc83.png)
API_KEY = "7e061e4e93msh7dda34be332134ep1038b9jsn3e9b3ef3677f"

def buscar_dados_vivos():
    # Este é o endpoint mais provável de conter jogos reais na sua API
    url = "https://free-api-live-football-data.p.rapidapi.com/football-get-all-popular-league"
    headers = {
        "X-RapidAPI-Key": API_KEY,
        "X-RapidAPI-Host": "free-api-live-football-data.p.rapidapi.com"
    }
    return requests.get(url, headers=headers)

# 2. BOTÃO DE VARREDURA
if st.button('🔥 ESCANEAR JOGOS AGORA'):
    with st.spinner('Acessando base de dados...'):
        res = buscar_dados_vivos()
        
        if res.status_code == 200:
            st.success("CONEXÃO ESTABELECIDA!")
            # A estrutura da sua API confirmada na imagem 11c4db.png
            dados = res.json().get('response', {}).get('popular_league', [])
            
            if dados:
                df = pd.DataFrame(dados)
                st.write("### 🏟️ Ligas com Jogos Ativos")
                st.dataframe(df, use_container_width=True)
            else:
                st.warning("Conectado! Mas a API não retornou jogos nas ligas populares agora.")
        else:
            st.error(f"Erro {res.status_code}. A API não reconheceu este comando.")
