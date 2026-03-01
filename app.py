import streamlit as st
import requests
import pandas as pd

# Interface Profissional
st.set_page_config(page_title="APEXPITCH RADAR", layout="wide")
st.title("🏆 APEXPITCH: RADAR DE OPORTUNIDADES")

# Sua chave mestre validada (conforme imagem 11cc83)
API_KEY = "7e061e4e93msh7dda34be332134ep1038b9jsn3e9b3ef3677f"

def buscar_radar_principal():
    # Este é o ÚNICO endereço que seu painel aprovou com Status 200 (imagem 11c4db)
    url = "https://free-api-live-football-data.p.rapidapi.com/football-get-all-popular-league"
    headers = {
        "X-RapidAPI-Key": API_KEY,
        "X-RapidAPI-Host": "free-api-live-football-data.p.rapidapi.com"
    }
    return requests.get(url, headers=headers)

if st.button('🔥 ESCANEAR MERCADO AGORA'):
    with st.spinner('Sincronizando com o banco de dados...'):
        res = buscar_radar_principal()
        
        if res.status_code == 200:
            st.success("CONEXÃO ESTABELECIDA!")
            # Estrutura exata da resposta desta API (conforme imagem 11c4db)
            dados = res.json().get('response', {}).get('popular_league', [])
            
            if dados:
                df = pd.DataFrame(dados)
                st.write("### Ligas e Jogos em Monitoramento:")
                st.dataframe(df, use_container_width=True)
            else:
                st.warning("Conectado, mas nenhum jogo foi retornado nas ligas principais agora.")
        else:
            st.error(f"Erro {res.status_code}. A API rejeitou o comando.")
