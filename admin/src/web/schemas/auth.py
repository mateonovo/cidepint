from marshmallow import Schema, fields


class AuthSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str()
    tipo_doc = fields.Str()
    nro_doc = fields.Str()
    direccion = fields.Str()
    telefono = fields.Str()
    email = fields.Email()
    password = fields.Str()
    statistics_permissions = fields.List(fields.Str(), dump_only=True)


auth_schema = AuthSchema(only=["email", "password"])
profile_schema = AuthSchema(exclude=["password"])
