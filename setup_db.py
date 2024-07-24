import sqlite3

def to_connect():
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT NOT NULL,
    password TEXT NOT NULL,
    name TEXT NOT NULL,
    status INTEGER NOT NULL)
    ''')
    connection.commit()
    connection.close()

# Executar a função para criar o banco de dados e a tabela
to_connect()
