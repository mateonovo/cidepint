from marshmallow import Schema, fields, validate


class InstitutionSchema(Schema):
    id = fields.Int(dump_only=True)
    nombre = fields.String()
    informacion = fields.String()
    calle = fields.String()
    numero = fields.String()
    localizacion = fields.String()
    palabras_claves = fields.String()
    horarios = fields.String()
    web = fields.String()
    contacto = fields.String()
    habilitado = fields.Boolean()


class PaginatedInstitutionSchema(Schema):
    data = fields.Nested(InstitutionSchema, many=True)
    tipo = fields.Str(alias="type")
    page = fields.Integer(validate=validate.Range(min=1), missing=1)
    per_page = fields.Integer(validate=validate.Range(min=1, max=10), missing=1)
    total = fields.Integer()


paginated_schema = PaginatedInstitutionSchema()
institution_schema = InstitutionSchema(exclude=['palabras_claves'])
list_institutions = PaginatedInstitutionSchema(only=['data'])
