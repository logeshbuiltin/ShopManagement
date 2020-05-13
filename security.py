from werkzeug.security import safe_str_cmp 
from models.UserModel import UserModel

def authenticate(username, password):
    user_data = UserModel.find_by_username(username)
    if user_data and safe_str_cmp(user_data.password, password):
        return user_data


def identity(_payload):
    user_id = _payload["identity"]
    return UserModel.find_by_uerid(user_id)