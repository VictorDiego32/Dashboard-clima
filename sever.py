from flask import Flask, render_template, jsonify
import sqlite3
import os

app = Flask(__name__)

# Força o Flask a olhar na mesma pasta do script
DIRETORIO_ATUAL = os.path.dirname(os.path.abspath(__file__))
CAMINHO_BANCO = os.path.join(DIRETORIO_ATUAL, 'clima_global.db')

def buscar_do_banco():
    try:
        # Usa o caminho absoluto
        conn = sqlite3.connect(CAMINHO_BANCO)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM clima")
        linhas = cursor.fetchall()
        conn.close()
        return [dict(l) for l in linhas]
    except Exception as e:
        print(f"Erro ao acessar o banco: {e}")
        return [] # Retorna vazio se der erro, mas não quebra o site

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/clima')
def api_clima():
    dados = buscar_do_banco()
    return jsonify(dados)

if __name__ == '__main__':
    app.run(debug=True)