from login.login import Login
from flask import request, render_template, redirect, Blueprint, url_for
from flask_login import login_user, logout_user, current_user
from user.models import User
from werkzeug.security import check_password_hash
from urllib.parse import urlsplit


login_blueprint = Blueprint('login', __name__, template_folder='templates', static_folder='static')


@login_blueprint.route("/login", methods=["GET", "POST"])
def login():
    form = Login()

    if request.method == 'POST':

        if form.validate_on_submit():
            username = form.username.data
            password = form.password.data
            data = {'username': username, 'password': password}

            user: User = User.query.filter_by(username=request.form['username']).first()

            data['id'] = user.id

            if user and check_password_hash(user.password, password):
                login_user(user)

                next_page = request.args.get('next')
                if not next_page or urlsplit(next_page).netloc != '':
                    return redirect(url_for('index'))
                return redirect(next_page)

            else:
                return render_template('login.html', form=form)

    return render_template('login.html', form=form)


@login_blueprint.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login.login'))