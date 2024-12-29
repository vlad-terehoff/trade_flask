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
from webhook.urls import webhooks_blueprint
from datetime import datetime, timezone, timedelta
from typing import List
from transaction.models import Transaction
import requests
from user.models import User
from tronpy import Tron
from sqlalchemy import and_


app = Flask(__name__)


api = Api(app, title="API", description="API", doc="/documentation")

app.config['CELERY_BROKER_URL'] = f'redis://{settings.redis_host}:6379/5'
app.config['result_backend'] = f'redis://{settings.redis_host}:6379/5'

celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)
app.config.broker_connection_retry_on_startup = True

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

@celery.task(name='tasks.check_transactions')
def check_transactions():
    with app.app_context():
        fifteen_minutes_ago = datetime.now(timezone.utc) - timedelta(minutes=15)
        transactions_to_check = Transaction.query.filter(and_(Transaction.created_at < fifteen_minutes_ago,
                                                              Transaction.status == 'Ожидание')).all()

        urls_users_webhook = {}

        for transaction in transactions_to_check:
            transaction.status = 'Истекла'
            db.session.commit()

            url_user_webhook = urls_users_webhook.get(transaction.user_id)
            if url_user_webhook:

                data = {
                    "user_id": transaction.user_id,
                    "id_transaction": transaction.id,
                    "status": "Истекла",
                    "amount": float(transaction.amount),
                    "created_at": transaction.created_at.isoformat(),
                    "token": settings.token
                }

                requests.post(url_user_webhook, json=data)

            else:
                user: User = User.query.get(transaction.user_id)
                url_user_webhook = user.url_webhook
                urls_users_webhook[user.id] = url_user_webhook

                data = {
                    "user_id": transaction.user_id,
                    "id_transaction": transaction.id,
                    "status": "Истекла",
                    "amount": float(transaction.amount),
                    "created_at": transaction.created_at.isoformat(),
                    "token": settings.token
                }

                requests.post(url_user_webhook, json=data)


@celery.task(name='tasks.check_usdt_wallet')
def check_usdt_wallet():
    with app.app_context():
        client = Tron()

        users: List[User] = User.query.all()

        for user in users:
            balance = client.get_account_balance(user.usdt_wallet)

@app.route('/')
@app.route('/index')
@login_required
def index():
    return render_template('index.html', user=current_user)


if __name__ == '__main__':
    app.run(debug=settings.debug)
