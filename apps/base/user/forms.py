from flask_wtf import FlaskForm
from wtforms.fields import SubmitField, StringField, PasswordField, SelectField
from wtforms.validators import DataRequired


class EditUserFormAdmin(FlaskForm):
    username = StringField('username', default='')
    balance = StringField('balance', default='')
    commission = StringField('commission', default='')
    usdt_wallet = StringField('usdt_wallet', default='')
    role = SelectField('Role', choices=[('', ''), ('Обычный', 'Обычный'), ('Админ', 'Админ')], default='')
    submit = SubmitField('submit', render_kw={'class': 'button'})


class EditUserForm(FlaskForm):
    username = StringField('username', default='')
    usdt_wallet = StringField('usdt_wallet', default='')
    submit = SubmitField('submit', render_kw={'class': 'button'})


class CreatetUserForm(FlaskForm):
    username = StringField('username',validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    balance = StringField('balance', default='50')
    usdt_wallet = StringField('usdt_wallet', default='')
    role = SelectField('Role', choices=[('Обычный', 'Обычный'), ('Админ', 'Админ')])
    submit = SubmitField('submit', render_kw={'class': 'button'})