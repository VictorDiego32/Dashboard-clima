import sqlite3
import pandas as pd
import requests
import flask   
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
pd.api.extensions.register_dataframe_accessor("banco_de_dados")
import requests
import pandas as pd
import time

# Sua chave de API do OpenWeatherMap
API_KEY = "767fbbd6abf1f7c9cc0779f9013f96ae"

# Panorama Global: Principais metrópoles de todos os continentes
cidades_globais = [
    # Américas
    "Nova York", "Los Angeles", "Toronto", "Cidade do México", 
    "São Paulo", "Buenos Aires", "Bogotá", "Santiago",
    # Europa
    "Londres", "Paris", "Berlim", "Moscou", "Roma", "Madrid",
    # Ásia
    "Tóquio", "Pequim", "Nova Deli", "Seul", "Bangkok", "Jakarta",
    # Oriente Médio e África
    "Dubai", "Riad", "Cairo", "Cidade do Cabo", "Nairóbi", "Lagos",
    # Oceania
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
            
            # Ajustando a lista de 'weather' para o Pandas ler perfeitamente
            dados['weather_desc'] = dados['weather'][0]['description']
            del dados['weather']
            
            dados_brutos.append(dados)
            print(f"✅ Dados coletados: {cidade}")
        else:
            print(f"❌ Erro ao buscar {cidade}. Código: {resposta.status_code}")
            
    except Exception as e:
        print(f"⚠️ Ocorreu um erro de conexão em {cidade}: {e}")
        
    # TRAVA DE SEGURANÇA: Pausa de 1 segundo para não estourar o limite de 60 requisições/minuto
    time.sleep(1)

# Transforma tudo em um DataFrame
df_clima_global = pd.json_normalize(dados_brutos)

# Organiza e seleciona as colunas mais importantes para não virar uma bagunça visual
colunas_importantes = [
    'name', 'sys.country', 'weather_desc', 'main.temp', 'main.feels_like', 
    'main.humidity', 'wind.speed', 'coord.lat', 'coord.lon'
]

# Filtra apenas as colunas selecionadas
df_final = df_clima_global[colunas_importantes].copy()

# Renomeia as colunas para português para ficar profissional
df_final.columns = [
    'Cidade', 'País', 'Condição', 'Temp Atual (°C)', 'Sensação (°C)', 
    'Umidade (%)', 'Vento (m/s)', 'Latitude', 'Longitude'
]

print("\n🌍 *** PANORAMA DO CLIMA GLOBAL *** 🌍\n")
pd.set_option('display.max_rows', None) # Garante que todas as cidades apareçam
pd.set_option('display.width', 1000)
print(df_final)
df_final.to_html('tabela-clima.html', index=False, classes='tabela-dados')