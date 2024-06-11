from src.core.services.services import Servicio, Solicitud
from src.core.api.api_user import ApiUsers
from src.core.database import database as db
from src.core.auth.user import Users
from src.core.users.role import UserRoleInstitution
from src.core.instituciones.institucion import Institucion
from collections import Counter

def create_service(**kwargs):
    service = Servicio(**kwargs)
    db.session.add(service)
    db.session.commit()

    return service


def list_services(id):
    services = Servicio.query.filter_by(institucion_id=id).all()
    return services


def get_service(id):
    service = Servicio.query.filter_by(id=id).first()
    return service

def get_all_services():
    return Servicio.query.all()

def update_service(form, service):
    form.populate_obj(service)
    db.session.commit()


def delete_service(id):
    service = Servicio.query.filter_by(id=id).first()
    db.session.delete(service)
    db.session.commit()


def paginate_services(page, per_page, institucion_id):
    return Servicio.query.filter_by(institucion_id=institucion_id).paginate(page=page, per_page=per_page)


def paginate_services_api(page, per_page):
    return Servicio.query.paginate(page=page, per_page=per_page)


def search_services_api(**kwargs):
    """
    Realiza una búsqueda de servicios usando varios criterios de filtrado.
    """
    query = Servicio.query

    if 'nombre' in kwargs and kwargs['nombre']:
        query = query.filter(Servicio.nombre.ilike(f"%{kwargs['nombre']}"))
    if 'descripcion' in kwargs and kwargs['descripcion']:
        query = query.filter(Servicio.descripcion.ilike(f"%{kwargs['descripcion']}"))
    if 'institucion' in kwargs and kwargs['institucion']:
        query = query.join(Servicio.institucion).filter(Institucion.nombre.ilike(f"%{kwargs['institucion']}"))
    if 'tipo_servicio' in kwargs and kwargs['tipo_servicio']:
        query = query.filter(Servicio.tipo_servicio == kwargs['tipo_servicio'])
    if 'keywords' in kwargs and kwargs['keywords']:
        query = query.filter(Servicio.keywords.contains(kwargs['keywords']))
    
    return query.paginate(page=kwargs['page'], per_page=kwargs['per_page'])

# ------------------------ SOLICITUDES


def paginate_solicitudes(page, per_page, institucion_id):
    solicitudes = Solicitud.query.join(Solicitud.servicio).filter(Servicio.institucion_id == institucion_id).paginate(page=page, per_page=per_page)

    return solicitudes


def paginate_solicitudes_api(page, per_page):
    solicitudes = Solicitud.query.join(Solicitud.servicio).paginate(page=page, per_page=per_page)

    return solicitudes


def paginate_solicitudes_api_id(page, per_page,id):
    solicitudes = Solicitud.query.filter( Solicitud.cliente_id == id).paginate(page=page, per_page=per_page)
    return solicitudes


def paginate_solicitudes_api_id(page, per_page, id, sort, order, fecha_inicio, fecha_fin, estado):
    """
    Se devuelven las solicitudes paginadas del user cuyo id es el pasado por
    parametro, filtradas por los parametros y ordenadas si es que se mandaron 
    los mismos.
    """

    if order == 'asc':
        solicitudes = Solicitud.query.filter(Solicitud.cliente_id == id).order_by(db.asc(sort))
    elif order == 'desc':
        solicitudes = Solicitud.query.filter(Solicitud.cliente_id == id).order_by(db.desc(sort))
    else:
        solicitudes = Solicitud.query.filter(Solicitud.cliente_id == id)

    if fecha_inicio:
        solicitudes = solicitudes.filter(Solicitud.fecha_creacion > fecha_inicio)

    if fecha_fin:
        solicitudes = solicitudes.filter(Solicitud.fecha_creacion < fecha_fin)

    if estado:
        solicitudes = solicitudes.filter(Solicitud.estado == estado)

    paginated_solicitudes = solicitudes.paginate(page=page, per_page=per_page)

    return paginated_solicitudes


def solicitudes_api_id(cliente_id, solicitud_id):
    """
    Este metodo devuelve una solicitud que pertenezca al cliente_id
    y que tenga el id de solicitud_id
    """
    solicitudes = Solicitud.query.filter(Solicitud.cliente_id == cliente_id, Solicitud.id == solicitud_id).first()
    return solicitudes


def paginate_solicitudes_filtradas(page, per_page, inicio, fin, estado, tipo, username, institucion_id):
    """
    Este metodo recibe los filtros a aplicar en las solicitudes
    y, valga la redundancia, aplica aquellos que se hayan enviado.
    Luego pagina los resultados y los devuelve
    """
    query = Solicitud.query
    query = query.join(Solicitud.servicio).filter(Servicio.institucion_id == institucion_id)

    if inicio:
        query = query.filter(Solicitud.fecha_creacion > inicio)

    if fin:
        query = query.filter(Solicitud.fecha_creacion < fin)

    if estado:
        query = query.filter(Solicitud.estado == estado)

    if tipo:
        query = query.join(Solicitud.servicio).filter(Servicio.tipo_servicio == tipo)

    if username:
        query = query.join(Solicitud.cliente).filter(Users.nombre == username)

    # Ejecuta la consulta y obtén los resultados
    solicitudes = query.paginate(page=page, per_page=per_page)

    return solicitudes


def show_solicitud(id):
    solicitud = Solicitud.query.filter_by(id=id).first()
    return solicitud


def update_solicitud(solicitud, **kwargs):
    for key, value in kwargs.items():
        if hasattr(solicitud, key):
            setattr(solicitud, key, value)
    db.session.commit()


def delete_solicitud(id):
    solicitud = Solicitud.query.filter_by(id=id).first()
    db.session.delete(solicitud)
    db.session.commit()


def create_solicitud(**kwargs):
    solicitud = Solicitud(**kwargs)
    db.session.add(solicitud)
    db.session.commit()
    return solicitud


def get_top_institutions():
    """
    Obtiene las 10 instituciones con el mejor tiempo de resolución.

    Calcula el tiempo de resolución para cada institución basándose en las solicitudes finalizadas.
    """
    subquery = (
        db.session.query(
            Servicio.institucion_id,
            db.func.sum(Solicitud.fecha_cambio_estado - Solicitud.fecha_creacion).label("tiempo_resolucion")
        )
        .join(Solicitud, Servicio.id == Solicitud.servicio_id)
        .filter(Solicitud.estado.like('FINALIZADA'))
        .group_by(Servicio.institucion_id)
        .subquery()
    )

    query = (
        db.session.query(Institucion)
        .join(subquery, subquery.c.institucion_id == Institucion.id)
        .order_by(subquery.c.tiempo_resolucion.asc())
        .limit(10)
    )

    return query.all()


def solicitudes_por_estado():
    """
    Obtiene todas las solicitudes, las agrupa por estados y las ordena de mayor a menor
    """
    solicitudes = Solicitud.query.all()
    frecuencia_estados = Counter(solicitud.estado for solicitud in solicitudes)
    estados_ordenados = frecuencia_estados.most_common()
    return estados_ordenados


def ranking_servicios(user):
    """
    Obtiene los servicios de las instituciones pertenecientes al usuario que se pasa
    por parametro. Agrupa las solicitudes a dichos servicios y los devuelve.
    """
    instituciones_duenas = [
        uir.institution_id for uir in UserRoleInstitution.query.filter_by(user_id=user.id, role_id=2).all()
    ]

    solicitudes = Solicitud.query.join(Servicio).filter(Servicio.institucion_id.in_(instituciones_duenas)).all()

    frecuencia_servicios = Counter((f"{solicitud.servicio.nombre}-{solicitud.servicio.institucion.nombre}", solicitud.servicio, solicitud.servicio.institucion.nombre) for solicitud in solicitudes)

    servicios_con_cantidad = [{'servicio': servicio[0], 'cantidad_solicitudes': cantidad} for servicio, cantidad in frecuencia_servicios.items()]

    return servicios_con_cantidad


def ranking_all_servicios():
    """
    Obtiene los servicios de todas las instituciones y agrupa las solicitudes a los mismos.
    """
    solicitudes = Solicitud.query.all()

    frecuencia_servicios = Counter((f"{solicitud.servicio.nombre}-{solicitud.servicio.institucion.nombre}", solicitud.servicio, solicitud.servicio.institucion.nombre) for solicitud in solicitudes)

    servicios_con_cantidad = [{'servicio': servicio[0], 'cantidad_solicitudes': cantidad} for servicio, cantidad in frecuencia_servicios.items()]

    return servicios_con_cantidad
