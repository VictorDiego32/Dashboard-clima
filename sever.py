from flask import Flask, render_template, jsonify
import sqlite3

app = Flask(__name__)

def buscar_do_banco():
    conn = sqlite3.connect('clima_global.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM clima")
    linhas = cursor.fetchall()
    conn.close()
    # Transforma os dados do banco em uma lista que o JavaScript entende
    return [dict(l) for l in linhas]

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/clima')
def api_clima():
    dados = buscar_do_banco()
    return jsonify(dados)

if __name__ == '__main__':
    app.run(debug=True)