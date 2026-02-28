import streamlit as st
import requests
import pandas as pd

# 1. CONFIGURAÇÃO VISUAL DARK & GOLD
st.set_page_config(page_title="APEXPITCH REVOLUTION", layout="wide")
st.markdown("<style>body {background-color: #000; color: #D4AF37;}</style>", unsafe_allow_html=True)

st.title("🏆 APEXPITCH: INTELLIGENCE & ODDS RADAR")

# Sua chave que já está funcionando
API_KEY = "7e061e4e93msh7dda34be332134ep1038b9jsn3e9b3ef3677f"

def get_live_data():
    url = "https://api-football-v1.p.rapidapi.com/v3/fixtures?live=all"
    headers = {"X-RapidAPI-Key": API_KEY, "X-RapidAPI-Host": "api-football-v1.p.rapidapi.com"}
    return requests.get(url, headers=headers).json()

# 2. BARRA LATERAL DE FILTROS TÁTICOS
st.sidebar.header("🎯 FILTROS DE ELITE")
sensibilidade = st.sidebar.slider("Sensibilidade do Alerta (Power Surge)", 5, 50, 15)

# 3. BOTÃO DE EXECUÇÃO
if st.button('🔥 ESCANEAR MERCADO MUNDIAL AGORA'):
    res = get_live_data()
    
    if res and 'response' in res and len(res['response']) > 0:
        jogos = res['response']
        analise_final = []
        
        for j in jogos:
            tempo = j['fixture']['status']['elapsed']
            casa = j['teams']['home']['name']
            fora = j['teams']['away']['name']
            gols_c = j['goals']['home']
            gols_f = j['goals']['away']
            
            # CÁLCULO REVOLUCIONÁRIO: Momentum Progressivo (Power Surge)
            # Cruzamos o tempo de jogo com a movimentação do placar
            momentum = (gols_c + gols_f + 1) * (tempo / 30)
            
            # DEFINIÇÃO DE ALERTAS INTELIGENTES
            alerta = "⚖️ Estável"
            if tempo > 80 and gols_c == gols_f:
                alerta = "💎 GOLDEN GOAL (Zoião)"
            elif momentum > sensibilidade:
                alerta = "⚡ PRESSÃO MÁXIMA"
            
            analise_final.append({
                "Min": f"{tempo}'",
                "Confronto": f"{casa} x {fora}",
                "Placar": f"{gols_c}-{gols_f}",
                "Power Surge ⚡": round(momentum, 2),
                "Oportunidade": alerta,
                "Liga": j['league']['name']
            })
        
        # Tabela ordenada pelo jogo com maior chance de evento
        df = pd.DataFrame(analise_final).sort_values(by="Power Surge ⚡", ascending=False)
        st.success(f"Radar Ativo: {len(jogos)} jogos monitorados simultaneamente.")
        st.dataframe(df, use_container_width=True)
    else:
        st.info("🔄 Quase lá! Clique no botão novamente em 60 segundos para atualizar os dados.")
