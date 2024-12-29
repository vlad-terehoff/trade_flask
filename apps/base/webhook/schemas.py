from datetime import date
from settings.dto_base import BaseDto
from pydantic import field_serializer
from datetime import datetime


class WebhookDTO(BaseDto):
    id: int
    user_id: int
    id_transaction: int
    status: str
    amount: float
    created_at: datetime

    @field_serializer('created_at')
    def serialize_date(self, d: date):
        return date.strftime(d, "%d.%m.%Y %H.%M.%S")