from flask import session, abort
from src.core import auth
from src.core import users
from functools import wraps


def is_authenticated(session):
    return session.get("user_id") is not None


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not is_authenticated(session):
            return abort(401)
        return f(*args, **kwargs)
    return decorated_function


def has_permissions(required_permissions_list):
    user_permission_list = session["permissions"]

    for permission in required_permissions_list:
        if permission not in user_permission_list:
            return False
    return True


# Cambiar por session["permissions"]
def has_permissions_mail(required_permissions_list, mail):
    user = auth.find_user_by_mail(mail)
    user_permission_list = users.list_permissions_by_user(user)

    for permission in required_permissions_list:
        if permission in user_permission_list:
            return True
    return False


def is_superadmin():
    if not is_authenticated(session):
        return False
    return session.get("is_superadmin")


def user_is_superadmin(user):
    for role in users.get_user_roles(user):
        if role.nombre == "superadmin":
            return True
    return False


def is_owner():
    user = auth.find_user_by_mail(session["user_id"])
    for role in users.get_user_roles(user):
        if role.nombre == "owner":
            return True
    return False
