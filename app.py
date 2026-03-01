import streamlit as st
import requests
import pandas as pd

# Configuração de Layout "Dark Mode" Profissional
st.set_page_config(page_title="APEXPITCH PRO RADAR", layout="wide")
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: #ffffff; }
    .stButton>button { width: 100%; background-color: #ff4b4b; color: white; border-radius: 10px; height: 3em; }
    </style>
    """, unsafe_allow_html=True)

st.title("🏆 APEXPITCH: SCANNER DE ELITE")
st.write("---")

API_KEY = "7e061e4e93msh7dda34be332134ep1038b9jsn3e9b3ef3677f"
HOST = "free-api-live-football-data.p.rapidapi.com"

def request_api(endpoint, params=None):
    url = f"https://{HOST}/{endpoint}"
    headers = {"X-RapidAPI-Key": API_KEY, "X-RapidAPI-Host": HOST}
    return requests.get(url, headers=headers, params=params)

# COLUNA LATERAL DE FILTROS
with st.sidebar:
    st.header("🎯 Filtros de Precisão")
    res_paises = request_api("football-get-all-countries")
    if res_paises.status_code == 200:
        paises = res_paises.json().get('response', {}).get('countries', [])
        lista_paises = {p['name']: p['ccode'] for p in paises}
        escolha = st.selectbox("Selecione o País:", ["Selecione..."] + list(lista_paises.keys()))
    else:
        st.error("Erro ao carregar países. Verifique seus créditos.")

# ÁREA PRINCIPAL: ANÁLISE DE JOGOS
if escolha != "Selecione...":
    ccode = lista_paises[escolha]
    if st.button(f'🔥 ESCANEAR LIGAS EM {escolha.upper()}'):
        with st.spinner('Analisando mercados...'):
            res_ligas = request_api("football-get-all-leagues-by-country", params={"ccode": ccode})
            
            if res_ligas.status_code == 200:
                ligas = res_ligas.json().get('response', {}).get('leagues', [])
                if ligas:
                    st.success(f"Radar ativo em {escolha}!")
                    df = pd.DataFrame(ligas)
                    
                    # Filtros de análise surpreendente
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric("Ligas Monitoradas", len(df))
                    with col2:
                        st.metric("Créditos Restantes", "Ver no Painel")
                    
                    st.dataframe(df[['id', 'name', 'ccode']], use_container_width=True)
                else:
                    st.warning("Nenhuma liga encontrada para este mercado agora.")
            else:
                st.error(f"Erro {res_ligas.status_code}. Endpoint bloqueado ou limite atingido.")
else:
    st.info("💡 Escolha um país na barra lateral para iniciar a varredura de elite.")
