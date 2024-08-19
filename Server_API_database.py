from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3

# Flask Application Initialization
app = Flask(__name__) # Create an Instance of the Flask Class
CORS(app) # Enable CORS for the Flask Application

def to_connect():
    connection = sqlite3.connect("database.db") # Create Connection to the Database
    cursor = connection.cursor() # Cursor Is Used to Execute SQL Commands on the Database
    return connection, cursor

def check_id_exists(user_id):
    connection, cursor = to_connect()
    cursor.execute("SELECT EXISTS(SELECT 1 FROM users WHERE id = ?)", (user_id,))
    exists = cursor.fetchone()[0]
    connection.close()
    return exists

def check_email_exists(email):
    connection, cursor = to_connect()
    cursor.execute("SELECT EXISTS(SELECT 1 FROM users WHERE email = ?)", (email,))
    exists = cursor.fetchone()[0]
    connection.close()
    return exists

# Endpoint to Get Users
@app.route('/users', methods=['GET']) # Set the Route for the Endpoint - Supports GET Method
def get_users():
    try:
        connection, cursor = to_connect()
        cursor.execute("SELECT id, email, password, name, status FROM users")
        users = cursor.fetchall()
        connection.close()
        result = []
        for user in users:
            v = {"id": user[0], "email": user[1], "password": user[2], "name": user[3], "status": user[4]}
            result.append(v)
        return jsonify(result)
    except sqlite3.Error as e:
        return jsonify({'error': str(e)}), 500

# ENDPOINT TO ADD USERS
@app.route('/users', methods=['POST'])
def add_user():
    data = request.get_json() # Gets Data Sent as a Python Dictionary and Converts It to JSON Format
    try:
        connection, cursor = to_connect()
        cursor.execute('INSERT INTO users (email, password, name, status) VALUES (?, ?, ?, ?)',
                       (data['email'], data['password'], data['name'], data['status']))
        connection.commit()
        connection.close()
        return jsonify({'message': 'User added successfully'})
    except sqlite3.Error as e:
        return jsonify({'error': str(e)}), 500

# ENDPOINT TO UPDATE USERS
@app.route('/users/<int:id>', methods=['PUT'])
def update_user(id):
    data = request.get_json()
    try:
        connection, cursor = to_connect()

        # Verifies Which Fields Were Included in the JSON and Updates Only Those
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
    except sqlite3.Error as e:
        return jsonify({'error': str(e)}), 500

# ENDPOINT TO DELETE USERS
@app.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    try:
        connection, cursor = to_connect()
        cursor.execute('DELETE FROM users WHERE id = ?', (id,))
        connection.commit()
        connection.close()
        return jsonify({'message': 'User deleted successfully'})
    except sqlite3.Error as e:
        return jsonify({'error': str(e)}), 500

# ENDPOINT TO HEALTH CHECK
@app.route('/health', methods=['GET'])
def health_check():
    try:
        connection, cursor = to_connect()
        cursor.execute('SELECT 1')
        connection.close()
        return jsonify({'status': 'Database connection is active'}), 200
    except sqlite3.Error as e:
        return jsonify({'status': 'Database connection failed', 'error': str(e)}), 500

@app.route('/users/exists', methods=['GET'])
def id_exists_endpoint():
    user_id = request.args.get('id')
    exists = check_id_exists(user_id)
    return jsonify({'exists': exists})

@app.route('/users/email_exists', methods=['GET'])
def email_exists_endpoint():
    email = request.args.get('email')
    exists = check_email_exists(email)
    return jsonify({'exists': exists})

if __name__ == '__main__':
    app.run(debug=True) # Starts the Server in Debug Mode (Provides Error Details and Auto-Restarts on Code Changes)
