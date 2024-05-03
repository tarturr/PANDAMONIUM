import flask as fk

import os
import yaml
import typing

from pandamonium.routes import auth
from pandamonium.commands import register_commands
from pandamonium.database import close_db


def create_app(test_config: typing.Mapping[str, typing.Any] = None):
    """Fonction de création de l'application Flask avec la possibilité de définir une configuration spécifique durant
    la phase de test. Si elle n'est pas fournie, alors Flask va chercher le fichier de configuration par défaut,
    config.yml, qui n'existe pour le moment pas.

    :param test_config: Configuration de test de l'application."""
    app = fk.Flask(__name__, instance_relative_config=True)

    with app.open_resource('db_credentials.yml') as db_credentials_file:
        db_credentials = yaml.safe_load(db_credentials_file)

    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE_CREDENTIALS=db_credentials,
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    register_commands(app)
    app.teardown_appcontext(close_db)
    app.register_blueprint(auth.blueprint)

    @app.route('/')
    def index():
        if 'username' in fk.session :
            return fk.render_template('logged_in_index.html') # afficher le feed*
        else :
            return fk.render_template('index.html')

    return app
