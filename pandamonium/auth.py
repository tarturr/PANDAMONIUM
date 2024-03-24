import flask as fk

from pandamonium.security import get_security_error, date_from_string, is_security_error
from pandamonium.user import User

blueprint = fk.Blueprint('auth', __name__, url_prefix='/auth')


# TODO: Create template for these pages.

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
        user.create()

        if is_security_error():
            fk.flash(get_security_error())
        else:
            return fk.redirect(fk.url_for('index'))

    return '<p>Register</p>'


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

    return '<p>Login</p>'


@blueprint.route('/logout')
def logout_page():
    """Page dont l'usage unique est de déconnecter l'utilisateur du site web."""
    fk.session.clear()
    return fk.redirect(fk.url_for('index'))
