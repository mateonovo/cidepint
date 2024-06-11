from flask import Blueprint, request, jsonify
from src.core import api
from src.core import auth
from src.web.schemas.auth import auth_schema, profile_schema
from src.web.schemas.services import service_schema, solicitud_schema, request_show_schema
from src.web.schemas.services import solicitudes_schema, get_solicitud_schema, paginated_services, paginated_search_services
from src.web.schemas.service_type import service_type
from src.web.schemas.institutions import paginated_schema, institution_schema
from marshmallow import ValidationError
from src.core import services
from src.core import configuracion
from src.core import instituciones as module_institutions
from src.core import auth, users
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token
from flask_jwt_extended import set_access_cookies, unset_jwt_cookies, jwt_required
from src.web.helpers.auth import has_permissions, user_is_superadmin


api_bp = Blueprint("api", __name__, url_prefix="/api")


@api_bp.get('/user_jwt')
@jwt_required()
def user_jwt():
    """
    Obtiene los datos del usuario autenticado vía JWT.

    Retorna los datos del usuario junto con sus permisos de estadísticas.
    """
    current_user = get_jwt_identity()
    user = auth.get_user_by_id(current_user)

    statistics_permissions = [p for p in users.list_permissions_by_user(user) if p.startswith("statistics_")]

    user_data = profile_schema.dump(user)
    user_data["statistics_permissions"] = statistics_permissions

    return user_data, 200


@api_bp.post('/login_jwt')
def login_jwt():
    """
    Realiza el inicio de sesión del usuario mediante JWT.

    Se espera un cuerpo JSON con las credenciales del usuario (email y passwd).
    Si las credenciales son válidas, se genera un token de acceso y se devuelve en la respuesta.
    """
    data = request.get_json()
    email = data['email']
    password = data['password']
    user = auth.check_user(email, password)
    if user:
        access_token = create_access_token(identity=user.id, fresh=True)
        response = jsonify({'token':access_token})
        set_access_cookies(response, access_token)
        return response, 201
    else:
        return jsonify(message="Debe registrarse antes de hacer el login"), 403


@api_bp.get('/logout_jwt')
@jwt_required()
def logout_jwt():
    """
    Cierra la sesión del usuario autenticado mediante JWT.

    Elimina las cookies relacionadas con el token de acceso.
    """
    response = jsonify(message="Logged out successfully")
    unset_jwt_cookies(response)
    return response, 200


@api_bp.get("/me/profile/")
@jwt_required()
def profile():
    """
    Retorna la información de un usuario a partir de su ID.
    """
    user = auth.get_user_by_id(get_jwt_identity())

    if user is None:
        return jsonify({"error": "Usuario no encontrado"}), 404

    return profile_schema.dump(user), 200


@api_bp.get("/services/<id>")
def service(id):
    if not id.isdigit():
        return jsonify({"error": "Parametros invalidos"}), 400
    service = services.get_service(id)
    if service is None:
        return jsonify({"error": "Parametros invalidos"}), 404
    data = service_schema.dump(service)
    return data, 200


@api_bp.get("/instituciones/<id>")
def institution(id):
    if not id.isdigit():
        return jsonify({"error": "Parametros invalidos"}), 400
    institucion = module_institutions.find_institucion_by_id(id)
    if institucion is None:
        return jsonify({"error": "Parametros invalidos"}), 404
    data = institution_schema.dump(institucion)
    return data, 200


@api_bp.get("/contacto")
def contacto():
    informacion = configuracion.get_info_contacto()
    return jsonify({'email': informacion.email,
                    'telefono': informacion.telefono,
                    'direccion': informacion.direccion}), 200


@api_bp.get("/all_services")
def all_services():
    """
    Obtiene una lista paginada de todos los servicios.

    Los parámetros aceptados para la paginación son 'page' y 'per_page'.
    Retorna un JSON con los servicios, información de paginación y total de servicios.
    """
    try:
        request_data = paginated_services.load(request.args)
    except ValidationError:
        return jsonify({"error": "Parámetros inválidos"}), 400

    page = request_data['page']
    per_page = request_data['per_page']
    services_list = services.paginate_services_api(page, per_page)

    response_data = {
        'data': service_schema.dump(services_list, many=True),
        'total': services_list.total,
        'page': page,
        'per_page': per_page,
        'pages': services_list.pages
    }
    return paginated_services.dump(response_data), 200


@api_bp.get("/services-type")
def services_type():
    services_type_list = ["Análisis", "Consultoría", "Desarrollo"]
    return service_type.dump({"data": services_type_list}), 200


@api_bp.get("/search_services")
def search_services():
    """
    Busca servicios con parámetros especificos y retorna una lista página de resultados.

    Los parámetros aceptados para la búsqueda y paginación son 'nombre', 'descripcion',
    'institucion', 'tipo_servicio', 'keywords', 'page' y 'per_page'
    """
    try:
        request_data = paginated_search_services.load(request.args)
    except ValidationError:
        return jsonify({"error": "Parámetros inválidos"}), 400

    page = request_data['page']
    per_page = request_data['per_page']
    nombre = request_data['nombre']
    descripcion = request_data['descripcion']
    institucion = request_data['institucion']
    tipo_servicio = request_data['tipo_servicio']
    keywords = request_data['keywords']

    services_list = services.search_services_api(
        nombre=nombre,
        descripcion=descripcion,
        institucion=institucion,
        tipo_servicio=tipo_servicio,
        keywords=keywords,
        page=page,
        per_page=per_page
    )

    response_data = {
        'data': service_schema.dump(services_list, many=True),
        'total': services_list.total,
        'page': page,
        'per_page': per_page,
        'pages': services_list.pages
    }

    return paginated_services.dump(response_data), 200


@api_bp.get("/institutions")
def institutions():
    """
    Obtiene una lista paginada de instituciones habilitadas.

    Los parámetros aceptados son 'page' y 'per_page'
    Retorna un JSON con las instituciones, información de paginación y total de instituciones.
    """
    try:
        request_data = paginated_schema.load(request.args)
    except ValidationError:
        return jsonify({"error": "Parametros invalidos"}), 400

    page = request_data['page']
    per_page = request_data['per_page']
    list_institutions_paginated = module_institutions.paginate_institutions_habilited(page, per_page)
    serialized_institutions = institution_schema.dump(list_institutions_paginated.items, many=True)
    response_data = {
        "data": serialized_institutions,
        "page": page,
        "per_page": per_page,
        "total": list_institutions_paginated.total
    }

    return paginated_schema.dump(response_data), 200


@api_bp.get("/me/requests/<id>")
@jwt_required()
def get_request(id):
    """
    Obtiene detalles de una solicitud especifica perteneciente al usuario autenticado.
    """
    if not id.isdigit():
        return jsonify({"error": "Parametros invalidos"}), 400
    request = services.solicitudes_api_id(get_jwt_identity(),id)
    if request is None:
        return jsonify({"error": "No le pertence ninguna solicitud con ese id"}), 400
    return request_show_schema.dump(request), 200


@api_bp.post("/me/requests")
@jwt_required()
def solicitud():
    """
    Crea una nueva solicitud para el usuario autenticado.

    Se espera un JSON con información de la solicitud.
    """
    try:
        data = request.json
        data['cliente_id'] = get_jwt_identity()

        errors = solicitud_schema.validate(data)

        solicitud = services.create_solicitud(**data)
    except ValidationError:
        return jsonify({"error": "Parametros invalidos"}), 400

    return jsonify({'id': solicitud.id, 'detalles': solicitud.detalles, 'fecha de creacion': solicitud.fecha_creacion,
                    'estado': solicitud.estado}), 201


@api_bp.post("/me/requests/<id>/notes")
@jwt_required()
def comentar_solicitud(id):
    """
    Añade un comentario a una solicitud existente.
    """
    try:
        solicitud = services.show_solicitud(id)
        data = request.json
        comentario = data.get('comentario', '') 
        services.update_solicitud(solicitud, comentario=comentario)
    except ValidationError as err:
        print(err.messages)  
        print(err.valid_data) 
        return jsonify({"error": "Parametros invalidos"}), 400

    return jsonify({'id': solicitud.id, 'comentario': solicitud.comentario}), 201


@api_bp.get("/me/requests")
@jwt_required()
def solicitudes():
    """
    Obtiene una lista paginada de solicitudes del usuario autenticado

    Los parámetros aceptados para la paginación y filtrado son 'page', 'per_page',
    'fecha_inicio', 'fecha_fin' y 'estado'. Para el orden 'sort' indica la columna
    y 'order' si es ascendente o descendente.
    """
    try:
        request_data = solicitudes_schema.load(request.args)
    except ValidationError as err:
        print(err.messages)  
        print(err.valid_data) 
        return jsonify({"error": "Parametros invalidos"}), 400

    page = request_data['page']
    per_page = request_data['per_page']
    sort = request_data['sort']
    order = request_data['order']
    fecha_inicio = request_data['fecha_inicio']
    fecha_fin = request_data['fecha_fin']
    estado = request_data['estado']
    solicitudes_paginadas = services.paginate_solicitudes_api_id(page, per_page, get_jwt_identity(), sort, order, fecha_inicio, fecha_fin, estado)
    solicitudes_serializadas = get_solicitud_schema.dump(solicitudes_paginadas.items, many=True)
    response_data = {
        "data": solicitudes_serializadas,
        "page": page,
        "per_page": per_page,
        "total": solicitudes_paginadas.total,
        "pages": solicitudes_paginadas.pages
    }

    return solicitudes_schema.dump(response_data), 200


@api_bp.get("/top-institutions")
def top_institutions():
    """
    Se obtienen las instituciones que mas rapido resuelven las 
    solicitudes que le fueron realizadas. Es decir, desde que se crean
    hasta que su estado pasa a 'FINALIZADA'
    """
    institutions = services.get_top_institutions()
    result = paginated_schema.dump({"data": institutions})

    return result, 200


@api_bp.get("/solicitudes_por_estado")
@jwt_required()
def solicitudes_por_estado():
    """
    Se obtienen los distintos estados que puede tomar cada solicitud
    junto con la cantidad de solicitudes en dicha etapa del proceso.
    """
    solicitudes = services.solicitudes_por_estado()
    return jsonify({'data': solicitudes}), 200


@api_bp.get("/ranking_servicios")
@jwt_required()
def ranking_servicios():
    """
    En caso de que la llamada sea realizada por el Super Admin, se
    obtienen todos los servicios junto con su cantidad de solicitudes.
    Si la misma fue hecha por un dueño de una/s institucion/es, solo
    se devuelven los servicios (y sus solicitudes) de aquellas que le
    pertenecen.
    """
    user_id = get_jwt_identity()
    user = auth.get_user_by_id(user_id)
    if user_is_superadmin(user=user):
        servicios = services.ranking_all_servicios()
    else:
        servicios = services.ranking_servicios(user)
    return jsonify({'data': servicios}), 200
