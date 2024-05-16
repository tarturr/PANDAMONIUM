import flask as fk
import flask_socketio as sock

from pandamonium.entities.message import Message
from pandamonium.entities.user import User
from pandamonium.routes.auth import login_required
from pandamonium.routes import bamboo

blueprint = fk.Blueprint('app', __name__, url_prefix='/app')


@blueprint.before_app_request
def before_request():
    """Fonction qui charge les données de l'utilisateur à partir de son nom stocké dans la session du client. Celle-ci
    s'exécute avant de charger une quelconque page du blueprint courant."""
    username = fk.session.get('username')

    if username is None:
        fk.g.user = None
    else:
        fk.g.user = User.fetch_by(username=username)


blueprint.register_blueprint(bamboo.blueprint)


@blueprint.route('/')
@blueprint.route('/feed')
@login_required
def feed():
    """Retourne le feed de l'utilisateur."""
    return fk.render_template('app/feed.html')


def register_events(socket: sock.SocketIO):
    """Enregistre tous les events de messagerie existants dans l'application PANDAMONIUM.

    :param sock.SocketIO socket: L'instance de l'application Flask SocketIO."""
    socket.on_event('user_logged', user_logged)
    socket.on_event('user_message', user_message)


def user_logged(data):
    print('Yup', data)


def user_message(data):
    Message.instant(data['data'], fk.g.user.get_column('uuid'), fk.g.branch.get_column('uuid'))
    sock.emit('user_message', data, broadcast=True)
