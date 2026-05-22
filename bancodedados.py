import sqlite3
import pandas as pd
import requests
import flask   
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
pd.api.extensions.register_dataframe_accessor("banco_de_dados")
import pandas as pd
import time
from datetime import datetime, timezone, timedelta

# NOVA CHAVE DE API ATUALIZADA
API_KEY = "767fbbd6abf1f7c9cc0779f9013f96ae"

cidades_globais = [
    "Nova York", "Los Angeles", "Toronto", "Cidade do México", 
    "São Paulo", "Buenos Aires", "Bogotá", "Santiago",
    "Londres", "Paris", "Berlim", "Moscou", "Roma", "Madrid",
    "Tóquio", "Pequim", "Nova Deli", "Seul", "Bangkok", "Jakarta",
    "Dubai", "Riad", "Cairo", "Cidade do Cabo", "Nairóbi", "Lagos",
    "Sydney", "Auckland", "Melbourne"
]

dados_brutos = []

print(f"Iniciando varredura global em {len(cidades_globais)} cidades...")
print("Isso pode levar cerca de 30 segundos para respeitar os limites da API.\n")

for cidade in cidades_globais:
    url = f"http://api.openweathermap.org/data/2.5/weather?q={cidade}&appid={API_KEY}&units=metric&lang=pt_br"
    
    try:
        resposta = requests.get(url)
        if resposta.status_code == 200:
            dados = resposta.json()
            
            # Ajuste da descrição do clima
            dados['weather_desc'] = dados['weather'][0]['description'].capitalize()
            del dados['weather']
            
            # Cálculo da hora local
            timestamp_utc = dados['dt']
            fuso_segundos = dados['timezone']
            hora_local = datetime.fromtimestamp(timestamp_utc, tz=timezone.utc) + timedelta(seconds=fuso_segundos)
            dados['hora_formatada'] = hora_local.strftime('%H:%M')
            
            dados_brutos.append(dados)
            print(f"✅ Dados coletados: {cidade}")
        else:
            print(f"❌ Erro ao buscar {cidade}. Código: {resposta.status_code}")
            
    except Exception as e:
        print(f"⚠️ Ocorreu um erro de conexão em {cidade}: {e}")
        
    time.sleep(1)

# Transforma tudo em um DataFrame
df_clima_global = pd.json_normalize(dados_brutos)

# Adicionamos a 'hora_formatada' na nossa lista de colunas que vão para a tela
colunas_importantes = [
    'name', 'sys.country', 'hora_formatada', 'weather_desc', 'main.temp', 
    'main.feels_like', 'main.humidity', 'wind.speed'
]

df_final = df_clima_global[colunas_importantes].copy()

# Renomeia para ficar profissional
df_final.columns = [
    'Cidade', 'País', 'Hora Local', 'Condição', 'Temp Atual (°C)', 
    'Sensação (°C)', 'Umidade (%)', 'Vento (m/s)'
]

print("\n🌍 *** PANORAMA DO CLIMA GLOBAL *** 🌍\n")
pd.set_option('display.max_rows', None)
pd.set_option('display.width', 1000)
print(df_final)
df_final.to_html('tabela_clima.html', index=False, classes='tabela-dados')