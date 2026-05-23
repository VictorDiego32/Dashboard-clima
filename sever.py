from flask import Flask, render_template, jsonify
import sqlite3

app = Flask(__name__)
DB_NAME = "clima_global.db"

def obter_dados_bd():
    """Conecta ao banco e busca os dados climáticos mais recentes"""
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row  # Permite acessar colunas pelo nome
    cursor = conn.cursor()
    
    # Busca os dados ordenados por nome da cidade
    cursor.execute("""
        SELECT cidade, pais, hora_local, condicao, temperatura, sensacao, umidade, vento 
        FROM clima 
        ORDER BY cidade ASC
    """)
    linhas = cursor.fetchall()
    conn.close()
    
    # Converte os dados para uma lista de dicionários
    return [dict(linha) for list_row in [linhas] for linha in list_row]

@app.route('/')
def index():
    """Rota principal que renderiza a página da Dashboard"""
    return render_template('index.html')

@app.route('/api/clima')
def api_clima():
    """Rota de API que o JavaScript vai consultar em segundo plano para atualizar a tabela"""
    dados = obter_dados_bd()
    return jsonify(dados)

if __name__ == '__main__':
    # Inicializa o servidor Flask. 
    # host='0.0.0.0' permite que qualquer pessoa na sua rede local acesse o site pelo seu IP
    app.run(host='0.0.0.0', port=5000, debug=True)