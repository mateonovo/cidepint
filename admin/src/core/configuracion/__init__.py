from src.core.configuracion.mantenimiento import Mantenimiento
from src.core.configuracion.informacion_contacto import Contacto
from src.core.database import database as db


def create_info_contacto(**kwargs):
    info_contacto = Contacto(**kwargs)
    db.session.add( info_contacto)
    db.session.commit()

    return info_contacto


def get_info_contacto():
    info = Contacto.query.first()
    return info


def update_info(tel, email, direc):
    info = Contacto.query.first()
    info.email = email
    info.telefono = tel
    info.direccion = direc
    db.session.commit()


def update_state(mode):
    mant = Mantenimiento.query.first()
    mant.mode = mode
    db.session.commit()


def get_state():
    mant = Mantenimiento.query.first()
    return mant.mode


def get_mensaje():
    mant = Mantenimiento.query.first()
    return mant.mensaje


def create_maintenance(**kwargs):
    maintenance = Mantenimiento(**kwargs)
    db.session.add(maintenance)
    db.session.commit()

    return maintenance


def update_mensaje(mensaje):
    mant = Mantenimiento.query.first()
    mant.mensaje = mensaje
    db.session.commit()


def update_per_page(per_page):
    mant = Mantenimiento.query.first()
    mant.per_page = per_page
    db.session.commit()


def get_per_page():
    mant = Mantenimiento.query.first()
    return mant.per_page