import sqlite3
import os

CUR_DIR = os.path.dirname(__file__)
DATA_FILE = os.path.join(CUR_DIR, 'schema.sql')

# Open connection at database file
connection = sqlite3.connect('database.db')

# Open and execute content file to create post table
with open(DATA_FILE) as file:
    connection.executescript(file.read())

# instance of Cursor class
cursor = connection.cursor()

# Insert content in post table with execute method of Cursor class
post1 = {
    "title" : "Mes connaissances en Python",
    "content" : "Ce que je connais de Python mais surtout ce que je pratique sur des petits projets : Les types natifs, Manipuler des chaînes de caractères, Manipuler des objets natifs, Les variables, Affectation simple, parallèle et multiple, Conversion de nommage, Les opérateurs mathématiques, Le formatage des chaînes de caractères, Interagir avec l'utilisateur, Les structures conditionnelles, Les erreurs, Les listes, Modifier une liste, Les appartenances, Les Boucles, Les fichiers, Les dictionnaires, La gestion des erreurs, Les fonctions, Les modules et packages, Documenter son code, Le logging, Installer des packages avec PIP, La programmation orientée objet, Les bases de données",
}
cursor.execute("INSERT INTO posts (title, content) VALUES (:title, :content)", post1)
post2 = {
    "title" : "Points de Progression ",
    "content" : "Les différents points de progression que je dois encore approfondir sont les suivants : La gestion des dates, L'Étude plus approfondi des différents modules et packages pour ne pas réinventer la roue ! Les différentes bases de données, Le framework Flask et Django, La data science, les applications de bureaux",
}
cursor.execute("INSERT INTO posts (title, content) VALUES (:title, :content)", post2)
connection.commit()
connection.close()