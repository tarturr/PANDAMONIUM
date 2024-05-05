import flask as fk
import flask_socketio as sock

from pandamonium.entities.user import User
from pandamonium.routes.auth import login_required

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


@blueprint.route('/')
@blueprint.route('/feed')
@login_required
def feed():
    """Retourne le feed de l'utilisateur."""
    return fk.render_template('feed.html')


@blueprint.route('/bamboo/<string:bamboo_uuid>')
@login_required
def bamboo(bamboo_uuid: str = None):
    """Charge le bamboo visé s'il y en a un, sinon affiche la liste des bamboos de l'utilisateur."""
    user = fk.g.user
    return fk.render_template('app/bamboo.html', user=user)

    # if bamboo_uuid is not None:
    #     # Si l'utilisateur a bien le bamboo dans sa liste de bamboos
    #     if any([bamboo_uuid == bamboo_column.name for bamboo_column in user.get_column('bamboos').value]):
    #         # Rediriger vers le bamboo en question
    #         return fk.render_template('app/bamboo.html', user=user)
    #
    # return fk.render_template('app/bamboos.html', user=user)


def register_events(socket: sock.SocketIO):
    """Enregistre tous les events de messagerie existants dans l'application PANDAMONIUM.

    :param sock.SocketIO socket: L'instance de l'application Flask SocketIO."""
    socket.on_event('user_logged', user_logged)


def user_logged(data):
    print('Yup', data)
