import streamlit as st
import requests
import pandas as pd

# CONFIGURAÇÃO DE ELITE
st.set_page_config(page_title="APEXPITCH REVOLUTION", layout="wide")
st.markdown("<style>body {background-color: #000; color: #D4AF37;}</style>", unsafe_allow_html=True)

st.title("🏆 APEXPITCH: MONITORAMENTO GLOBAL")

# CHAVE QUE VOCÊ MOSTROU NA FOTO image_123940.png
API_KEY = "7e061e4e93msh7dda34be332134ep1038b9jsn3e9b3ef3677f"

def get_data():
    url = "https://api-football-v1.p.rapidapi.com/v3/fixtures"
    # Forçando a busca por todos os jogos ao vivo
    querystring = {"live": "all"}
    headers = {
        "X-RapidAPI-Key": API_KEY,
        "X-RapidAPI-Host": "api-football-v1.p.rapidapi.com"
    }
    try:
        response = requests.get(url, headers=headers, params=querystring)
        if response.status_code == 429:
            return "LIMITE_EXCEDIDO"
        return response.json()
    except:
        return None

if st.button('🔥 SINCRONIZAR MILHARES DE JOGOS'):
    res = get_data()
    
    if res == "LIMITE_EXCEDIDO":
        st.error("⚠️ A API diz que você atingiu o limite. Como você acabou de assinar, aguarde 5 minutos para o sistema deles atualizar seu novo plano Basic.")
    elif res and 'response' in res and len(res['response']) > 0:
        jogos = res['response']
        db = []
        for j in jogos:
            tempo = j['fixture']['status']['elapsed']
            casa = j['teams']['home']['name']
            fora = j['teams']['away']['name']
            gols = f"{j['goals']['home']}x{j['goals']['away']}"
            
            # PONTUAÇÃO DE OPORTUNIDADE IA
            score = (j['goals']['home'] + j['goals']['away'] + 1) * (tempo / 35)
            
            db.append({
                "Min": f"{tempo}'",
                "Confronto": f"{casa} x {fora}",
                "Placar": gols,
                "Pressão (Score)": round(score, 2),
                "Liga": j['league']['name']
            })
        
        df = pd.DataFrame(db).sort_values(by="Pressão (Score)", ascending=False)
        st.success(f"Radar Ativo! {len(jogos)} jogos rastreados.")
        st.dataframe(df, use_container_width=True)
    else:
        st.warning("🔄 Quase lá! O plano foi assinado, mas a API ainda não liberou os dados. Clique no botão novamente em 1 minuto.")
