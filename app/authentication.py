from . import auth
from functools import wraps
from flask import request
from .models.user import User


@auth.get_password
def get_passwd(username):
    user = User.query.filter_by(email=username).first()
    if user is not None:
        return user.senha
    else:
        return None


def is_administrator(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        user = User.query\
            .filter_by(email=request.authorization.username).first()
        if user.is_admin is True:
            return f(*args, **kwargs)
        else:
            return auth.auth_error_callback()
    return decorated
