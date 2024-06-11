from marshmallow import Schema, fields


class ServiceTypeSchema(Schema):
    data = fields.List(fields.Str)


service_type = ServiceTypeSchema()
