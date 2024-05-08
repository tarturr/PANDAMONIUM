import flask as fk

from pandamonium.entities.bamboo import Bamboo
from pandamonium.entities.user import User
from pandamonium.entities.branch import Branch
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

        user_bamboo = fk.session.get('bamboo')
        user_branch = fk.session.get('branch')

        if user_bamboo is None:
            fk.g.bamboo = None
        else:
            fk.g.bamboo = Bamboo(user_bamboo)

        if user_branch is None:
            fk.g.branch = None
        else:
            fk.g.branch = Branch(user_branch)


@blueprint.route('/')
@login_required
def bamboos():
    return fk.render_template('app/bamboos.html')


@blueprint.route('/<bamboo_uuid>')
@blueprint.route('/<bamboo_uuid>/<branch_uuid>')
@login_required
def bamboo_page(bamboo_uuid, branch_uuid=None):
    return fk.render_template('app/bamboo.html')


@blueprint.route('/create')
@login_required
def creation_form():
    return fk.render_template('app/create_bamboo.html')


@blueprint.route('/creation-ongoing', methods=['POST'])
@login_required
def creation_execution():
    bamboo_created = Bamboo(name=fk.request.form['bamboo_name'])
    fk.session['bamboo'] = bamboo_created.uuid
    return fk.redirect(fk.url_for('app.bamboo.bamboo_page', bamboo_uuid=bamboo_created.uuid))


@blueprint.route('/create-branch')
@login_required
def create_branch():
    return fk.render_template('app/create_branch.html')


@blueprint.route('/branch-creation-ongoing', methods=['POST'])
@login_required
def branch_creation_execution():
    branch_created = Branch(fk.g.bamboo, name=fk.request.form['branch_name'])
    return fk.redirect(fk.url_for('app.bamboo.bamboo_page', bamboo_uuid=fk.g.bamboo.uuid,
                                  branch_uuid=branch_created.uuid))
