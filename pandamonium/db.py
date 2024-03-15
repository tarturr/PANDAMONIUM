import sqlite3

from flask import g, current_app


def get_db() -> sqlite3.Connection:
    """Retourne un objet Connection représentant la connexion à la base de données. Si la connexion n'a pas encore été
    établie, elle le devient. Sinon, elle est renvoyée telle quelle.

    :return: Une instance de la connexion à la base de données.
    :rtype: sqlite3.Connection"""
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            timeout=20.0,

            # convertira les résultats obtenus des requêtes SQL en types natifs de Python.
            detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES
        )

        g.db.row_factory = sqlite3.Row

    return g.db


def init_db(set_default_values: bool):
    """Initialise la base de données en se servant du schema.sql fourni. Charge les valeurs par défaut si
    set_default_values=True.

    :param bool set_default_values: paramètre activant ou désactivant la création de valeurs par défaut dans la base de
    données."""
    db = get_db()

    with current_app.open_resource('schema_dev.sql' if set_default_values else 'schema.sql') as schema:
        db.executescript(schema.read().decode())


def close_db(e=None):
    """Ferme la connexion à la base de données."""
    db = g.pop('db', None)

    if db is not None:
        db.close()
