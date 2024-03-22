import mysql.connector as connector

from flask import g, current_app
from mysql.connector.abstracts import MySQLConnectionAbstract
from mysql.connector.pooling import PooledMySQLConnection


def get_db() -> PooledMySQLConnection | MySQLConnectionAbstract:
    """Retourne un objet Connection représentant la connexion à la base de données. Si la connexion n'a pas encore été
    établie, elle le devient. Sinon, elle est renvoyée telle quelle.

    :return: Une instance de la connexion à la base de données.
    :rtype: MySQLCursorAbstract"""
    if 'db' not in g:
        g.db = connector.connect(**current_app.config['DATABASE_CREDENTIALS'])

        if g.db.is_connected():
            print('[PANDAMONIUM] Successfully connected to database!')
        else:
            raise RuntimeError('Unable to connect to the database.')

    return g.db


def init_db(set_default_values: bool):
    """Initialise la base de données en se servant du schema.sql fourni. Charge les valeurs par défaut si
    set_default_values=True.

    :param bool set_default_values: paramètre activant ou désactivant la création de valeurs par défaut dans la base de
    données."""
    with current_app.open_resource('schema_dev.sql' if set_default_values else 'schema.sql') as resource:
        sql_statements = filter(
            lambda line: not (line.startswith('--') or line.startswith('/*') or not line.strip()),
            resource.read().decode().split('\n')
        )

    db = get_db()

    with db.cursor() as cursor:
        for sql_statement in sql_statements:
            print(f"Executing statement {sql_statement}")
            cursor.execute(sql_statement)

    db.commit()


def close_db(e=None):
    """Ferme la connexion à la base de données."""
    db = g.pop('db', None)

    if db is not None:
        db.close()
