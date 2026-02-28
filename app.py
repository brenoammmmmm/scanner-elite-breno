import streamlit as st
import requests
import pandas as pd

# CONFIGURAÇÃO VISUAL PROFISSIONAL
st.set_page_config(page_title="APEXPITCH REVOLUTION", layout="wide")
st.title("🏆 APEXPITCH: MONITORAMENTO GLOBAL AO VIVO")

# SUA CHAVE DA API
API_KEY = "7e061e4e93msh7dda34be332134ep1038b9jsn3e9b3ef3677f"

def buscar_dados_brutos():
    # Endpoint focado em TODOS os jogos live do mundo
    url = "https://api-football-v1.p.rapidapi.com/v3/fixtures"
    querystring = {"live": "all"}
    headers = {
        "X-RapidAPI-Key": API_KEY,
        "X-RapidAPI-Host": "api-football-v1.p.rapidapi.com"
    }
    try:
        response = requests.get(url, headers=headers, params=querystring)
        return response.json()
    except Exception as e:
        st.error(f"Erro de conexão: {e}")
        return None

if st.button('🔥 SINCRONIZAR MILHARES DE JOGOS AGORA'):
    with st.spinner('Varrendo todos os estádios do planeta...'):
        dados_api = buscar_dados_brutos()
        
        # O PULO DO GATO: Verificar se a resposta tem a lista de jogos corretamente
        if dados_api and 'response' in dados_api:
            jogos = dados_api['response']
            
            if len(jogos) > 0:
                lista_analise = []
                for j in jogos:
                    # EXTRAÇÃO DE DADOS PARA ANÁLISE REVOLUCIONÁRIA
                    tempo = j['fixture']['status']['elapsed']
                    casa = j['teams']['home']['name']
                    fora = j['teams']['away']['name']
                    placar = f"{j['goals']['home']}x{j['goals']['away']}"
                    liga = j['league']['name']
                    
                    # CÁLCULO DE POWER SURGE (PRESSÃO REAL)
                    # Consideramos o tempo de jogo e a movimentação do placar
                    ps_score = (j['goals']['home'] + j['goals']['away'] + 1) * (tempo / 25)
                    
                    lista_analise.append({
                        "Min": f"{tempo}'",
                        "Confronto": f"{casa} x {fora}",
                        "Placar": placar,
                        "Power Surge ⚡": round(ps_score, 2),
                        "Liga": liga
                    })
                
                # Exibe a tabela completa ordenada pela maior pressão (Power Surge)
                df = pd.DataFrame(lista_analise).sort_values(by="Power Surge ⚡", ascending=False)
                st.write(f"✅ **{len(jogos)} jogos encontrados e analisados com sucesso!**")
                st.dataframe(df, use_container_width=True)
            else:
                st.warning("A API confirmou: no exato momento não há jogos registrados como 'Live'. Tente novamente em alguns minutos.")
        else:
            st.error("Falha ao processar dados da API. Verifique se seu plano na RapidAPI está ativo.")
