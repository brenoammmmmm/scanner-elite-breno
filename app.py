import streamlit as st
import requests
import pandas as pd

# Configuração visual do seu site
st.set_page_config(page_title="APEXPITCH RADAR", layout="wide")
st.title("🏆 APEXPITCH: RADAR DE OPORTUNIDADES")

# Sua chave mestre validada (imagem 11cc83)
API_KEY = "7e061e4e93msh7dda34be332134ep1038b9jsn3e9b3ef3677f"

def buscar_radar():
    # Este é o ÚNICO endereço que seu painel aprovou com 200 OK (imagem 11c4db)
    url = "https://free-api-live-football-data.p.rapidapi.com/football-get-all-popular-league"
    headers = {
        "X-RapidAPI-Key": API_KEY,
        "X-RapidAPI-Host": "free-api-live-football-data.p.rapidapi.com"
    }
    return requests.get(url, headers=headers)

if st.button('🔥 ESCANEAR MERCADO AGORA'):
    with st.spinner('Sincronizando com os estádios...'):
        res = buscar_radar()
        
        if res.status_code == 200:
            st.success("CONEXÃO ESTABELECIDA!")
            # Estrutura real da sua API conforme a imagem 11c4db
            ligas = res.json().get('response', {}).get('popular_league', [])
            
            if ligas:
                st.write("### 🏟️ Jogos e Ligas Detectados:")
                df = pd.DataFrame(ligas)
                # Exibe a tabela com as informações que a API mandou
                st.dataframe(df, use_container_width=True)
            else:
                st.warning("Conectado, mas a API não retornou jogos ativos no momento.")
        else:
            st.error(f"Erro {res.status_code}. Verifique a aba Authorizations no painel.")
