import sqlite3
from flask import Flask
# which allows the use of the Jinja template engine
from flask import render_template
# to access data from the incoming request that will be submitted using an HTML form
from flask import request
# to generate URLs
from flask import url_for
# to display a message when a request is processed
from flask import flash
# to redirect the client to another location
from flask import redirect
# to acces erros page
from werkzeug.exceptions import abort

app = Flask(__name__)
# The user can access the information stored in the session, but cannot modify it if he does not have the secret key
app.config['SECRET_KEY'] = '59#MHsXLYP^iUnT3g4ebeoEasjrn5fz^ekBDvrVQ7yi$34SEx'

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
    """
    Sélectionne la ligne dans la table post présent dans la base de donnée corresponsant a l'id 

    Args:
        post_id (int): identifiant du post (unique pour chaque post contenu dans la base de donnée)

    Returns:
        post: retourne le contenu du post 
    """
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
    """
    Page d'accueil

    Returns:
        template: template index.html
    """
    conn = get_db_connection()
    posts = conn.execute('SELECT * FROM posts').fetchall()
    conn.close()
    return render_template('index.html', posts=posts)

@app.route('/<int:post_id>')
def post(post_id):
    """
    Page : Zoom article

    Args:
        post_id (int): identifiant de l'article

    Returns:
        template: template post.html
    """
    post = get_db_post(post_id)
    return render_template('post.html', post=post)

@app.route('/create', methods=('GET', 'POST'))
def create_post():
    return render_template('create.html')

