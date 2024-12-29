from flask_wtf import FlaskForm
from wtforms.validators import DataRequired
from wtforms.fields import PasswordField, StringField, SubmitField


class Login(FlaskForm):
    username = StringField('username', validators=[DataRequired()])
    password = PasswordField('passwrod', validators=[DataRequired()])
    submit = SubmitField('submit', render_kw={'class': 'button'})

