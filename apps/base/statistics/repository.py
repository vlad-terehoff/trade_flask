from settings.data_base import db
from transaction.models import Transaction
from sqlalchemy import func, and_
from datetime import datetime, timezone
from transaction.schemas.transaction_schemas import TransactionDTO
from user.models import User

today = datetime.now(timezone.utc)


def get_statistic(user_role, user_id: int | None = None):
    if user_role == 'Админ':
        last_ten_transaction = db.session.query(Transaction).where(func.date(Transaction.created_at) == today.date()).limit(10).all()
        total_sum = db.session.query(func.sum(Transaction.amount)).where(func.date(Transaction.created_at) == today.date()).scalar()
        user_count = db.session.query(func.count(User.id)).scalar()
        transaction_count = db.session.query(func.count(Transaction.id)).scalar()

        total_sum = total_sum if total_sum else 0

        clean_last_ten_transaction = [TransactionDTO.model_validate(i).model_dump() for i in last_ten_transaction]

        return {'last_ten_transaction': clean_last_ten_transaction,
                'total_sum': total_sum,
                'user_count': user_count,
                'transaction_count': transaction_count}

    if user_role == 'Обычный':
        last_ten_transaction = (db.session.query(Transaction).filter(and_(
            func.date(Transaction.created_at) == today.date(),
            Transaction.user_id == user_id)).limit(10).all())
        total_sum = db.session.query(func.sum(Transaction.amount)).filter(and_(
            func.date(Transaction.created_at) == today.date(),
            Transaction.user_id == user_id)).scalar()

        transaction_count = db.session.query(func.count(Transaction.id)).where(Transaction.user_id == user_id).scalar()

        total_sum = total_sum if total_sum else 0

        clean_last_ten_transaction = [TransactionDTO.model_validate(i).model_dump() for i in last_ten_transaction]

        return {'last_ten_transaction': clean_last_ten_transaction,
                'total_sum': total_sum,
                'transaction_count': transaction_count}

