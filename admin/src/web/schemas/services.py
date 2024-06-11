from marshmallow import Schema, fields, validate


class ServiceSchema(Schema):
    id = fields.Int(dump_only=True)
    nombre = fields.Str()
    descripcion = fields.Str()
    institucion = fields.Str()
    tipo_servicio = fields.Str(validate=validate.OneOf(['Análisis', 'Desarrollo', 'Consultoría']))
    keywords = fields.Str()
    habilitado = fields.Boolean()
    institucion_id = fields.Int()


service_schema = ServiceSchema()


class PaginatedServicesSchema(Schema):
    data = fields.Nested(ServiceSchema, many=True)
    nombre = fields.Str()
    descripcion = fields.Str()
    institucion = fields.Str()
    tipo_servicio = fields.Str(validate=validate.OneOf(['Análisis', 'Desarrollo', 'Consultoría', '']))
    keywords = fields.Str()
    page = fields.Integer(validate=validate.Range(min=1), missing=1)
    per_page = fields.Integer(validate=validate.Range(min=1, max=10), missing=1)
    total = fields.Integer()
    pages = fields.Integer()


paginated_services = PaginatedServicesSchema(exclude=[
    "nombre", "descripcion", "institucion", "tipo_servicio", "keywords"])
paginated_search_services = PaginatedServicesSchema()


class SolicitudSchema(Schema):
    id = fields.Int(dump_only=True)
    cliente_id = fields.Int()
    servicio_id = fields.Str()
    detalles = fields.Str()
    estado = fields.Str()
    fecha_creacion = fields.Str()
    fecha_cambio_estado = fields.Str()
    observacion_cambio_estado = fields.Str()
    comentario = fields.Str()
    servicio = fields.Nested(ServiceSchema)


solicitud_schema = SolicitudSchema(exclude=['fecha_creacion', 'estado', 'servicio', 'fecha_cambio_estado', 'observacion_cambio_estado', 'id'])
get_solicitud_schema = SolicitudSchema()


class PaginatedSolicitudesSchema(Schema):
    data = fields.Nested(SolicitudSchema, many=True)
    page = fields.Integer(validate=validate.Range(min=1), missing=1)
    per_page = fields.Integer(validate=validate.Range(min=1, max=10), missing=1)
    sort = fields.Str()
    order = fields.Str()
    fecha_inicio = fields.Str()
    fecha_fin = fields.Str()
    estado = fields.Str()
    total = fields.Integer()
    pages = fields.Int()


solicitudes_schema = PaginatedSolicitudesSchema()


class RequestShowSchema(Schema):
    id = fields.Int(dump_only=True)
    fecha_creacion = fields.Date()
    fecha_cambio_estado = fields.Date()
    estado = fields.Str()
    detalles = fields.Str()


request_show_schema = RequestShowSchema()
