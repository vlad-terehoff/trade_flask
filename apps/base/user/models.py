from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, Numeric, CheckConstraint
from flask_login import UserMixin
from enum import StrEnum
from decimal import Decimal
from settings.data_base import db


class UserRoles(StrEnum):
    ADMIN = 'Админ'
    ORDINARY = 'Обычный'


class User(db.Model, UserMixin):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(255))
    password: Mapped[str] = mapped_column(String(255))
    balance: Mapped[Decimal] = mapped_column(default=0)
    commission: Mapped[Decimal] = mapped_column(Numeric(1, 3), default=0.001)
    url_webhook: Mapped[str] = mapped_column(String(255), nullable=True)
    usdt_wallet: Mapped[str] = mapped_column(String(255), nullable=True)
    role: Mapped[UserRoles] = mapped_column(default=UserRoles.ORDINARY)

    transactions: Mapped[list["Transaction"]] = relationship(back_populates='user')

    webhooks: Mapped[list["Webhook"]] = relationship(back_populates='user')

    __table_args__ = (
        CheckConstraint('balance >= 0', name='check_balance_non_negative'),
    )

    def __repr__(self):
        return f'{self.username}'


from transaction.models import Transaction
from webhook.models import Webhook
