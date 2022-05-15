import sqlite3
from flask import Flask, render_template

app = Flask(__name__)

def get_db_connection():
    """
    Connection a la base de donnée

    Returns:
        connection: connection valide 
    """
    connection = sqlite3.connect('database.db')
    connection.row_factory = sqlite3.Row
    return connection


app = Flask(__name__)

@app.route('/')
def index():
    conn = get_db_connection()
    posts = conn.execute('SELECT * FROM posts').fetchall()
    conn.close()
    return render_template('index.html', posts=posts)