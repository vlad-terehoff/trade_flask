from flask import request, render_template, Blueprint
from flask_login import login_required, current_user
from user.forms import EditUserFormAdmin, CreatetUserForm, EditUserForm
from user.repository import get_all_users, get_one_user, edit_one_user_for_admin, create_one_user, delete_user, \
    edit_one_user
from settings.settings import settings
from webhook.repository import cretae_webhook

profiles_blueprint = Blueprint('profiles', __name__, template_folder='templates', static_folder='static')


@profiles_blueprint.route('/webhook', methods=["POST"])
def receive_webhook():
    data = request.get_json()

    try:

        if data['token'] == settings.token:

            del data['token']

            if cretae_webhook(data):
                return {'ok': 'ok'}, 200

        return 404

    except:
        return 404



@profiles_blueprint.route('/profiles')
@login_required
def get_profiles():
    if current_user.role == 'Админ':
        profiles = get_all_users()
        return render_template('profiles.html', profiles=profiles)


@profiles_blueprint.route('/profiles/<int:id>')
@login_required
def get_profile_one(id: int):
    user = get_one_user(id)
    return render_template('profile_one.html', user=user)


@profiles_blueprint.route('/profile/<int:id>')
@login_required
def get_profile_for_admin(id: int):
    if current_user.role == 'Админ':
        user = get_one_user(id)
        return render_template('profile_for_admin.html', user=user)


@profiles_blueprint.route('/profile/edit/<int:id>', methods=["GET", "POST"])
@login_required
def edit_profile_for_admin(id: int):
    if current_user.role == 'Админ':
        form = EditUserFormAdmin()

        if request.method == 'POST':

            if form.validate_on_submit():
                id = int(request.form.get('id'))
                data = form.data
                user = edit_one_user_for_admin(id=id, body=data)
                return render_template('profile_for_admin.html', user=user)

        return render_template('edit_profiles.html', form=form, id=id)


@profiles_blueprint.route('/profile/create/', methods=["GET", "POST"])
@login_required
def create_profile_for_admin():
    if current_user.role == 'Админ':
        form = CreatetUserForm()

        if request.method == 'POST':

            if form.validate_on_submit():
                data = form.data
                user = create_one_user(body=data)
                return render_template('profile_for_admin.html', user=user)

        return render_template('create_profiles.html', form=form)


@profiles_blueprint.route('/profile/delete/<int:id>', methods=["GET"])
@login_required
def delete_profile_for_admin(id: int):
    if current_user.role == 'Админ':
        delete_user(id)
        profiles = get_all_users()
        return render_template('profiles.html', profiles=profiles)


@profiles_blueprint.route('/profile_one/edit/<int:id>', methods=["GET", "POST"])
@login_required
def edit_profile(id: int):
    form = EditUserForm()
    if request.method == 'POST':

        if form.validate_on_submit():
            id = int(request.form.get('id'))
            data = form.data
            user = edit_one_user(id=id, body=data)
            return render_template('profile_one.html', user=user)

    return render_template('edit_profiles_one.html', form=form, id=id)