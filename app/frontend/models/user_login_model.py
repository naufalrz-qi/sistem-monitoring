from flask_login import UserMixin
from ..extensions import login_manager
from flask import session


@login_manager.user_loader
def load_user(user_id):
    user = UserLogin()
    user.id = user_id
    return user


class UserLogin(UserMixin):
    id = None
    username = None
    firstName = None
    lastName = None
    gender = None
    alamat = None
    group = None

    @property
    def is_authenticated(self):
        return self.id
