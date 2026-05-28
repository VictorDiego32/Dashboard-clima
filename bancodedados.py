import requests
import pandas as pd
import sqlite3
import time
from datetime import datetime, timezone, timedelta

API_KEY = "767fbbd6abf1f7c9cc0779f9013f96ae"
DB_NAME = "clima_global.db"

cidades_globais = [
    "Nova York", "Los Angeles", "Toronto", "Cidade do México", 
    "São Paulo", "Buenos Aires", "Bogotá", "Santiago",
    "Londres", "Paris", "Berlim", "Moscou", "Roma", "Madrid",
    "Tóquio", "Pequim", "Nova Deli", "Seul", "Bangkok", "Jakarta",
    "Dubai", "Riad", "Cairo", "Cidade do Cabo", "Nairóbi", "Lagos",
    "Sydney", "Auckland", "Melbourne"
]

def inicializar_banco():
    """Cria a tabela no banco de dados se ela não existir"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS clima (
            cidade TEXT PRIMARY KEY,
            pais TEXT,
            hora_local TEXT,
            condicao TEXT,
            temperatura REAL,
            sensacao REAL,
            umidade INTEGER,
            vento REAL
        )
    """)
    conn.commit()
    conn.close()

def atualizar_dados_no_banco():
    inicializar_banco()
    print("Iniciando motor de atualização climática contínua...")

    while True:
        dados_brutos = []
        print(f"\n[{datetime.now().strftime('%H:%M:%S')}] Coletando dados novos da API OpenWeather...")

        for cidade in cidades_globais:
            url = f"http://api.openweathermap.org/data/2.5/weather?q={cidade}&appid={API_KEY}&units=metric&lang=pt_br"
            try:
                resposta = requests.get(url, timeout=10)
                if resposta.status_code == 200:
                    dados = resposta.json()
                    
                    # Tratamento com fuso horário
                    timestamp_utc = dados['dt']
                    fuso_segundos = dados['timezone']
                    hora_local = datetime.fromtimestamp(timestamp_utc, tz=timezone.utc) + timedelta(seconds=fuso_segundos)
                    
                    registro = {
                        "cidade": dados["name"],
                        "pais": dados["sys"]["country"],
                        "hora_local": hora_local.strftime('%H:%M'),
                        "condicao": dados["weather"][0]["description"].capitalize(),
                        "temperatura": dados["main"]["temp"],
                        "sensacao": dados["main"]["feels_like"],
                        "umidade": dados["main"]["humidity"],
                        "vento": dados["wind"]["speed"]
                    }
                    dados_brutos.append(registro)
            except Exception as e:
                print(f"Erro ao coletar {cidade}: {e}")
            
            time.sleep(1) # Evita bloqueio da API

        # Grava os dados tratados usando o Pandas e SQL
        if dados_brutos:
            df = pd.DataFrame(dados_brutos)
            
            conn = sqlite3.connect(DB_NAME)
            # O 'REPLACE' garante que se a cidade já existir, ela apenas atualiza os dados antigos
            df.to_sql('clima', conn, if_exists='replace', index=False)
            conn.close()
            print("💾 Banco de dados atualizado com sucesso!")
        
        # Faz a varredura na API a cada 10 minutos
        print("Aguardando 10 minutos para a próxima coleta de dados...")
        time.sleep(600)

if __name__ == "__main__":
    atualizar_dados_no_banco()
