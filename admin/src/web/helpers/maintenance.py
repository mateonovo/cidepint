from functools import wraps
from flask import abort
from src.web.helpers.auth import has_permissions
from src.web.config import cache
from src.core import configuracion


def maintenance(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not has_permissions(['config_show']):
            return abort(401)
        return f(*args, **kwargs)
    return decorated_function


def maintenanceActivated(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if configuracion.get_state() :
            return abort(503)
        return f(*args, **kwargs)
    return decorated_function


def is_maintenance():
    return configuracion.get_state()


def info_contacto():
    data = cache.get('info_contacto')

    if data is None:
        data = configuracion.get_info_contacto()
        cache.set('info_contacto', data, timeout=3600)

    return data
