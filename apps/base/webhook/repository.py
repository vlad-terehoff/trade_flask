from typing import List
from settings.data_base import db
from webhook.models import Webhook
from webhook.schemas import WebhookDTO


def cretae_webhook(body: dict):
    transaction: Webhook = Webhook(**body)
    db.session.add(transaction)

    db.session.commit()

    return True


def users_webhooks(id):
    webhooks: List[Webhook] = db.session.query(Webhook).where(Webhook.user_id == id).all()

    clear_webhooks = [WebhookDTO.model_validate(i).model_dump() for i in webhooks]

    return clear_webhooks
