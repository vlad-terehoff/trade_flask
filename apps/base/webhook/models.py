from datetime import datetime
from settings.data_base import db
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, ForeignKey


class Webhook(db.Model):
    __tablename__ = "webhooks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    user: Mapped["User"] = relationship(back_populates='webhooks')

    id_transaction: Mapped[int]
    status: Mapped[str] = mapped_column(String(255))

    amount: Mapped[float]

    created_at: Mapped[datetime]

    def __repr__(self):
        return f'{self.username}'


from user.models import User