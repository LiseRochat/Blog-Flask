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
app.config['SECRET_KEY'] = 'fWnVHxWvfaxYYKwvcYGmmiQnZjELBLWw'

def get_db_connection():
    """
    Connection to the database

    Returns:
        connection: valid connection 
    """
    connection = sqlite3.connect('database.db')
    connection.row_factory = sqlite3.Row
    return connection

def get_db_post(post_id):
    """
    Select the line in the post table present in the database corresponding to the id

    Args:
        post_id (int): post identifier (unique for each post contained in the database)

    Returns:
        post: returns the content of the post
    """
    dict_post_id = {"id" : post_id}
    conn = get_db_connection()
    post = conn.execute('SELECT * FROM posts WHERE id = :id', dict_post_id).fetchone()
    conn.close()
    if post is None:
        abort(404)
    return post

@app.route('/')
def index():
    """
    Home page

    Returns:
        template: template index.html
    """
    conn = get_db_connection()
    posts = conn.execute('SELECT * FROM posts').fetchall()
    conn.close()
    return render_template('blog/index.html', posts=posts)

@app.route('/<int:post_id>')
def post(post_id):
    """
    Page: Zoom article

    Args:
        post_id (int): item id

    Returns:
        template: template post.html
    """
    post = get_db_post(post_id)
    return render_template('blog/post.html', post=post)

@app.route('/create', methods=('GET', 'POST'))
def create_post():
    """
    Article creation form page

    Returns:
        template: template create.html or index.html if post is adding on database 
    """
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        post = {
            "title" : title,
            "content" : content
        }
        if not title and not content:
            flash('Tous les champs sont requis !')
        else:
            conn = get_db_connection()
            conn.execute('INSERT INTO posts (title, content) VALUES (:title, :content)', post)
            conn.commit()
            conn.close()
            return redirect(url_for('index'))

    return render_template('blog/create.html')

@app.route('/<int:id>/edit', methods=('GET', 'POST'))
def edit(id):
    """
    Edit one article

    Args:
        id (int): item id

    Returns:
        template: template edit.html or index.html if post is adding on database 
    """
    post = get_db_post(id)

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        post = {
            "id" : id,
            "title" : title,
            "content" : content
        }
        if not title and not content:
            flash('Tous les champs sont requis !')
        else:
            conn = get_db_connection()
            conn.execute('UPDATE posts SET title = :title, content = :content'
                         ' WHERE id = :id', post)
            conn.commit()
            conn.close()
            return redirect(url_for('index'))

    return render_template('blog/edit.html', post=post)

@app.route('/<int:id>/delete', methods=('POST',))
def delete(id):
    """delete one article

    Args:
        id (int): id post

    Returns:
        url: redirect to home page
    """
    post = get_db_post(id)
    d = {
        "id" : id
    }
    conn = get_db_connection()
    conn.execute('DELETE FROM posts WHERE id = :id', d)
    conn.commit()
    conn.close()
    flash('"{}" was successfully deleted!'.format(post['title']))
    return redirect(url_for('index'))
