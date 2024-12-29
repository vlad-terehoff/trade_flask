from flask import request
from transaction.repository import create_transaction_rep, cancel_transaction_rep, check_transaction_rep
from transaction.schemas.transaction_schemas import TransactionDTO
from flask_restx import Resource, Namespace, fields


transaction_blueprint = Namespace('transaction', description='Transaction operations')

transaction_model_create = transaction_blueprint.model('Transaction create', {
    'user_id': fields.Integer(required=True, description='ID пользователя'),
    'amount': fields.Float(required=True, description='Сумма операции')
})

# Определяем модель для возвращаемых данных (если отличается от входящих)
response_model = transaction_blueprint.model('TransactionResponse', {
    'id': fields.Integer(description='ID транзакции'),
    'user_id': fields.Integer(description='ID пользователя'),
    'created_at': fields.DateTime(description='Время создания'),
    'status': fields.String(description='Статус транзакции'),
    'amount': fields.Float(description='Сумма транзакции'),
    'commission': fields.Float(description='Комиссия транзакции'),

})

transaction_model_cancel = transaction_blueprint.model('Transaction cancel', {
    'transaction_id': fields.Integer(required=True, description='ID транзакции'),
})


@transaction_blueprint.route('/create_transaction')
class TransactionResourceCreate(Resource):
    @transaction_blueprint.doc(
        description="Create a new transaction",
        responses={
            200: ('Transaction created successfully', response_model),
            400: 'Insufficient funds',
            404: 'User not found'
        }
    )
    @transaction_blueprint.expect(transaction_model_create)
    def post(self):

        data = request.get_json()

        result = create_transaction_rep(data)

        return TransactionDTO.from_orm(result).model_dump(), 200


@transaction_blueprint.route('/cancel_transaction')
class TransactionResourceCancel(Resource):
    @transaction_blueprint.doc(
        description="Cancel transaction",
        responses={
            200: ('Transaction canceled successfully', response_model),
            404: 'transaction not found'
        }
    )
    @transaction_blueprint.expect(transaction_model_cancel)
    def post(self):

        data = request.get_json()

        result = cancel_transaction_rep(data)

        return TransactionDTO.model_validate(result).model_dump(), 200


@transaction_blueprint.route('/check_transaction')
class TransactionResourceCheck(Resource):
    @transaction_blueprint.doc(
        params={
            'transaction_id': {'description': 'ID транзакции', 'type': 'integer', 'required': True},},
        description="Check transaction",
        responses={
            200: ('Transaction find successfully', response_model),
            404: 'transaction not found'
        }
    )
    def get(self):

        transaction_id = request.args.get('transaction_id', type=int)

        result = check_transaction_rep(transaction_id)

        return TransactionDTO.model_validate(result).model_dump(), 200