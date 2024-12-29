from pydantic import field_serializer
from settings.dto_base import BaseDto
from datetime import date
from transaction.models import TransactionStatus
from datetime import datetime


class TransactionDTO(BaseDto):
    id: int
    user_id: int
    created_at: datetime
    status: TransactionStatus
    amount: float
    commission: float

    @field_serializer('created_at')
    def serialize_date(self, d: date):
        return date.strftime(d, "%d.%m.%Y %H.%M.%S")


class EditTransactionDTO(BaseDto):
    status: TransactionStatus
