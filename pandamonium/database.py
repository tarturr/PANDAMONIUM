import flask as fk

import mysql.connector as connector
import mysql.connector.abstracts as abstracts

from uuid import uuid4

import functools

from pandamonium.security import set_security_error


def requires(func):
    @functools.wraps(func)
    def wrapper(value, **kwargs):
        for key in kwargs:
            error_msg = func(kwargs[key], **kwargs)

            if error_msg:
                set_security_error(error_msg)
                return False

        return True

    return wrapper


def get_db() -> abstracts.MySQLConnectionAbstract:
    """Crée une instance de Connection représentant la connexion à la base de données. Si la connexion n'a pas encore
    été établie, elle le devient. Sinon, elle est renvoyée telle quelle.

    :rtype: MySQLCursorAbstract
    :return: Instance de la connexion à la base de données."""
    if 'db' not in fk.g:
        fk.g.db = connector.connect(**fk.current_app.config['DATABASE_CREDENTIALS'])
        fk.g.db.autocommit = True

        if fk.g.db.is_connected():
            print('[PANDAMONIUM] Successfully connected to database!')
        else:
            raise RuntimeError('Unable to connect to the database.')

    return fk.g.db


def init_db(set_default_values: bool):
    """Initialise la base de données en se servant du schema.sql fourni. Charge les valeurs par défaut si le paramètre
    set_default_values est défini sur True.

    :param bool set_default_values: Activer/désactiver la création de valeurs par défaut dans la base de données."""
    with fk.current_app.open_resource('schema_dev.sql' if set_default_values else 'schema.sql') as resource:
        sql_statements = filter(
            lambda line: not (line.startswith('--') or line.startswith('/*') or not line.strip()),
            resource.read().decode().split('\n')
        )

    db = get_db()

    with db.cursor() as cursor:
        for sql_statement in sql_statements:
            cursor.execute(sql_statement)


def close_db(e=None):
    """Ferme la connexion à la base de données."""
    db = fk.g.pop('db', None)

    if db is not None:
        db.close()