from flask import session, redirect, url_for
from functools import wraps
from src.core import users, auth


def user_institutions():
    user = auth.find_user_by_mail(session["user_id"])
    return users.get_user_institutions(user)


def user_in_institution(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        institucion_id = kwargs.get('institucion_id')
        user = auth.find_user_by_mail(session["user_id"])
        instituciones = users.get_user_institutions(user)
        if any(institucion.id == institucion_id for institucion in instituciones):
            return f(*args, **kwargs)
        else:
            return redirect(url_for("home.index"))
    return decorated_function
