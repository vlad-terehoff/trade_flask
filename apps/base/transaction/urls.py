from flask import request, render_template, Blueprint
from flask_login import login_required, current_user

from transaction.form_repository import get_all_transactions_for_admin, get_all_transactions, \
    edit_one_transaction_for_admin, get_all_users
from transaction.forms import EditTransactionForm

for_transaction_blueprint = Blueprint('form_transaction',
                                      __name__,
                                      template_folder='templates',
                                      static_folder='static')



@for_transaction_blueprint.route('/transactions')
@login_required
def get_transaction():
    if current_user.role == 'Админ':
        user_id = request.args.get('user_id')
        status = request.args.get('status')

        transactions = get_all_transactions_for_admin(user_id, status)
        users = get_all_users()
        return render_template('transactions.html', transactions=transactions, users=users)


@for_transaction_blueprint.route('/users_transactions/<int:id>')
@login_required
def get_users_transaction(id: int):
    transactions = get_all_transactions(id)
    return render_template('transactions.html', transactions=transactions)


@for_transaction_blueprint.route('/transaction/edit/<int:id>', methods=["GET", "POST"])
@login_required
def edit_transaction_for_admin(id: int):
    if current_user.role == 'Админ':
        form = EditTransactionForm()
        if request.method == 'POST':
            if form.validate_on_submit():
                id = int(request.form.get('id'))
                data = form.data
                transaction = edit_one_transaction_for_admin(id=id, body=data)
                return render_template('one_transaction.html', transaction=transaction)

        return render_template('edit_transaction.html', form=form, id=id)