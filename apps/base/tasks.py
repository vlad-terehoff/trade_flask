from datetime import datetime, timezone, timedelta
from typing import List
from app import celery
from settings.data_base import db
from transaction.models import Transaction
import requests
from settings.settings import settings
from user.models import User
from tronpy import Tron


@celery.task(name='tasks.check_transactions')
def check_transactions():
    fifteen_minutes_ago = datetime.now(timezone.utc) - timedelta(minutes=15)
    transactions_to_check = Transaction.query.filter(Transaction.created_at < fifteen_minutes_ago).all()

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
    client = Tron()

    users: List[User] = User.query.all()

    for user in users:
        balance = client.get_account_balance(user.usdt_wallet)


