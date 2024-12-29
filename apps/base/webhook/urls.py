from flask import render_template, Blueprint
from flask_login import login_required, current_user

from webhook.repository import users_webhooks

webhooks_blueprint = Blueprint('webhooks', __name__, template_folder='templates', static_folder='static')


@webhooks_blueprint.route('/webhooks')
@login_required
def get_users_webhooks():

    webhooks = users_webhooks(current_user.id)
    return render_template('webhooks.html', webhooks=webhooks)