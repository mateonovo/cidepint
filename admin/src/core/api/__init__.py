from src.core.api.api_user import ApiUsers
from src.core.database import database as db
from passlib.hash import sha256_crypt


def create_user(**kwargs):
    raw_password = kwargs.get("password")
    hashed_password = sha256_crypt.hash(raw_password)
    kwargs["password"] = hashed_password
    user = ApiUsers(**kwargs)
    db.session.add(user)
    db.session.commit()
    return user


def get_user_by_id(id):
    return ApiUsers.query.filter_by(id=id).first()


def find_user_by_mail(email):
    user = ApiUsers.query.filter_by(email=email).first()
    return user


def check_user(email, password):
    """
    Verifica la contraseña ingresada por un usuario
    """
    user = find_user_by_mail(email)

    if user and sha256_crypt.verify(password, user.password):
        return user
    else:
        return None
