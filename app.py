import streamlit as st
import requests
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="APEXPITCH SCANNER", layout="wide")
st.title("🏆 APEXPITCH: RADAR DE OPORTUNIDADES")

# SUA CHAVE VERIFICADA (imagem 11cc83.png)
API_KEY = "7e061e4e93msh7dda34be332134ep1038b9jsn3e9b3ef3677f"

def buscar_jogos_hoje():
    # Pega a data atual no formato que a API exige (Ex: 2026-02-28)
    hoje = datetime.now().strftime('%Y-%m-%d')
    url = "https://free-api-live-football-data.p.rapidapi.com/football-get-all-fixtures-by-date"
    querystring = {"date": hoje}
    headers = {
        "X-RapidAPI-Key": API_KEY,
        "X-RapidAPI-Host": "free-api-live-football-data.p.rapidapi.com"
    }
    return requests.get(url, headers=headers, params=querystring)

if st.button('🔥 ESCANEAR JOGOS DE HOJE'):
    with st.spinner('Buscando confrontos nos estádios...'):
        res = buscar_jogos_hoje()
        
        if res.status_code == 200:
            st.success("DADOS RECEBIDOS COM SUCESSO!")
            # A estrutura desta API coloca os jogos em response -> fixtures
            jogos = res.json().get('response', {}).get('fixtures', [])
            
            if jogos:
                dados_limpos = []
                for j in jogos:
                    dados_limpos.append({
                        "Horário": j.get('time'),
                        "Campeonato": j.get('league_name'),
                        "Casa": j.get('home_name'),
                        "Placar": f"{j.get('home_score')} x {j.get('away_score')}",
                        "Fora": j.get('away_name'),
                        "Status": j.get('status')
                    })
                
                df = pd.DataFrame(dados_limpos)
                st.dataframe(df, use_container_width=True)
            else:
                st.warning("Nenhum jogo encontrado para a data de hoje.")
        else:
            st.error(f"Erro na conexão: {res.status_code}")
