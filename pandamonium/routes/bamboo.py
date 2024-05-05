import flask as fk

from pandamonium.entities.bamboo import Bamboo
from pandamonium.entities.user import User
from pandamonium.routes.auth import login_required

blueprint = fk.Blueprint('bamboo', __name__, url_prefix='/bamboo')


@blueprint.before_app_request
def load_user():
    """Fonction qui charge les données de l'utilisateur à partir de son nom stocké dans la session du client. Celle-ci
    s'exécute avant de charger une quelconque page du blueprint courant."""
    username = fk.session.get('username')

    if username is None:
        fk.g.user = None
    else:
        fk.g.user = User.fetch_by(username=username)


@blueprint.route('/')
@login_required
def bamboos():
    return fk.render_template('app/bamboos.html')


@blueprint.route('/<bamboo_uuid>')
@login_required
def bamboo_page(bamboo_uuid):
    user_bamboos = fk.session.get('bamboos')

    if user_bamboos is None:
        fk.g.bamboos = {}

    fk.g.bamboos['bamboo' + bamboo_uuid] = Bamboo(bamboo_uuid)

    return fk.render_template('app/bamboo.html', bamboo_name=fk.g.bamboos['bamboo' + bamboo_uuid].name)


@blueprint.route('/create')
@login_required
def creation_form():
    return fk.render_template('app/create_bamboo.html')


@blueprint.route('/creation-ongoing', methods=['POST'])
@login_required
def creation_execution():
    bamboo_created = Bamboo(name=fk.request.form['bamboo_name'])
    return fk.redirect(fk.url_for('app.bamboo.bamboo_page', bamboo_uuid=bamboo_created.uuid))
