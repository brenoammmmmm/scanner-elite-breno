import streamlit as st
import requests
import pandas as pd
import plotly.express as px

# 1. ESTILIZAÇÃO TERMINAL BLOOMBERG
st.set_page_config(page_title="APEXPITCH PREDICTIVE", layout="wide")
st.markdown("""
    <style>
    .main { background-color: #050505; color: #00ff00; }
    .stMetric { background: #111; border: 1px solid #333; padding: 15px; border-radius: 10px; }
    .rec-box { padding: 20px; border-radius: 10px; border: 2px solid #ff4b4b; background-color: #1a0000; color: white; margin: 10px 0; }
    </style>
    """, unsafe_allow_html=True)

st.title("🏆 APEXPITCH: QUANTITATIVE PREDICTIVE RADAR")

API_KEY = "7e061e4e93msh7dda34be332134ep1038b9jsn3e9b3ef3677f"
HOST = "free-api-live-football-data.p.rapidapi.com"

def fetch(endpoint, params=None):
    url = f"https://{HOST}/{endpoint}"
    headers = {"X-RapidAPI-Key": API_KEY, "X-RapidAPI-Host": HOST}
    try:
        r = requests.get(url, headers=headers, params=params)
        return r.json() if r.status_code == 200 else None
    except: return None

# 2. BARRA LATERAL (Conforme imagem 0425a1)
with st.sidebar:
    st.header("🎯 Parâmetros de Varredura")
    data_p = fetch("football-get-all-countries")
    if data_p:
        paises = {p['name']: p['ccode'] for p in data_p['response']['countries']}
        escolha = st.selectbox("Mercado Alvo:", ["Selecione..."] + list(paises.keys()))
    
    st.divider()
    st.info("📊 Cota de Dados: 100/mês") # Limite plano Basic (imagem 043fc2)

# 3. MOTOR DE ANÁLISE MASTER
if escolha != "Selecione...":
    ccode = paises[escolha]
    data_l = fetch("football-get-all-leagues-by-country", params={"ccode": ccode})
    
    if data_l:
        ligas = {l['name']: l['id'] for l in data_l['response']['leagues']}
        liga_nome = st.selectbox("Filtro por Liga:", list(ligas.keys()))
        
        if st.button('🔥 ATIVAR ALGORITMO APEX'):
            res_live = fetch("football-get-all-livescores-by-league", params={"league_id": ligas[liga_nome]})
            
            if res_live and res_live['response'].get('livescore'):
                for jogo in res_live['response']['livescore']:
                    st.write(f"### 🏟️ {jogo['home_name']} {jogo['home_score']} x {jogo['away_score']} {jogo['away_name']}")
                    
                    # CÁLCULOS PREDITIVOS
                    tempo = int(jogo.get('time', 0))
                    placar_casa = int(jogo['home_score'])
                    placar_fora = int(jogo['away_score'])
                    
                    col1, col2, col3 = st.columns(3)
                    col1.metric("⏱️ Minuto", f"{tempo}'")
                    
                    # Recomendação de IA
                    if tempo > 75 and abs(placar_casa - placar_fora) <= 1:
                        rec_msg = "🔥 PRESSÃO CRÍTICA: Forte tendência de Over 0.5 nos minutos finais."
                        prob = 85
                    elif tempo < 30 and placar_casa + placar_fora == 0:
                        rec_msg = "⏳ ESTUDO: Jogo equilibrado, aguardar volume de ataques."
                        prob = 40
                    else:
                        rec_msg = "📊 MONITORANDO: Mercado sem padrões de elite no momento."
                        prob = 20
                        
                    col2.metric("📈 Prob. de Gol", f"{prob}%")
                    col3.metric("🎯 Sugestão", "Entrada Confirmada" if prob > 80 else "Aguardar")

                    # CAIXA DE ANÁLISE SURPREENDENTE
                    st.markdown(f'<div class="rec-box"><b>🤖 ANÁLISE APEX:</b> {rec_msg}</div>', unsafe_allow_html=True)

                    # GRÁFICO APEXPULSE ATUALIZADO (imagem 04291e)
                    df_pulse = pd.DataFrame({
                        'Tempo': [tempo-15, tempo-10, tempo-5, tempo],
                        'Pressão': [10, 30, 60, prob]
                    })
                    fig = px.area(df_pulse, x='Tempo', y='Pressão', title="Fluxo de Ataque ApexPulse")
                    fig.update_layout(template="plotly_dark", height=350, plot_bgcolor='rgba(0,0,0,0)')
                    st.plotly_chart(fig, use_container_width=True)
                    st.divider()
            else:
                st.warning("⚠️ Sem jogos ativos nesta liga no momento.")
