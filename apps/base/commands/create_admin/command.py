import click
from flask.cli import with_appcontext
from werkzeug.security import generate_password_hash
from settings.data_base import db
from user.models import User, UserRoles
from user.utils import create_usdt_wallet, generate_tax


@click.command('create-admin')
@click.option('--username', default='admin', help='Username for the admin')
@click.option('--password', prompt=True, hide_input=True, confirmation_prompt=True, help='Password for the admin')
@with_appcontext
def create_admin(username: str, password: str):
    with db.session.begin():  # Используем контекст
        user = User.query.filter_by(username=username).first()
        if user:
            click.echo(f'Admin user {username} already exists')
        else:
            usdt_wallet = create_usdt_wallet()
            commission = generate_tax()
            hashed_password = generate_password_hash(password, method='pbkdf2:sha256', salt_length=16)
            new_user = User(username=username,
                            password=hashed_password,
                            role=UserRoles.ADMIN,
                            usdt_wallet=usdt_wallet,
                            commission=commission)
            db.session.add(new_user)
            click.echo(f'Admin user {username} created successfully')

