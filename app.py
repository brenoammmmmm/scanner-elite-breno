import streamlit as st
import requests
import pandas as pd
import plotly.express as px

# 1. CONFIGURAÇÃO DE INTERFACE DE ALTA PERFORMANCE
st.set_page_config(page_title="APEXPITCH GLOBAL SCANNER", layout="wide")
st.markdown("""
    <style>
    .main { background-color: #050505; color: #00ff00; }
    .stMetric { background: #111; border: 1px solid #333; padding: 15px; border-radius: 10px; }
    .live-card { padding: 20px; border-radius: 10px; border: 1px solid #444; background-color: #111; margin-bottom: 15px; }
    .gol-alert { background: linear-gradient(90deg, #ff4b4b, #8b0000); padding: 10px; border-radius: 5px; color: white; font-weight: bold; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

st.title("🏆 APEXPITCH: GLOBAL LIVE SCANNER")

# CREDENCIAIS (imagem 11cc83)
API_KEY = "7e061e4e93msh7dda34be332134ep1038b9jsn3e9b3ef3677f"
HOST = "free-api-live-football-data.p.rapidapi.com"

def fetch(endpoint, params=None):
    url = f"https://{HOST}/{endpoint}"
    headers = {"X-RapidAPI-Key": API_KEY, "X-RapidAPI-Host": HOST}
    try:
        r = requests.get(url, headers=headers, params=params)
        return r.json() if r.status_code == 200 else None
    except: return None

# 2. BARRA LATERAL - GESTÃO DE COTA
with st.sidebar:
    st.header("📡 Radar Central")
    st.info("💡 Este scanner busca jogos em tempo real nas ligas mais importantes.")
    st.write("---")
    st.write("💳 **Plano:** Basic (100 Req/Mês)")
    st.warning("Evite atualizar a página muitas vezes para poupar seus créditos.")

# 3. SCANNER GLOBAL DE JOGOS AO VIVO
if st.button('🔥 ESCANEAR TODOS OS JOGOS AO VIVO AGORA'):
    with st.spinner('Varrendo estádios ao redor do mundo...'):
        # Usamos o endpoint de Ligas Populares que costuma concentrar os jogos ao vivo (imagem 11c4db)
        res_popular = fetch("football-get-all-popular-league")
        
        if res_popular and res_popular['response'].get('popular_league'):
            ligas = res_popular['response']['popular_league']
            encontrou_jogo = False
            
            for liga in ligas:
                # Para cada liga popular, vamos tentar puxar os jogos ao vivo
                res_live = fetch("football-get-all-livescores-by-league", params={"league_id": liga['id']})
                
                if res_live and res_live['response'].get('livescore'):
                    encontrou_jogo = True
                    for jogo in res_live['response']['livescore']:
                        with st.container():
                            st.markdown(f'<div class="live-card">', unsafe_allow_html=True)
                            
                            c1, c2, c3 = st.columns([2,1,2])
                            c1.subheader(f"🏠 {jogo['home_name']}")
                            c2.title(f"{jogo['home_score']} - {jogo['away_score']}")
                            c3.subheader(f"🚀 {jogo['away_name']}")
                            
                            tempo = int(jogo.get('time', 0))
                            st.write(f"**Liga:** {liga['name']} | **Minuto:** {tempo}'")
                            
                            # LÓGICA DE PRESSÃO APEX
                            if tempo > 75 and abs(int(jogo['home_score']) - int(jogo['away_score'])) <= 1:
                                st.markdown('<div class="gol-alert">🚨 ALERTA: PRESSÃO MÁXIMA - POSSÍVEL GOL!</div>', unsafe_allow_html=True)
                            
                            # GRÁFICO DE FLUXO (Power Pulse)
                            df_pulse = pd.DataFrame({'Min': [tempo-10, tempo-5, tempo], 'P': [10, 40, 80 if tempo > 70 else 30]})
                            fig = px.area(df_pulse, x='Min', y='P', title="Fluxo de Ataque")
                            fig.update_layout(template="plotly_dark", height=200, margin=dict(l=0,r=0,t=30,b=0))
                            st.plotly_chart(fig, use_container_width=True)
                            
                            st.markdown('</div>', unsafe_allow_html=True)
                            st.divider()
            
            if not encontrou_jogo:
                st.warning("⚠️ Conectado à API, mas não há jogos ao vivo nas ligas monitoradas agora. Tente novamente em 15 minutos.")
        else:
            st.error("Erro ao acessar a base de dados. Verifique sua cota de 100 requisições.")
else:
    st.success("✅ Sistema pronto. Clique no botão acima para iniciar o Scanner Global.")
