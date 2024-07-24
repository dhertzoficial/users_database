# API RESTfull

from flask import Flask, request, jsonify
import sqlite3

# INICIALIZAÇÃO DA APLICAÇÃO FLASK
app = Flask(__name__) # CRIA UMA INSTÂNCIA DA CLASSE FLASK

def to_connect():
    connection = sqlite3.connect("database.db") # CRIA CONEXÃO COM DATABASE
    cursor = connection.cursor() # CURSOS O QUAL É USADO PARA EXECUTAR COMANDOS SQL NO DATABASE
    return connection, cursor

# ENDPOINT PARA OBTER USUÁRIOS
@app.route('/users', methods=['GET']) # DEFINE A ROTA PARA O ENDPOINT - ACEITA MÉTODO GET
def get_users():
    connection, cursor = to_connect()
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    connection.close()
    return jsonify(users)

# ENDPOINT TO ADD USERS
@app.route('/users', methods=['POST'])
def add_user():
    data = request.get_json() # OBTEM DADOS ENVIADOS EM UM DICIO PYTHON CONVERTENDO PARA FORMATO JSON
    connection, cursor = to_connect()
    cursor.execute('INSERT INTO users (email, password, name, status) VALUES (?, ?, ?, ?)',
                   (data['email'], data['password'], data['name'], data['status']))
    connection.commit()
    connection.close()
    return jsonify({'message': 'User added successfully'})


# ENDPOINT TO UPDATE USERS
@app.route('/users/<int:id>', methods=['PUT'])
def update_user(id):
    data = request.get_json()
    connection, cursor = to_connect()

    # VERIFICA QUAIS CAMPOS FORAM ENVIADOS NO JSON E ATUALIZA SOMENTE OS MESMOS

    fields = []
    values = []

    if 'email' in data:
        fields.append('email = ?')
        values.append(data['email'])

    if 'password' in data:
        fields.append('password = ?')
        values.append(data['password'])

    if 'name' in data:
        fields.append('name = ?')
        values.append(data['name'])
    
    if 'status' in data:
        fields.append('status = ?')
        values.append(data['status'])

    values.append(id)

    cursor.execute(f"UPDATE users SET {', '.join(fields)} WHERE id = ?", values)        

    connection.commit()
    connection.close()
    return jsonify({'message': 'User updated successfully'})

# ENDPOINT TO DELETE USERS
@app.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    connection, cursor = to_connect()
    cursor.execute('DELETE FROM users WHERE id = ?', (id,))
    connection.commit()
    connection.close()
    return jsonify({'message': 'User deleted successfully'})

# ENDPOINT TO HEALTH CHECK
@app.route('/health', methods=['GET'])
def health_check():
    try:
        connection, cursor = to_connect()
        cursor.execute('SELECT 1')
        connection.close()
        return jsonify({'status': 'Database connection is active'}), 200
    except sqlite3.Error as e:
        return jsonify({'status': 'Database connection faild'}), 500

if __name__ == '__main__':
    app.run(debug=True) # INICIA O SERVIDOR EM MODO DEPURAÇÃO (FORNECE DETALHES DE ERROS E REINICIA AUTO QUANDO CÓDIGO ALTERADO)


