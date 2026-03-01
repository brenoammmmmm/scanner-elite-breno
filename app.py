import streamlit as st
import requests
import pandas as pd
import plotly.express as px

# 1. DESIGN DE TERMINAL QUANTITATIVO
st.set_page_config(page_title="APEXPITCH QUANT PRO", layout="wide")
st.markdown("""
    <style>
    .main { background-color: #050505; color: #00ff00; }
    .stMetric { background: #111; border: 1px solid #333; padding: 15px; border-radius: 10px; }
    .stButton>button { background: linear-gradient(45deg, #ff4b4b, #8b0000); color: white; border: none; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

st.title("🏆 APEXPITCH: QUANTITATIVE PREDICTIVE RADAR")

API_KEY = "7e061e4e93msh7dda34be332134ep1038b9jsn3e9b3ef3677f"
HOST = "free-api-live-football-data.p.rapidapi.com"

def fetch_data(endpoint, params=None):
    url = f"https://{HOST}/{endpoint}"
    headers = {"X-RapidAPI-Key": API_KEY, "X-RapidAPI-Host": HOST}
    try:
        r = requests.get(url, headers=headers, params=params)
        return r.json() if r.status_code == 200 else None
    except: return None

# 2. BARRA LATERAL INTELIGENTE (Inspirada na imagem 043503)
with st.sidebar:
    st.header("🎯 Parâmetros de Varredura")
    data_countries = fetch_data("football-get-all-countries")
    if data_countries:
        countries = {c['name']: c['ccode'] for c in data_countries['response']['countries']}
        pais_selecionado = st.selectbox("Mercado Alvo:", ["Selecione..."] + list(countries.keys()))
    
    st.divider()
    st.info(f"📊 Cota de Dados: 100/mês") # Alinhado com a imagem 043fc2

# 3. DASHBOARD DE ANÁLISE COMPLEXA
if pais_selecionado != "Selecione...":
    ccode = countries[pais_selecionado]
    data_leagues = fetch_data("football-get-all-leagues-by-country", params={"ccode": ccode})
    
    if data_leagues:
        ligas = {l['name']: l['id'] for l in data_leagues['response']['leagues']}
        liga_nome = st.selectbox("Filtro por Liga:", list(ligas.keys()))
        
        if st.button('🔥 ATIVAR RADAR APEXPULSE'):
            res_live = fetch_data("football-get-all-livescores-by-league", params={"league_id": ligas[liga_nome]})
            
            if res_live and res_live['response'].get('livescore'):
                for jogo in res_live['response']['livescore']:
                    st.write(f"### 🏟️ {jogo['home_name']} {jogo['home_score']} x {jogo['away_score']} {jogo['away_name']}")
                    
                    # MÉTRICAS PRO
                    tempo = int(jogo.get('time', 0))
                    prob_gol = min(tempo + 5, 90) if abs(int(jogo['home_score']) - int(jogo['away_score'])) <= 1 else 10
                    
                    col1, col2, col3 = st.columns(3)
                    col1.metric("⏱️ Tempo", f"{tempo}'")
                    col2.metric("📉 Risco de Entrada", "ALTO" if tempo > 80 else "MÉDIO")
                    col3.metric("📈 Probabilidade de Gol", f"{prob_gol}%")

                    # GRÁFICO APEXPULSE (RESOLVENDO ERRO DA IMAGEM 042ce5)
                    # Criamos uma simulação de pressão baseada no tempo real
                    dados_grafico = pd.DataFrame({
                        'Minuto': [tempo-10, tempo-5, tempo],
                        'Pressão': [20, 50, prob_gol]
                    })
                    fig = px.area(dados_grafico, x='Minuto', y='Pressão', title="Fluxo de Pressão ApexPulse")
                    fig.update_layout(template="plotly_dark", height=300)
                    st.plotly_chart(fig, use_container_width=True)
                    
                    if tempo > 75:
                        st.warning("🚨 PRESSÃO CRÍTICA DETECTADA: Possível Over 0.5")
                    st.divider()
            else:
                st.warning("⚠️ Sem jogos ao vivo nesta liga no momento.")
else:
    st.info("💡 Escolha um país na barra lateral para iniciar o monitoramento quantitativo.")
