import functools

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
            fk.g.bamboo = Bamboo.fetch_by(user_bamboo)

        if user_branch is None:
            fk.g.branch = None
        else:
            fk.g.branch = Branch.fetch_by(user_branch)


@blueprint.route('/')
@login_required
def bamboos():
    user_bamboos = [Bamboo.fetch_by(bamboo_uuid) for bamboo_uuid in fk.g.user.get_column('bamboos')]

    return fk.render_template(
        'app/bamboos.html',
        bamboos=user_bamboos
    )


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
    bamboo_created = Bamboo.instant(fk.request.form['bamboo_name'], fk.g.user.get_column('uuid'))
    fk.g.user.get_column('bamboos').append(bamboo_created.get_column('uuid'))
    fk.g.user.update()
    fk.session['bamboo'] = bamboo_created.get_column('uuid')
    return fk.redirect(fk.url_for('app.bamboo.bamboo_page'))


def bamboo_required(view):
    @functools.wraps(view)
    def wrapped_view(*args, **kwargs):
        if fk.g.bamboo is None:
            return fk.redirect(fk.url_for('app.bamboo.creation_form'))

        return view(*args, **kwargs)

    return wrapped_view


@blueprint.route('/create-branch')
@login_required
@bamboo_required
def create_branch():
    return fk.render_template('app/create_branch.html')


@blueprint.route('/branch-creation-ongoing', methods=['POST'])
@login_required
@bamboo_required
def branch_creation_execution():
    branch_created = Branch.instant(fk.request.form['branch_name'], fk.g.bamboo.get_column('uuid'))
    fk.session['branch'] = branch_created.get_column('uuid')
    return fk.redirect(fk.url_for('app.bamboo.bamboo_page', bamboo_uuid=fk.g.bamboo.get_column('uuid'),
                                  branch_uuid=branch_created.get_column('uuid')))
