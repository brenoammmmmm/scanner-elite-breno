import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="APEXPITCH DEBUG", layout="wide")
st.title("🏆 APEXPITCH: TESTE DE CONEXÃO AO VIVO")

API_KEY = "7e061e4e93msh7dda34be332134ep1038b9jsn3e9b3ef3677f"

if st.button('📡 TESTAR CONEXÃO AGORA'):
    url = "https://api-football-v1.p.rapidapi.com/v3/fixtures?live=all"
    headers = {
        "X-RapidAPI-Key": API_KEY,
        "X-RapidAPI-Host": "api-football-v1.p.rapidapi.com"
    }
    
    res = requests.get(url, headers=headers)
    
    # Mostra o que a API está dizendo de verdade
    st.write(f"Código de Resposta: {res.status_code}")
    
    if res.status_code == 200:
        dados = res.json().get('response', [])
        if dados:
            st.success(f"SUCESSO! {len(dados)} jogos encontrados.")
            df = pd.DataFrame([{
                "Min": j['fixture']['status']['elapsed'],
                "Jogo": f"{j['teams']['home']['name']} x {j['teams']['away']['name']}",
                "Placar": f"{j['goals']['home']}x{j['goals']['away']}"
            } for j in dados])
            st.dataframe(df, use_container_width=True)
        else:
            st.warning("Conectado, mas a API retornou 0 jogos live agora.")
    elif res.status_code == 403:
        st.error("ERRO 403: Sua chave foi negada. Verifique se o plano Basic está ativo no painel da RapidAPI.")
    else:
        st.error(f"ERRO {res.status_code}: A API está com instabilidade. Tente novamente em instantes.")
