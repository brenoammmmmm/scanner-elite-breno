import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="APEXPITCH RADAR", layout="wide")
st.title("🏆 APEXPITCH: RADAR DE OPORTUNIDADES")

# Sua chave mestre validada (imagem 11cc83)
API_KEY = "7e061e4e93msh7dda34be332134ep1038b9jsn3e9b3ef3677f"

def api_request(endpoint, params=None):
    url = f"https://free-api-live-football-data.p.rapidapi.com/{endpoint}"
    headers = {
        "X-RapidAPI-Key": API_KEY,
        "X-RapidAPI-Host": "free-api-live-football-data.p.rapidapi.com"
    }
    return requests.get(url, headers=headers, params=params)

# 1. BUSCA DE PAÍSES (O que já deu certo na imagem 049a5c)
res_paises = api_request("football-get-all-countries")

if res_paises.status_code == 200:
    paises_data = res_paises.json().get('response', {}).get('countries', [])
    df_paises = pd.DataFrame(paises_data)
    
    # Criar um menu de seleção no site
    lista_nomes = df_paises['name'].tolist()
    pais_selecionado = st.selectbox("Escolha um país para escanear ligas ao vivo:", ["Selecione..."] + lista_nomes)

    if pais_selecionado != "Selecione...":
        ccode = df_paises[df_paises['name'] == pais_selecionado]['ccode'].values[0]
        
        if st.button(f'🔍 ESCANEAR LIGAS EM {pais_selecionado.upper()}'):
            # Endpoint específico para ligas por país desta API
            res_ligas = api_request("football-get-all-leagues-by-country", params={"ccode": ccode})
            
            if res_ligas.status_code == 200:
                ligas = res_ligas.json().get('response', {}).get('leagues', [])
                if ligas:
                    st.success(f"Ligas encontradas em {pais_selecionado}!")
                    st.dataframe(pd.DataFrame(ligas), use_container_width=True)
                else:
                    st.warning(f"Sem ligas ativas para {pais_selecionado} no momento.")
            else:
                st.error(f"Erro {res_ligas.status_code} ao buscar ligas.")
else:
    st.error("Erro ao conectar com a API. Verifique sua chave no painel.")
