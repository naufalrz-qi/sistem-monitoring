import os
from flask_login import UserMixin
from ..lib.json import JsonFileObject
from ..extensions import login_manager


@login_manager.user_loader
def load_user(user_id):
    user = UserLogin()
    user.id = user_id
    return user


json_file = os.getcwd() + "/data.json"
t = JsonFileObject(json_file)
data = t.get_json()


class UserLogin(UserMixin):

    id = data["group"] if data else None
    username = data["group"] if data else None
    group = data["group"] if data else None
    first_name = data["first_name"] if data else None
    last_name = data["last_name"] if data else None
    gender = data["gender"] if data else None
    alamat = data["alamat"] if data else None

    def __repr__(self) -> str:
        return f"username : {self.group}"
