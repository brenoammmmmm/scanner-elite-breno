import streamlit as st
import requests
import pandas as pd
import plotly.express as px
from datetime import datetime

# 1. ESTILIZAÇÃO 'DARK QUANT'
st.set_page_config(page_title="APEXPITCH TERMINAL", layout="wide")
st.markdown("""
    <style>
    .main { background-color: #050505; color: #00ff00; }
    .stMetric { background: #111; border: 1px solid #333; padding: 15px; border-radius: 10px; }
    .alert-card { padding: 15px; border-radius: 10px; border-left: 5px solid #ff4b4b; background: #1a1a1a; margin-bottom: 10px; }
    .success-card { padding: 15px; border-radius: 10px; border-left: 5px solid #00ff00; background: #0a1a0a; margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

st.title("🏆 APEXPITCH: PERFORMANCE & PREDICTIVE TERMINAL")

# CREDENCIAIS VALIDADA (imagem 11cc83)
API_KEY = "7e061e4e93msh7dda34be332134ep1038b9jsn3e9b3ef3677f"
HOST = "free-api-live-football-data.p.rapidapi.com"

def fetch(endpoint, params=None):
    url = f"https://{HOST}/{endpoint}"
    headers = {"X-RapidAPI-Key": API_KEY, "X-RapidAPI-Host": HOST}
    try:
        r = requests.get(url, headers=headers, params=params)
        return r.json() if r.status_code == 200 else None
    except: return None

# 2. BARRA LATERAL - CONTROLE DE FLUXO (imagem 0425a1)
with st.sidebar:
    st.header("⚡ Radar de Elite")
    data_p = fetch("football-get-all-countries")
    if data_p:
        paises = {p['name']: p['ccode'] for p in data_p['response']['countries']}
        escolha = st.selectbox("Mercado Alvo:", ["Selecione..."] + list(paises.keys()))
    
    st.divider()
    st.write(f"⏱️ **Última Atualização:** {datetime.now().strftime('%H:%M:%S')}")
    st.info("📊 Créditos Plano Basic: 100/mês") # Referência imagem 043fc2

# 3. DASHBOARD ANALÍTICO E LOG DE ENTRADAS
if escolha != "Selecione...":
    ccode = paises[escolha]
    data_l = fetch("football-get-all-leagues-by-country", params={"ccode": ccode})
    
    if data_l:
        ligas = {l['name']: l['id'] for l in data_l['response']['leagues']}
        liga_nome = st.selectbox("Monitorar Liga:", list(ligas.keys()))
        
        if st.button('🔥 SINCRONIZAR RADAR DE ALTA FREQUÊNCIA'):
            res_live = fetch("football-get-all-livescores-by-league", params={"league_id": ligas[liga_nome]})
            
            if res_live and res_live['response'].get('livescore'):
                st.write("## 📉 MONITORAMENTO ATIVO")
                
                for jogo in res_live['response']['livescore']:
                    tempo = int(jogo.get('time', 0))
                    score_h = int(jogo['home_score'])
                    score_a = int(jogo['away_score'])
                    
                    # ALGORITMO DE DECISÃO APEX (Nível 8)
                    pressao_critica = tempo > 75 and abs(score_h - score_a) <= 1
                    
                    with st.container():
                        if pressao_critica:
                            st.markdown(f"""<div class="alert-card">
                                <b>🚨 ALERTA DE ENTRADA:</b> {jogo['home_name']} vs {jogo['away_name']} <br>
                                Placar: {score_h}x{score_a} | Minuto: {tempo}' | <b>Sugestão: OVER 0.5 FT</b>
                                </div>""", unsafe_allow_html=True)
                        
                        col1, col2, col3 = st.columns(3)
                        col1.metric("⏱️ Tempo", f"{tempo}'")
                        col2.metric("⚽ Placar", f"{score_h} - {score_a}")
                        col3.metric("📈 Índice ApexPulse", f"{min(tempo+10, 95)}%")

                        # GRÁFICO DE PRESSÃO (imagem 04291e)
                        df_pulse = pd.DataFrame({
                            'M': [tempo-10, tempo-5, tempo],
                            'P': [20, 50, 85 if pressao_critica else 40]
                        })
                        fig = px.area(df_pulse, x='M', y='P', title="Power Surge Flow")
                        fig.update_layout(template="plotly_dark", height=250, margin=dict(l=0, r=0, t=30, b=0))
                        st.plotly_chart(fig, use_container_width=True)
                        st.divider()
            else:
                st.warning("⚠️ Nenhuma partida ao vivo detectada nesta liga.")
else:
    st.info("💡 Terminal aguardando seleção de mercado na barra lateral.")
