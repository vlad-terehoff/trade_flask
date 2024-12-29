from settings.data_base import db
from transaction.models import Transaction
from transaction.schemas.transaction_schemas import TransactionDTO, EditTransactionDTO
from user.models import User
from user.schemas.user_schemas import UserDTO
from sqlalchemy import and_


def get_all_users():
    users = User.query.all()

    profiles = [UserDTO.model_validate(i).model_dump() for i in users]
    return profiles


def get_all_transactions_for_admin(user_id, status):
    if user_id and status:
        transactions = db.session.query(Transaction).filter(and_(Transaction.user_id == user_id,
                                                                 Transaction.status == status)).all()


    elif user_id:
        transactions = db.session.query(Transaction).where(Transaction.user_id == user_id).all()


    elif status:
        transactions = db.session.query(Transaction).where(Transaction.status == status).all()


    else:
        transactions = Transaction.query.all()

    clear_transactions = [TransactionDTO.model_validate(i).model_dump() for i in transactions]
    return clear_transactions


def get_all_transactions(id):
    transactions = db.session.query(Transaction).where(Transaction.user_id == id).all()

    clear_transactions = [TransactionDTO.model_validate(i).model_dump() for i in transactions]
    return clear_transactions


def edit_one_transaction_for_admin(id, body):
    clear_body= EditTransactionDTO(**body).model_dump()
    stmt = (
        db.update(Transaction).
        where(Transaction.id == id).
        values(clear_body).
        returning(Transaction)
    )

    result = db.session.execute(stmt)
    db.session.commit()

    updated_user = result.fetchone()

    if updated_user:
        return updated_user[0]