import functools

import flask as fk

from pandamonium.security import get_security_error, date_from_string, is_security_error
from pandamonium.user import User

blueprint = fk.Blueprint('auth', __name__, url_prefix='/auth')


@blueprint.before_app_request
def load_user():
    """Fonction qui charge les données de l'utilisateur à partir de son nom stocké dans la session du client. Celle-ci
    s'exécute avant de charger une quelconque page du blueprint courant."""
    username = fk.session.get('username')

    if username is None:
        fk.g.user = None
    else:
        fk.g.user = User.fetch_by(username=username)


@blueprint.route('/register', methods=('GET', 'POST'))
def register_page():
    """Page d'inscription du site web."""
    if fk.request.method == 'POST':
        username = fk.request.form['username']
        email = fk.request.form['email']
        password = fk.request.form['password']
        date_of_birth = fk.request.form['date_of_birth']

        user = User(username, email, password, date_from_string(date_of_birth))

        if is_security_error():
            fk.flash(get_security_error())
        else:
            return fk.redirect(fk.url_for('index'))

    return fk.render_template('register.html')


@blueprint.route('/login', methods=('GET', 'POST'))
def login_page():
    """Page de connexion du site web."""
    if fk.request.method == 'POST':
        identifier = fk.request.form['identifier']
        password = fk.request.form['password']

        user = User.login(username=identifier, password=password)

        if user is None:
            fk.flash(get_security_error())
        else:
            fk.redirect(fk.url_for('index'))

    return fk.render_template('login.html')


@blueprint.route('/logout')
def logout_page():
    """Page dont l'usage unique est de déconnecter l'utilisateur du site web."""
    fk.session.clear()
    return fk.redirect(fk.url_for('index'))


def login_required(view):
    """Décorateur de view servant à rediriger l'utilisateur vers la page de connexion si ce dernier n'est pas encore
    connecté ou enregistré sur le site web.

    :param view: La fonction servant de view à la page web."""
    @functools.wraps(view)
    def view_wrapper(*args, **kwargs):
        if fk.g.user is None:
            return fk.redirect(fk.url_for('index'))

        return view(*args, **kwargs)

    return view_wrapper
