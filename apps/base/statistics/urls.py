from flask import render_template, Blueprint
from flask_login import login_required, current_user
from statistics.repository import get_statistic


statistics_blueprint = Blueprint('statistics', __name__, template_folder='templates', static_folder='static')


@statistics_blueprint.route('/statistics')
@login_required
def statistic():

    role = current_user.role
    data = get_statistic(role, current_user.id)
    return render_template('statistics.html', data=data)