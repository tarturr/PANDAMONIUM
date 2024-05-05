import flask as fk
import flask_socketio as sock

import os
import yaml
import typing

from pandamonium.routes import auth, app
from pandamonium.commands import register_commands
from pandamonium.database import close_db
from pandamonium.routes.app import register_events


flask_app = fk.Flask(__name__, instance_relative_config=True)

with flask_app.open_resource('db_credentials.yml') as db_credentials_file:
    db_credentials = yaml.safe_load(db_credentials_file)

flask_app.config.from_mapping(
    SECRET_KEY='dev',
    DATABASE_CREDENTIALS=db_credentials,
)

socket = sock.SocketIO(flask_app)
flask_app.config.from_pyfile('config.py', silent=True)

try:
    os.makedirs(flask_app.instance_path)
except OSError:
    pass

register_commands(flask_app)
flask_app.teardown_appcontext(close_db)
flask_app.register_blueprint(auth.blueprint)
flask_app.register_blueprint(app.blueprint)


@flask_app.route('/')
def index():
    if 'username' in fk.session:
        return fk.redirect(fk.url_for('app.feed'))
    else:
        return fk.render_template('index.html')


register_events(socket)

if __name__ == '__main__':
    socket.run(flask_app, allow_unsafe_werkzeug=True)
