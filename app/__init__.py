import sqlite3
from flask import Flask, render_template
from werkzeug.exceptions import abort

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

def get_db_post(post_id):
    dict_post_id = {"id" : post_id}
    conn = get_db_connection()
    post = conn.execute('SELECT * FROM posts WHERE id = :id', dict_post_id).fetchone()
    conn.close()
    if post is None:
        abort(404)
    return post

app = Flask(__name__)

@app.route('/')
def index():
    conn = get_db_connection()
    posts = conn.execute('SELECT * FROM posts').fetchall()
    conn.close()
    return render_template('index.html', posts=posts)


