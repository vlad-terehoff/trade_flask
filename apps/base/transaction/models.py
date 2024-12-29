from settings.data_base import db
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import text, Integer, Numeric, ForeignKey, CheckConstraint
from enum import StrEnum
from datetime import datetime
from decimal import Decimal


class TransactionStatus(StrEnum):
    WAITING = 'Ожидание'
    CONFIRMED = 'Подтверждена'
    CANCELLED = 'Отменена'
    EXPIRED = 'Истекла'


class Transaction(db.Model):
    __tablename__ = "transactions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    user: Mapped["User"] = relationship(back_populates='transactions')

    created_at: Mapped[datetime] = mapped_column(
        server_default=text("TIMEZONE('utc', now())")
    )

    status: Mapped[TransactionStatus] = mapped_column(default=TransactionStatus.WAITING)
    amount: Mapped[Decimal] = mapped_column(Numeric(precision=None, scale=5))
    commission: Mapped[Decimal] = mapped_column(Numeric(precision=None, scale=3))

    __table_args__ = (
        CheckConstraint('amount >= 0', name='check_commission_non_negative'),
    )


from user.models import User
