from settings.login_manager import login_manager
from user.models import User


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


login_manager.user_loader(load_user)