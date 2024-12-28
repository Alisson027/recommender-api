from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

# 1. Função para criar o banco de dados e inserir dados fictícios
def create_db():
    conn = sqlite3.connect('sales.db')
    cursor = conn.cursor()

    # Criação da tabela de compras
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS purchases (
            user_id INTEGER,
            product_id INTEGER,
            product_name TEXT
        )
    ''')

    # Dados fictícios de compras
    purchases = [
        (1, 101, "Laptop"),
        (1, 102, "Mouse"),
        (2, 101, "Laptop"),
        (2, 103, "Headphones"),
        (3, 104, "Smartphone"),
        (3, 102, "Mouse"),
    ]

    # Inserir dados no banco
    cursor.executemany('INSERT INTO purchases VALUES (?, ?, ?)', purchases)
    conn.commit()
    conn.close()

# 2. Função para obter as compras de um usuário
def get_purchases(user_id):
    conn = sqlite3.connect('sales.db')
    cursor = conn.cursor()
    
    cursor.execute('SELECT product_id, product_name FROM purchases WHERE user_id = ?', (user_id,))
    purchases = cursor.fetchall()
    
    conn.close()
    return purchases

# 3. Função para recomendar produtos com base nas compras de outros usuários
def recommend_products(user_id):
    conn = sqlite3.connect('sales.db')
    cursor = conn.cursor()

    # Busca os produtos comprados por outros usuários, excluindo o próprio
    cursor.execute('''
        SELECT DISTINCT product_id, product_name
        FROM purchases
        WHERE user_id != ?
    ''', (user_id,))
    
    recommendations = cursor.fetchall()
    conn.close()
    
    return recommendations

# 4. Endpoint da API para recomendar produtos
@app.route('/recommend', methods=['POST'])
def recommend():
    data = request.get_json()
    user_id = str(data.get('user_id'))

    # Busca as compras do usuário
    purchases = get_purchases(user_id)
    if not purchases:
        return jsonify({"message": "No purchases found for this user."})

    # Gera recomendações simples com base nas compras de outros usuários
    recommendations = recommend_products(user_id)

    return jsonify({
        "purchases": purchases,
        "recommendations": recommendations
    })


if __name__ == '__main__':
    # Cria o banco de dados
    create_db()
    
    app.run(debug=True)
