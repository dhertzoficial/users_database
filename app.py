from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

def to_connect():
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()
    return connection, cursor

@app.route('/users', methods=['GET'])
def get_users():
    connection, cursor = to_connect()
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    connection.close()
    return jsonify(users)

@app.route('/users', methods=['POST'])
def add_user():
    data = request.get_json()
    connection, cursor = to_connect()
    cursor.execute('INSERT INTO users (email, password, name, status) VALUES (?, ?, ?, ?)',
                   (data['email'], data['password'], data['name'], data['status']))
    connection.commit()
    connection.close()
    return jsonify({'message': 'User added successfully'})

@app.route('/users/<int:id>', methods=['PUT'])
def update_user(id):
    data = request.get_json()
    connection, cursor = to_connect()
    cursor.execute('''
        UPDATE users
        SET email = ?, password = ?, name = ?, status = ?
        WHERE id = ?
    ''', (data['email'], data['password'], data['name'], data['status'], id))
    connection.commit()
    connection.close()
    return jsonify({'message': 'User updated successfully'})

@app.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    connection, cursor = to_connect()
    cursor.execute('DELETE FROM users WHERE id = ?', (id,))
    connection.commit()
    connection.close()
    return jsonify({'message': 'User deleted successfully'})

if __name__ == '__main__':
    app.run(debug=True)


