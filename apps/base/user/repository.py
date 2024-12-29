from settings.data_base import db
from user.models import User
from user.schemas.user_schemas import UserDTO, EditUserAdminDTO, EditUserDTO
from user.utils import create_usdt_wallet, generate_tax
from werkzeug.security import generate_password_hash
from flask import flash
from settings.settings import settings


def get_all_users():
    users = User.query.all()

    profiles = [UserDTO.model_validate(i).model_dump() for i in users]
    return profiles


def get_one_user(id):
    user = User.query.get(id)
    return UserDTO.model_validate(user).model_dump()


def edit_one_user_for_admin(id: int, body: dict):
    clear_body= EditUserAdminDTO(**body).model_dump(exclude_none=True)
    stmt = (
        db.update(User).
        where(User.id == id).
        values(clear_body).
        returning(User)
    )

    result = db.session.execute(stmt)
    db.session.commit()

    updated_user = result.fetchone()

    if updated_user:
        return updated_user[0]


def edit_one_user(id: int, body: dict):
    clear_body= EditUserDTO(**body).model_dump(exclude_none=True)
    stmt = (
        db.update(User).
        where(User.id == id).
        values(clear_body).
        returning(User)
    )

    result = db.session.execute(stmt)
    db.session.commit()

    updated_user = result.fetchone()

    if updated_user:
        return updated_user[0]

def create_one_user(body: dict):
    usdt_wallet = create_usdt_wallet()
    commission = generate_tax()
    hashed_password = generate_password_hash(body.get('password'), method='pbkdf2:sha256', salt_length=16)
    body['password'] = hashed_password
    body['usdt_wallet'] = usdt_wallet
    body['commission'] = commission
    body['url_webhook'] = settings.url_webhook
    del body['submit']
    del body['csrf_token']
    user = User(**body)
    db.session.add(user)
    db.session.commit()
    return UserDTO.model_validate(user).model_dump()


def delete_user(id: int):
    user = User.query.get(id)
    if user:
        db.session.delete(user)
        db.session.commit()
        flash('User deleted successfully!', 'success')
    else:
        flash('User not found!', 'error')