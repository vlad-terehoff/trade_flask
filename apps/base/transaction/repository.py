from settings.data_base import db
from flask import abort, jsonify
from transaction.models import Transaction, TransactionStatus
from user.models import User
from decimal import Decimal as D


def create_transaction_rep(data):
    user_id = data.get('user_id')
    amount = data.get('amount')

    with db.session.begin():
        user: User = User.query.filter_by(id=user_id).with_for_update().first()
        if user:
            user_balance = user.balance

            amount = D(amount)

            final_amount = user_balance - amount

            if final_amount >= 0:
                user.balance -= amount

                tax = round((amount * user.commission), 3)
                final_amount = round((amount - tax), 3)
                transaction: Transaction = Transaction(user_id=user_id, amount=final_amount, commission=tax)
                db.session.add(transaction)

                db.session.commit()

                return transaction

            return abort(400, description="Insufficient funds!")

        return abort(404, description="User not found!")


def cancel_transaction_rep(data):
    transaction_id = data.get('transaction_id')

    stmt = (
        db.update(Transaction).
        where(Transaction.id == transaction_id).
        values(status=TransactionStatus.CANCELLED).
        returning(Transaction)
    )

    result = db.session.execute(stmt)
    db.session.commit()

    updated_transaction = result.fetchone()

    if updated_transaction:

        return updated_transaction[0]

    return abort(404, description="Transaction not found!")


def check_transaction_rep(transaction_id):

    transaction = Transaction.query.get(transaction_id)

    if transaction:
        return transaction

    return abort(404, description="Transaction not found!")

