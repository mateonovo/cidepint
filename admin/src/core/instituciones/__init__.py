from src.core.instituciones.institucion import Institucion
from src.core.users import UserRoleInstitution
from src.core.database import database as db


def create_institucion(**kwargs):
    institucion = Institucion(**kwargs)
    db.session.add(institucion)
    db.session.commit()
    return institucion


def delete_institucion(id):
    """
    Elimina la institucion y genera un borrado en cascada de todas las 
    tupas de UserRoleInstitution en donde se encontraba referenciada
    """
    institucion = Institucion.query.filter_by(id=id).first()
    user_institution_roles = UserRoleInstitution.query.filter_by(institution_id=id).all()
    for uir in user_institution_roles:
        db.session.delete(uir)
    db.session.delete(institucion)
    db.session.commit()


def find_institucion_by_id(id):
    return Institucion.query.filter_by(id=id).first()


def update_institucion(institucion, **kwargs):
    for key, value in kwargs.items():
        if hasattr(institucion, key):
            setattr(institucion, key, value)
    db.session.commit()


def habilitar_institucion(institucion, value):
    setattr(institucion, 'habilitado', value)
    db.session.commit()


def list_instituciones():
    instituciones = Institucion.query.filter(Institucion.id != 1).all()
    return instituciones


def paginate_instituciones(page, per_page):
    return Institucion.query.filter(Institucion.id != 1).paginate(page=page, per_page=per_page)


def get_institutions_by_id(inst):
    insti = set()
    for t in inst:
        if t.institution_id != 1:
            insti.add(t.institution)
    return list(inst)


def paginate_institutions_habilited(page, per_page):
    """
    Retorna todas las instituciones habilitadas de manera paginada
    """
    return Institucion.query.filter(Institucion.id != 1, Institucion.habilitado == True).paginate(page=page, per_page=per_page)
