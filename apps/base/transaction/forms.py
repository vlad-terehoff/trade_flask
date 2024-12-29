from flask_wtf import FlaskForm
from wtforms.fields import SubmitField, SelectField


class EditTransactionForm(FlaskForm):
    status = SelectField('status', choices=[('Подтверждена', 'Подтверждена'), ('Отменена', 'Отменена')])
    submit = SubmitField('submit', render_kw={'class': 'button'})