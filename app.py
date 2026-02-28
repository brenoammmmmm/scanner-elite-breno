import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="APEXPITCH PRO", layout="wide")
st.title("🏆 APEXPITCH: SCANNER PROFISSIONAL")

# SUA CHAVE VERIFICADA (imagem 11cc83.png)
API_KEY = "7e061e4e93msh7dda34be332134ep1038b9jsn3e9b3ef3677f"

def buscar_dados():
    # MUDANÇA CRUCIAL: Usando o endpoint de Livescores que essa API aceita
    url = "https://free-api-live-football-data.p.rapidapi.com/football-get-all-livescores"
    headers = {
        "X-RapidAPI-Key": API_KEY,
        "X-RapidAPI-Host": "free-api-live-football-data.p.rapidapi.com"
    }
    return requests.get(url, headers=headers)

if st.button('🔥 INICIAR SCANNER AGORA'):
    with st.spinner('Sincronizando com os estádios...'):
        res = buscar_dados()
        
        if res.status_code == 200:
            st.success("CONECTADO COM SUCESSO!")
            # A estrutura desta API coloca os dados em 'livescore'
            dados = res.json().get('response', {}).get('livescore', [])
            if dados:
                df = pd.DataFrame(dados)
                st.dataframe(df, use_container_width=True)
            else:
                st.warning("Conectado, mas não há jogos ao vivo no banco de dados agora.")
        else:
            st.error(f"Erro {res.status_code}. A API diz: {res.text}")
            st.info("Dica: Verifique se você deu 'Subscribe' no endpoint de Livescores no painel da RapidAPI.")
