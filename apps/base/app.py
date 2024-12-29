from flask import Flask, render_template
from commands.create_admin.command import create_admin
from login.api import login_blueprint
from flask_migrate import Migrate
from settings.data_base import db
from settings.login_manager import login_manager
from settings.settings import settings
from settings.user_loader import load_user
from statistics.urls import statistics_blueprint
from transaction.api import transaction_blueprint
from flask_restx import Api
from flask_login import login_required, current_user
from celery import Celery
from transaction.urls import for_transaction_blueprint
from user.urls import profiles_blueprint
from datetime import timedelta

from webhook.urls import webhooks_blueprint

app = Flask(__name__)


api = Api(app, title="API", description="API", doc="/documentation")

app.config['CELERY_BROKER_URL'] = f'redis://{settings.redis_host}:6379/5'
app.config['CELERY_RESULT_BACKEND'] = f'redis://{settings.redis_host}:6379/5'

celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

app.secret_key = settings.secret_key

app.config['SQLALCHEMY_DATABASE_URI'] = settings.database_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
login_manager.init_app(app)
login_manager.login_view = 'login.login'
migrate = Migrate(app, db)

app.cli.add_command(create_admin)

app.register_blueprint(login_blueprint)
app.register_blueprint(statistics_blueprint)
app.register_blueprint(profiles_blueprint)
app.register_blueprint(for_transaction_blueprint)
app.register_blueprint(webhooks_blueprint)


api.add_namespace(transaction_blueprint)


celery.conf.beat_schedule = {
    'check-transactions-every-15-minutes': {
        'task': 'tasks.check_transactions',
        'schedule': timedelta(minutes=15),
    },

    'check-check_usdt_wallet-every-5-minutes': {
        'task': 'tasks.check_usdt_wallet',
        'schedule': timedelta(minutes=5),
    },
}


@app.route('/')
@app.route('/index')
@login_required
def index():
    return render_template('index.html', user=current_user)


if __name__ == '__main__':
    app.run(debug=settings.debug)
