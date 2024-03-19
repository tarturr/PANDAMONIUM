from flask import Flask
import os

import yaml

import pandamonium.commands as commands
import pandamonium.db as db


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    with open(os.path.join(app.root_path, 'db_credentials.yml'), 'r') as db_credentials_file:
        db_credentials = yaml.safe_load(db_credentials_file)

    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE_CREDENTIALS=db_credentials,
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    commands.register_commands(app)
    app.teardown_appcontext(db.close_db)

    return app
