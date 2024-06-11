from src.core.database import database as db
from src.core.admin_instituciones.historial import Historial


def create_historial(**kwargs):
    historial = Historial(**kwargs)
    db.session.add(historial)
    db.session.commit()
    return historial


def paginate_historial(page, per_page, institucion_id):
    query = Historial.query.filter_by(institucion_id=institucion_id)
    asigns = query.paginate(page=page, per_page=per_page)
    return asigns


def get_historial_by_institucion_id(institucion_id):
    return Historial.query.filter_by(institucion_id=institucion_id).all()